from collections import defaultdict
from typing import Any

import polars as pl
from amsdal_glue_core.common.data_models.aggregation import AggregationQuery
from amsdal_glue_core.common.data_models.annotation import ValueAnnotation
from amsdal_glue_core.common.data_models.conditions import Conditions
from amsdal_glue_core.common.data_models.data import Data
from amsdal_glue_core.common.data_models.field_reference import Field
from amsdal_glue_core.common.data_models.field_reference import FieldReference
from amsdal_glue_core.common.data_models.field_reference import FieldReferenceAliased
from amsdal_glue_core.common.data_models.group_by import GroupByQuery
from amsdal_glue_core.common.data_models.limit import LimitQuery
from amsdal_glue_core.common.data_models.order_by import OrderByQuery
from amsdal_glue_core.common.executors.interfaces import FinalDataQueryExecutor
from amsdal_glue_core.queries.data_query_nodes import FinalDataQueryNode
from amsdal_glue_core.queries.final_query_statement import AnnotationQueryNode
from amsdal_glue_core.queries.final_query_statement import FinalQueryStatement
from amsdal_glue_core.queries.final_query_statement import JoinQueryNode
from amsdal_glue_core.queries.final_query_statement import QueryStatementNode

from amsdal_glue.queries.polars_operator_constructor import polars_operator_constructor


