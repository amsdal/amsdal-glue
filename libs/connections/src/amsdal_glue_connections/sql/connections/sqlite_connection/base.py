import json
import logging
import re
from contextlib import suppress
from datetime import date
from datetime import datetime
from typing import Any

from amsdal_glue_core.common.data_models.constraints import BaseConstraint
from amsdal_glue_core.common.data_models.constraints import ForeignKeyConstraint
from amsdal_glue_core.common.data_models.constraints import PrimaryKeyConstraint
from amsdal_glue_core.common.data_models.constraints import UniqueConstraint
from amsdal_glue_core.common.data_models.data import Data
from amsdal_glue_core.common.data_models.schema import ArraySchemaModel
from amsdal_glue_core.common.data_models.schema import DictSchemaModel
from amsdal_glue_core.common.data_models.schema import NestedSchemaModel
from amsdal_glue_core.common.data_models.schema import Schema
from amsdal_glue_core.common.data_models.schema import SchemaReference

from amsdal_glue_connections.sql.constants import SCHEMA_REGISTRY_TABLE
from amsdal_glue_connections.sql.sql_builders.math_operator_transform import sqlite_math_operator_transform
from amsdal_glue_connections.sql.sql_builders.sqlite_utils.cast import sqlite_cast_transform
from amsdal_glue_connections.sql.sql_builders.sqlite_utils.func_transform import func_transform
from amsdal_glue_connections.sql.sql_builders.sqlite_utils.nested_field import sqlite_nested_field_transform
from amsdal_glue_connections.sql.sql_builders.sqlite_utils.type_transform import sqlite_value_type_transform
from amsdal_glue_connections.sql.sql_builders.sqlite_utils.value_placeholder import sqlite_value_placeholder_transform
from amsdal_glue_connections.sql.sql_builders.sqlite_utils.value_transform import sqlite_value_transform
from amsdal_glue_connections.sql.sql_builders.transform import Transform
from amsdal_glue_connections.sql.sql_builders.transform import TransformTypes

logger = logging.getLogger(__name__)

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


_sqlite_transform = None


def get_sqlite_transform() -> Transform:
    global _sqlite_transform  # noqa: PLW0603

    if not _sqlite_transform:
        _sqlite_transform = Transform()
        _sqlite_transform.register(TransformTypes.CAST, sqlite_cast_transform)
        _sqlite_transform.register(TransformTypes.VALUE_PLACEHOLDER, sqlite_value_placeholder_transform)
        _sqlite_transform.register(TransformTypes.VALUE, sqlite_value_transform)
        _sqlite_transform.register(TransformTypes.NESTED_FIELD, sqlite_nested_field_transform)
        _sqlite_transform.register(TransformTypes.MATH_OPERATOR, sqlite_math_operator_transform)
        _sqlite_transform.register(TransformTypes.FUNC, func_transform)
    return _sqlite_transform


class SqliteConnectionMixin:
    TABLE_SQL = (
        f'SELECT * FROM (SELECT name AS table_name FROM sqlite_master WHERE type="table") AS {SCHEMA_REGISTRY_TABLE}'  # noqa: S608
    )

    def __init__(self) -> None:
        self._queries: list[str] = []

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

    @staticmethod
    def to_sql_type(
        property_type: Schema | SchemaReference | NestedSchemaModel | ArraySchemaModel | DictSchemaModel | type[Any],
    ) -> str:
        with suppress(ValueError):
            return sqlite_value_type_transform(property_type)  # type: ignore[arg-type]

        if isinstance(property_type, Schema | SchemaReference):
            return 'TEXT'
        if isinstance(property_type, NestedSchemaModel | ArraySchemaModel | DictSchemaModel):
            logger.warning('Unsupported type: %s. Using JSON instead.', property_type)
            return 'JSON'

        msg = f'Unsupported type: {property_type}'
        raise ValueError(msg)

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

    def to_python_type(self, sql_type: str) -> type[Any]:  # noqa: PLR0911
        sql_type = sql_type.upper()

        if sql_type == 'TEXT' or sql_type.startswith('VARCHAR'):
            return str
        if sql_type in ('INTEGER', 'INT'):
            return int
        if sql_type == 'REAL':
            return float
        if sql_type == 'BOOLEAN':
            return bool
        if sql_type in ('JSON', 'JSONB'):
            return JsonType
        if sql_type == 'BLOB':
            return bytes
        if sql_type == 'TIMESTAMP':
            return datetime
        if sql_type == 'DATE':
            return date

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
