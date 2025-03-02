import json
import logging
import re
from contextlib import suppress
from copy import copy
from datetime import date
from datetime import datetime
from typing import Any

from amsdal_glue_core.common.data_models.conditions import Condition
from amsdal_glue_core.common.data_models.conditions import Conditions
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
from amsdal_glue_core.common.expressions.field_reference import FieldReferenceExpression

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

UNIQUE_CONSTRAINT_RE = re.compile(r'CONSTRAINT ["\'](?P<name>\w+)["\'] UNIQUE \((?P<fields>[^)]+)\)')
PRIMARY_KEY_RE = re.compile(r'CONSTRAINT ["\'](?P<name>\w+)["\'] PRIMARY KEY')
FIELDS_RE = re.compile(r'["\'](?P<name>\w+)["\']')


class JsonTypeMeta(type):
    def __eq__(cls, other: object) -> bool:
        return other in (list, dict)


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

    def _get_unique_constrains(self, table_sql: str) -> list[UniqueConstraint]:
        unique_constraints = []

        for constraint_name, field_names in UNIQUE_CONSTRAINT_RE.findall(table_sql):
            fields = FIELDS_RE.findall(field_names)
            unique_constraints.append(
                UniqueConstraint(
                    name=constraint_name,
                    fields=fields,
                    condition=None,
                )
            )

        return unique_constraints

    def _get_pk_name(self, table_sql: str) -> str:
        for constraint_name in PRIMARY_KEY_RE.findall(table_sql):
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

    def _replace_table_name(self, conditions: Conditions, replace_name: str) -> Conditions:
        items: list[Conditions | Condition] = []

        for _child in conditions.children:
            if isinstance(_child, Conditions):
                items.append(self._replace_table_name(_child, replace_name))
            elif (
                isinstance(_child.left, FieldReferenceExpression)
                and _child.left.field_reference.table_name == SCHEMA_REGISTRY_TABLE
            ):
                _copy = copy(_child)
                _copy.left.field_reference.table_name = replace_name  # type: ignore[attr-defined]
                items.append(_copy)
            else:
                items.append(_child)

        return Conditions(*items, connector=conditions.connector, negated=conditions.negated)

    @property
    def queries(self) -> list[str]:
        """
        Returns the queries executed on this connection.

        Returns:
            list[str]: The queries executed.
        """
        return self._queries
