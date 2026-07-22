"""Async twin of the SQLite introspection review fixes.

The async connection shares the assembly mixin with the sync one, so this asserts the same
non-fatal / correct behaviour holds on the awaited ``query_schema`` path.
"""

from amsdal_glue_core.common.data_models.conditions import Condition
from amsdal_glue_core.common.data_models.conditions import Conditions
from amsdal_glue_core.common.data_models.constraints import CheckConstraint
from amsdal_glue_core.common.data_models.field_reference import Field
from amsdal_glue_core.common.data_models.field_reference import FieldReference
from amsdal_glue_core.common.data_models.indexes import IndexField
from amsdal_glue_core.common.data_models.query import QueryStatement
from amsdal_glue_core.common.data_models.schema import Schema
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.enums import FieldLookup
from amsdal_glue_core.common.enums import OrderDirection
from amsdal_glue_core.common.enums import Version
from amsdal_glue_core.common.expressions.field_reference import FieldReferenceExpression
from amsdal_glue_core.common.expressions.value import Value

from amsdal_glue_connections.sql.connections.sqlite_connection import AsyncSqliteConnection
from amsdal_glue_connections.sql.schema_registry import TABLE_REGISTRY


async def _get_schema(connection: AsyncSqliteConnection, table_name: str) -> Schema:
    query = QueryStatement(table=SchemaReference(name=TABLE_REGISTRY, version=Version.LATEST))
    schemas = [schema for schema in await connection.query_schema(query) if schema.name == table_name]
    assert schemas, f'schema {table_name!r} not found'
    return schemas[0]


def _field_ref(name: str) -> FieldReferenceExpression:
    return FieldReferenceExpression(field_reference=FieldReference(field=Field(name=name), table_name=''))


async def test_async_partial_index_is_not_null_reconstructed(database_connection: AsyncSqliteConnection) -> None:
    await database_connection.execute('CREATE TABLE "users" ("id" INTEGER PRIMARY KEY, "email" TEXT)')
    await database_connection.execute('CREATE INDEX "idx_has_email" ON "users" ("id") WHERE "email" IS NOT NULL')

    schema = await _get_schema(database_connection, 'users')
    idx = next(i for i in (schema.indexes or []) if i.name == 'idx_has_email')

    assert idx.condition == Conditions(
        Condition(left=_field_ref('email'), lookup=FieldLookup.ISNULL, right=Value(value=False))
    )


async def test_async_check_with_like_reconstructed(database_connection: AsyncSqliteConnection) -> None:
    await database_connection.execute(
        'CREATE TABLE "people" ('
        '"id" INTEGER PRIMARY KEY, '
        '"email" TEXT NOT NULL, '
        'CONSTRAINT "chk_email" CHECK (email LIKE \'%@%\')'
        ')'
    )

    schema = await _get_schema(database_connection, 'people')
    checks = [c for c in (schema.constraints or []) if isinstance(c, CheckConstraint)]

    assert checks == [
        CheckConstraint(
            name='chk_email',
            condition=Conditions(
                Condition(left=_field_ref('email'), lookup=FieldLookup.CONTAINS, right=Value(value='@'))
            ),
        )
    ]


async def test_async_without_rowid_index_reports_only_key_columns(
    database_connection: AsyncSqliteConnection,
) -> None:
    await database_connection.execute('CREATE TABLE "wr" ("a" INTEGER, "b" INTEGER, PRIMARY KEY("a")) WITHOUT ROWID')
    await database_connection.execute('CREATE INDEX "idx_b" ON "wr" ("b")')

    schema = await _get_schema(database_connection, 'wr')
    idx = next(i for i in (schema.indexes or []) if i.name == 'idx_b')

    assert idx.fields == [IndexField(name='b', direction=OrderDirection.ASC)]
