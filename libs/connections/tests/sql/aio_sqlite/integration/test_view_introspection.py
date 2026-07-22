"""View-based schema introspection gates for the async SQLite connection.

Mirrors the sync SQLite ``test_view_introspection`` schema-shape + no-per-table gates for the async path:
the async ``query_schema`` must reconstruct the exact same ``Schema`` objects and must never fall
back to standalone per-table ``PRAGMA`` reads.
"""

from amsdal_glue_core.common.data_models.constraints import CheckConstraint
from amsdal_glue_core.common.data_models.constraints import ForeignKeyConstraint
from amsdal_glue_core.common.data_models.constraints import PrimaryKeyConstraint
from amsdal_glue_core.common.data_models.constraints import UniqueConstraint
from amsdal_glue_core.common.data_models.indexes import IndexField
from amsdal_glue_core.common.data_models.indexes import IndexSchema
from amsdal_glue_core.common.data_models.query import QueryStatement
from amsdal_glue_core.common.data_models.schema import PropertySchema
from amsdal_glue_core.common.data_models.schema import Schema
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.data_models.types import DecimalType
from amsdal_glue_core.common.enums import BuiltinIndexType
from amsdal_glue_core.common.enums import OrderDirection
from amsdal_glue_core.common.enums import ReferentialAction
from amsdal_glue_core.common.enums import ScalarType
from amsdal_glue_core.common.enums import Version
from amsdal_glue_core.common.expressions.value import Value

from amsdal_glue_connections.sql.connections.sqlite_connection import AsyncSqliteConnection
from amsdal_glue_connections.sql.parsers.conditions import parse_conditions
from amsdal_glue_connections.sql.parsers.default import parser as _default_parser
from amsdal_glue_connections.sql.parsers.default import sqlite_mapper as _sqlite_mapper
from amsdal_glue_connections.sql.schema_registry import TABLE_REGISTRY

_TABLES = ('orders', 'parents', 'pairs')

# Feature-rich DDL: composite PKs, a multi-column FK, a NUMERIC-typed UNIQUE constraint,
# a CASCADE/SET NULL FK, a CHECK constraint, a generated STORED column, a COLLATE NOCASE column,
# a DESC multi-column index, a partial index, and an AUTOINCREMENT identity column.
_FEATURE_RICH_DDL = [
    'CREATE TABLE "parents" ("id" INTEGER PRIMARY KEY AUTOINCREMENT, "code" TEXT NOT NULL, "email" TEXT)',
    'CREATE TABLE "pairs" ("px" INTEGER NOT NULL, "py" INTEGER NOT NULL, "note" TEXT, PRIMARY KEY ("px", "py"))',
    (
        'CREATE TABLE "orders" ('
        '"a" INTEGER NOT NULL, "b" INTEGER NOT NULL, '
        '"amount" NUMERIC(10,2) NOT NULL DEFAULT 0, '
        '"status" TEXT NOT NULL DEFAULT \'new\' COLLATE NOCASE, '
        '"parent_id" INTEGER, "fx" INTEGER, "fy" INTEGER, '
        '"total" INTEGER GENERATED ALWAYS AS (a * b) STORED, '
        'PRIMARY KEY ("a", "b"), '
        'CONSTRAINT "uq_amount" UNIQUE ("amount"), '
        'CONSTRAINT "fk_parent" FOREIGN KEY ("parent_id") REFERENCES "parents" ("id") '
        'ON DELETE CASCADE ON UPDATE SET NULL, '
        'CONSTRAINT "fk_pair" FOREIGN KEY ("fx", "fy") REFERENCES "pairs" ("px", "py"), '
        'CONSTRAINT "chk_amount" CHECK (amount > 0))'
    ),
    'CREATE INDEX "idx_status_amount" ON "orders" ("status", "amount" DESC)',
    'CREATE INDEX "idx_pending" ON "orders" ("a") WHERE b = 0',
    'CREATE UNIQUE INDEX "uix_email" ON "parents" ("email")',
]

# The generated STORED expression `a * b` is parsed through the shared default-expression parser +
# SQLite mapper -- the exact path the connection uses to reconstruct a `generated` expression.
_TOTAL_GENERATED = _sqlite_mapper.map_node(_default_parser.parse('a * b'))

