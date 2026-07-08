from decimal import Decimal

from amsdal_glue_core.common.data_models.query import QueryStatement
from amsdal_glue_core.common.data_models.schema import PropertySchema
from amsdal_glue_core.common.data_models.schema import Schema
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.data_models.types import DecimalType
from amsdal_glue_core.common.enums import ScalarType
from amsdal_glue_core.common.enums import Version
from amsdal_glue_core.common.operations.commands import SchemaCommand
from amsdal_glue_core.common.operations.mutations.schema import RegisterSchema

from amsdal_glue_connections.sql.connections.postgres_connection import PostgresConnection
from amsdal_glue_connections.sql.schema_registry import TABLE_REGISTRY


def _register_amount(database_connection: PostgresConnection, amount_type: DecimalType) -> None:
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


def _introspect_amount_type(database_connection: PostgresConnection) -> object:
    query = QueryStatement(table=SchemaReference(name=TABLE_REGISTRY, version=Version.LATEST))
    schema = next(s for s in database_connection.query_schema(query) if s.name == 'invoice')
    return next(p.type for p in schema.properties if p.name == 'amount')


def test_decimal_column_is_numeric_and_round_trips(database_connection: PostgresConnection) -> None:
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
                            PropertySchema(
                                name='amount',
                                type=DecimalType(precision=10, scale=2),
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


def test_decimal_schema_round_trips_precision_and_scale(database_connection: PostgresConnection) -> None:
    _register_amount(database_connection, DecimalType(precision=10, scale=2))

    # Full RegisterSchema -> introspect cycle must recover BOTH precision and scale exactly
    # from the Postgres catalog (numeric_precision / numeric_scale).
    assert _introspect_amount_type(database_connection) == DecimalType(precision=10, scale=2)


def test_decimal_schema_round_trips_precision_only(database_connection: PostgresConnection) -> None:
    # NUMERIC(10) in Postgres has an implicit scale of 0; the catalog reports numeric_scale=0,
    # so introspection recovers DecimalType(precision=10, scale=0) (not scale=None).
    _register_amount(database_connection, DecimalType(precision=10))

    assert _introspect_amount_type(database_connection) == DecimalType(precision=10, scale=0)
