# mypy: disable-error-code="type-abstract"
"""Native-pydantic request DTOs for the operations controllers.

Every DTO here maps 1:1 onto a request JSON wire shape and is fully
pydantic-native: no ``amsdal_glue_core`` ``@dataclass`` that references a
``TYPE_CHECKING``-only name is used as a field type, so pydantic can build the
JSON schema without any monkey-patching of core modules.

The recursive expression tree (``ExpressionBody``) is a discriminated union
driven by a *callable* discriminator that inspects the raw dict structure. This
keeps the wire tag-free -- the same key-presence disambiguation the API always
used -- while giving a single clear validation error instead of a union spray.
"""

from typing import Annotated
from typing import Any
from typing import Union

from amsdal_glue_core.common.data_models.conditions import Condition as CoreCondition
from amsdal_glue_core.common.data_models.conditions import Conditions as CoreConditions
from amsdal_glue_core.common.data_models.distinct import DistinctClause
from amsdal_glue_core.common.data_models.field_reference import FieldReference
from amsdal_glue_core.common.data_models.field_reference import FieldReferenceAliased
from amsdal_glue_core.common.data_models.group_by import GroupByQuery
from amsdal_glue_core.common.data_models.join import JoinQuery
from amsdal_glue_core.common.data_models.limit import LimitQuery
from amsdal_glue_core.common.data_models.order_by import OrderByQuery
from amsdal_glue_core.common.data_models.query import QueryStatement
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.data_models.select_expression import SelectExpression
from amsdal_glue_core.common.data_models.sub_query import SubQueryStatement
from amsdal_glue_core.common.enums import FieldLookup
from amsdal_glue_core.common.enums import FilterConnector
from amsdal_glue_core.common.enums import JoinType
from amsdal_glue_core.common.enums import OrderDirection
from amsdal_glue_core.common.enums import ScalarType
from amsdal_glue_core.common.expressions.aggregation import Avg
from amsdal_glue_core.common.expressions.aggregation import Count
from amsdal_glue_core.common.expressions.aggregation import Max
from amsdal_glue_core.common.expressions.aggregation import Min
from amsdal_glue_core.common.expressions.aggregation import Sum
from amsdal_glue_core.common.expressions.expression import Expression
from amsdal_glue_core.common.expressions.field_reference import FieldReferenceExpression
from amsdal_glue_core.common.expressions.value import Value
from pydantic import BaseModel
from pydantic import Discriminator
from pydantic import Tag

# ---------------------------------------------------------------------------
# Expression DTOs (arms of the ExpressionBody union)
#
# ``FieldReference`` (and friends like ``FieldReferenceAliased``) are plain core
# dataclasses whose own annotations resolve at runtime, so pydantic builds them
# natively -- they are reused directly as leaf field types. The types that used
# to force the monkey-patch (``Value``, ``FieldReferenceExpression``,
# ``OrderByQuery``, ``DistinctClause``) are the ones replaced by the DTOs below.
# ---------------------------------------------------------------------------


class ValueBody(BaseModel):
    """Wire: ``{"value": <scalar>, "output_type"?: <ScalarType>}``."""

    value: Any
    output_type: ScalarType | None = None


class FieldRefBody(BaseModel):
    """Wire: ``{"field_reference": {<FieldReference>}}`` (a field-reference expression)."""

    field_reference: FieldReference


class SumBody(BaseModel):
    field: FieldReference
    name: str = 'SUM'


class CountBody(BaseModel):
    field: FieldReference
    name: str = 'COUNT'


class AvgBody(BaseModel):
    field: FieldReference
    name: str = 'AVG'


class MinBody(BaseModel):
    field: FieldReference
    name: str = 'MIN'


class MaxBody(BaseModel):
    field: FieldReference
    name: str = 'MAX'


class SubQueryStatementBody(BaseModel):
    """Wire: ``{"query": {<QueryStatementBody>}, "alias": <str>}``."""

    query: 'QueryStatementBody'
    alias: str


_AGGREGATION_TAGS = frozenset({'SUM', 'COUNT', 'AVG', 'MIN', 'MAX'})


