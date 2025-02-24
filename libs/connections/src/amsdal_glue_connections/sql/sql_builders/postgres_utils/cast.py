from amsdal_glue_core.common.data_models.output_type import OutputType

from amsdal_glue_connections.sql.sql_builders.postgres_utils.type_transform import pg_value_type_transform


def pg_cast_transform(statement: str, output_type: type | OutputType | None) -> str:
    if output_type is None:
        return statement

    db_type = str(output_type) if isinstance(output_type, OutputType) else pg_value_type_transform(output_type)

    return f'({statement})::{db_type}'
