from collections.abc import Callable
from typing import Any

from amsdal_glue_core.common.data_models.aggregation import AggregationQuery
from amsdal_glue_core.common.data_models.annotation import AnnotationQuery
from amsdal_glue_core.common.data_models.conditions import Conditions
from amsdal_glue_core.common.data_models.field_reference import FieldReference
from amsdal_glue_core.common.data_models.field_reference import FieldReferenceAliased
from amsdal_glue_core.common.data_models.group_by import GroupByQuery
from amsdal_glue_core.common.data_models.join import JoinQuery
from amsdal_glue_core.common.data_models.limit import LimitQuery
from amsdal_glue_core.common.data_models.order_by import OrderByQuery
from amsdal_glue_core.common.data_models.query import QueryStatement
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.data_models.sub_query import SubQueryStatement
from amsdal_glue_core.common.enums import FieldLookup
from amsdal_glue_core.common.expressions.value import Value

from amsdal_glue_connections.sql.sql_builders.nested_field_transform import default_nested_field_transform
from amsdal_glue_connections.sql.sql_builders.operator_constructor import default_operator_constructor


def build_sql_query(  # noqa: PLR0913
    query: QueryStatement,
    value_placeholder: str = '?',
    table_separator: str = '.',
    operator_constructor: Callable[
        [
            str,
            FieldLookup,
            FieldReference | Value,
            str,
            str,
            str,
            str,
            str,
            Callable[[Any], Any],
            Callable[[str, str, list[str], Any, str, str, str], str],
        ],
        tuple[str, list[Any]],
    ] = default_operator_constructor,
    table_quote: str = '',
    field_quote: str = '',
    value_transform: Callable[[Any], Any] = lambda x: x,
    nested_field_transform: Callable[[str, str, list[str], Any, str, str, str], str] = default_nested_field_transform,
) -> tuple[str, list[Any]]:
    """
    Builds an SQL query for the given query statement.

    Args:
        query (QueryStatement): The query statement to be converted to an SQL query.
        value_placeholder (str, optional): The placeholder for values in the SQL query. Defaults to '?'.
        table_separator (str, optional): The separator for table names. Defaults to '.'.
        operator_constructor (Callable, optional): The function to construct operators.
                                                   Defaults to default_operator_constructor.
        table_quote (str, optional): The quote character for table names. Defaults to ''.
        field_quote (str, optional): The quote character for field names. Defaults to ''.
        value_transform (Callable, optional): The function to transform values. Defaults to lambda x: x.
        nested_field_transform (Callable, optional): The function to transform nested fields.
                                                     Defaults to default_nested_field_transform.

    Returns:
        tuple[str, list[Any]]: The SQL query and the list of values.
    """
    values = []
    stmt_parts: list[str | None] = [
        'SELECT',
    ]

    # Only & Aggregations
    smtp_selection: list[str | None] = [
        build_only(
            query.only,
            table_separator=table_separator,
            table_quote=table_quote,
            field_quote=field_quote,
            distinct=query.distinct,
            nested_field_transform=nested_field_transform,
        ),
        build_aggregations(
            query.aggregations,
            table_separator=table_separator,
            table_quote=table_quote,
            field_quote=field_quote,
            nested_field_transform=nested_field_transform,
        ),
    ]

    # Annotations
    _annotations, _values = build_annotations(
        query.annotations,
        value_placeholder=value_placeholder,
        table_separator=table_separator,
        operator_constructor=operator_constructor,
        table_quote=table_quote,
        field_quote=field_quote,
        value_transform=value_transform,
        nested_field_transform=nested_field_transform,
    )
    values.extend(_values)

    smtp_selection.append(_annotations)
    _cleaned_smtp_selection = list(filter(None, smtp_selection))
    stmt_parts.append(', '.join(_cleaned_smtp_selection) if _cleaned_smtp_selection else '*')

    # From
    _from, _values = build_from(
        query.table,
        value_placeholder=value_placeholder,
        table_separator=table_separator,
        operator_constructor=operator_constructor,
        table_quote=table_quote,
        field_quote=field_quote,
        value_transform=value_transform,
        nested_field_transform=nested_field_transform,
    )
    values.extend(_values)

    # Joins
    _joins, _values = build_joins(
        query.joins,
        value_placeholder=value_placeholder,
        table_separator=table_separator,
        operator_constructor=operator_constructor,
        table_quote=table_quote,
        field_quote=field_quote,
        value_transform=value_transform,
        nested_field_transform=nested_field_transform,
    )
    values.extend(_values)
    _where, _values = build_where(
        query.where,
        operator_constructor=operator_constructor,
        value_placeholder=value_placeholder,
        table_separator=table_separator,
        table_quote=table_quote,
        field_quote=field_quote,
        value_transform=value_transform,
        nested_field_transform=nested_field_transform,
    )

    if _where:
        _where = f'WHERE {_where}'

    values.extend(_values)

    stmt_parts.extend([
        'FROM',
        _from,
        _joins,
        _where,
        build_group_by(
            query.group_by,
            table_separator=table_separator,
            table_quote=table_quote,
            field_quote=field_quote,
            nested_field_transform=nested_field_transform,
        ),
        build_order_by(
            query.order_by,
            table_separator=table_separator,
            table_quote=table_quote,
            field_quote=field_quote,
            nested_field_transform=nested_field_transform,
        ),
        build_limit(query.limit),
    ])

    return ' '.join(filter(None, stmt_parts)), values


