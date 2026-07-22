"""Round-trip introspection tests for reconstructed SQLite schema metadata.

Each test creates a table (or index) exercising one feature that PROD previously
dropped or represented as a raw string, then asserts ``query_schema`` reconstructs
it into the correct typed model.
"""

from amsdal_glue_core.common.data_models.conditions import Condition
from amsdal_glue_core.common.data_models.conditions import Conditions
from amsdal_glue_core.common.data_models.constraints import CheckConstraint
from amsdal_glue_core.common.data_models.constraints import ForeignKeyConstraint
from amsdal_glue_core.common.data_models.field_reference import Field
from amsdal_glue_core.common.data_models.field_reference import FieldReference
from amsdal_glue_core.common.data_models.query import QueryStatement
from amsdal_glue_core.common.data_models.schema import Schema
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.enums import BuiltinIndexType
from amsdal_glue_core.common.enums import FieldLookup
from amsdal_glue_core.common.enums import OrderDirection
from amsdal_glue_core.common.enums import ReferentialAction
from amsdal_glue_core.common.enums import Version
from amsdal_glue_core.common.expressions.field_reference import FieldReferenceExpression
from amsdal_glue_core.common.expressions.value import Value

from amsdal_glue_connections.sql.connections.sqlite_connection import SqliteConnection
from amsdal_glue_connections.sql.schema_registry import TABLE_REGISTRY


def _get_schema(connection: SqliteConnection, table_name: str) -> Schema:
    query = QueryStatement(table=SchemaReference(name=TABLE_REGISTRY, version=Version.LATEST))
    schemas = [schema for schema in connection.query_schema(query) if schema.name == table_name]
    assert schemas, f'schema {table_name!r} not found'
    return schemas[0]


def _field_ref(name: str) -> FieldReferenceExpression:
    return FieldReferenceExpression(field_reference=FieldReference(field=Field(name=name), table_name=''))


def test__check_constraint_reconstructed(database_connection: SqliteConnection) -> None:
    database_connection.execute(
        'CREATE TABLE "products" ('
        '"id" INTEGER PRIMARY KEY, '
        '"price" INTEGER NOT NULL, '
        'CONSTRAINT "chk_price" CHECK (price > 0)'
        ')'
    )

    schema = _get_schema(database_connection, 'products')
    checks = [c for c in (schema.constraints or []) if isinstance(c, CheckConstraint)]

    assert checks == [
        CheckConstraint(
            name='chk_price',
            condition=Conditions(Condition(left=_field_ref('price'), lookup=FieldLookup.GT, right=Value(value=0))),
        ),
    ]


def test__typed_default_reconstructed(database_connection: SqliteConnection) -> None:
    database_connection.execute(
        'CREATE TABLE "accounts" ('
        '"id" INTEGER PRIMARY KEY, '
        '"balance" INTEGER NOT NULL DEFAULT 100, '
        '"status" TEXT NOT NULL DEFAULT \'active\''
        ')'
    )

    schema = _get_schema(database_connection, 'accounts')
    by_name = {p.name: p for p in schema.properties}

    # Parsed into typed Value expressions, not RawExpression strings.
    assert by_name['balance'].default == Value(value=100)
    assert by_name['status'].default == Value(value='active')


def test__generated_column_reconstructed(database_connection: SqliteConnection) -> None:
    database_connection.execute(
        'CREATE TABLE "rectangles" ('
        '"id" INTEGER PRIMARY KEY, '
        '"width" INTEGER NOT NULL, '
        '"height" INTEGER NOT NULL, '
        '"area" INTEGER GENERATED ALWAYS AS (width * height) STORED'
        ')'
    )

    schema = _get_schema(database_connection, 'rectangles')
    area = next(p for p in schema.properties if p.name == 'area')

    from amsdal_glue_core.common.expressions.combined import Combined

    assert area.generated == Combined(_field_ref('width'), '*', _field_ref('height'))


def test__partial_index_condition_reconstructed(database_connection: SqliteConnection) -> None:
    database_connection.execute(
        'CREATE TABLE "tasks" ("id" INTEGER PRIMARY KEY, "done" INTEGER NOT NULL, "priority" INTEGER NOT NULL)'
    )
    database_connection.execute('CREATE INDEX "idx_pending" ON "tasks" ("priority") WHERE done = 0')

    schema = _get_schema(database_connection, 'tasks')
    idx = next(i for i in (schema.indexes or []) if i.name == 'idx_pending')

    assert idx.condition == Conditions(Condition(left=_field_ref('done'), lookup=FieldLookup.EQ, right=Value(value=0)))
    assert idx.index_type == BuiltinIndexType.BTREE


def test__fk_referential_actions_reconstructed(database_connection: SqliteConnection) -> None:
    database_connection.execute('CREATE TABLE "parents" ("id" INTEGER PRIMARY KEY)')
    database_connection.execute(
        'CREATE TABLE "children" ('
        '"id" INTEGER PRIMARY KEY, '
        '"parent_id" INTEGER, '
        'CONSTRAINT "fk_parent" FOREIGN KEY ("parent_id") REFERENCES "parents" ("id") '
        'ON DELETE CASCADE ON UPDATE SET NULL'
        ')'
    )

    schema = _get_schema(database_connection, 'children')
    fks = [c for c in (schema.constraints or []) if isinstance(c, ForeignKeyConstraint)]

    assert len(fks) == 1
    fk = fks[0]
    assert fk.fields == ['parent_id']
    assert fk.reference_fields == ['id']
    assert fk.on_delete == ReferentialAction.CASCADE
    assert fk.on_update == ReferentialAction.SET_NULL


def test__desc_index_direction_reconstructed(database_connection: SqliteConnection) -> None:
    database_connection.execute('CREATE TABLE "events" ("id" INTEGER PRIMARY KEY, "ts" INTEGER NOT NULL)')
    database_connection.execute('CREATE INDEX "idx_ts_desc" ON "events" ("ts" DESC)')

    schema = _get_schema(database_connection, 'events')
    idx = next(i for i in (schema.indexes or []) if i.name == 'idx_ts_desc')

    assert idx.fields[0].name == 'ts'
    assert idx.fields[0].direction == OrderDirection.DESC
    assert idx.index_type == BuiltinIndexType.BTREE
