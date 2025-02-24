import json
import logging
from contextlib import suppress
from copy import copy
from datetime import date
from datetime import datetime
from functools import partial
from typing import Any

from amsdal_glue_core.common.data_models.conditions import Condition
from amsdal_glue_core.common.data_models.conditions import Conditions
from amsdal_glue_core.common.data_models.constraints import BaseConstraint
from amsdal_glue_core.common.data_models.constraints import CheckConstraint
from amsdal_glue_core.common.data_models.constraints import ForeignKeyConstraint
from amsdal_glue_core.common.data_models.constraints import PrimaryKeyConstraint
from amsdal_glue_core.common.data_models.constraints import UniqueConstraint
from amsdal_glue_core.common.data_models.data import Data
from amsdal_glue_core.common.data_models.indexes import IndexSchema
from amsdal_glue_core.common.data_models.schema import ArraySchemaModel
from amsdal_glue_core.common.data_models.schema import DictSchemaModel
from amsdal_glue_core.common.data_models.schema import NestedSchemaModel
from amsdal_glue_core.common.data_models.schema import PropertySchema
from amsdal_glue_core.common.data_models.schema import Schema
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.expressions.field_reference import FieldReferenceExpression

from amsdal_glue_connections.sql.constants import SCHEMA_REGISTRY_TABLE
from amsdal_glue_connections.sql.sql_builders.build_only_constructor import pg_build_only
from amsdal_glue_connections.sql.sql_builders.math_operator_transform import pg_math_operator_transform
from amsdal_glue_connections.sql.sql_builders.operator_constructor import repr_operator_constructor
from amsdal_glue_connections.sql.sql_builders.postgres_utils.cast import pg_cast_transform
from amsdal_glue_connections.sql.sql_builders.postgres_utils.func_transform import func_transform
from amsdal_glue_connections.sql.sql_builders.postgres_utils.nested_field import pg_nested_field_transform
from amsdal_glue_connections.sql.sql_builders.postgres_utils.operator_constructor import pg_operator_constructor
from amsdal_glue_connections.sql.sql_builders.postgres_utils.type_transform import pg_value_type_transform
from amsdal_glue_connections.sql.sql_builders.postgres_utils.value_placeholder import pg_value_placeholder_transform
from amsdal_glue_connections.sql.sql_builders.postgres_utils.value_transfrom import pg_value_transform
from amsdal_glue_connections.sql.sql_builders.query_builder import build_where
from amsdal_glue_connections.sql.sql_builders.transform import Transform
from amsdal_glue_connections.sql.sql_builders.transform import TransformTypes

logger = logging.getLogger(__name__)

_pg_transform = None


def get_pg_transform() -> Transform:
    global _pg_transform  # noqa: PLW0603

    if not _pg_transform:
        _pg_transform = Transform()
        _pg_transform.register(TransformTypes.CAST, pg_cast_transform)
        _pg_transform.register(TransformTypes.OPERATOR_CONSTRUCTOR, pg_operator_constructor)
        _pg_transform.register(TransformTypes.VALUE, pg_value_transform)
        _pg_transform.register(TransformTypes.NESTED_FIELD, pg_nested_field_transform)
        _pg_transform.register(TransformTypes.VALUE_PLACEHOLDER, pg_value_placeholder_transform)
        _pg_transform.register(TransformTypes.TABLE_QUOTE, partial(Transform.str_wrapper, '"'))
        _pg_transform.register(TransformTypes.FIELD_QUOTE, partial(Transform.str_wrapper, '"'))
        _pg_transform.register(TransformTypes.BUILD_ONLY, pg_build_only)
        _pg_transform.register(TransformTypes.MATH_OPERATOR, pg_math_operator_transform)
        _pg_transform.register(TransformTypes.FUNC, func_transform)
    return _pg_transform


_pg_transform_repr = None


def get_pg_transform_repr() -> Transform:
    global _pg_transform_repr  # noqa: PLW0603

    if not _pg_transform_repr:
        _pg_transform_repr = copy(get_pg_transform())
        _pg_transform_repr.register(TransformTypes.OPERATOR_CONSTRUCTOR, repr_operator_constructor)
    return _pg_transform_repr


