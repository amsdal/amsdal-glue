"""Round-trip introspection tests for reconstructed PostgreSQL schema metadata (async)."""

from amsdal_glue_core.common.data_models.conditions import Condition
from amsdal_glue_core.common.data_models.conditions import Conditions
from amsdal_glue_core.common.data_models.constraints import CheckConstraint
from amsdal_glue_core.common.data_models.constraints import ExclusionConstraint
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
from amsdal_glue_core.common.expressions.combined import Combined
from amsdal_glue_core.common.expressions.field_reference import FieldReferenceExpression
from amsdal_glue_core.common.expressions.value import Value

from amsdal_glue_connections.sql.connections.postgres_connection import AsyncPostgresConnection
from amsdal_glue_connections.sql.schema_registry import TABLE_REGISTRY


async def _introspect_one(connection: AsyncPostgresConnection, table_name: str) -> Schema:
    schemas = await connection.introspect_schema(
        QueryStatement(
            table=SchemaReference(name=TABLE_REGISTRY, version=Version.LATEST),
            where=Conditions(
                Condition(
                    left=FieldReferenceExpression(
                        field_reference=FieldReference(field=Field(name='name'), table_name=TABLE_REGISTRY),
                    ),
                    lookup=FieldLookup.EQ,
                    right=Value(table_name),
                ),
            ),
        )
    )
    assert len(schemas) == 1
    return schemas[0]


def _field_ref(name: str) -> FieldReferenceExpression:
    return FieldReferenceExpression(field_reference=FieldReference(field=Field(name=name), table_name=''))


async def test__check_constraint_reconstructed(database_connection: AsyncPostgresConnection) -> None:
    await database_connection.execute(
        'CREATE TABLE products (id INT, price INT NOT NULL, CONSTRAINT chk_price CHECK (price > 0))'
    )

    schema = await _introspect_one(database_connection, 'products')
    checks = [c for c in (schema.constraints or []) if isinstance(c, CheckConstraint)]

    assert checks == [
        CheckConstraint(
            name='chk_price',
            condition=Conditions(Condition(left=_field_ref('price'), lookup=FieldLookup.GT, right=Value(value=0))),
        ),
    ]


async def test__typed_default_reconstructed(database_connection: AsyncPostgresConnection) -> None:
    await database_connection.execute(
        "CREATE TABLE accounts (id INT, balance INT NOT NULL DEFAULT 100, status TEXT NOT NULL DEFAULT 'active')"
    )

    schema = await _introspect_one(database_connection, 'accounts')
    by_name = {p.name: p for p in schema.properties}

    assert by_name['balance'].default == Value(value=100)
    assert by_name['status'].default == Value(value='active')


async def test__generated_column_reconstructed(database_connection: AsyncPostgresConnection) -> None:
    await database_connection.execute(
        'CREATE TABLE rectangles ('
        'id INT, width INT NOT NULL, height INT NOT NULL, '
        'area INT GENERATED ALWAYS AS (width * height) STORED)'
    )

    schema = await _introspect_one(database_connection, 'rectangles')
    area = next(p for p in schema.properties if p.name == 'area')

    assert area.generated == Combined(_field_ref('width'), '*', _field_ref('height'))


async def test__fk_referential_actions_reconstructed(database_connection: AsyncPostgresConnection) -> None:
    await database_connection.execute('CREATE TABLE parents (id INT PRIMARY KEY)')
    await database_connection.execute(
        'CREATE TABLE children ('
        'id INT PRIMARY KEY, parent_id INT, '
        'CONSTRAINT fk_parent FOREIGN KEY (parent_id) REFERENCES parents (id) '
        'ON DELETE CASCADE ON UPDATE SET NULL)'
    )

    schema = await _introspect_one(database_connection, 'children')
    fks = [c for c in (schema.constraints or []) if isinstance(c, ForeignKeyConstraint)]

    assert len(fks) == 1
    fk = fks[0]
    assert fk.fields == ['parent_id']
    assert fk.reference_fields == ['id']
    assert fk.on_delete == ReferentialAction.CASCADE
    assert fk.on_update == ReferentialAction.SET_NULL


async def test__desc_index_direction_reconstructed(database_connection: AsyncPostgresConnection) -> None:
    await database_connection.execute('CREATE TABLE events (id INT, ts INT NOT NULL)')
    await database_connection.execute('CREATE INDEX idx_ts_desc ON events (ts DESC)')

    schema = await _introspect_one(database_connection, 'events')
    idx = next(i for i in (schema.indexes or []) if i.name == 'idx_ts_desc')

    assert idx.fields[0].name == 'ts'
    assert idx.fields[0].direction == OrderDirection.DESC
    assert idx.index_type == BuiltinIndexType.BTREE


async def test__include_columns_reconstructed(database_connection: AsyncPostgresConnection) -> None:
    await database_connection.execute('CREATE TABLE covering (id INT, a INT, b INT)')
    await database_connection.execute('CREATE INDEX idx_cover ON covering (a) INCLUDE (b)')

    schema = await _introspect_one(database_connection, 'covering')
    idx = next(i for i in (schema.indexes or []) if i.name == 'idx_cover')

    assert [f.name for f in idx.fields] == ['a']
    assert idx.include == ['b']


async def test__exclusion_constraint_reconstructed(database_connection: AsyncPostgresConnection) -> None:
    await database_connection.execute('CREATE EXTENSION IF NOT EXISTS btree_gist')
    await database_connection.execute(
        'CREATE TABLE bookings (id INT, room_id INT, CONSTRAINT no_overlap EXCLUDE USING gist (room_id WITH =))'
    )

    schema = await _introspect_one(database_connection, 'bookings')
    exclusions = [c for c in (schema.constraints or []) if isinstance(c, ExclusionConstraint)]

    assert len(exclusions) == 1
    excl = exclusions[0]
    assert excl.name == 'no_overlap'
    assert excl.index_method == 'gist'
    assert [(e.field, e.operator) for e in excl.elements] == [('room_id', '=')]
