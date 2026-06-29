from dataclasses import dataclass

from amsdal_glue_core.common.data_models.conditions import Conditions
from amsdal_glue_core.common.data_models.cte import CommonTableExpression
from amsdal_glue_core.common.data_models.distinct import DistinctClause
from amsdal_glue_core.common.data_models.field_reference import FieldReference
from amsdal_glue_core.common.data_models.field_reference import FieldReferenceAliased
from amsdal_glue_core.common.data_models.group_by import GroupByQuery
from amsdal_glue_core.common.data_models.join import JoinQuery
from amsdal_glue_core.common.data_models.limit import LimitQuery
from amsdal_glue_core.common.data_models.order_by import OrderByQuery
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.data_models.select_expression import SelectExpression
from amsdal_glue_core.common.data_models.select_lock import SelectLock
from amsdal_glue_core.common.data_models.set_operation import SetOperation
from amsdal_glue_core.common.data_models.sub_query import SubQueryStatement


@dataclass(kw_only=True)
class QueryStatement:
    table: SchemaReference | SubQueryStatement | SetOperation
    only: list[FieldReference | FieldReferenceAliased] | None = None
    distinct: DistinctClause | None = None
    expressions: list[SelectExpression] | None = None
    joins: list[JoinQuery] | None = None
    where: Conditions | None = None
    group_by: list[GroupByQuery] | None = None
    having: Conditions | None = None
    order_by: list[OrderByQuery] | None = None
    limit: LimitQuery | None = None
    ctes: list[CommonTableExpression] | None = None
    lock: SelectLock | None = None

    @property
    def has_joins(self):
        return bool(self.joins)

    def get_related_tables(self) -> set[str]:
        if isinstance(self.table, SchemaReference):
            tables = {self.table.name}
        elif isinstance(self.table, SubQueryStatement):
            tables = {*self.table.query.get_related_tables()}
        else:
            tables = {*self.table.left.get_related_tables(), *self.table.right.get_related_tables()}

        if self.expressions:
            for expr in self.expressions:
                if isinstance(expr.expression, SubQueryStatement):
                    tables.update(expr.expression.query.get_related_tables())

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
            distinct=self.distinct,
            expressions=list(self.expressions) if self.expressions else None,
            joins=list(self.joins) if self.joins else None,
            where=self.where.copy() if self.where else None,
            having=self.having.copy() if self.having else None,
            order_by=list(self.order_by) if self.order_by else None,
            group_by=list(self.group_by) if self.group_by else None,
            limit=self.limit,
            ctes=list(self.ctes) if self.ctes else None,
            lock=self.lock,
        )