def _discriminate_expression(value: Any) -> str | None:  # noqa: C901, PLR0911
    """Map a raw expression to its union tag by structure (no wire tag needed).

    Mirrors the historical key-presence disambiguation:
    ``value`` -> value, ``field_reference`` -> field reference, ``query`` ->
    subquery, ``name``/``field`` -> aggregation. Returns ``None`` on no match so
    pydantic raises a single ``union_tag_invalid`` error.
    """
    if isinstance(value, dict):
        if 'value' in value:
            return 'value'
        if 'field_reference' in value:
            return 'field_reference'
        if 'query' in value:
            return 'sub_query'
        if 'name' in value:
            name = str(value['name']).upper()
            return name if name in _AGGREGATION_TAGS else None
        if 'field' in value:
            # Aggregation body without an explicit name defaults to SUM.
            return 'SUM'
        return None

    if isinstance(value, ValueBody):
        return 'value'
    if isinstance(value, FieldRefBody):
        return 'field_reference'
    if isinstance(value, SubQueryStatementBody):
        return 'sub_query'
    if isinstance(value, SumBody | CountBody | AvgBody | MinBody | MaxBody):
        return value.name
    return None


ExpressionBody = Annotated[
    Annotated[ValueBody, Tag('value')]
    | Annotated[FieldRefBody, Tag('field_reference')]
    | Annotated[SumBody, Tag('SUM')]
    | Annotated[CountBody, Tag('COUNT')]
    | Annotated[AvgBody, Tag('AVG')]
    | Annotated[MinBody, Tag('MIN')]
    | Annotated[MaxBody, Tag('MAX')]
    | Annotated[SubQueryStatementBody, Tag('sub_query')],
    Discriminator(_discriminate_expression),
]


# ---------------------------------------------------------------------------
# Condition DTOs
# ---------------------------------------------------------------------------


class Condition(BaseModel):
    left: ExpressionBody
    lookup: FieldLookup
    right: ExpressionBody
    negate: bool = False


class Conditions(BaseModel):
    children: list[Union[Condition, 'Conditions']]

    connector: FilterConnector = FilterConnector.AND
    negated: bool = False


# ---------------------------------------------------------------------------
# Query DTOs
# ---------------------------------------------------------------------------


class JoinQueryBody(BaseModel):
    table: SchemaReference | SubQueryStatementBody
    on: Conditions
    join_type: JoinType = JoinType.INNER


class GroupByBody(BaseModel):
    field: FieldReference


class OrderByBody(BaseModel):
    """Wire: ``{"field": {<FieldReference>}, "direction"?: <ASC|DESC>, "expression"?: <ExpressionBody>}``."""

    field: FieldReference
    direction: OrderDirection = OrderDirection.ASC
    expression: ExpressionBody | None = None


class DistinctBody(BaseModel):
    on_fields: list[FieldReference] | None = None


class SelectExpressionBody(BaseModel):
    expression: ExpressionBody
    alias: str


class QueryStatementBody(BaseModel):
    table: SchemaReference | SubQueryStatementBody
    only: list[FieldReference | FieldReferenceAliased] | None = None
    distinct: DistinctBody | None = None
    expressions: list[SelectExpressionBody] | None = None
    joins: list[JoinQueryBody] | None = None
    where: Conditions | None = None
    group_by: list[GroupByBody] | None = None
    order_by: list[OrderByBody] | None = None
    limit: LimitQuery | None = None


# Resolve the genuine self-referential / mutually-recursive forward refs.
SubQueryStatementBody.model_rebuild()
QueryStatementBody.model_rebuild()
Conditions.model_rebuild()
Condition.model_rebuild()


# ---------------------------------------------------------------------------
# Converters: DTO -> core
# ---------------------------------------------------------------------------


def _aggregation_body_to_expression(
    body: SumBody | CountBody | AvgBody | MinBody | MaxBody,
) -> Sum | Count | Avg | Min | Max:
    field_expr = FieldReferenceExpression(field_reference=body.field)
    if isinstance(body, SumBody):
        return Sum(expression=field_expr)
    if isinstance(body, CountBody):
        return Count(expression=field_expr)
    if isinstance(body, AvgBody):
        return Avg(expression=field_expr)
    if isinstance(body, MinBody):
        return Min(expression=field_expr)
    if isinstance(body, MaxBody):
        return Max(expression=field_expr)
    msg = f'Unsupported aggregation body: {body}'
    raise TypeError(msg)