class PolarsFinalQueryDataExecutor(FinalDataQueryExecutor):
    def execute(self, query_node: FinalDataQueryNode, transaction_id: str | None, lock_id: str | None) -> None:  # noqa: ARG002
        if query_node.result is not None:
            return

        if self.has_subquery_annotations(query_node.query):
            msg = 'PolarsFinalQueryExecutor does not support subquery annotations'
            raise RuntimeError(msg)

        sql_context = self._build_sql_context(query_node.query)
        sql = self._build_sql(query_node.query)
        query_node.result = self.process_results(
            sql_context.execute(sql).collect().to_dicts(),  # type: ignore[attr-defined]
        )

    def has_subquery_annotations(self, query: FinalQueryStatement) -> bool:
        return any(isinstance(annotation.value, QueryStatementNode) for annotation in (query.annotations or []))

    def process_results(self, data: list[dict[str, Any]]) -> list[Data]:
        _first_item = data[0] if data else {}

        # check columns duplications

        for key in _first_item:
            if ':' in key:
                msg = f'Column name {key.split(":", 1)[1]} is duplicated'
                raise ValueError(msg)

        return [Data(data=_item) for _item in data] if data is not None else []

    def _build_sql_context(self, query: FinalQueryStatement) -> pl.SQLContext:
        _frames: dict[str, pl.LazyFrame] = {}

        _name, _frame = self._get_frame_from_table(query.table)
        _frames[_name] = _frame

        _join: JoinQueryNode
        for _join in query.joins or []:
            _name, _frame = self._get_frame_from_table(_join.table)
            _frames[_name] = _frame

        _annotation: AnnotationQueryNode
        for _annotation in query.annotations or []:
            if isinstance(_annotation.value, ValueAnnotation):
                continue

            _name, _frame = self._get_frame_from_table(_annotation.value)
            _frames[_name] = _frame

        return pl.SQLContext(frames=_frames)

    def _build_sql(self, query: FinalQueryStatement) -> str:
        _sql = [
            'SELECT',
        ]
        _selection_stmt = self._sql_build_selection_stmt(
            query.only,
            query.annotations,
            query.aggregations,
        )

        _sql.append(_selection_stmt or '*')
        _sql.append(f'FROM {query.table.alias}')
        _sql.append(self._sql_build_joins(query.joins))
        _sql.append(self._sql_build_where(query.where))
        _sql.append(self._sql_build_group_by(query.group_by))
        _sql.append(self._sql_build_order_by(query.order_by))
        _sql.append(self._sql_build_limit(query.limit))

        return ' '.join(filter(None, _sql))

    def _get_frame_from_table(
        self,
        table: QueryStatementNode,
    ) -> tuple[str, pl.LazyFrame]:
        return (
            table.alias,
            self._build_frame_from_result(table.query_node.result),
        )

    def _build_frame_from_result(self, result: Any) -> pl.LazyFrame:
        if result is None:
            msg = 'QueryNode has no result'
            raise RuntimeError(msg)

        _data = defaultdict(list)

        for item in result:
            for key, value in item.data.items():
                _data[key].append(value)

        return pl.LazyFrame(_data)

    def _sql_build_selection_stmt(
        self,
        only: list[FieldReference | FieldReferenceAliased] | None,
        annotations: list[AnnotationQueryNode] | None,
        aggregations: list[AggregationQuery] | None,
    ) -> str:
        _stmt = [self._build_field_reference_stmt(_item) for _item in only or []]

        for annotation in annotations or []:
            if isinstance(annotation.value, QueryStatementNode):
                msg = 'PolarsFinalQueryExecutor does not support subquery annotations'
                raise TypeError(msg)

            _val = repr(annotation.value.value)
            _stmt.append(f'{_val} AS {annotation.value.alias}')

        for aggregation in aggregations or []:
            _aggr_field = self._build_field_reference_stmt(aggregation.field)
            _stmt.append(f'{aggregation.expression.name}({_aggr_field}) AS {aggregation.alias}')

        return ', '.join(filter(None, _stmt))

    def _build_field(self, field: Field) -> str:
        parts = []

        while field:
            parts.append(field.name)
            field = field.child  # type: ignore[assignment]

        return '__'.join(parts)

    def _extract_value(self, field_key: str, data: Any) -> Any:
        if not data:
            return None

        if isinstance(data, list):
            msg = f'Cannot extract value from list: {data}'
            raise RuntimeError(msg)  # noqa: TRY004

        if isinstance(data, dict):
            return data.get(field_key)

        return data

    def _build_field_reference_stmt(
        self,
        field: FieldReference | FieldReferenceAliased,
    ) -> str:
        _item_stmt = f'{field.table_name}.{self._build_field(field.field)}'

        if isinstance(field, FieldReferenceAliased):
            _item_stmt += f' AS {field.alias}'

        return _item_stmt

    def _sql_build_joins(
        self,
        joins: list[JoinQueryNode] | None,
    ) -> str:
        if not joins:
            return ''

        _stmt = []

        for join in joins:
            _conditions = self._sql_build_conditions(join.on)
            _stmt.append(f'{join.join_type.value} JOIN {join.table.alias} ON {_conditions}')

        return ' '.join(_stmt)

    def _sql_build_conditions(
        self,
        conditions: Conditions,
    ) -> str:
        _stmt = []

        for condition in conditions.children:
            if isinstance(condition, Conditions):
                _stmt.append(f'({self._sql_build_conditions(condition)})')
                continue

            _field = self._build_field_reference_stmt(condition.field)
            _stmt.append(
                polars_operator_constructor(
                    field=_field,
                    lookup=condition.lookup,
                    value=condition.value,
                )
            )

        return f' {conditions.connector.value} '.join(_stmt)

    def _sql_build_where(
        self,
        where: Conditions | None,
    ) -> str:
        if not where:
            return ''

        return f'WHERE {self._sql_build_conditions(where)}'

    def _sql_build_group_by(
        self,
        group_by: list[GroupByQuery] | None,
    ) -> str:
        if not group_by:
            return ''

        _stmt = [self._build_field_reference_stmt(_item.field) for _item in group_by]

        return f'GROUP BY {", ".join(_stmt)}'

    def _sql_build_order_by(
        self,
        order_by: list[OrderByQuery] | None,
    ) -> str:
        if not order_by:
            return ''

        _stmt = []

        for field in order_by:
            _item_stmt = self._build_field_reference_stmt(field.field)
            _stmt.append(f'{_item_stmt} {field.direction.value}')

        return f'ORDER BY {", ".join(_stmt)}'

    def _sql_build_limit(
        self,
        limit: LimitQuery | None,
    ) -> str:
        if not limit:
            return ''

        _stmt = f'LIMIT {limit.limit}'

        if limit.offset:
            _stmt += f' OFFSET {limit.offset}'

        return _stmt