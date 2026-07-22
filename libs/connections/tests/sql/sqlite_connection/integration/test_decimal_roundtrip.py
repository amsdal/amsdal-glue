from decimal import Decimal

from amsdal_glue_core.common.data_models.data import DataInput
from amsdal_glue_core.common.data_models.query import QueryStatement
from amsdal_glue_core.common.data_models.schema import PropertySchema
from amsdal_glue_core.common.data_models.schema import Schema
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.data_models.types import DecimalType
from amsdal_glue_core.common.enums import ScalarType
from amsdal_glue_core.common.enums import Version
from amsdal_glue_core.common.operations.commands import SchemaCommand
from amsdal_glue_core.common.operations.mutations.data import InsertData
from amsdal_glue_core.common.operations.mutations.schema import RegisterSchema

from amsdal_glue_connections.sql.connections.sqlite_connection import SqliteConnection
from amsdal_glue_connections.sql.schema_registry import TABLE_REGISTRY


def _register_invoice(
    database_connection: SqliteConnection,
    amount_type: DecimalType | None = None,
) -> SchemaReference:
    if amount_type is None:
        amount_type = DecimalType(precision=10, scale=2)
    database_connection.run_schema_command(
        SchemaCommand(
            mutations=[
                RegisterSchema(
                    schema_ref=SchemaReference(name='invoice', version=Version.LATEST),
                    schema=Schema(
                        name='invoice',
                        version=Version.LATEST,
                        properties=[
                            PropertySchema(name='id', type=ScalarType.INTEGER, required=True),
                            PropertySchema(name='amount', type=amount_type, required=True),
                        ],
                    ),
                ),
            ],
        ),
    )
    return SchemaReference(name='invoice', version=Version.LATEST)


def _introspect_amount_type(database_connection: SqliteConnection) -> object:
    query = QueryStatement(table=SchemaReference(name=TABLE_REGISTRY, version=Version.LATEST))
    schema = next(s for s in database_connection.query_schema(query) if s.name == 'invoice')
    return next(p.type for p in schema.properties if p.name == 'amount')


def test_decimal_column_uses_text_affinity(database_connection: SqliteConnection) -> None:
    _register_invoice(database_connection)

    columns = database_connection.execute('PRAGMA table_info(invoice)').fetchall()
    # row format: (cid, name, type, notnull, dflt_value, pk)
    amount_col = next(col for col in columns if col[1] == 'amount')
    assert amount_col[2] == 'DECIMAL_TEXT(10, 2)'


def test_decimal_round_trips_exactly(database_connection: SqliteConnection) -> None:
    schema_ref = _register_invoice(database_connection)

    database_connection.run_mutations([
        InsertData(
            schema=schema_ref,
            data=[
                DataInput(data={'id': 1, 'amount': Decimal('0.10')}),
                DataInput(data={'id': 2, 'amount': Decimal('1234567.99')}),
            ],
        ),
    ])

    result = database_connection.query(QueryStatement(table=schema_ref))
    stored = sorted((row.data['id'], row.data['amount']) for row in result)

    # The DECIMAL_TEXT converter re-hydrates the TEXT-affinity storage into exact Decimals
    # (no float drift like 0.1), so glue returns typed Decimal values, not strings.
    assert stored == [(1, Decimal('0.10')), (2, Decimal('1234567.99'))]
    assert all(isinstance(amount, Decimal) for _, amount in stored)


def test_decimal_schema_round_trips_precision_and_scale(database_connection: SqliteConnection) -> None:
    _register_invoice(database_connection)

    # Full RegisterSchema -> introspect cycle must recover BOTH precision and scale exactly.
    assert _introspect_amount_type(database_connection) == DecimalType(precision=10, scale=2)


def test_decimal_schema_round_trips_precision_only(database_connection: SqliteConnection) -> None:
    # A scale-less DecimalType renders DECIMAL_TEXT(10) and round-trips to precision-only.
    _register_invoice(database_connection, amount_type=DecimalType(precision=10))

    assert _introspect_amount_type(database_connection) == DecimalType(precision=10, scale=None)