class PostgresConnectionMixin:
    def __init__(self) -> None:
        self._queries: list[str] = []

    @classmethod
    def _adjust_schema_filters(cls, filters: Conditions | None) -> None:
        """
        Transform "name" attribute of the filters to the correct column name: "table_name"
        """

        if filters is None:
            return

        for _filter in filters.children:
            if isinstance(_filter, Conditions):
                cls._adjust_schema_filters(_filter)
                continue

            if not isinstance(_filter.left, FieldReferenceExpression):
                continue

            if _filter.left.field_reference.field.name == 'name':
                _filter.left.field_reference.field.name = 'table_name'

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

    def _build_column(self, column: PropertySchema, *, force_nullable: bool = False) -> str:
        return (
            f'"{column.name}" {self._to_sql_type(column.type)}'
            f'{" NOT NULL" if column.required and not force_nullable else ""}'
        )

    def _build_column_update(self, column: PropertySchema) -> str:
        sql_type = self._to_sql_type(column.type)
        _stm = f'"{column.name}" TYPE {sql_type}{" NOT NULL" if column.required else ""}'

        if sql_type in ['DOUBLE PRECISION', 'BIGINT']:
            _stm += f' USING "{column.name}"::{sql_type}'

        return _stm

    def _join_fields(self, fields: list[str]) -> str:
        return ', '.join(f'"{f}"' for f in fields)

    def _build_constraint(self, constraint: BaseConstraint) -> str:
        if isinstance(constraint, PrimaryKeyConstraint):
            return f'CONSTRAINT {constraint.name} PRIMARY KEY ({self._join_fields(constraint.fields)}) '
        if isinstance(constraint, ForeignKeyConstraint):
            return (
                f'CONSTRAINT "{constraint.name}" '
                f'FOREIGN KEY ({self._join_fields(constraint.fields)}) '
                f'REFERENCES "{constraint.reference_schema.name}" ({self._join_fields(constraint.reference_fields)})'
            )
        if isinstance(constraint, UniqueConstraint):
            return f'CONSTRAINT {constraint.name} UNIQUE ({self._join_fields(constraint.fields)})'
        if isinstance(constraint, CheckConstraint):
            _where, _ = build_where(
                constraint.condition,
                transform=get_pg_transform(),
                embed_values=True,
            )

            return f'CONSTRAINT {constraint.name} CHECK ({_where})'

        msg = f'Unsupported constraint: {type(constraint)}'
        raise ValueError(msg)

    def _build_index(self, schema_name: str, namespace: str, index: IndexSchema) -> str:
        _namespace_prefix = f'"{namespace}".' if namespace else ''
        _index = (
            f'CREATE INDEX {_namespace_prefix}"{index.name}" '
            f'ON {_namespace_prefix}"{schema_name}" ({", ".join(index.fields)})'
        )

        if index.condition:
            where, _ = build_where(
                index.condition,
                transform=get_pg_transform_repr(),
            )
            _index += f' WHERE {where}'

        return _index

    def _to_sql_type(
        self,
        property_type: Schema | SchemaReference | NestedSchemaModel | ArraySchemaModel | DictSchemaModel | type[Any],
    ) -> str:
        with suppress(ValueError):
            return pg_value_type_transform(property_type)  # type: ignore[arg-type]

        if isinstance(property_type, Schema | SchemaReference):
            return 'TEXT'
        if isinstance(property_type, NestedSchemaModel | ArraySchemaModel | DictSchemaModel):
            logger.warning('Unsupported type: %s. Using JSON instead.', property_type)
            return 'JSONB'

        msg = f'Unsupported type: {property_type}'
        raise ValueError(msg)

    def _to_python_type(self, sql_type: str) -> type[Any]:  # noqa: PLR0911
        sql_type = sql_type.upper()

        if sql_type in ['TEXT', 'CHARACTER VARYING'] or sql_type.startswith('VARCHAR'):
            return str
        if sql_type in ('BIGINT', 'INT', 'INTEGER', 'SMALLINT'):
            return int
        if sql_type in ('DOUBLE PRECISION', 'REAL', 'NUMERIC', 'DECIMAL'):
            return float
        if sql_type == 'BOOLEAN':
            return bool
        if sql_type in ['JSON', 'JSONB']:
            return dict
        if sql_type == 'BYTEA':
            return bytes
        if sql_type == 'TIMESTAMP' or sql_type.startswith('TIMESTAMP'):
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
