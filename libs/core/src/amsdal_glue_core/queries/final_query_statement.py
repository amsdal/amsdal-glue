from dataclasses import dataclass
from typing import TYPE_CHECKING

from amsdal_glue_core.common.data_models.aggregation import AggregationQuery
from amsdal_glue_core.common.data_models.annotation import ExpressionAnnotation
from amsdal_glue_core.common.data_models.annotation import ValueAnnotation
from amsdal_glue_core.common.data_models.conditions import Conditions
from amsdal_glue_core.common.data_models.field_reference import FieldReference
from amsdal_glue_core.common.data_models.field_reference import FieldReferenceAliased
from amsdal_glue_core.common.data_models.group_by import GroupByQuery
from amsdal_glue_core.common.data_models.limit import LimitQuery
from amsdal_glue_core.common.data_models.order_by import OrderByQuery
from amsdal_glue_core.common.enums import JoinType

if TYPE_CHECKING:
    from amsdal_glue_core.queries.data_query_nodes import DataQueryNode


@dataclass(kw_only=True)
class QueryStatementNode:
    """
    Represents a node in a query statement.

    Attributes:
        alias (str): The alias for the query node.
        query_node (DataQueryNode): The query node associated with this statement.
    """

    alias: str
    query_node: 'DataQueryNode'


@dataclass(kw_only=True)
class AnnotationQueryNode:
    """
    Represents a node for annotation queries.

    Attributes:
        value (QueryStatementNode | ValueAnnotation | ExpressionAnnotation): The value of the annotation query node,
                                                      which can be a query statement node or a value annotation.
    """

    value: QueryStatementNode | ValueAnnotation | ExpressionAnnotation


@dataclass(kw_only=True)
class JoinQueryNode:
    """
    Represents a node for join queries.

    Attributes:
        table (QueryStatementNode): The table to join.
        on (Conditions): The conditions for the join.
        join_type (JoinType): The type of join. Defaults to JoinType.INNER.
    """

    table: QueryStatementNode
    on: Conditions
    join_type: JoinType = JoinType.INNER


@dataclass(kw_only=True)
class FinalQueryStatement:
    """
    Represents the final query statement.

    Attributes:
        table (QueryStatementNode): The main table for the query.
        only (list[FieldReference | FieldReferenceAliased] | None): The fields to select in the query. Defaults to None.
        annotations (list[AnnotationQueryNode] | None): The annotations for the query. Defaults to None.
        aggregations (list[AggregationQuery] | None): The aggregations for the query. Defaults to None.
        joins (list[JoinQueryNode] | None): The join conditions for the query. Defaults to None.
        where (Conditions | None): The where conditions for the query. Defaults to None.
        group_by (list[GroupByQuery] | None): The group by conditions for the query. Defaults to None.
        order_by (list[OrderByQuery] | None): The order by conditions for the query. Defaults to None.
        limit (LimitQuery | None): The limit for the query. Defaults to None.
    """

    table: QueryStatementNode
    only: list[FieldReference | FieldReferenceAliased] | None = None
    annotations: list[AnnotationQueryNode] | None = None
    aggregations: list[AggregationQuery] | None = None
    joins: list[JoinQueryNode] | None = None
    where: Conditions | None = None
    group_by: list[GroupByQuery] | None = None
    order_by: list[OrderByQuery] | None = None
    limit: LimitQuery | None = None
