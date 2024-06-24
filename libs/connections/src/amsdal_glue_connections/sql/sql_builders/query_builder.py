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

from amsdal_glue_connections.sql.sql_builders.operator_constructor import default_operator_constructor


def build_sql_query(
    query: QueryStatement,
    value_placeholder: str = '?',
    field_separator: str = '__',
    table_separator: str = '.',
    operator_constructor: Callable[
        [str, FieldLookup, FieldReference | Value, str, str, str, str],
        tuple[str, list[Any]],
    ] = default_operator_constructor,
) -> tuple[str, list[Any]]:
    values = []
    stmt_parts: list[str | None] = [
        'SELECT',
    ]

    # Only & Aggregations
    smtp_selection: list[str | None] = [
        build_only(query.only, field_separator=field_separator, table_separator=table_separator),
        build_aggregations(query.aggregations, field_separator=field_separator, table_separator=table_separator),
    ]

    # Annotations
    _annotations, _values = build_annotations(
        query.annotations,
        value_placeholder=value_placeholder,
        field_separator=field_separator,
        table_separator=table_separator,
        operator_constructor=operator_constructor,
    )
    values.extend(_values)

    smtp_selection.append(_annotations)
    _cleaned_smtp_selection = list(filter(None, smtp_selection))
    stmt_parts.append(', '.join(_cleaned_smtp_selection) if _cleaned_smtp_selection else '*')

    # From
    _from, _values = build_from(
        query.table,
        value_placeholder=value_placeholder,
        field_separator=field_separator,
        table_separator=table_separator,
        operator_constructor=operator_constructor,
    )
    values.extend(_values)

    # Joins
    _joins, _values = build_joins(
        query.joins,
        value_placeholder=value_placeholder,
        field_separator=field_separator,
        table_separator=table_separator,
        operator_constructor=default_operator_constructor,
    )
    values.extend(_values)
    _where, _values = build_where(query.where)

    if _where:
        _where = f'WHERE {_where}'

    values.extend(_values)

    stmt_parts.extend([
        'FROM',
        _from,
        _joins,
        _where,
        build_group_by(query.group_by, field_separator=field_separator, table_separator=table_separator),
        build_order_by(query.order_by, field_separator=field_separator, table_separator=table_separator),
        build_limit(query.limit),
    ])

    return ' '.join(filter(None, stmt_parts)), values


def build_only(
    only: list[FieldReference | FieldReferenceAliased] | None,
    field_separator: str = '__',
    table_separator: str = '.',
) -> str | None:
    if not only:
        return None

    items = [build_field(_only, field_separator=field_separator, table_separator=table_separator) for _only in only]

    return ', '.join(items)


def build_annotations(
    annotations: list[AnnotationQuery] | None,
    value_placeholder: str = '?',
    field_separator: str = '__',
    table_separator: str = '.',
    operator_constructor: Callable[
        [str, FieldLookup, FieldReference | Value, str, str, str, str],
        tuple[str, list[Any]],
    ] = default_operator_constructor,
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
                field_separator=field_separator,
                table_separator=table_separator,
                operator_constructor=operator_constructor,
            )
            items.append(f'({_query}) AS {annotation.value.alias}')
            values.extend(_values)
        else:
            items.append(f'{value_placeholder} AS {annotation.value.alias}')
            values.append(annotation.value.value.value)

    return ', '.join(items), values


def build_aggregations(
    aggregations: list[AggregationQuery] | None,
    field_separator: str = '__',
    table_separator: str = '.',
) -> str | None:
    if not aggregations:
        return None

    items = []

    for aggregation in aggregations:
        _field = build_field(
            aggregation.expression.field,
            field_separator=field_separator,
            table_separator=table_separator,
        )
        items.append(f'{aggregation.expression.name}({_field}) AS {aggregation.alias}')

    return ', '.join(items)


def build_field(
    field: FieldReference | FieldReferenceAliased,
    field_separator: str = '__',
    table_separator: str = '.',
) -> str:
    _item = []
    _field = field.field

    while _field:
        _item.append(_field.name)
        _field = _field.child  # type: ignore[assignment]

    _field_stm = field_separator.join(_item)

    if field.table_name:
        _field_stm = f'{field.table_name}{table_separator}{_field_stm}'

    if isinstance(field, FieldReferenceAliased) and field.alias:
        _field_stm = f'{_field_stm} AS {field.alias}'

    return _field_stm