def expression_body_to_core(expression: ExpressionBody) -> Expression:
    if isinstance(expression, ValueBody):
        # Build through the real Value constructor so coerce_to_field_type runs.
        return Value(value=expression.value, output_type=expression.output_type)
    if isinstance(expression, FieldRefBody):
        return FieldReferenceExpression(field_reference=expression.field_reference)
    if isinstance(expression, SubQueryStatementBody):
        return subquery_statement_to_core_subquery_statement(expression)
    if isinstance(expression, SumBody | CountBody | AvgBody | MinBody | MaxBody):
        return _aggregation_body_to_expression(expression)
    msg = f'Unsupported expression body: {expression!r}'
    raise TypeError(msg)


def condition_to_core_condition(condition: Condition) -> CoreCondition:
    return CoreCondition(
        left=expression_body_to_core(condition.left),
        lookup=condition.lookup,
        right=expression_body_to_core(condition.right),
        negate=condition.negate,
    )


def conditions_to_core_conditions(conditions: Conditions | None) -> CoreConditions | None:
    if conditions is None:
        return None

    return conditions_to_core_conditions_required(conditions)


def conditions_to_core_conditions_required(conditions: Conditions) -> CoreConditions:
    return CoreConditions(
        *[_process_condition(c) for c in conditions.children],
        connector=conditions.connector,
        negated=conditions.negated,
    )


def _process_condition(condition: Condition | Conditions) -> CoreCondition | CoreConditions:
    if isinstance(condition, Condition):
        return condition_to_core_condition(condition)
    return conditions_to_core_conditions_required(condition)


def order_by_body_to_core(order_by: OrderByBody) -> OrderByQuery:
    return OrderByQuery(
        field=order_by.field,
        direction=order_by.direction,
        expression=expression_body_to_core(order_by.expression) if order_by.expression is not None else None,
    )


def distinct_body_to_core(distinct: DistinctBody | None) -> DistinctClause | None:
    if distinct is None:
        return None
    return DistinctClause(on_fields=distinct.on_fields)


def join_query_to_core_join_query(join: JoinQueryBody) -> JoinQuery:
    return JoinQuery(
        table=(
            subquery_statement_to_core_subquery_statement(join.table)
            if isinstance(join.table, SubQueryStatementBody)
            else join.table
        ),
        on=conditions_to_core_conditions_required(join.on),
        join_type=join.join_type,
    )


def subquery_statement_to_core_subquery_statement(subquery: SubQueryStatementBody) -> SubQueryStatement:
    return SubQueryStatement(
        query=query_statement_to_core_query_statement(subquery.query),
        alias=subquery.alias,
    )


def select_expression_body_to_core(body: SelectExpressionBody) -> SelectExpression:
    return SelectExpression(expression=expression_body_to_core(body.expression), alias=body.alias)


def query_statement_to_core_query_statement(query: QueryStatementBody) -> QueryStatement:
    joins = [join_query_to_core_join_query(join) for join in query.joins] if query.joins else None

    expressions = [select_expression_body_to_core(e) for e in query.expressions] if query.expressions else None

    group_by = (
        [GroupByQuery(expression=FieldReferenceExpression(field_reference=g.field)) for g in query.group_by]
        if query.group_by
        else None
    )

    order_by = [order_by_body_to_core(o) for o in query.order_by] if query.order_by else None

    table: SchemaReference | SubQueryStatement = (
        subquery_statement_to_core_subquery_statement(query.table)
        if isinstance(query.table, SubQueryStatementBody)
        else query.table
    )

    return QueryStatement(
        table=table,
        only=query.only,
        distinct=distinct_body_to_core(query.distinct),
        expressions=expressions,
        joins=joins,
        where=conditions_to_core_conditions(query.where),
        group_by=group_by,
        order_by=order_by,
        limit=query.limit,
    )
