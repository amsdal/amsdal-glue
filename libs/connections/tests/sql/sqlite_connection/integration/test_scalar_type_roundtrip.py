"""Round-trip tests for scalar types that glue must faithfully carry on SQLite.

Covers DOUBLE (must render a valid ``double precision`` and introspect back to
``ScalarType.DOUBLE``) and TIMESTAMPTZ (must render, introspect back to
``ScalarType.TIMESTAMPTZ``, and read a stored ``datetime`` back as a Python
``datetime`` -- not a raw ISO string).
"""

from datetime import datetime
from datetime import timezone

from amsdal_glue_core.common.data_models.data import DataInput
from amsdal_glue_core.common.data_models.query import QueryStatement
from amsdal_glue_core.common.data_models.schema import PropertySchema
from amsdal_glue_core.common.data_models.schema import Schema
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.enums import ScalarType
from amsdal_glue_core.common.enums import Version
from amsdal_glue_core.common.operations.commands import SchemaCommand
from amsdal_glue_core.common.operations.mutations.data import InsertData
from amsdal_glue_core.common.operations.mutations.schema import RegisterSchema

from amsdal_glue_connections.sql.connections.sqlite_connection import SqliteConnection
from amsdal_glue_connections.sql.schema_registry import TABLE_REGISTRY


def _register(connection: SqliteConnection, name: str, properties: list[PropertySchema]) -> SchemaReference:
    connection.run_schema_command(
        SchemaCommand(
            mutations=[
                RegisterSchema(
                    schema_ref=SchemaReference(name=name, version=Version.LATEST),
                    schema=Schema(name=name, version=Version.LATEST, properties=properties),
                ),
            ],
        ),
    )
    return SchemaReference(name=name, version=Version.LATEST)


def _get_schema(connection: SqliteConnection, table_name: str) -> Schema:
    query = QueryStatement(table=SchemaReference(name=TABLE_REGISTRY, version=Version.LATEST))
    schemas = [schema for schema in connection.query_schema(query) if schema.name == table_name]
    assert schemas, f'schema {table_name!r} not found'
    return schemas[0]


def test_double_column_round_trips_to_double(database_connection: SqliteConnection) -> None:
    _register(
        database_connection,
        'metric',
        [
            PropertySchema(name='id', type=ScalarType.INTEGER, required=True),
            PropertySchema(name='value', type=ScalarType.DOUBLE, required=True),
        ],
    )

    schema = _get_schema(database_connection, 'metric')
    by_name = {p.name: p for p in schema.properties}
    assert by_name['value'].type == ScalarType.DOUBLE


def test_timestamptz_column_round_trips_to_timestamptz(database_connection: SqliteConnection) -> None:
    _register(
        database_connection,
        'event',
        [
            PropertySchema(name='id', type=ScalarType.INTEGER, required=True),
            PropertySchema(name='created_at', type=ScalarType.TIMESTAMPTZ, required=True),
        ],
    )

    schema = _get_schema(database_connection, 'event')
    by_name = {p.name: p for p in schema.properties}
    assert by_name['created_at'].type == ScalarType.TIMESTAMPTZ


def test_timestamptz_datetime_reads_back_as_python_datetime(database_connection: SqliteConnection) -> None:
    schema_ref = _register(
        database_connection,
        'event',
        [
            PropertySchema(name='id', type=ScalarType.INTEGER, required=True),
            PropertySchema(name='created_at', type=ScalarType.TIMESTAMPTZ, required=True),
        ],
    )

    created_at = datetime(2020, 1, 2, 3, 4, 5, tzinfo=timezone.utc)
    database_connection.run_mutations([
        InsertData(schema=schema_ref, data=[DataInput(data={'id': 1, 'created_at': created_at})]),
    ])

    result = database_connection.query(QueryStatement(table=schema_ref))
    assert len(result) == 1
    row = result[0].data

    # A timestamptz-declared column must re-hydrate into a Python datetime, not stay an ISO string.
    assert isinstance(row['created_at'], datetime)
    assert row['created_at'] == created_at
