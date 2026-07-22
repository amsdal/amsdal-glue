"""View-based schema introspection gates for the async Postgres connection.

Mirrors the sync Postgres ``test_view_introspection`` schema-shape + no-per-table-catalog gates for the
async path: the async ``query_schema`` must reconstruct the exact same ``Schema`` objects and must
never fall back to per-table ``information_schema`` / ``pg_get_serial_sequence`` reads.
"""

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

from amsdal_glue_connections.sql.connections.postgres_connection import AsyncPostgresConnection
from amsdal_glue_connections.sql.parsers.conditions import parse_conditions
from amsdal_glue_connections.sql.parsers.default import parse_pg_default
from amsdal_glue_connections.sql.schema_registry import TABLE_REGISTRY

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

# The exact `Schema` shape the sync per-table catalog path produced for the same DDL,
# pinned so the async fully view-based path stays equivalent.
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


async def _create_feature_rich_tables(connection: AsyncPostgresConnection) -> None:
    for ddl in _FEATURE_RICH_DDL:
        await connection.execute(ddl)


async def test_async_pg_no_per_table_catalog(database_connection: AsyncPostgresConnection) -> None:
    """The async `query_schema` must not fall back to per-table `information_schema` / sequence reads.

    The fully view-based path reads every catalog fact through the registry views, so the statement
    count stays constant regardless of table count. The registry-view DDL legitimately references
    those catalogs, so only standalone ``SELECT`` statements (never the ``CREATE ... VIEW`` DDL) are
    inspected.
    """
    await _create_feature_rich_tables(database_connection)

    database_connection.debug_mode = True
    await database_connection.query_schema(_all_tables_query())

    offending = [
        q
        for q in database_connection.queries
        if q.lstrip().upper().startswith('SELECT')
        and ('information_schema.columns' in q.lower() or 'pg_get_serial_sequence' in q.lower())
    ]
    assert offending == [], f'query_schema issued per-table catalog statements: {offending}'


async def test_async_pg_query_schema_matches_golden(database_connection: AsyncPostgresConnection) -> None:
    """Regression gate: the async fully view-based `query_schema` must equal the pinned golden `Schema`s."""
    await _create_feature_rich_tables(database_connection)

    schemas = {s.name: s for s in await database_connection.query_schema(_all_tables_query()) if s.name in _TABLES}
    assert set(schemas) == set(_TABLES)

    for table_name in _TABLES:
        assert schemas[table_name] == _EXPECTED_SCHEMAS[table_name], (
            f'{table_name}: got={schemas[table_name]!r} expected={_EXPECTED_SCHEMAS[table_name]!r}'
        )
