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


def _register_account(database_connection: SqliteConnection) -> SchemaReference:
    database_connection.run_schema_command(
        SchemaCommand(
            mutations=[
                RegisterSchema(
                    schema_ref=SchemaReference(name='account', version=Version.LATEST),
                    schema=Schema(
                        name='account',
                        version=Version.LATEST,
                        properties=[
                            PropertySchema(name='id', type=ScalarType.INTEGER, required=True),
                            PropertySchema(name='secret', type=ScalarType.BYTEA, required=True),
                        ],
                    ),
                ),
            ],
        ),
    )
    return SchemaReference(name='account', version=Version.LATEST)


def _introspect_secret_type(database_connection: SqliteConnection) -> object:
    query = QueryStatement(table=SchemaReference(name=TABLE_REGISTRY, version=Version.LATEST))
    schema = next(s for s in database_connection.query_schema(query) if s.name == 'account')
    return next(p.type for p in schema.properties if p.name == 'secret')


def test_bytea_schema_round_trips_to_scalar_bytea(database_connection: SqliteConnection) -> None:
    # A full RegisterSchema -> introspect cycle must recover ScalarType.BYTEA, not a CustomType.
    # If it does not, a re-migration diff (existing_prop != new_prop) spuriously emits UpdateProperty.
    _register_account(database_connection)

    assert _introspect_secret_type(database_connection) == ScalarType.BYTEA


def test_bytea_value_round_trips_as_bytes(database_connection: SqliteConnection) -> None:
    schema_ref = _register_account(database_connection)

    secret = b'\x00\x01hashed\xff'
    database_connection.run_mutations(
        [
            InsertData(schema=schema_ref, data=[DataInput(data={'id': 1, 'secret': secret})]),
        ]
    )

    result = database_connection.query(QueryStatement(table=schema_ref))
    stored = [row.data['secret'] for row in result]

    assert stored == [secret]
