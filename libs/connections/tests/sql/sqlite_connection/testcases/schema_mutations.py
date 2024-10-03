from amsdal_glue_core.common.data_models.schema import PropertySchema
from amsdal_glue_core.common.data_models.schema import Schema
from amsdal_glue_core.common.enums import Version
from amsdal_glue_core.common.operations.commands import SchemaCommand
from amsdal_glue_core.common.operations.mutations.schema import RegisterSchema

from amsdal_glue_connections.sql.connections.sqlite_connection import SqliteConnection


def create_json_fields(database_connection: SqliteConnection) -> Schema:
    schema = Schema(
        name='JsonFieldsTable',
        version=Version.LATEST,
        properties=[
            PropertySchema(
                name='field_dict',
                type=dict,
                required=True,
            ),
            PropertySchema(
                name='field_list',
                type=list,
                required=True,
            ),
        ],
    )
    schemas = database_connection.run_schema_command(
        SchemaCommand(
            mutations=[
                RegisterSchema(schema=schema),
            ],
        ),
    )

    return schemas[0]  # type: ignore[return-value]
