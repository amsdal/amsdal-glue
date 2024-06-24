from typing import Any

from amsdal_glue_core.common.data_models.field_reference import FieldReference
from amsdal_glue_core.common.enums import FieldLookup
from amsdal_glue_core.common.expressions.value import Value


def default_operator_constructor(  # noqa: C901, PLR0915, PLR0912, PLR0913
    field: str,
    lookup: FieldLookup,
    value: FieldReference | Value,
    value_placeholder: str,
    field_separator: str,
    table_separator: str,
    null_value: str = 'NULL',
) -> tuple[str, list[Any]]:
    from amsdal_glue_connections.sql.sql_builders.query_builder import build_field

    values = []
    is_value: bool = False

    if isinstance(value, FieldReference):
        _value = build_field(
            value,
            field_separator=field_separator,
            table_separator=table_separator,
        )
    elif isinstance(value, Value):
        _value = value_placeholder
        is_value = True
    else:
        msg = f'Unsupported value type: {type(value)}'
        raise ValueError(msg)  # noqa: TRY004

    match lookup:
        case FieldLookup.EXACT:
            _statement = f'IS {_value}'

            if is_value:
                values.append(value.value)  # type: ignore[union-attr]
        case FieldLookup.EQ:
            _statement = f'= {_value}'

            if is_value:
                values.append(value.value)  # type: ignore[union-attr]
        case FieldLookup.NEQ:
            _statement = f'!= {_value}'

            if is_value:
                values.append(value.value)  # type: ignore[union-attr]
        case FieldLookup.GT:
            _statement = f'> {_value}'

            if is_value:
                values.append(value.value)  # type: ignore[union-attr]
        case FieldLookup.GTE:
            _statement = f'>= {_value}'

            if is_value:
                values.append(value.value)  # type: ignore[union-attr]
        case FieldLookup.LT:
            _statement = f'< {_value}'

            if is_value:
                values.append(value.value)  # type: ignore[union-attr]
        case FieldLookup.LTE:
            _statement = f'<= {_value}'

            if is_value:
                values.append(value.value)  # type: ignore[union-attr]
        case FieldLookup.IN:
            _statement = f'IN ({_value})'

            if is_value:
                values.append(value.value)  # type: ignore[union-attr]
        case FieldLookup.CONTAINS:
            _statement = f'LIKE {_value}'

            if is_value:
                values.append(f'%{value.value}%')  # type: ignore[union-attr]
        case FieldLookup.ICONTAINS:
            field = f'LOWER({field})'
            _statement = f'LIKE LOWER({_value})'

            if is_value:
                values.append(f'%{value.value}%')  # type: ignore[union-attr]
        case FieldLookup.STARTSWITH:
            _statement = f'LIKE {_value}'

            if is_value:
                values.append(f'{value.value}%')  # type: ignore[union-attr]
        case FieldLookup.ISTARTSWITH:
            field = f'LOWER({field})'
            _statement = f'LIKE LOWER({_value})'

            if is_value:
                values.append(f'{value.value}%')  # type: ignore[union-attr]
        case FieldLookup.ENDSWITH:
            _statement = f'LIKE {_value}'

            if is_value:
                values.append(f'%{value.value}')  # type: ignore[union-attr]
        case FieldLookup.IENDSWITH:
            field = f'LOWER({field})'
            _statement = f'LIKE LOWER({_value})'

            if is_value:
                values.append(f'%{value.value}')  # type: ignore[union-attr]
        case FieldLookup.ISNULL:
            _statement = f'IS {null_value}' if value.value else f'IS NOT {null_value}'  # type: ignore[union-attr]
        case FieldLookup.REGEX:
            _statement = f'REGEXP {_value}'

            if is_value:
                values.append(value.value)  # type: ignore[union-attr]
        case FieldLookup.IREGEX:
            field = f'LOWER({field})'
            _statement = f'REGEXP {_value}'

            if is_value:
                values.append(value.value)  # type: ignore[union-attr]
        case _:
            msg = f'{lookup} not supported'
            raise ValueError(msg)

    return f'{field} {_statement}', values


def repr_operator_constructor(  # noqa: C901, PLR0915, PLR0912, PLR0913
    field: str,
    lookup: FieldLookup,
    value: FieldReference | Value,
    value_placeholder: str,  # noqa: ARG001
    field_separator: str,
    table_separator: str,
    null_value: str = 'NULL',
) -> tuple[str, list[Any]]:
    from amsdal_glue_connections.sql.sql_builders.query_builder import build_field

    if isinstance(value, FieldReference):
        _value = build_field(
            value,
            field_separator=field_separator,
            table_separator=table_separator,
        )
    elif isinstance(value, Value):
        if isinstance(value.value, str):
            _value = f"'{value.value}'"
        elif value.value is None:
            _value = null_value
        else:
            _value = value.value
    else:
        msg = f'Unsupported value type: {type(value)}'
        raise ValueError(msg)  # noqa: TRY004

    match lookup:
        case FieldLookup.EXACT:
            _statement = f'IS {_value}'
        case FieldLookup.EQ:
            _statement = f'= {_value}'
        case FieldLookup.NEQ:
            _statement = f'!= {_value}'
        case FieldLookup.GT:
            _statement = f'> {_value}'
        case FieldLookup.GTE:
            _statement = f'>= {_value}'
        case FieldLookup.LT:
            _statement = f'< {_value}'
        case FieldLookup.LTE:
            _statement = f'<= {_value}'
        case FieldLookup.IN:
            _statement = f'IN ({_value})'
        case FieldLookup.CONTAINS:
            _statement = f"LIKE '%{value.value}%'"  # type: ignore[union-attr]
        case FieldLookup.ICONTAINS:
            field = f'LOWER({field})'
            _statement = f"LIKE '%{value.value.lower()}%'"  # type: ignore[union-attr]
        case FieldLookup.STARTSWITH:
            _statement = f"LIKE '{value.value}%'"  # type: ignore[union-attr]
        case FieldLookup.ISTARTSWITH:
            field = f'LOWER({field})'
            _statement = f"LIKE '{value.value.lower()}%'"  # type: ignore[union-attr]
        case FieldLookup.ENDSWITH:
            _statement = f"LIKE '%{value.value}'"  # type: ignore[union-attr]
        case FieldLookup.IENDSWITH:
            field = f'LOWER({field})'
            _statement = f"LIKE '%{value.value.lower()}'"  # type: ignore[union-attr]
        case FieldLookup.ISNULL:
            _statement = f'IS {null_value}' if value.value else f'IS NOT {null_value}'  # type: ignore[union-attr]
        case FieldLookup.REGEX:
            _statement = f'REGEXP {_value}'
        case FieldLookup.IREGEX:
            field = f'LOWER({field})'
            _statement = f'REGEXP {_value.lower()}'
        case _:
            msg = f'{lookup} not supported'
            raise ValueError(msg)

    return f'{field} {_statement}', []
