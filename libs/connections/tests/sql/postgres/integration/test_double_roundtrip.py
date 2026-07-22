"""Round-trip test for ``ScalarType.DOUBLE`` on Postgres.

A bare ``double`` is not a valid Postgres type (``type "double" does not exist``);
glue must render the ANSI ``double precision`` so ``CREATE TABLE`` succeeds and the
catalog reports it back as ``double precision`` -> ``ScalarType.DOUBLE``.
"""

from amsdal_glue_core.common.data_models.query import QueryStatement
from amsdal_glue_core.common.data_models.schema import PropertySchema
from amsdal_glue_core.common.data_models.schema import Schema
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.enums import ScalarType
from amsdal_glue_core.common.enums import Version
from amsdal_glue_core.common.operations.commands import SchemaCommand
from amsdal_glue_core.common.operations.mutations.schema import RegisterSchema

from amsdal_glue_connections.sql.connections.postgres_connection import PostgresConnection
from amsdal_glue_connections.sql.schema_registry import TABLE_REGISTRY


def _register_metric(database_connection: PostgresConnection) -> None:
    database_connection.run_schema_command(
        SchemaCommand(
            mutations=[
                RegisterSchema(
                    schema_ref=SchemaReference(name='metric', version=Version.LATEST),
                    schema=Schema(
                        name='metric',
                        version=Version.LATEST,
                        properties=[
                            PropertySchema(name='id', type=ScalarType.INTEGER, required=True),
                            PropertySchema(name='value', type=ScalarType.DOUBLE, required=True),
                        ],
                    ),
                ),
            ],
        ),
    )


def test_double_column_creates_valid_type(database_connection: PostgresConnection) -> None:
    _register_metric(database_connection)

    column_type = database_connection.execute(
        "SELECT data_type FROM information_schema.columns WHERE table_name = 'metric' AND column_name = 'value'"
    ).fetchall()
    assert column_type == [('double precision',)]


def test_double_schema_round_trips_to_double(database_connection: PostgresConnection) -> None:
    _register_metric(database_connection)

    query = QueryStatement(table=SchemaReference(name=TABLE_REGISTRY, version=Version.LATEST))
    schema = next(s for s in database_connection.query_schema(query) if s.name == 'metric')
    value_type = next(p.type for p in schema.properties if p.name == 'value')
    assert value_type == ScalarType.DOUBLE
