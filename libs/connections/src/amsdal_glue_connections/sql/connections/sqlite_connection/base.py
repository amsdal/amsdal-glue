import datetime as _dt
import json
import logging
import re
import sqlite3
from decimal import Decimal
from typing import Any
from uuid import UUID

from amsdal_glue_core.common.data_models.constraints import BaseConstraint
from amsdal_glue_core.common.data_models.constraints import ForeignKeyConstraint
from amsdal_glue_core.common.data_models.constraints import PrimaryKeyConstraint
from amsdal_glue_core.common.data_models.constraints import UniqueConstraint
from amsdal_glue_core.common.data_models.data import Data
from amsdal_glue_core.common.data_models.types import CustomType
from amsdal_glue_core.common.data_models.types import FieldType
from amsdal_glue_core.common.enums import ScalarType

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
}

UNIQUE_CONSTRAINT_RE = re.compile(r'CONSTRAINT\s["\']?(?P<name>\w+)["\']?\s+UNIQUE\s+\((?P<fields>[^)]+)\)')
PRIMARY_KEY_RE = re.compile(r'CONSTRAINT\s+["\']?(?P<name>\w+)["\']?\s+PRIMARY KEY', re.IGNORECASE)
FOREIGN_KEY_RE = re.compile(
    r'CONSTRAINT\s+["\']?(?P<name>\w+)["\']?\s+FOREIGN\s+KEY\s*\(\s*["\']?(?P<fields>[^)]+)["\']?\s*\)',
    re.IGNORECASE,
)
FOREIGN_KEY_INLINE_RE = re.compile(
    r'(?P<field>\w+)\s+(\w+\s+)*CONSTRAINT\s+["\']?(?P<name>\w+)["\']?\s+REFERENCES',
    re.IGNORECASE,
)
FIELDS_RE = re.compile(r'["\'](?P<name>\w+)["\']')


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

    @staticmethod
    def _is_constraint(index_fields: list[str], constraints: list[BaseConstraint]) -> bool:
        for constraint in constraints:
            if not isinstance(constraint, PrimaryKeyConstraint | ForeignKeyConstraint | UniqueConstraint):
                continue

            if index_fields == constraint.fields:
                return True
        return False

    def _get_unique_constrains(self, table_name: str, table_sql: str) -> list[UniqueConstraint]:
        unique_constraints = []
        _unique_fields = []

        for constraint_name, field_names in UNIQUE_CONSTRAINT_RE.findall(table_sql):
            fields = FIELDS_RE.findall(field_names)
            _unique_fields.append(fields)
            unique_constraints.append(
                UniqueConstraint(
                    name=constraint_name,
                    fields=fields,
                    condition=None,
                )
            )

        # Match unique constraints defined inline within column definitions
        normalized_table_sql = re.sub(r'\s+', ' ', table_sql.strip())
        inline_unique_re = re.compile(
            r'["\']?(?P<name>\w+)["\']?\s+\w+(?:\([^)]*\))?\s*(?:NOT\s+NULL|NULL)?\s+UNIQUE(?:\s|,|\)|$)',
            re.IGNORECASE,
        )

        for match in inline_unique_re.finditer(normalized_table_sql):
            field_name = match.group('name')

            if [field_name] in _unique_fields:
                continue

            _unique_fields.append([field_name])
            unique_constraints.append(
                UniqueConstraint(
                    name=f'unq_{table_name}_{field_name}',
                    fields=[field_name],
                    condition=None,
                )
            )

        return unique_constraints

    def _get_pk_name(self, table_sql: str) -> str:
        for constraint_name in PRIMARY_KEY_RE.findall(table_sql):
            return constraint_name

        return ''

    def _get_fk_name(self, table_sql: str, field_name: str) -> str:
        # Look for a foreign key constraint that includes this field
        for match in FOREIGN_KEY_RE.finditer(table_sql):
            constraint_name = match.group('name')
            fields_str = match.group('fields')
            fields = [f.strip(' "\'') for f in fields_str.split(',')]

            if field_name in fields:
                return constraint_name

        for match in FOREIGN_KEY_INLINE_RE.finditer(table_sql):
            constraint_name = match.group('name')
            field_str = match.group('field')
            fields = [field_str]

            if field_name in fields:
                return constraint_name

        return ''

    def to_python_type(self, sql_type: str) -> FieldType:  # noqa: PLR0911, C901
        sql_type = sql_type.upper()

        if sql_type.startswith('DECIMAL_TEXT'):
            m = re.match(r'DECIMAL_TEXT\s*\(\s*(\d+)\s*,\s*(\d+)\s*\)', sql_type)
            if m:
                return CustomType(name='decimal_text', params={'precision': int(m.group(1)), 'scale': int(m.group(2))})
            return CustomType(name='decimal_text')
        if sql_type == 'TEXT' or sql_type.startswith('VARCHAR'):
            return ScalarType.TEXT
        if sql_type in ('INTEGER', 'INT'):
            return ScalarType.INTEGER
        if sql_type == 'REAL':
            return ScalarType.FLOAT
        if sql_type == 'BOOLEAN':
            return ScalarType.BOOLEAN
        if sql_type in ('JSON', 'JSONB'):
            return ScalarType.JSONB
        if sql_type == 'BLOB':
            return ScalarType.BYTEA
        if sql_type == 'TIMESTAMP':
            return ScalarType.TIMESTAMP
        if sql_type == 'DATE':
            return ScalarType.DATE

        msg = f'Unsupported type: {sql_type}'
        raise ValueError(msg)

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
