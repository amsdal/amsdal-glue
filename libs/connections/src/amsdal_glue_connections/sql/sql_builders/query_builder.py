from typing import Any
from typing import TYPE_CHECKING

from amsdal_glue_core.common.data_models.aggregation import AggregationQuery
from amsdal_glue_core.common.data_models.annotation import AnnotationQuery
from amsdal_glue_core.common.data_models.annotation import ExpressionAnnotation
from amsdal_glue_core.common.data_models.annotation import ValueAnnotation
from amsdal_glue_core.common.data_models.conditions import Conditions
from amsdal_glue_core.common.data_models.group_by import GroupByQuery
from amsdal_glue_core.common.data_models.join import JoinQuery
from amsdal_glue_core.common.data_models.limit import LimitQuery
from amsdal_glue_core.common.data_models.order_by import OrderByQuery
from amsdal_glue_core.common.data_models.query import QueryStatement
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.data_models.sub_query import SubQueryStatement

from amsdal_glue_connections.sql.sql_builders.build_expression import build_expression
from amsdal_glue_connections.sql.sql_builders.build_field import build_field
from amsdal_glue_connections.sql.sql_builders.transform import Transform
from amsdal_glue_connections.sql.sql_builders.transform import TransformTypes

if TYPE_CHECKING:
    from amsdal_glue_connections.sql.sql_builders.operator_constructor import OperatorConstructor


def build_sql_query(
    query: QueryStatement,
    transform: Transform,
) -> tuple[str, list[Any]]:
    """
    Builds an SQL query for the given query statement.

    Args:
        query (QueryStatement): The query statement to be converted to an SQL query.
        transform: (Transform): The transform object to transform database specific SQL parts.

    Returns:
        tuple[str, list[Any]]: The SQL query and the list of values.
    """
    values = []
    stmt_parts: list[str | None] = [
        'SELECT',
    ]

    # Only & Aggregations
    smtp_selection: list[str | None] = [
        transform.apply(TransformTypes.BUILD_ONLY, only=query.only, transform=transform, distinct=query.distinct),
        build_aggregations(
            query.aggregations,
            transform=transform,
        ),
    ]

    _annotations, _values = build_annotations(
        query.annotations,
        transform=transform,
    )
    values.extend(_values)

    smtp_selection.append(_annotations)
    _cleaned_smtp_selection = list(filter(None, smtp_selection))
    stmt_parts.append(', '.join(_cleaned_smtp_selection) if _cleaned_smtp_selection else '*')

    # From
    _from, _values = build_from(
        query.table,
        transform=transform,
    )
    values.extend(_values)

    # Joins
    _joins, _values = build_joins(
        query.joins,
        transform=transform,
    )
    values.extend(_values)
    _where, _values = build_where(
        query.where,
        transform=transform,
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
            transform=transform,
        ),
        build_order_by(
            query.order_by,
            transform=transform,
        ),
        build_limit(query.limit),
    ])

    return ' '.join(filter(None, stmt_parts)), values


def build_annotations(
    annotations: list[AnnotationQuery] | None,
    transform: Transform,
) -> tuple[str | None, list[Any]]:
    if not annotations:
        return None, []

    items = []
    values = []

    for annotation in annotations:
        _alias = transform.apply(TransformTypes.FIELD_QUOTE, annotation.value.alias)

        if isinstance(annotation.value, SubQueryStatement):
            _query, _values = build_sql_query(
                annotation.value.query,
                transform=transform,
            )
            items.append(f'({_query}) AS {_alias}')
            values.extend(_values)
        elif isinstance(annotation.value, ExpressionAnnotation):
            _expression, _values = build_expression(
                annotation.value.expression,
                transform=transform,
            )
            items.append(f'({_expression}) AS {_alias}')
            values.extend(_values)
        elif isinstance(annotation.value, ValueAnnotation):
            _expression, _values = build_expression(
                annotation.value.value,
                transform=transform,
            )
            _values = [transform.apply(TransformTypes.VALUE, _value) for _value in _values]
            items.append(f'{_expression} AS {_alias}')
            values.extend(_values)

    return ', '.join(items), values


