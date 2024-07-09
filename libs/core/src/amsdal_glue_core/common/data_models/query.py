from dataclasses import dataclass

from amsdal_glue_core.common.data_models.aggregation import AggregationQuery
from amsdal_glue_core.common.data_models.annotation import AnnotationQuery
from amsdal_glue_core.common.data_models.conditions import Conditions
from amsdal_glue_core.common.data_models.field_reference import FieldReference
from amsdal_glue_core.common.data_models.field_reference import FieldReferenceAliased
from amsdal_glue_core.common.data_models.group_by import GroupByQuery
from amsdal_glue_core.common.data_models.join import JoinQuery
from amsdal_glue_core.common.data_models.limit import LimitQuery
from amsdal_glue_core.common.data_models.order_by import OrderByQuery
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.data_models.sub_query import SubQueryStatement


@dataclass(kw_only=True)
class QueryStatement:
    table: SchemaReference | SubQueryStatement
    only: list[FieldReference | FieldReferenceAliased] | None = None
    distinct: bool = False
    annotations: list[AnnotationQuery] | None = None
    aggregations: list[AggregationQuery] | None = None
    joins: list[JoinQuery] | None = None
    where: Conditions | None = None
    group_by: list[GroupByQuery] | None = None
    order_by: list[OrderByQuery] | None = None
    limit: LimitQuery | None = None

    @property
    def has_joins(self):
        return bool(self.joins)

    def get_related_tables(self) -> set[str]:
        if isinstance(self.table, SchemaReference):
            tables = {self.table.name}
        else:
            tables = {*self.table.query.get_related_tables()}

        if self.annotations:
            for annotation in self.annotations:
                if isinstance(annotation.value, SubQueryStatement):
                    tables.update(annotation.value.query.get_related_tables())

        if self.joins:
            for join in self.joins:
                if isinstance(join.table, SchemaReference):
                    tables.add(join.table.name)
                else:
                    tables.update(join.table.query.get_related_tables())

        return tables

    def __copy__(self):
        return QueryStatement(
            table=self.table,
            only=list(self.only) if self.only else None,
            annotations=list(self.annotations) if self.annotations else None,
            aggregations=list(self.aggregations) if self.aggregations else None,
            joins=list(self.joins) if self.joins else None,
            where=self.where.copy() if self.where else None,
            order_by=list(self.order_by) if self.order_by else None,
            group_by=list(self.group_by) if self.group_by else None,
            limit=self.limit,
        )
