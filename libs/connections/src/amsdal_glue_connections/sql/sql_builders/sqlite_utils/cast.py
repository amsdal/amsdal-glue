from amsdal_glue_core.common.data_models.output_type import OutputType

from amsdal_glue_connections.sql.sql_builders.sqlite_utils.type_transform import sqlite_value_type_transform


def sqlite_cast_transform(statement: str, output_type: type | OutputType | None) -> str:
    if output_type is None:
        return statement

    db_type = str(output_type) if isinstance(output_type, OutputType) else sqlite_value_type_transform(output_type)

    if db_type.lower() in ('jsonb', 'json'):
        return f'{db_type.lower()}({statement})'

    return f'cast({statement} as {db_type})'
