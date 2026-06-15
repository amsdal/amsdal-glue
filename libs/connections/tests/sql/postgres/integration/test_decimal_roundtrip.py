from decimal import Decimal

from amsdal_glue_core.common.data_models.schema import DecimalSchemaModel
from amsdal_glue_core.common.data_models.schema import PropertySchema
from amsdal_glue_core.common.data_models.schema import Schema
from amsdal_glue_core.common.enums import Version
from amsdal_glue_core.common.operations.commands import SchemaCommand
from amsdal_glue_core.common.operations.mutations.schema import RegisterSchema

from amsdal_glue_connections.sql.connections.postgres_connection import PostgresConnection


def test_decimal_column_is_numeric_and_round_trips(database_connection: PostgresConnection) -> None:
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

    column_type = database_connection.execute(
        'SELECT data_type, numeric_precision, numeric_scale '
        "FROM information_schema.columns WHERE table_name = 'invoice' AND column_name = 'amount'"
    ).fetchall()
    assert column_type == [('numeric', 10, 2)]

    database_connection.execute('INSERT INTO invoice (id, amount) VALUES (1, %s)', Decimal('0.10'))
    database_connection.execute('INSERT INTO invoice (id, amount) VALUES (2, %s)', Decimal('1234567.99'))

    rows = database_connection.execute('SELECT amount FROM invoice ORDER BY id').fetchall()
    assert rows == [(Decimal('0.10'),), (Decimal('1234567.99'),)]
    assert all(isinstance(row[0], Decimal) for row in rows)
