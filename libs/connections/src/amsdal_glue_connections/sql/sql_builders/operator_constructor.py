from collections.abc import Callable
from typing import Any

from amsdal_glue_core.common.data_models.field_reference import FieldReference
from amsdal_glue_core.common.enums import FieldLookup
from amsdal_glue_core.common.expressions.value import Value

from amsdal_glue_connections.sql.sql_builders.exceptions import BinaryValuesNotSupportedError
from amsdal_glue_connections.sql.sql_builders.nested_field_transform import default_nested_field_transform


def default_operator_constructor(  # noqa: C901, PLR0915, PLR0912, PLR0913
    field: str,
    lookup: FieldLookup,
    value: FieldReference | Value,
    value_placeholder: str,
    table_separator: str,
    null_value: str = 'NULL',
    table_quote: str = '',
    field_quote: str = '',
    value_transform: Callable[[Any], Any] = lambda x: x,
    nested_field_transform: Callable[[str, str, list[str], Any, str, str, str], str] = default_nested_field_transform,
) -> tuple[str, list[Any]]:
    """
    Constructs an SQL operator for the given field and lookup.

    Args:
        field (str): The field name.
        lookup (FieldLookup): The lookup type.
        value (FieldReference | Value): The value or field reference.
        value_placeholder (str): The placeholder for values in the SQL command.
        table_separator (str): The separator for table names.
        null_value (str, optional): The representation of NULL values. Defaults to 'NULL'.
        table_quote (str, optional): The quote character for table names. Defaults to ''.
        field_quote (str, optional): The quote character for field names. Defaults to ''.
        value_transform (Callable, optional): The function to transform values. Defaults to lambda x: x.
        nested_field_transform (Callable, optional): The function to transform nested fields.
                                                     Defaults to default_nested_field_transform.

    Returns:
        tuple[str, list[Any]]: The SQL operator and the list of values.
    """
    from amsdal_glue_connections.sql.sql_builders.query_builder import build_field

    values = []
    is_value: bool = False

    if isinstance(value, FieldReference):
        _value = build_field(
            value,
            table_separator=table_separator,
            table_quote=table_quote,
            field_quote=field_quote,
            nested_field_transform=nested_field_transform,
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
                values.append(value_transform(value.value))  # type: ignore[union-attr]
        case FieldLookup.EQ:
            _statement = f'= {_value}'

            if is_value:
                values.append(value_transform(value.value))  # type: ignore[union-attr]
        case FieldLookup.NEQ:
            _statement = f'!= {_value}'

            if is_value:
                values.append(value_transform(value.value))  # type: ignore[union-attr]
        case FieldLookup.GT:
            _statement = f'> {_value}'

            if is_value:
                values.append(value_transform(value.value))  # type: ignore[union-attr]
        case FieldLookup.GTE:
            _statement = f'>= {_value}'

            if is_value:
                values.append(value_transform(value.value))  # type: ignore[union-attr]
        case FieldLookup.LT:
            _statement = f'< {_value}'

            if is_value:
                values.append(value_transform(value.value))  # type: ignore[union-attr]
        case FieldLookup.LTE:
            _statement = f'<= {_value}'

            if is_value:
                values.append(value_transform(value.value))  # type: ignore[union-attr]
        case FieldLookup.IN:
            _statement = 'IN (' + ','.join(['?'] * len(value.value)) + ')'

            if is_value:
                if any(isinstance(val, bytes | bytearray) for val in value.value):  # type: ignore[union-attr]
                    raise BinaryValuesNotSupportedError

                values.extend([
                    value_transform(value)
                    for value in value.value  # type: ignore[union-attr]
                ])
        case FieldLookup.CONTAINS:
            _statement = f'LIKE {_value}'

            if is_value:
                values.append(f'%{value_transform(value.value)}%')  # type: ignore[union-attr]
        case FieldLookup.ICONTAINS:
            field = f'LOWER({field})'
            _statement = f'LIKE LOWER({_value})'

            if is_value:
                values.append(f'%{value_transform(value.value)}%')  # type: ignore[union-attr]
        case FieldLookup.STARTSWITH:
            _statement = f'GLOB {_value}'

            if is_value:
                values.append(f'{value_transform(value.value)}*')  # type: ignore[union-attr]
        case FieldLookup.ISTARTSWITH:
            field = f'LOWER({field})'
            _statement = f'LIKE LOWER({_value})'

            if is_value:
                values.append(f'{value_transform(value.value)}%')  # type: ignore[union-attr]
        case FieldLookup.ENDSWITH:
            _statement = f'GLOB {_value}'

            if is_value:
                values.append(f'*{value_transform(value.value)}')  # type: ignore[union-attr]
        case FieldLookup.IENDSWITH:
            field = f'LOWER({field})'
            _statement = f'LIKE LOWER({_value})'

            if is_value:
                values.append(f'%{value_transform(value.value)}')  # type: ignore[union-attr]
        case FieldLookup.ISNULL:
            _statement = f'IS {null_value}' if value.value else f'IS NOT {null_value}'  # type: ignore[union-attr]
        case FieldLookup.REGEX:
            _statement = f'REGEXP {_value}'

            if is_value:
                values.append(value_transform(value.value))  # type: ignore[union-attr]
        case FieldLookup.IREGEX:
            field = f'LOWER({field})'
            _statement = f'REGEXP {_value}'

            if is_value:
                values.append(value_transform(value.value))  # type: ignore[union-attr]
        case _:
            msg = f'{lookup} not supported'
            raise ValueError(msg)

    return f'{field} {_statement}', values


def repr_operator_constructor(  # noqa: PLR0913, PLR0912, C901, PLR0915
    field: str,
    lookup: FieldLookup,
    value: FieldReference | Value,
    value_placeholder: str,  # noqa: ARG001
    table_separator: str,
    null_value: str = 'NULL',
    table_quote: str = '',
    field_quote: str = '',
    value_transform: Callable[[Any], Any] = lambda x: x,
    nested_field_transform: Callable[[str, str, list[str], Any, str, str, str], str] = default_nested_field_transform,
) -> tuple[str, list[Any]]:
    from amsdal_glue_connections.sql.sql_builders.query_builder import build_field

    if isinstance(value, FieldReference):
        _value = build_field(
            value,
            table_separator=table_separator,
            table_quote=table_quote,
            field_quote=field_quote,
            nested_field_transform=nested_field_transform,
        )
    elif isinstance(value, Value):
        if isinstance(value.value, str):
            _value = f"'{value.value}'"
        elif value.value is None:
            _value = null_value
        else:
            _value = value_transform(value.value)
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
