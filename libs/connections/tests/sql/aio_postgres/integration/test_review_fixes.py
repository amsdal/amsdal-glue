"""Async twin of the Postgres introspection review fixes.

The async Postgres connection shares the assembly mixin with the sync one, so this asserts the same
crash-free / partial-index-condition behaviour on the awaited ``query_schema`` path.
"""

from amsdal_glue_core.common.data_models.conditions import Condition
from amsdal_glue_core.common.data_models.conditions import Conditions
from amsdal_glue_core.common.data_models.field_reference import Field
from amsdal_glue_core.common.data_models.field_reference import FieldReference
from amsdal_glue_core.common.data_models.query import QueryStatement
from amsdal_glue_core.common.data_models.schema import Schema
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.enums import FieldLookup
from amsdal_glue_core.common.enums import Version
from amsdal_glue_core.common.expressions.field_reference import FieldReferenceExpression
from amsdal_glue_core.common.expressions.value import Value

from amsdal_glue_connections.sql.connections.postgres_connection import AsyncPostgresConnection
from amsdal_glue_connections.sql.schema_registry import TABLE_REGISTRY


def _all_tables_query() -> QueryStatement:
    return QueryStatement(table=SchemaReference(name=TABLE_REGISTRY, version=Version.LATEST))


async def _get_schema(connection: AsyncPostgresConnection, table_name: str) -> Schema:
    schemas = [s for s in await connection.query_schema(_all_tables_query()) if s.name == table_name]
    assert schemas, f'schema {table_name!r} not found'
    return schemas[0]


def _field_ref(name: str) -> FieldReferenceExpression:
    return FieldReferenceExpression(field_reference=FieldReference(field=Field(name=name), table_name=''))


async def test_async_expression_index_with_include_does_not_crash(
    database_connection: AsyncPostgresConnection,
) -> None:
    await database_connection.execute('CREATE TABLE "t_expr" ("a" TEXT, "b" INT)')
    await database_connection.execute('CREATE INDEX "idx_ei" ON "t_expr" (lower("a")) INCLUDE ("b")')

    schema = await _get_schema(database_connection, 't_expr')
    index_names = {i.name for i in (schema.indexes or [])}
    assert 'idx_ei' not in index_names


async def test_async_partial_index_condition_captured(database_connection: AsyncPostgresConnection) -> None:
    await database_connection.execute('CREATE TABLE "t_part" ("id" INT PRIMARY KEY, "x" INT NOT NULL)')
    await database_connection.execute('CREATE INDEX "idx_partial" ON "t_part" ("x") WHERE "x" > 5')

    schema = await _get_schema(database_connection, 't_part')
    idx = next(i for i in (schema.indexes or []) if i.name == 'idx_partial')

    assert idx.condition == Conditions(Condition(left=_field_ref('x'), lookup=FieldLookup.GT, right=Value(value=5)))
