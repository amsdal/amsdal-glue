from amsdal_glue_core.common.data_models.output_type import OutputType

from amsdal_glue_connections.sql.sql_builders.transform import Transform
from amsdal_glue_connections.sql.sql_builders.transform import TransformTypes


def sqlite_nested_field_transform(
    table_alias: str,
    namespace: str,  # noqa: ARG001
    field: str,
    fields: list[str],
    transform: Transform,
    output_type: type | OutputType | None = None,
) -> str:
    nested_fields_selection = '.'.join([
        '$',
        *fields,
    ])

    if output_type in (int, bool):
        _cast_type = 'integer'
    elif output_type is float:
        _cast_type = 'real'

    else:
        _cast_type = 'text'

    _alias = transform.apply(TransformTypes.TABLE_QUOTE, table_alias)
    _field = transform.apply(TransformTypes.FIELD_QUOTE, field)
    _stmt_field = transform.apply(TransformTypes.TABLE_SEPARATOR, _alias, _field)
    _stmt = f"jsonb_extract({_stmt_field}, '{nested_fields_selection}')"

    return transform.apply(TransformTypes.CAST, _stmt, output_type)
