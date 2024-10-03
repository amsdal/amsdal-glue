import amsdal_glue as glue


def create_json_fields(database_connection: glue.SqliteConnection) -> glue.Schema:
    schema = glue.Schema(
        name='JsonFieldsTable',
        version=glue.Version.LATEST,
        properties=[
            glue.PropertySchema(
                name='field_dict',
                type=dict,
                required=True,
            ),
            glue.PropertySchema(
                name='field_list',
                type=list,
                required=True,
            ),
        ],
    )
    schemas = database_connection.run_schema_command(
        glue.SchemaCommand(
            mutations=[
                glue.RegisterSchema(schema=schema),
            ],
        ),
    )

    return schemas[0]