# The exact `Schema` shape the sync per-table PRAGMA path produced for the same DDL,
# pinned so the async view-based path is byte-for-byte equivalent.
_EXPECTED_SCHEMAS = {
    'orders': Schema(
        name='orders',
        version=Version.LATEST,
        properties=[
            PropertySchema(name='a', type=ScalarType.INTEGER, required=True),
            PropertySchema(name='b', type=ScalarType.INTEGER, required=True),
            PropertySchema(
                name='amount', type=DecimalType(precision=10, scale=2), required=True, default=Value(value=0)
            ),
            PropertySchema(
                name='status', type=ScalarType.TEXT, required=True, default=Value(value='new'), db_collation='NOCASE'
            ),
            PropertySchema(name='parent_id', type=ScalarType.INTEGER, required=False),
            PropertySchema(name='fx', type=ScalarType.INTEGER, required=False),
            PropertySchema(name='fy', type=ScalarType.INTEGER, required=False),
            PropertySchema(name='total', type=ScalarType.INTEGER, required=False, generated=_TOTAL_GENERATED),
        ],
        constraints=[
            PrimaryKeyConstraint(name='pk_orders', fields=['a', 'b']),
            ForeignKeyConstraint(
                name='fk_pair',
                fields=['fx', 'fy'],
                reference_schema=SchemaReference(name='pairs', version=Version.LATEST),
                reference_fields=['px', 'py'],
                on_delete=ReferentialAction.NO_ACTION,
                on_update=ReferentialAction.NO_ACTION,
            ),
            ForeignKeyConstraint(
                name='fk_parent',
                fields=['parent_id'],
                reference_schema=SchemaReference(name='parents', version=Version.LATEST),
                reference_fields=['id'],
                on_delete=ReferentialAction.CASCADE,
                on_update=ReferentialAction.SET_NULL,
            ),
            UniqueConstraint(name='uq_amount', fields=['amount']),
            CheckConstraint(name='chk_amount', condition=parse_conditions('amount > 0')),
        ],
        indexes=[
            IndexSchema(
                name='idx_pending',
                fields=[IndexField(name='a', direction=OrderDirection.ASC)],
                unique=False,
                index_type=BuiltinIndexType.BTREE,
                condition=parse_conditions('b = 0'),
            ),
            IndexSchema(
                name='idx_status_amount',
                fields=[
                    IndexField(name='status', direction=OrderDirection.ASC),
                    IndexField(name='amount', direction=OrderDirection.DESC),
                ],
                unique=False,
                index_type=BuiltinIndexType.BTREE,
            ),
        ],
    ),
    'parents': Schema(
        name='parents',
        version=Version.LATEST,
        properties=[
            PropertySchema(name='id', type=ScalarType.INTEGER, required=False, identity=True),
            PropertySchema(name='code', type=ScalarType.TEXT, required=True),
            PropertySchema(name='email', type=ScalarType.TEXT, required=False),
        ],
        constraints=[
            PrimaryKeyConstraint(name='pk_parents', fields=['id']),
        ],
        indexes=[
            IndexSchema(
                name='uix_email',
                fields=[IndexField(name='email', direction=OrderDirection.ASC)],
                unique=True,
                index_type=BuiltinIndexType.BTREE,
            ),
        ],
    ),
    'pairs': Schema(
        name='pairs',
        version=Version.LATEST,
        properties=[
            PropertySchema(name='px', type=ScalarType.INTEGER, required=True),
            PropertySchema(name='py', type=ScalarType.INTEGER, required=True),
            PropertySchema(name='note', type=ScalarType.TEXT, required=False),
        ],
        constraints=[
            PrimaryKeyConstraint(name='pk_pairs', fields=['px', 'py']),
        ],
    ),
}


def _all_tables_query() -> QueryStatement:
    return QueryStatement(table=SchemaReference(name=TABLE_REGISTRY, version=Version.LATEST))


async def _create_feature_rich_tables(connection: AsyncSqliteConnection) -> None:
    for ddl in _FEATURE_RICH_DDL:
        await connection.execute(ddl)


async def test_async_sqlite_no_per_table_pragma(database_connection: AsyncSqliteConnection) -> None:
    """The async `query_schema` must not fall back to standalone per-table `PRAGMA table_...(...)` reads.

    The view-based path reads every catalog fact through the registry views plus one batched
    ``sqlite_master`` DDL query, so the statement count stays constant regardless of table count.
    """
    await _create_feature_rich_tables(database_connection)

    database_connection.debug_mode = True
    await database_connection.query_schema(_all_tables_query())

    offending = [q for q in database_connection.queries if q.lstrip().upper().startswith('PRAGMA')]
    assert offending == [], f'query_schema issued standalone PRAGMA statements: {offending}'


async def test_async_sqlite_query_schema_matches_golden(database_connection: AsyncSqliteConnection) -> None:
    """Regression gate: async view-based `query_schema` must equal the pinned golden `Schema` objects."""
    await _create_feature_rich_tables(database_connection)

    schemas = {s.name: s for s in await database_connection.query_schema(_all_tables_query()) if s.name in _TABLES}
    assert set(schemas) == set(_TABLES)

    for table_name in _TABLES:
        assert schemas[table_name] == _EXPECTED_SCHEMAS[table_name], (
            f'{table_name}: got={schemas[table_name]!r} expected={_EXPECTED_SCHEMAS[table_name]!r}'
        )
