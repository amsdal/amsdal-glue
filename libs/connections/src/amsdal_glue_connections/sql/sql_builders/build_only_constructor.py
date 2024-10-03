from typing import Any
from typing import Protocol

from amsdal_glue_core.common.data_models.field_reference import FieldReference
from amsdal_glue_core.common.data_models.field_reference import FieldReferenceAliased

from amsdal_glue_connections.sql.sql_builders.exceptions import DistinctOnNotSupportedError
from amsdal_glue_connections.sql.sql_builders.nested_field_transform import default_nested_field_transform
from amsdal_glue_connections.sql.sql_builders.nested_field_transform import NestedFieldTransform


class BuildOnlyConstructor(Protocol):
    def __call__(
        self,
        only: list[FieldReference | FieldReferenceAliased] | None,
        table_separator: str = '.',
        table_quote: str = '',
        field_quote: str = '',
        nested_field_transform: NestedFieldTransform = default_nested_field_transform,
        *,
        distinct: bool | list[FieldReference | FieldReferenceAliased] = False,
    ) -> str | None: ...


def build_field(
    field: FieldReference | FieldReferenceAliased,
    table_separator: str = '.',
    table_quote: str = '',
    field_quote: str = '',
    value_type: Any = str,
    nested_field_transform: NestedFieldTransform = default_nested_field_transform,
) -> str:
    _item = []
    _field = field.field
    _namespace_prefix = f'{table_quote}{field.namespace}{table_quote}{table_separator}' if field.namespace else ''

    while _field:
        _item.append(_field.name)
        _field = _field.child  # type: ignore[assignment]

    if len(_item) == 1:
        _field_stm = _item[0]

        _field_quote = '' if _field_stm == '*' else field_quote

        if field.table_name:
            _field_stm = (
                f'{_namespace_prefix}'
                f'{table_quote}{field.table_name}{table_quote}{table_separator}'
                f'{_field_quote}{_field_stm}{_field_quote}'
            )
        else:
            _field_stm = f'{_field_quote}{_field_stm}{_field_quote}'
    else:
        _field_stm = nested_field_transform(
            field.table_name,
            field.namespace,
            _item[0],
            _item[1:],
            value_type,
            table_separator,
            table_quote,
            field_quote,
        )

    if isinstance(field, FieldReferenceAliased) and field.alias:
        _field_stm = f'{_field_stm} AS {field_quote}{field.alias}{field_quote}'

    return _field_stm


def default_build_only(
    only: list[FieldReference | FieldReferenceAliased] | None,
    table_separator: str = '.',
    table_quote: str = '',
    field_quote: str = '',
    nested_field_transform: NestedFieldTransform = default_nested_field_transform,
    *,
    distinct: bool | list[FieldReference | FieldReferenceAliased] = False,
) -> str | None:
    if not only:
        return None

    items = [
        build_field(
            _only,
            table_separator=table_separator,
            table_quote=table_quote,
            field_quote=field_quote,
            nested_field_transform=nested_field_transform,
        )
        for _only in only
    ]

    fields = ', '.join(items)

    if distinct:
        if isinstance(distinct, list):
            raise DistinctOnNotSupportedError

        return f'DISTINCT {fields}'

    return fields


def pg_build_only(
    only: list[FieldReference | FieldReferenceAliased] | None,
    table_separator: str = '.',
    table_quote: str = '',
    field_quote: str = '',
    nested_field_transform: NestedFieldTransform = default_nested_field_transform,
    *,
    distinct: bool | list[FieldReference | FieldReferenceAliased] = False,
) -> str | None:
    if not only:
        return None

    items = [
        build_field(
            _only,
            table_separator=table_separator,
            table_quote=table_quote,
            field_quote=field_quote,
            nested_field_transform=nested_field_transform,
        )
        for _only in only
    ]

    fields = ', '.join(items)

    if distinct:
        if isinstance(distinct, list):
            distinct_fields = ', '.join([
                build_field(
                    _distinct,
                    table_separator=table_separator,
                    table_quote=table_quote,
                    field_quote=field_quote,
                    nested_field_transform=nested_field_transform,
                )
                for _distinct in distinct
            ])

            return f'DISTINCT ON ({distinct_fields}) {fields}'

        return f'DISTINCT {fields}'

    return fields
