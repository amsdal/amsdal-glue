from amsdal_glue_core.common.data_models.constraints import CheckConstraint
from amsdal_glue_core.common.data_models.constraints import ForeignKeyConstraint
from amsdal_glue_core.common.data_models.constraints import PrimaryKeyConstraint
from amsdal_glue_core.common.data_models.constraints import UniqueConstraint
from amsdal_glue_core.common.data_models.indexes import IndexField
from amsdal_glue_core.common.data_models.indexes import IndexSchema
from amsdal_glue_core.common.data_models.query import QueryStatement
from amsdal_glue_core.common.data_models.schema import IdentityConfig
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
from amsdal_glue_connections.sql.parsers.default import parse_pg_default
from amsdal_glue_connections.sql.schema_registry import TABLE_CONSTRAINT_REGISTRY
from amsdal_glue_connections.sql.schema_registry import TABLE_INDEX_REGISTRY
from amsdal_glue_connections.sql.schema_registry import TABLE_REGISTRY
from tests.sql.test_registry_view_parity import _view_columns
from tests.sql.test_registry_view_parity import EXPECTED_COLUMNS

_TABLES = ('orders', 'parents', 'pairs')

# Feature-rich DDL: composite PKs, a multi-column FK, a NUMERIC-typed UNIQUE constraint,
# a CASCADE/SET NULL FK, a CHECK constraint, a generated STORED column, a non-default COLLATE
# column, a DESC multi-column index, a covering (INCLUDE) index, and a GENERATED ALWAYS AS
# IDENTITY column.
_FEATURE_RICH_DDL = [
    'CREATE TABLE parents (id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY, code TEXT NOT NULL, email TEXT)',
    'CREATE TABLE pairs (px INT NOT NULL, py INT NOT NULL, note TEXT, PRIMARY KEY (px, py))',
    (
        'CREATE TABLE orders ('
        'a INT NOT NULL, b INT NOT NULL, '
        'amount NUMERIC(10,2) NOT NULL DEFAULT 0, '
        'status TEXT NOT NULL DEFAULT \'new\' COLLATE "C", '
        'parent_id INT, fx INT, fy INT, '
        'total INT GENERATED ALWAYS AS (a * b) STORED, '
        'PRIMARY KEY (a, b), '
        'CONSTRAINT uq_amount UNIQUE (amount), '
        'CONSTRAINT fk_parent FOREIGN KEY (parent_id) REFERENCES parents(id) '
        'ON DELETE CASCADE ON UPDATE SET NULL, '
        'CONSTRAINT fk_pair FOREIGN KEY (fx, fy) REFERENCES pairs (px, py), '
        'CONSTRAINT chk_amount CHECK (amount > 0))'
    ),
    'CREATE INDEX idx_status_amount ON orders (status, amount DESC)',
    'CREATE INDEX idx_cover ON orders (a) INCLUDE (b)',
    'CREATE UNIQUE INDEX uix_email ON parents (email)',
]

# The generated STORED expression `(a * b)` (as Postgres stores it in `generation_expression`) is
# parsed through the shared default-expression parser + Postgres mapper -- the exact path the
# connection uses to reconstruct a `generated` expression.
_TOTAL_GENERATED = parse_pg_default('(a * b)')

