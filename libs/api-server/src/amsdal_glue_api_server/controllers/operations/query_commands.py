# mypy: disable-error-code="type-abstract"
from amsdal_glue_core.common.data_models.data import Data
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
from amsdal_glue_core.common.enums import JoinType
from amsdal_glue_core.common.expressions.aggregation import Avg
from amsdal_glue_core.common.expressions.aggregation import Count
from amsdal_glue_core.common.expressions.aggregation import Max
from amsdal_glue_core.common.expressions.aggregation import Min
from amsdal_glue_core.common.expressions.aggregation import Sum
from amsdal_glue_core.common.expressions.field_reference import FieldReferenceExpression
from amsdal_glue_core.common.operations.queries import DataQueryOperation
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


class SelectExpressionBody(BaseModel):
    expression: SumBody | CountBody | AvgBody | MinBody | MaxBody | SubQueryStatementBody
    alias: str


class GroupByBody(BaseModel):
    field: FieldReference


class QueryStatementBody(BaseModel):
    table: SchemaReference | SubQueryStatementBody
    only: list[FieldReference | FieldReferenceAliased] | None = None
    distinct: DistinctClause | None = None
    expressions: list[SelectExpressionBody] | None = None
    joins: list[JoinQueryBody] | None = None
    where: Conditions | None = None
    group_by: list[GroupByBody] | None = None
    order_by: list[OrderByQuery] | None = None
    limit: LimitQuery | None = None


SubQueryStatementBody.model_rebuild()
QueryStatementBody.model_rebuild()


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
    expr = body.expression
    core_expr: Sum | Count | Avg | Min | Max | SubQueryStatement
    if isinstance(expr, SubQueryStatementBody):
        core_expr = subquery_statement_to_core_subquery_statement(expr)
    else:
        core_expr = _aggregation_body_to_expression(expr)
    return SelectExpression(expression=core_expr, alias=body.alias)


def query_statement_to_core_query_statement(query: QueryStatementBody) -> QueryStatement:
    joins = [join_query_to_core_join_query(join) for join in query.joins] if query.joins else None

    expressions = (
        [select_expression_body_to_core(e) for e in query.expressions] if query.expressions else None
    )

    group_by = (
        [GroupByQuery(expression=FieldReferenceExpression(field_reference=g.field)) for g in query.group_by]
        if query.group_by
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
        expressions=expressions,
        joins=joins,
        where=conditions_to_core_conditions(query.where),
        group_by=group_by,
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
