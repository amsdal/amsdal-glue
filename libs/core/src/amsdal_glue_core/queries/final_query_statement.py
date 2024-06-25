from dataclasses import dataclass
from typing import TYPE_CHECKING

from amsdal_glue_core.common.data_models.aggregation import AggregationQuery
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
    alias: str
    query_node: 'DataQueryNode'


@dataclass(kw_only=True)
class AnnotationQueryNode:
    value: QueryStatementNode | ValueAnnotation


@dataclass(kw_only=True)
class JoinQueryNode:
    table: QueryStatementNode
    on: Conditions
    join_type: JoinType = JoinType.INNER


@dataclass(kw_only=True)
class FinalQueryStatement:
    table: QueryStatementNode
    only: list[FieldReference | FieldReferenceAliased] | None = None
    annotations: list[AnnotationQueryNode] | None = None
    aggregations: list[AggregationQuery] | None = None
    joins: list[JoinQueryNode] | None = None
    where: Conditions | None = None
    group_by: list[GroupByQuery] | None = None
    order_by: list[OrderByQuery] | None = None
    limit: LimitQuery | None = None