def build_aggregations(
    aggregations: list[AggregationQuery] | None,
    transform: Transform,
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
                transform=transform,
            )
        _alias = transform.apply(TransformTypes.FIELD_QUOTE, aggregation.alias)
        items.append(f'{aggregation.expression.name}({_field}) AS {_alias}')

    return ', '.join(items)


def build_from(
    table: SchemaReference | SubQueryStatement,
    transform: Transform,
) -> tuple[str, list[Any]]:
    _alias = transform.apply(TransformTypes.FIELD_QUOTE, table.alias)

    if isinstance(table, SubQueryStatement):
        _query, _values = build_sql_query(
            table.query,
            transform=transform,
        )
        return f'({_query}) AS {_alias}', _values

    _namespace = transform.apply(TransformTypes.TABLE_QUOTE, table.namespace)
    _table = transform.apply(TransformTypes.TABLE_QUOTE, table.name)
    _stmt = transform.apply(TransformTypes.TABLE_SEPARATOR, _namespace, _table)

    if table.alias:
        return f'{_stmt} AS {_alias}', []
    return _stmt, []


def build_joins(
    joins: list[JoinQuery] | None,
    transform: Transform,
) -> tuple[str, list[Any]]:
    if not joins:
        return '', []

    items = []
    values = []

    for join in joins:
        _on, _values = build_conditions(
            join.on,
            transform=transform,
        )
        values.extend(_values)

        if isinstance(join.table, SubQueryStatement):
            _query, _values = build_sql_query(
                join.table.query,
                transform=transform,
            )
            _alias = transform.apply(TransformTypes.FIELD_QUOTE, join.table.alias)
            _table = f'({_query}) AS {_alias}'
            values.extend(_values)
        else:
            _namespace = transform.apply(TransformTypes.TABLE_QUOTE, join.table.namespace)
            _table = transform.apply(TransformTypes.TABLE_QUOTE, join.table.name)
            _table = transform.apply(TransformTypes.TABLE_SEPARATOR, _namespace, _table)

            if join.table.alias:
                table_quote = transform.apply(TransformTypes.TABLE_QUOTE, join.table.alias)
                _table += f' AS {table_quote}'
        items.append(f'{join.join_type.value} JOIN {_table} ON {_on}')

    return ' '.join(items), values


def build_conditions(
    conditions: Conditions | None,
    transform: Transform,
    *,
    embed_values: bool = False,
) -> tuple[str, list[Any]]:
    items = []
    values = []

    if not conditions:
        return '', []

    for condition in conditions.children:
        if isinstance(condition, Conditions):
            _condition, _values = build_conditions(
                condition,
                transform=transform,
                embed_values=embed_values,
            )
            _stmt = f'({_condition})'

            if condition.negated:
                _stmt = f'NOT {_stmt}'

            items.append(_stmt)
            values.extend(_values)
            continue

        operator_constructor: OperatorConstructor = transform.resolve(TransformTypes.OPERATOR_CONSTRUCTOR)
        _statement, _values = operator_constructor(
            condition.left,
            condition.lookup,
            condition.right,
            transform=transform,
            embed_values=embed_values,
        )

        if condition.negate:
            _statement = f'NOT ({_statement})'

        items.append(_statement)
        values.extend(_values)

    return f' {conditions.connector.value} '.join(items), values


def build_where(
    where: Conditions | None,
    transform: Transform,
    *,
    embed_values: bool = False,
) -> tuple[str, list[Any]]:
    if not where:
        return '', []

    return build_conditions(
        where,
        transform=transform,
        embed_values=embed_values,
    )


def build_group_by(
    group_by: list[GroupByQuery] | None,
    transform: Transform,
) -> str | None:
    if not group_by:
        return None

    items: list[str] = [
        build_field(
            _group_by.field,
            transform=transform,
        )
        for _group_by in group_by
    ]

    return f'GROUP BY {", ".join(items)}'


def build_order_by(
    order_by: list[OrderByQuery] | None,
    transform: Transform,
) -> str | None:
    if not order_by:
        return None

    items = []

    for _order_by in order_by:
        _field = build_field(
            _order_by.field,
            transform=transform,
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
