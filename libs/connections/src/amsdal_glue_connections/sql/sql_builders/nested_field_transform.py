from typing import Any


def default_nested_field_transform(  # noqa: PLR0913
    table_alias: str,
    field: str,
    fields: list[str],
    value_type: Any = str,  # noqa: ARG001
    table_separator: str = '.',
    table_quote: str = '',
    field_quote: str = "'",
) -> str:
    stmt = '__'.join([field, *fields])

    if table_alias:
        stmt = f'{table_quote}{table_alias}{table_quote}{table_separator}{field_quote}{stmt}{field_quote}'

    return stmt