def build_only(
    only: list[FieldReference | FieldReferenceAliased] | None,
    table_separator: str = '.',
    table_quote: str = '',
    field_quote: str = '',
    nested_field_transform: Callable[[str, str, list[str], Any, str, str, str], str] = default_nested_field_transform,
    *,
    distinct: bool = False,
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
        return f'DISTINCT {fields}'

    return fields


def build_annotations(  # noqa: PLR0913
    annotations: list[AnnotationQuery] | None,
    value_placeholder: str = '?',
    table_separator: str = '.',
    operator_constructor: Callable[
        [
            str,
            FieldLookup,
            FieldReference | Value,
            str,
            str,
            str,
            str,
            str,
            Callable[[Any], Any],
            Callable[[str, str, list[str], Any, str, str, str], str],
        ],
        tuple[str, list[Any]],
    ] = default_operator_constructor,
    table_quote: str = '',
    field_quote: str = '',
    value_transform: Callable[[Any], Any] = lambda x: x,
    nested_field_transform: Callable[[str, str, list[str], Any, str, str, str], str] = default_nested_field_transform,
) -> tuple[str | None, list[Any]]:
    if not annotations:
        return None, []

    items = []
    values = []

    for annotation in annotations:
        if isinstance(annotation.value, SubQueryStatement):
            _query, _values = build_sql_query(
                annotation.value.query,
                value_placeholder=value_placeholder,
                table_separator=table_separator,
                operator_constructor=operator_constructor,
                table_quote=table_quote,
                field_quote=field_quote,
                value_transform=value_transform,
                nested_field_transform=nested_field_transform,
            )
            items.append(f'({_query}) AS {field_quote}{annotation.value.alias}{field_quote}')
            values.extend(_values)
        else:
            items.append(f'{value_placeholder} AS {field_quote}{annotation.value.alias}{field_quote}')
            values.append(annotation.value.value.value)

    return ', '.join(items), values


def build_aggregations(
    aggregations: list[AggregationQuery] | None,
    table_separator: str = '.',
    table_quote: str = '',
    field_quote: str = '',
    nested_field_transform: Callable[[str, str, list[str], Any, str, str, str], str] = default_nested_field_transform,
) -> str | None:
    if not aggregations:
        return None

    items = []

    for aggregation in aggregations:
        _field = build_field(
            aggregation.expression.field,
            table_separator=table_separator,
            table_quote=table_quote,
            field_quote=field_quote,
            nested_field_transform=nested_field_transform,
        )
        items.append(f'{aggregation.expression.name}({_field}) AS {field_quote}{aggregation.alias}{field_quote}')

    return ', '.join(items)


def build_field(
    field: FieldReference | FieldReferenceAliased,
    table_separator: str = '.',
    table_quote: str = '',
    field_quote: str = '',
    value_type: Any = str,
    nested_field_transform: Callable[[str, str, list[str], Any, str, str, str], str] = default_nested_field_transform,
) -> str:
    _item = []
    _field = field.field

    while _field:
        _item.append(_field.name)
        _field = _field.child  # type: ignore[assignment]

    if len(_item) == 1:
        _field_stm = _item[0]

        if field.table_name:
            _field_stm = (
                f'{table_quote}{field.table_name}{table_quote}{table_separator}{field_quote}{_field_stm}{field_quote}'
            )
        else:
            _field_stm = f'{field_quote}{_field_stm}{field_quote}'
    else:
        _field_stm = nested_field_transform(
            field.table_name,
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


def build_from(  # noqa: PLR0913
    table: SchemaReference | SubQueryStatement,
    value_placeholder: str = '?',
    table_separator: str = '.',
    operator_constructor: Callable[
        [
            str,
            FieldLookup,
            FieldReference | Value,
            str,
            str,
            str,
            str,
            str,
            Callable[[Any], Any],
            Callable[[str, str, list[str], Any, str, str, str], str],
        ],
        tuple[str, list[Any]],
    ] = default_operator_constructor,
    table_quote: str = '',
    field_quote: str = '',
    value_transform: Callable[[Any], Any] = lambda x: x,
    nested_field_transform: Callable[[str, str, list[str], Any, str, str, str], str] = default_nested_field_transform,
) -> tuple[str, list[Any]]:
    if isinstance(table, SubQueryStatement):
        _query, _values = build_sql_query(
            table.query,
            value_placeholder=value_placeholder,
            table_separator=table_separator,
            operator_constructor=operator_constructor,
            table_quote=table_quote,
            field_quote=field_quote,
            value_transform=value_transform,
            nested_field_transform=nested_field_transform,
        )
        return f'({_query}) AS {table_quote}{table.alias}{table_quote}', _values

    if table.alias:
        return f'{table_quote}{table.name}{table_quote} AS {table_quote}{table.alias}{table_quote}', []
    return f'{table_quote}{table.name}{table_quote}', []


def build_joins(  # noqa: PLR0913
    joins: list[JoinQuery] | None,
    value_placeholder: str = '?',
    table_separator: str = '.',
    operator_constructor: Callable[
        [
            str,
            FieldLookup,
            FieldReference | Value,
            str,
            str,
            str,
            str,
            str,
            Callable[[Any], Any],
            Callable[[str, str, list[str], Any, str, str, str], str],
        ],
        tuple[str, list[Any]],
    ] = default_operator_constructor,
    table_quote: str = '',
    field_quote: str = '',
    value_transform: Callable[[Any], Any] = lambda x: x,
    nested_field_transform: Callable[[str, str, list[str], Any, str, str, str], str] = default_nested_field_transform,
) -> tuple[str, list[Any]]:
    if not joins:
        return '', []

    items = []
    values = []

    for join in joins:
        _on, _values = build_conditions(
            join.on,
            value_placeholder=value_placeholder,
            table_separator=table_separator,
            operator_constructor=operator_constructor,
            table_quote=table_quote,
            field_quote=field_quote,
            value_transform=value_transform,
            nested_field_transform=nested_field_transform,
        )
        values.extend(_values)

        if isinstance(join.table, SubQueryStatement):
            _query, _values = build_sql_query(
                join.table.query,
                value_placeholder=value_placeholder,
                table_separator=table_separator,
                operator_constructor=operator_constructor,
                table_quote=table_quote,
                field_quote=field_quote,
                value_transform=value_transform,
                nested_field_transform=nested_field_transform,
            )
            _table = f'({_query}) AS {table_quote}{join.table.alias}{table_quote}'
            values.extend(_values)
        else:
            _table = f'{table_quote}{join.table.name}{table_quote}'

            if join.table.alias:
                _table += f' AS {table_quote}{join.table.alias}{table_quote}'
        items.append(f'{join.join_type.value} JOIN {_table} ON {_on}')

    return ' '.join(items), values


def build_conditions(  # noqa: PLR0913
    conditions: Conditions | None,
    operator_constructor: Callable[
        [
            str,
            FieldLookup,
            FieldReference | Value,
            str,
            str,
            str,
            str,
            str,
            Callable[[Any], Any],
            Callable[[str, str, list[str], Any, str, str, str], str],
        ],
        tuple[str, list[Any]],
    ],
    value_placeholder: str = '?',
    table_separator: str = '.',
    null_value: str = 'NULL',
    table_quote: str = '',
    field_quote: str = '',
    value_transform: Callable[[Any], Any] = lambda x: x,
    nested_field_transform: Callable[[str, str, list[str], Any, str, str, str], str] = default_nested_field_transform,
) -> tuple[str, list[Any]]:
    items = []
    values = []

    if not conditions:
        return '', []

    for condition in conditions.children:
        if isinstance(condition, Conditions):
            _condition, _values = build_conditions(
                condition,
                operator_constructor,
                value_placeholder=value_placeholder,
                table_separator=table_separator,
                table_quote=table_quote,
                field_quote=field_quote,
                value_transform=value_transform,
                nested_field_transform=nested_field_transform,
            )
            items.append(f'({_condition})')
            values.extend(_values)
            continue

        _value_type = type(condition.value.value) if isinstance(condition.value, Value) else None
        _field = build_field(
            condition.field,
            table_separator=table_separator,
            table_quote=table_quote,
            field_quote=field_quote,
            value_type=_value_type,
            nested_field_transform=nested_field_transform,
        )

        _statement, _values = operator_constructor(
            _field,
            condition.lookup,
            condition.value,
            value_placeholder,
            table_separator,
            null_value,
            table_quote,
            field_quote,
            value_transform,
            nested_field_transform,
        )

        if condition.negate:
            _statement = f'NOT ({_statement})'

        items.append(_statement)
        values.extend(_values)

    return f' {conditions.connector.value} '.join(items), values


def build_where(  # noqa: PLR0913
    where: Conditions | None,
    operator_constructor: Callable[
        [
            str,
            FieldLookup,
            FieldReference | Value,
            str,
            str,
            str,
            str,
            str,
            Callable[[Any], Any],
            Callable[[str, str, list[str], Any, str, str, str], str],
        ],
        tuple[str, list[Any]],
    ] = default_operator_constructor,
    value_placeholder: str = '?',
    table_separator: str = '.',
    null_value: str = 'NULL',
    table_quote: str = '',
    field_quote: str = '',
    value_transform: Callable[[Any], Any] = lambda x: x,
    nested_field_transform: Callable[[str, str, list[str], Any, str, str, str], str] = default_nested_field_transform,
) -> tuple[str, list[Any]]:
    if not where:
        return '', []

    return build_conditions(
        where,
        operator_constructor,
        value_placeholder=value_placeholder,
        table_separator=table_separator,
        null_value=null_value,
        table_quote=table_quote,
        field_quote=field_quote,
        value_transform=value_transform,
        nested_field_transform=nested_field_transform,
    )


def build_group_by(
    group_by: list[GroupByQuery] | None,
    table_separator: str = '.',
    table_quote: str = '',
    field_quote: str = '',
    nested_field_transform: Callable[[str, str, list[str], Any, str, str, str], str] = default_nested_field_transform,
) -> str | None:
    if not group_by:
        return None

    items: list[str] = [
        build_field(
            _group_by.field,
            table_separator=table_separator,
            table_quote=table_quote,
            field_quote=field_quote,
            nested_field_transform=nested_field_transform,
        )
        for _group_by in group_by
    ]

    return f'GROUP BY {", ".join(items)}'


def build_order_by(
    order_by: list[OrderByQuery] | None,
    table_separator: str = '.',
    table_quote: str = '',
    field_quote: str = '',
    nested_field_transform: Callable[[str, str, list[str], Any, str, str, str], str] = default_nested_field_transform,
) -> str | None:
    if not order_by:
        return None

    items = []

    for _order_by in order_by:
        _field = build_field(
            _order_by.field,
            table_separator=table_separator,
            table_quote=table_quote,
            field_quote=field_quote,
            nested_field_transform=nested_field_transform,
        )
        items.append(f'{_field} {_order_by.direction.value}')

    return f'ORDER BY {", ".join(items)}'


def build_limit(limit: LimitQuery | None) -> str | None:
    if not limit:
        return None

    _limit_stm = f'LIMIT {limit.limit}'

    if limit.offset:
        _limit_stm += f' OFFSET {limit.offset}'

    return _limit_stm
