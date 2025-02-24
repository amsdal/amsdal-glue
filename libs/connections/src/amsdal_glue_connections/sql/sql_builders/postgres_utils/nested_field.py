from amsdal_glue_core.common.data_models.output_type import OutputType

from amsdal_glue_connections.sql.sql_builders.transform import Transform
from amsdal_glue_connections.sql.sql_builders.transform import TransformTypes


def pg_nested_field_transform(
    table_alias: str,
    namespace: str,
    field: str,
    fields: list[str],
    transform: Transform,
    output_type: type | OutputType | None = None,
) -> str:
    last_extract_operator = '->>' if output_type is str else '->'

    if len(fields) > 1:
        nested_fields_selection = '->'
        nested_fields_selection += '->'.join(f"'{_field}'" for _field in fields[:-1])
        nested_fields_selection += f"{last_extract_operator}'{fields[-1]}'"
    else:
        nested_fields_selection = f"{last_extract_operator}'{fields[0]}'"

    _namespace = transform.apply(TransformTypes.TABLE_QUOTE, namespace)
    _table = transform.apply(TransformTypes.TABLE_QUOTE, table_alias)
    _field = transform.apply(TransformTypes.FIELD_QUOTE, field)
    _field_stmt = transform.apply(TransformTypes.TABLE_SEPARATOR, _namespace, _table, _field)

    _stmt = f'{_field_stmt}{nested_fields_selection}'

    return transform.apply(TransformTypes.CAST, _stmt, output_type)
