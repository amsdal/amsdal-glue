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

from amsdal_glue_connections.sql.parsers.conditions import parse_conditions
from amsdal_glue_connections.sql.parsers.default import parser as _default_parser
from amsdal_glue_connections.sql.parsers.default import sqlite_mapper as _sqlite_mapper
from amsdal_glue_connections.sql.schema_registry import TABLE_REGISTRY
from tests.sql.test_registry_view_parity import _view_columns
from tests.sql.test_registry_view_parity import EXPECTED_COLUMNS

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

# The exact `Schema` shape `query_schema` produced for `_FEATURE_RICH_DDL` on the
# pre-view (per-table PRAGMA) introspection path, pinned so the view-based path is byte-for-byte
# equivalent (names/UNIQUE/CHECK from DDL, identity/generated/collation overlays, index conditions).
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


def _create_feature_rich_tables(connection) -> None:
    for ddl in _FEATURE_RICH_DDL:
        connection.execute(ddl)


def test_sqlite_view_columns_match_contract(database_connection):
    database_connection._ensure_schema_views()  # noqa: SLF001

    for view, expected in EXPECTED_COLUMNS.items():
        assert _view_columns(database_connection, view) >= expected, view


def test_sqlite_no_per_table_pragma(database_connection):
    """`query_schema` must not fall back to standalone per-table `PRAGMA table_...(...)` reads.

    The view-based path reads every catalog fact through the registry views plus one batched
    ``sqlite_master`` DDL query, so the statement count stays constant regardless of table count --
    no N+1 PRAGMA storm. The per-table introspection this replaced issued a `PRAGMA table_xinfo` /
    `table_info` / `index_list` / `index_xinfo` / `foreign_key_list` per table, which this test bans.
    """
    _create_feature_rich_tables(database_connection)

    database_connection.debug_mode = True
    database_connection.query_schema(_all_tables_query())

    offending = [q for q in database_connection.queries if q.lstrip().upper().startswith('PRAGMA')]
    assert offending == [], f'query_schema issued standalone PRAGMA statements: {offending}'


def test_sqlite_query_schema_matches_golden(database_connection):
    """Regression gate: view-based `query_schema` must equal the pinned golden `Schema` objects."""
    _create_feature_rich_tables(database_connection)

    schemas = {s.name: s for s in database_connection.query_schema(_all_tables_query()) if s.name in _TABLES}
    assert set(schemas) == set(_TABLES)

    for table_name in _TABLES:
        assert schemas[table_name] == _EXPECTED_SCHEMAS[table_name], (
            f'{table_name}: got={schemas[table_name]!r} expected={_EXPECTED_SCHEMAS[table_name]!r}'
        )


def _create_plain_tables(connection, count: int, *, start: int = 0) -> None:
    for i in range(start, start + count):
        connection.execute(f'CREATE TABLE "gen_{i}" ("id" INTEGER PRIMARY KEY, "v" INTEGER)')


def _statement_count_for_query_schema(connection) -> int:
    before = len(connection.queries)
    connection.query_schema(_all_tables_query())
    return len(connection.queries) - before


def test_sqlite_query_schema_statement_count_is_o1(database_connection):
    """`query_schema`'s statement count must not grow with the number of tables introspected.

    Every catalog fact is read through a constant, small set of bound registry queries plus one
    batched ``sqlite_master`` DDL read (see `query_schema`), never a per-table loop -- so the
    number of SQL statements issued for 2 tables must equal the number issued for 21 tables. A
    per-table introspection loop would make this test fail (statement count scaling with N).
    """
    database_connection.debug_mode = True

    _create_plain_tables(database_connection, 2)
    count_n2 = _statement_count_for_query_schema(database_connection)

    _create_plain_tables(database_connection, 19, start=2)  # 2 + 19 = 21 tables total
    count_n21 = _statement_count_for_query_schema(database_connection)

    assert count_n2 == count_n21, (
        f'statement count grew with table count: n(2)={count_n2} n(21)={count_n21} '
        f'queries(21)={database_connection.queries[-count_n21:]}'
    )


def test_sqlite_introspect_many_tables(database_connection):
    """Correctness + scale guard: 900 tables must all introspect correctly through chunked IN-lists.

    `SQLITE_MAX_VARIABLE_NUMBER` can be as low as 999 on some SQLite builds; a single unchunked
    `IN (...)` over 900 table names (or `_batch_ddls`'s 2x-bound query) would exceed that on such a
    build. `_run_registry`/`_batch_ddls` chunk at `_SQLITE_MAX_IN` (400) to stay under the limit
    regardless of the local build's actual ceiling.
    """
    table_count = 900
    _create_plain_tables(database_connection, table_count)

    schemas = database_connection.query_schema(_all_tables_query())
    generated = {s.name: s for s in schemas if s.name.startswith('gen_')}

    assert len(generated) == table_count
    assert {s.name for s in generated.values()} == {f'gen_{i}' for i in range(table_count)}

    sample = generated['gen_0']
    assert [p.name for p in sample.properties] == ['id', 'v']
    assert sample.constraints is not None
    assert any(c.name == 'pk_gen_0' for c in sample.constraints)
