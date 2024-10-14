from collections.abc import Callable
from typing import Any

from amsdal_glue_core.common.data_models.aggregation import AggregationQuery
from amsdal_glue_core.common.data_models.annotation import AnnotationQuery
from amsdal_glue_core.common.data_models.annotation import ExpressionAnnotation
from amsdal_glue_core.common.data_models.annotation import ValueAnnotation
from amsdal_glue_core.common.data_models.conditions import Conditions
from amsdal_glue_core.common.data_models.field_reference import FieldReference
from amsdal_glue_core.common.data_models.group_by import GroupByQuery
from amsdal_glue_core.common.data_models.join import JoinQuery
from amsdal_glue_core.common.data_models.limit import LimitQuery
from amsdal_glue_core.common.data_models.order_by import OrderByQuery
from amsdal_glue_core.common.data_models.query import QueryStatement
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.data_models.sub_query import SubQueryStatement
from amsdal_glue_core.common.enums import FieldLookup
from amsdal_glue_core.common.expressions.common import CombinedExpression
from amsdal_glue_core.common.expressions.common import Expression
from amsdal_glue_core.common.expressions.raw import RawExpression
from amsdal_glue_core.common.expressions.value import Value

from amsdal_glue_connections.sql.sql_builders.build_only_constructor import build_field
from amsdal_glue_connections.sql.sql_builders.build_only_constructor import BuildOnlyConstructor
from amsdal_glue_connections.sql.sql_builders.build_only_constructor import default_build_only
from amsdal_glue_connections.sql.sql_builders.math_operator_transform import default_math_operator_transform
from amsdal_glue_connections.sql.sql_builders.math_operator_transform import MathOperatorTransform
from amsdal_glue_connections.sql.sql_builders.nested_field_transform import default_nested_field_transform
from amsdal_glue_connections.sql.sql_builders.nested_field_transform import NestedFieldTransform
from amsdal_glue_connections.sql.sql_builders.operator_constructor import default_operator_constructor
from amsdal_glue_connections.sql.sql_builders.operator_constructor import OperatorConstructor