# The exact `Schema` shape `query_schema` produced for `_FEATURE_RICH_DDL` on the
# pre-view (per-table catalog) introspection path, pinned so the fully view-based path stays
# equivalent (real PK/FK/UNIQUE/CHECK names, identity sequence params, generated expression,
# COLLATE, DecimalType modifiers, DESC/INCLUDE index columns, canonical ``None`` namespace for the
# default schema).
_EXPECTED_SCHEMAS = {
    'orders': Schema(
        name='orders',
        version=Version.LATEST,
        namespace=None,
        properties=[
            PropertySchema(name='a', type=ScalarType.INTEGER, required=True),
            PropertySchema(name='b', type=ScalarType.INTEGER, required=True),
            PropertySchema(
                name='amount', type=DecimalType(precision=10, scale=2), required=True, default=Value(value=0)
            ),
            PropertySchema(
                name='status', type=ScalarType.TEXT, required=True, default=Value(value='new'), db_collation='C'
            ),
            PropertySchema(name='parent_id', type=ScalarType.INTEGER, required=False),
            PropertySchema(name='fx', type=ScalarType.INTEGER, required=False),
            PropertySchema(name='fy', type=ScalarType.INTEGER, required=False),
            PropertySchema(name='total', type=ScalarType.INTEGER, required=False, generated=_TOTAL_GENERATED),
        ],
        constraints=[
            PrimaryKeyConstraint(name='orders_pkey', fields=['a', 'b']),
            ForeignKeyConstraint(
                name='fk_parent',
                fields=['parent_id'],
                reference_schema=SchemaReference(name='parents', version=Version.LATEST),
                reference_fields=['id'],
                on_delete=ReferentialAction.CASCADE,
                on_update=ReferentialAction.SET_NULL,
            ),
            ForeignKeyConstraint(
                name='fk_pair',
                fields=['fx', 'fy'],
                reference_schema=SchemaReference(name='pairs', version=Version.LATEST),
                reference_fields=['px', 'py'],
                on_delete=ReferentialAction.NO_ACTION,
                on_update=ReferentialAction.NO_ACTION,
            ),
            UniqueConstraint(name='uq_amount', fields=['amount']),
            CheckConstraint(name='chk_amount', condition=parse_conditions('amount > (0)::numeric')),
        ],
        indexes=[
            IndexSchema(
                name='idx_cover',
                fields=[IndexField(name='a', direction=OrderDirection.ASC)],
                unique=False,
                index_type=BuiltinIndexType.BTREE,
                include=['b'],
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
        namespace=None,
        properties=[
            PropertySchema(
                name='id',
                type=ScalarType.INTEGER,
                required=True,
                identity=IdentityConfig(
                    always=True, start=1, increment=1, min_value=1, max_value=2147483647, cycle=False, cache=1
                ),
            ),
            PropertySchema(name='code', type=ScalarType.TEXT, required=True),
            PropertySchema(name='email', type=ScalarType.TEXT, required=False),
        ],
        constraints=[
            PrimaryKeyConstraint(name='parents_pkey', fields=['id']),
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
        namespace=None,
        properties=[
            PropertySchema(name='px', type=ScalarType.INTEGER, required=True),
            PropertySchema(name='py', type=ScalarType.INTEGER, required=True),
            PropertySchema(name='note', type=ScalarType.TEXT, required=False),
        ],
        constraints=[
            PrimaryKeyConstraint(name='pairs_pkey', fields=['px', 'py']),
        ],
    ),
}


def _all_tables_query() -> QueryStatement:
    return QueryStatement(table=SchemaReference(name=TABLE_REGISTRY, version=Version.LATEST))


def _create_feature_rich_tables(connection) -> None:
    for ddl in _FEATURE_RICH_DDL:
        connection.execute(ddl)


def test_postgres_view_columns_match_contract(database_connection):
    database_connection._ensure_schema_views()  # noqa: SLF001

    for view, expected in EXPECTED_COLUMNS.items():
        assert _view_columns(database_connection, view) >= expected, view


def test_pg_constraint_long_normalised(database_connection):
    database_connection.execute('CREATE TABLE "p" ("id" INT PRIMARY KEY)')
    database_connection.execute(
        'CREATE TABLE "c" ("a" INT, "b" INT, "pid" INT, '
        'CONSTRAINT "pk_c" PRIMARY KEY ("a","b"), '
        'CONSTRAINT "fk_c" FOREIGN KEY ("pid") REFERENCES "p"("id") ON DELETE CASCADE ON UPDATE SET NULL)'
    )
    database_connection.execute('CREATE INDEX "ix_c" ON "c" ("a","b" DESC)')
    database_connection._ensure_schema_views()  # noqa: SLF001

    cur = database_connection.execute(
        f'SELECT column_name, ordinal_position, ref_table, ref_column, on_delete, on_update '  # noqa: S608
        f"FROM \"{TABLE_CONSTRAINT_REGISTRY}\" WHERE table_name='c' AND type='f' ORDER BY ordinal_position"
    )
    rows = cur.fetchall()
    cur.close()
    assert rows == [('pid', 0, 'p', 'id', 'CASCADE', 'SET_NULL')]

    cur = database_connection.execute(
        f'SELECT column_name, is_descending FROM "{TABLE_INDEX_REGISTRY}" '  # noqa: S608
        f"WHERE table_name='c' AND name='ix_c' ORDER BY ordinal_position"
    )
    assert cur.fetchall() == [('a', 0), ('b', 1)]
    cur.close()


def test_pg_no_per_table_catalog(database_connection):
    """`query_schema` must not fall back to per-table `information_schema` / sequence catalog reads.

    The fully view-based path reads every catalog fact through the registry views, so the statement
    count stays constant regardless of table count -- no N+1 catalog storm. The per-table
    introspection this replaced issued a standalone `SELECT ... FROM information_schema.columns` read
    and a `SELECT pg_get_serial_sequence(...)` lookup per table/column, both of which this test bans.
    The registry-view DDL legitimately references those catalogs, so only standalone ``SELECT``
    statements (never the ``CREATE ... VIEW`` DDL) are inspected.
    """
    _create_feature_rich_tables(database_connection)

    database_connection.debug_mode = True
    database_connection.query_schema(_all_tables_query())

    offending = [
        q
        for q in database_connection.queries
        if q.lstrip().upper().startswith('SELECT')
        and ('information_schema.columns' in q.lower() or 'pg_get_serial_sequence' in q.lower())
    ]
    assert offending == [], f'query_schema issued per-table catalog statements: {offending}'


def test_postgres_query_schema_matches_golden(database_connection):
    """Regression gate: the fully view-based `query_schema` must equal the pinned golden `Schema`s."""
    _create_feature_rich_tables(database_connection)

    schemas = {s.name: s for s in database_connection.query_schema(_all_tables_query()) if s.name in _TABLES}
    assert set(schemas) == set(_TABLES)

    for table_name in _TABLES:
        assert schemas[table_name] == _EXPECTED_SCHEMAS[table_name], (
            f'{table_name}: got={schemas[table_name]!r} expected={_EXPECTED_SCHEMAS[table_name]!r}'
        )


def _create_plain_tables(connection, count: int, *, start: int = 0) -> None:
    for i in range(start, start + count):
        connection.execute(f'CREATE TABLE "gen_{i}" ("id" INT PRIMARY KEY, "v" INT)')


def _statement_count_for_query_schema(connection) -> int:
    before = len(connection.queries)
    connection.query_schema(_all_tables_query())
    return len(connection.queries) - before


def test_postgres_query_schema_statement_count_is_o1(database_connection):
    """`query_schema`'s statement count must not grow with the number of tables introspected.

    Every catalog fact is read through a constant, small set of bound registry queries (see
    `introspect_schema`), never a per-table loop -- so the number of SQL statements issued for 2
    tables must equal the number issued for 21 tables. A per-table introspection loop would make
    this test fail (statement count scaling with N).
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