def build_from(
    table: SchemaReference | SubQueryStatement,
    value_placeholder: str = '?',
    field_separator: str = '__',
    table_separator: str = '.',
    operator_constructor: Callable[
        [str, FieldLookup, FieldReference | Value, str, str, str, str],
        tuple[str, list[Any]],
    ] = default_operator_constructor,
) -> tuple[str, list[Any]]:
    if isinstance(table, SubQueryStatement):
        _query, _values = build_sql_query(
            table.query,
            value_placeholder=value_placeholder,
            field_separator=field_separator,
            table_separator=table_separator,
            operator_constructor=operator_constructor,
        )
        return f'({_query}) AS {table.alias}', _values

    if table.alias:
        return f'{table.name} AS {table.alias}', []
    return table.name, []


def build_joins(
    joins: list[JoinQuery] | None,
    value_placeholder: str = '?',
    field_separator: str = '__',
    table_separator: str = '.',
    operator_constructor: Callable[
        [str, FieldLookup, FieldReference | Value, str, str, str, str],
        tuple[str, list[Any]],
    ] = default_operator_constructor,
) -> tuple[str, list[Any]]:
    if not joins:
        return '', []

    items = []
    values = []

    for join in joins:
        _on, _values = build_conditions(
            join.on,
            value_placeholder=value_placeholder,
            field_separator=field_separator,
            table_separator=table_separator,
            operator_constructor=operator_constructor,
        )
        values.extend(_values)

        if isinstance(join.table, SubQueryStatement):
            _query, _values = build_sql_query(join.table.query)
            _table = f'({_query}) AS {join.table.alias}'
            values.extend(_values)
        else:
            _table = join.table.name

            if join.table.alias:
                _table += f' AS {join.table.alias}'
        items.append(f'{join.join_type.value} JOIN {_table} ON {_on}')

    return ' '.join(items), values


def build_conditions(
    conditions: Conditions | None,
    operator_constructor: Callable[
        [str, FieldLookup, FieldReference | Value, str, str, str, str],
        tuple[str, list[Any]],
    ],
    value_placeholder: str = '?',
    field_separator: str = '__',
    table_separator: str = '.',
    null_value: str = 'NULL',
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
                field_separator=field_separator,
                table_separator=table_separator,
            )
            items.append(f'({_condition})')
            values.extend(_values)
            continue

        _field = build_field(
            condition.field,
            field_separator=field_separator,
            table_separator=table_separator,
        )

        _statement, _values = operator_constructor(
            _field,
            condition.lookup,
            condition.value,
            value_placeholder,
            field_separator,
            table_separator,
            null_value,
        )

        if condition.negate:
            _statement = f'NOT ({_statement})'

        items.append(_statement)
        values.extend(_values)

    return f' {conditions.connector.value} '.join(items), values


def build_where(
    where: Conditions | None,
    operator_constructor: Callable[
        [str, FieldLookup, FieldReference | Value, str, str, str, str],
        tuple[str, list[Any]],
    ] = default_operator_constructor,
    value_placeholder: str = '?',
    field_separator: str = '__',
    table_separator: str = '.',
    null_value: str = 'NULL',
) -> tuple[str, list[Any]]:
    if not where:
        return '', []

    return build_conditions(
        where,
        operator_constructor,
        value_placeholder=value_placeholder,
        field_separator=field_separator,
        table_separator=table_separator,
        null_value=null_value,
    )


def build_group_by(
    group_by: list[GroupByQuery] | None,
    field_separator: str = '__',
    table_separator: str = '.',
) -> str | None:
    if not group_by:
        return None

    items: list[str] = [
        build_field(_group_by.field, field_separator=field_separator, table_separator=table_separator)
        for _group_by in group_by
    ]

    return f'GROUP BY {", ".join(items)}'


def build_order_by(
    order_by: list[OrderByQuery] | None,
    field_separator: str = '__',
    table_separator: str = '.',
) -> str | None:
    if not order_by:
        return None

    items = []

    for _order_by in order_by:
        _field = build_field(_order_by.field, field_separator=field_separator, table_separator=table_separator)
        items.append(f'{_field} {_order_by.direction.value}')

    return f'ORDER BY {", ".join(items)}'


def build_limit(limit: LimitQuery | None) -> str | None:
    if not limit:
        return None

    _limit_stm = f'LIMIT {limit.limit}'

    if limit.offset:
        _limit_stm += f' OFFSET {limit.offset}'

    return _limit_stm