def build_sql_query(  # noqa: PLR0913
    query: QueryStatement,
    value_placeholder: str = '?',
    table_separator: str = '.',
    operator_constructor: OperatorConstructor = default_operator_constructor,
    table_quote: str = '',
    field_quote: str = '',
    value_transform: Callable[[Any], Any] = lambda x: x,
    nested_field_transform: NestedFieldTransform = default_nested_field_transform,
    math_operator_transform: MathOperatorTransform = default_math_operator_transform,
    build_only: BuildOnlyConstructor = default_build_only,
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
        math_operator_transform (Callable, optional): The function to transform math operators.
        build_only (Callable, optional): The function to build fields for the SELECT statement.

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
        math_operator_transform=math_operator_transform,
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


def build_annotations(  # noqa: PLR0913
    annotations: list[AnnotationQuery] | None,
    value_placeholder: str = '?',
    table_separator: str = '.',
    operator_constructor: OperatorConstructor = default_operator_constructor,
    table_quote: str = '',
    field_quote: str = '',
    value_transform: Callable[[Any], Any] = lambda x: x,
    nested_field_transform: NestedFieldTransform = default_nested_field_transform,
    math_operator_transform: MathOperatorTransform = default_math_operator_transform,
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
        elif isinstance(annotation.value, ExpressionAnnotation):
            _expression, _values = build_expression(
                annotation.value.expression,
                value_placeholder=value_placeholder,
                table_separator=table_separator,
                table_quote=table_quote,
                field_quote=field_quote,
                nested_field_transform=nested_field_transform,
                math_operator_transform=math_operator_transform,
            )
            _val = f'({_expression})'
            items.append(f'{_val} AS {field_quote}{annotation.value.alias}{field_quote}')
            values.extend(_values)
        elif isinstance(annotation.value, ValueAnnotation):
            items.append(f'{value_placeholder} AS {field_quote}{annotation.value.alias}{field_quote}')
            values.append(annotation.value.value.value)

    return ', '.join(items), values


def build_aggregations(
    aggregations: list[AggregationQuery] | None,
    table_separator: str = '.',
    table_quote: str = '',
    field_quote: str = '',
    nested_field_transform: NestedFieldTransform = default_nested_field_transform,
) -> str | None:
    if not aggregations:
        return None

    items = []

    for aggregation in aggregations:
        if aggregation.expression.field.field.name == '*':
            _field = '*'
        else:
            _field = build_field(
                aggregation.expression.field,
                table_separator=table_separator,
                table_quote=table_quote,
                field_quote=field_quote,
                nested_field_transform=nested_field_transform,
            )
        items.append(f'{aggregation.expression.name}({_field}) AS {field_quote}{aggregation.alias}{field_quote}')

    return ', '.join(items)


def build_expression(  # noqa: PLR0913
    expression: Expression,
    value_placeholder: str = '?',
    table_separator: str = '.',
    table_quote: str = '',
    field_quote: str = '',
    value_type: Any = str,
    nested_field_transform: NestedFieldTransform = default_nested_field_transform,
    math_operator_transform: MathOperatorTransform = default_math_operator_transform,
) -> tuple[str, list[Any]]:
    values = []

    if isinstance(expression, CombinedExpression):
        _left, _values = build_expression(
            expression.left,
            value_placeholder=value_placeholder,
            table_separator=table_separator,
            table_quote=table_quote,
            field_quote=field_quote,
            value_type=value_type,
            nested_field_transform=nested_field_transform,
            math_operator_transform=math_operator_transform,
        )
        values.extend(_values)

        _right, _values = build_expression(
            expression.right,
            value_placeholder=value_placeholder,
            table_separator=table_separator,
            table_quote=table_quote,
            field_quote=field_quote,
            value_type=value_type,
            nested_field_transform=nested_field_transform,
            math_operator_transform=math_operator_transform,
        )
        values.extend(_values)

        return math_operator_transform(_left, expression.operator, _right), values
    if isinstance(expression, FieldReference):
        return build_field(
            expression,
            table_separator=table_separator,
            table_quote=table_quote,
            field_quote=field_quote,
            value_type=value_type,
            nested_field_transform=nested_field_transform,
        ), []
    if isinstance(expression, Value):
        return value_placeholder, [expression.value]
    if isinstance(expression, RawExpression):
        return expression.value, []

    msg = f'Unsupported expression type: {type(expression)}'
    raise ValueError(msg)


def build_from(  # noqa: PLR0913
    table: SchemaReference | SubQueryStatement,
    value_placeholder: str = '?',
    table_separator: str = '.',
    operator_constructor: OperatorConstructor = default_operator_constructor,
    table_quote: str = '',
    field_quote: str = '',
    value_transform: Callable[[Any], Any] = lambda x: x,
    nested_field_transform: NestedFieldTransform = default_nested_field_transform,
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

    _namespace_prefix = f'{table_quote}{table.namespace}{table_quote}{table_separator}' if table.namespace else ''
    _stmt = f'{_namespace_prefix}{table_quote}{table.name}{table_quote}'

    if table.alias:
        return f'{_stmt} AS {table_quote}{table.alias}{table_quote}', []
    return _stmt, []


def build_joins(  # noqa: PLR0913
    joins: list[JoinQuery] | None,
    value_placeholder: str = '?',
    table_separator: str = '.',
    operator_constructor: OperatorConstructor = default_operator_constructor,
    table_quote: str = '',
    field_quote: str = '',
    value_transform: Callable[[Any], Any] = lambda x: x,
    nested_field_transform: NestedFieldTransform = default_nested_field_transform,
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
            _namespace_prefix = (
                (f'{table_quote}' f'{join.table.namespace}{table_quote}{table_separator}')
                if join.table.namespace
                else ''
            )
            _table = f'{_namespace_prefix}{table_quote}{join.table.name}{table_quote}'

            if join.table.alias:
                _table += f' AS {table_quote}{join.table.alias}{table_quote}'
        items.append(f'{join.join_type.value} JOIN {_table} ON {_on}')

    return ' '.join(items), values


def build_conditions(  # noqa: PLR0913
    conditions: Conditions | None,
    operator_constructor: OperatorConstructor,
    value_placeholder: str = '?',
    table_separator: str = '.',
    null_value: str = 'NULL',
    table_quote: str = '',
    field_quote: str = '',
    value_transform: Callable[[Any], Any] = lambda x: x,
    nested_field_transform: NestedFieldTransform = default_nested_field_transform,
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
            _stmt = f'({_condition})'

            if condition.negated:
                _stmt = f'NOT {_stmt}'

            items.append(_stmt)
            values.extend(_values)
            continue

        _value_type = type(condition.value.value) if isinstance(condition.value, Value) else None
        if condition.lookup == FieldLookup.ISNULL and _value_type:
            _value_type = None

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
    operator_constructor: OperatorConstructor = default_operator_constructor,
    value_placeholder: str = '?',
    table_separator: str = '.',
    null_value: str = 'NULL',
    table_quote: str = '',
    field_quote: str = '',
    value_transform: Callable[[Any], Any] = lambda x: x,
    nested_field_transform: NestedFieldTransform = default_nested_field_transform,
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
    nested_field_transform: NestedFieldTransform = default_nested_field_transform,
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
    nested_field_transform: NestedFieldTransform = default_nested_field_transform,
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
    if not limit or limit.limit is None:
        return None

    _limit_stm = f'LIMIT {limit.limit}'

    if limit.offset:
        _limit_stm += f' OFFSET {limit.offset}'

    return _limit_stm
