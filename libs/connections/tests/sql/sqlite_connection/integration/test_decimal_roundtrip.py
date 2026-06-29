from decimal import Decimal

from amsdal_glue_core.common.data_models.data import Data
from amsdal_glue_core.common.data_models.query import QueryStatement
from amsdal_glue_core.common.data_models.schema import DecimalSchemaModel
from amsdal_glue_core.common.data_models.schema import PropertySchema
from amsdal_glue_core.common.data_models.schema import Schema
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.enums import Version
from amsdal_glue_core.common.operations.commands import SchemaCommand
from amsdal_glue_core.common.operations.mutations.data import InsertData
from amsdal_glue_core.common.operations.mutations.schema import RegisterSchema

from amsdal_glue_connections.sql.connections.sqlite_connection import SqliteConnection


def _register_invoice(database_connection: SqliteConnection) -> SchemaReference:
    database_connection.run_schema_command(
        SchemaCommand(
            mutations=[
                RegisterSchema(
                    schema=Schema(
                        name='invoice',
                        version=Version.LATEST,
                        properties=[
                            PropertySchema(name='id', type=int, required=True),
                            PropertySchema(
                                name='amount',
                                type=DecimalSchemaModel(precision=10, scale=2),
                                required=True,
                            ),
                        ],
                    ),
                ),
            ],
        ),
    )
    return SchemaReference(name='invoice', version=Version.LATEST)


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
                Data(data={'id': 1, 'amount': Decimal('0.10')}),
                Data(data={'id': 2, 'amount': Decimal('1234567.99')}),
            ],
        ),
    ])

    result = database_connection.query(QueryStatement(table=schema_ref))
    stored = sorted((row.data['id'], row.data['amount']) for row in result)

    # Stored verbatim as exact text (no float drift like '0.1')
    assert stored == [(1, '0.10'), (2, '1234567.99')]
    # And re-hydrates to the exact Decimal (what the model layer does via Pydantic)
    assert [Decimal(value) for _, value in stored] == [Decimal('0.10'), Decimal('1234567.99')]
