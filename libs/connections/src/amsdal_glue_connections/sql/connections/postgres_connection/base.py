import json
import logging
from typing import Any

from amsdal_glue_core.common.data_models.constraints import BaseConstraint
from amsdal_glue_core.common.data_models.constraints import ForeignKeyConstraint
from amsdal_glue_core.common.data_models.constraints import PrimaryKeyConstraint
from amsdal_glue_core.common.data_models.constraints import UniqueConstraint
from amsdal_glue_core.common.data_models.data import Data

from amsdal_glue_connections.sql.schema_registry import TABLE_CONSTRAINT_REGISTRY
from amsdal_glue_connections.sql.schema_registry import TABLE_INDEX_REGISTRY
from amsdal_glue_connections.sql.schema_registry import TABLE_PROPERTY_REGISTRY
from amsdal_glue_connections.sql.schema_registry import TABLE_REGISTRY

logger = logging.getLogger(__name__)

_REGISTRY_VIEW_SQL: dict[str, str] = {
    TABLE_REGISTRY: (
        f'CREATE OR REPLACE TEMPORARY VIEW "{TABLE_REGISTRY}" AS '  # noqa: S608
        'SELECT table_name AS name '
        'FROM information_schema.tables '
        "WHERE table_schema = 'public' AND table_type = 'BASE TABLE'"
    ),
    TABLE_PROPERTY_REGISTRY: (
        f'CREATE OR REPLACE TEMPORARY VIEW "{TABLE_PROPERTY_REGISTRY}" AS '  # noqa: S608
        'SELECT table_name, column_name AS name, data_type AS type, '
        'udt_name, is_nullable, column_default, ordinal_position '
        'FROM information_schema.columns '
        "WHERE table_schema = 'public'"
    ),
    TABLE_CONSTRAINT_REGISTRY: (
        f'CREATE OR REPLACE TEMPORARY VIEW "{TABLE_CONSTRAINT_REGISTRY}" AS '  # noqa: S608
        'SELECT cls.relname AS table_name, con.conname AS name, con.contype AS type '
        'FROM pg_constraint con '
        'JOIN pg_class cls ON cls.oid = con.conrelid '
        "JOIN pg_namespace nsp ON nsp.oid = cls.relnamespace AND nsp.nspname = 'public'"
    ),
    TABLE_INDEX_REGISTRY: (
        f'CREATE OR REPLACE TEMPORARY VIEW "{TABLE_INDEX_REGISTRY}" AS '  # noqa: S608
        'SELECT tc.relname AS table_name, ic.relname AS name, '
        'am.amname AS index_type, ix.indisunique AS is_unique '
        'FROM pg_index ix '
        'JOIN pg_class tc ON tc.oid = ix.indrelid '
        'JOIN pg_class ic ON ic.oid = ix.indexrelid '
        'JOIN pg_am am ON am.oid = ic.relam '
        "JOIN pg_namespace nsp ON nsp.oid = tc.relnamespace AND nsp.nspname = 'public' "
        'WHERE NOT ix.indisprimary'
    ),
}


class PostgresConnectionMixin:
    def __init__(self) -> None:
        self._queries: list[str] = []
        self._queries_params: list[tuple[Any, ...]] = []

    @staticmethod
    def build_data(data: dict[str, Any]) -> Data:
        """
        Builds a Data object from a dictionary.

        Args:
            data (dict[str, Any]): The data dictionary.

        Returns:
            Data: The built Data object.
        """
        for key, value in data.items():
            if isinstance(value, str) and (
                (value.startswith('{') and value.endswith('}')) or (value.startswith('[') and value.endswith(']'))
            ):
                data[key] = json.loads(value)
        return Data(data=data)

    @staticmethod
    def _is_constraint(index_fields: list[str], constraints: list[BaseConstraint]) -> bool:
        for constraint in constraints:
            if not isinstance(constraint, PrimaryKeyConstraint | ForeignKeyConstraint | UniqueConstraint):
                continue

            if index_fields == constraint.fields:
                return True
        return False

    @property
    def queries(self) -> list[str]:
        """
        Returns the queries executed on this connection.

        Returns:
            list[str]: The queries executed.
        """
        return self._queries

    @property
    def queries_params(self) -> list[tuple[Any, ...]]:
        """
        Returns the parameters bound to each captured query, aligned by index with ``queries``.

        Returns:
            list[tuple[Any, ...]]: The query parameters, in the same order as ``queries``.
        """
        return self._queries_params
