import datetime as _dt
import json
import logging
import sqlite3
from decimal import Decimal
from typing import Any
from uuid import UUID

from amsdal_glue_core.common.data_models.data import Data

from amsdal_glue_connections.sql.schema_registry import TABLE_CONSTRAINT_REGISTRY
from amsdal_glue_connections.sql.schema_registry import TABLE_INDEX_REGISTRY
from amsdal_glue_connections.sql.schema_registry import TABLE_PROPERTY_REGISTRY
from amsdal_glue_connections.sql.schema_registry import TABLE_REGISTRY

logger = logging.getLogger(__name__)

# The stdlib sqlite3 driver only binds int/float/str/bytes/None natively. Since `Value` now coerces
# typed params to canonical Python objects (Decimal for NUMERIC, uuid.UUID for UUID, date/datetime),
# register adapters so those bind as TEXT — restoring the Decimal→str behaviour previously done by the
# deleted `sqlite_value_transform`, and future-proofing date/datetime (whose default adapters were
# deprecated in Python 3.12). Module-level so it also covers the async (aiosqlite) driver.
sqlite3.register_adapter(Decimal, str)
sqlite3.register_adapter(UUID, str)
sqlite3.register_adapter(_dt.date, _dt.date.isoformat)
sqlite3.register_adapter(_dt.datetime, lambda value: value.isoformat(sep=' '))

_REGISTRY_VIEW_SQL: dict[str, str] = {
    TABLE_REGISTRY: (
        f'CREATE TEMPORARY VIEW IF NOT EXISTS "{TABLE_REGISTRY}" AS '  # noqa: S608
        "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
    ),
    TABLE_PROPERTY_REGISTRY: (
        f'CREATE TEMPORARY VIEW IF NOT EXISTS "{TABLE_PROPERTY_REGISTRY}" AS '  # noqa: S608
        'SELECT m.name AS table_name, p.name AS name, p.type AS type, '
        "p.type AS udt_name, CASE WHEN p.\"notnull\" THEN 'NO' ELSE 'YES' END AS is_nullable, "
        'p.dflt_value AS column_default, p.cid AS ordinal_position '
        "FROM sqlite_master m, pragma_table_info(m.name) p WHERE m.type='table' AND m.name NOT LIKE 'sqlite_%'"
    ),
    TABLE_INDEX_REGISTRY: (
        f'CREATE TEMPORARY VIEW IF NOT EXISTS "{TABLE_INDEX_REGISTRY}" AS '  # noqa: S608
        'SELECT m.name AS table_name, il.name AS name, '
        '\'btree\' AS index_type, il."unique" AS is_unique '
        "FROM sqlite_master m, pragma_index_list(m.name) il WHERE m.type='table' AND m.name NOT LIKE 'sqlite_%'"
    ),
    TABLE_CONSTRAINT_REGISTRY: (
        # SQLite has no constraint catalog, so approximate one from pragmas. `type` reuses the same
        # single-char codes Postgres exposes via ``pg_constraint.contype`` ('p' primary key,
        # 'u' unique, 'f' foreign key) so the SAME QueryStatement works on both back-ends. Only
        # PK/UNIQUE/FK are representable this way; CHECK/exclusion constraints are out of scope.
        f'CREATE TEMPORARY VIEW IF NOT EXISTS "{TABLE_CONSTRAINT_REGISTRY}" AS '  # noqa: S608
        'SELECT m.name AS table_name, il.name AS name, '
        "CASE il.origin WHEN 'pk' THEN 'p' ELSE 'u' END AS type "
        'FROM sqlite_master m, pragma_index_list(m.name) il '
        "WHERE m.type='table' AND m.name NOT LIKE 'sqlite_%' AND il.origin IN ('pk', 'u') "
        'UNION ALL '
        'SELECT m.name AS table_name, '
        "'fk_' || m.name || '_' || fk.\"id\" AS name, 'f' AS type "
        'FROM sqlite_master m, pragma_foreign_key_list(m.name) fk '
        "WHERE m.type='table' AND m.name NOT LIKE 'sqlite_%'"
    ),
}


class JsonTypeMeta(type):
    def __eq__(cls, other: object) -> bool:
        return other in (list, dict)

    def __hash__(cls) -> int:
        return super().__hash__()


class JsonType(dict, metaclass=JsonTypeMeta): ...  # type: ignore[misc]


class SqliteConnectionMixin:
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
            Data: The Data object.
        """
        for key, value in data.items():
            if isinstance(value, str) and (
                (value.startswith('{') and value.endswith('}')) or (value.startswith('[') and value.endswith(']'))
            ):
                data[key] = json.loads(value)

        return Data(data=data)

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
