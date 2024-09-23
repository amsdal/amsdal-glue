from typing import Any
from typing import Protocol


class NestedFieldTransform(Protocol):
    def __call__(  # noqa: PLR0913
        self,
        table_alias: str,
        namespace: str,
        field: str,
        fields: list[str],
        value_type: Any = str,
        table_separator: str = '.',
        table_quote: str = '',
        field_quote: str = "'",
    ) -> str: ...


def default_nested_field_transform(  # noqa: PLR0913
    table_alias: str,
    namespace: str,
    field: str,
    fields: list[str],
    value_type: Any = str,  # noqa: ARG001
    table_separator: str = '.',
    table_quote: str = '',
    field_quote: str = "'",
) -> str:
    stmt = '__'.join([field, *fields])

    if table_alias:
        _namespace_prefix = f'{table_quote}{namespace}{table_quote}{table_separator}' if namespace else ''
        stmt = (
            f'{_namespace_prefix}'
            f'{table_quote}{table_alias}{table_quote}{table_separator}'
            f'{field_quote}{stmt}{field_quote}'
        )

    return stmt
