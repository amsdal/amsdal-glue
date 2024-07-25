# mypy: disable-error-code="type-abstract"
from amsdal_glue_core.common.data_models.aggregation import AggregationQuery
from amsdal_glue_core.common.data_models.annotation import AnnotationQuery
from amsdal_glue_core.common.data_models.annotation import ValueAnnotation
from amsdal_glue_core.common.data_models.data import Data
from amsdal_glue_core.common.data_models.field_reference import FieldReference
from amsdal_glue_core.common.data_models.field_reference import FieldReferenceAliased
from amsdal_glue_core.common.data_models.group_by import GroupByQuery
from amsdal_glue_core.common.data_models.join import JoinQuery
from amsdal_glue_core.common.data_models.limit import LimitQuery
from amsdal_glue_core.common.data_models.order_by import OrderByQuery
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.data_models.sub_query import SubQueryStatement
from amsdal_glue_core.common.enums import JoinType
from amsdal_glue_core.common.expressions.aggregation import AggregationExpression
from amsdal_glue_core.common.expressions.aggregation import Avg
from amsdal_glue_core.common.expressions.aggregation import Count
from amsdal_glue_core.common.expressions.aggregation import Max
from amsdal_glue_core.common.expressions.aggregation import Min
from amsdal_glue_core.common.expressions.aggregation import Sum
from amsdal_glue_core.common.operations.queries import DataQueryOperation
from amsdal_glue_core.common.operations.queries import QueryStatement
from amsdal_glue_core.common.services.queries import DataQueryService
from amsdal_glue_core.containers import Container
from fastapi import HTTPException
from pydantic import BaseModel

from amsdal_glue_api_server.controllers.operations.models import Conditions
from amsdal_glue_api_server.controllers.operations.models import conditions_to_core_conditions
from amsdal_glue_api_server.controllers.operations.models import conditions_to_core_conditions_required


class SubQueryStatementBody(BaseModel):
    query: 'QueryStatementBody'
    alias: str


class AnnotationQueryBody(BaseModel):
    value: SubQueryStatementBody | ValueAnnotation


class JoinQueryBody(BaseModel):
    table: SchemaReference | SubQueryStatementBody
    on: Conditions
    join_type: JoinType = JoinType.INNER


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


class AggregationQueryBody(BaseModel):
    expression: SumBody | CountBody | AvgBody | MinBody | MaxBody
    alias: str


class QueryStatementBody(BaseModel):
    table: SchemaReference | SubQueryStatementBody
    only: list[FieldReference | FieldReferenceAliased] | None = None
    distinct: bool = False
    annotations: list[AnnotationQueryBody] | None = None
    aggregations: list[AggregationQueryBody] | None = None
    joins: list[JoinQueryBody] | None = None
    where: Conditions | None = None
    group_by: list[GroupByQuery] | None = None
    order_by: list[OrderByQuery] | None = None
    limit: LimitQuery | None = None


def aggregation_query_to_core_aggregation_query(aggregation: AggregationQueryBody) -> AggregationQuery:
    _expression = aggregation.expression
    expression: AggregationExpression
    if isinstance(_expression, SumBody):
        expression = Sum(field=_expression.field)
    elif isinstance(_expression, CountBody):
        expression = Count(field=_expression.field)
    elif isinstance(_expression, AvgBody):
        expression = Avg(field=_expression.field)
    elif isinstance(_expression, MinBody):
        expression = Min(field=_expression.field)
    elif isinstance(_expression, MaxBody):
        expression = Max(field=_expression.field)
    else:
        msg = f'Unsupported aggregation expression: {_expression}'
        raise TypeError(msg)

    return AggregationQuery(
        expression=expression,
        alias=aggregation.alias,
    )


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


def annotation_to_core_annotation(annotation: AnnotationQueryBody) -> AnnotationQuery:
    return AnnotationQuery(
        value=(
            subquery_statement_to_core_subquery_statement(annotation.value)
            if isinstance(annotation.value, SubQueryStatementBody)
            else annotation.value
        ),
    )


def query_statement_to_core_query_statement(query: QueryStatementBody) -> QueryStatement:
    joins = [join_query_to_core_join_query(join) for join in query.joins] if query.joins else None

    annotations = (
        [annotation_to_core_annotation(annotation) for annotation in query.annotations] if query.annotations else None
    )

    aggregations = (
        [aggregation_query_to_core_aggregation_query(aggregation) for aggregation in query.aggregations]
        if query.aggregations
        else None
    )

    table: SchemaReference | SubQueryStatement = (
        subquery_statement_to_core_subquery_statement(query.table)
        if isinstance(query.table, SubQueryStatementBody)
        else query.table
    )

    return QueryStatement(
        table=table,
        only=query.only,
        distinct=query.distinct,
        annotations=annotations,
        aggregations=aggregations,
        joins=joins,
        where=conditions_to_core_conditions(query.where),
        group_by=query.group_by,
        order_by=query.order_by,
        limit=query.limit,
    )


async def data_query_command(
    query: QueryStatementBody,
    lock_id: str | None = None,
    root_transaction_id: str | None = None,
    transaction_id: str | None = None,
) -> list[Data]:
    query_service = Container.services.get(DataQueryService)
    result = query_service.execute(
        DataQueryOperation(
            query=query_statement_to_core_query_statement(query),
            lock_id=lock_id,
            root_transaction_id=root_transaction_id,
            transaction_id=transaction_id,
        )
    )

    if not result.success:
        raise HTTPException(status_code=400, detail=result.message)

    return result.data or []
