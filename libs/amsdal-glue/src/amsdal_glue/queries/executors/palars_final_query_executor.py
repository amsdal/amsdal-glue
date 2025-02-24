from collections import defaultdict
from typing import Any

import polars as pl
from amsdal_glue_connections.sql.connections.postgres_connection import get_pg_transform
from amsdal_glue_core.common.data_models.aggregation import AggregationQuery
from amsdal_glue_core.common.data_models.annotation import ExpressionAnnotation
from amsdal_glue_core.common.data_models.annotation import ValueAnnotation
from amsdal_glue_core.common.data_models.conditions import Conditions
from amsdal_glue_core.common.data_models.data import Data
from amsdal_glue_core.common.data_models.field_reference import Field
from amsdal_glue_core.common.data_models.field_reference import FieldReference
from amsdal_glue_core.common.data_models.field_reference import FieldReferenceAliased
from amsdal_glue_core.common.data_models.group_by import GroupByQuery
from amsdal_glue_core.common.data_models.limit import LimitQuery
from amsdal_glue_core.common.data_models.order_by import OrderByQuery
from amsdal_glue_core.common.executors.interfaces import AsyncFinalDataQueryExecutor
from amsdal_glue_core.common.executors.interfaces import FinalDataQueryExecutor
from amsdal_glue_core.common.expressions.common import CombinedExpression
from amsdal_glue_core.common.expressions.common import Expression
from amsdal_glue_core.common.expressions.field_reference import FieldReferenceExpression
from amsdal_glue_core.common.expressions.value import Value
from amsdal_glue_core.queries.data_query_nodes import FinalDataQueryNode
from amsdal_glue_core.queries.final_query_statement import AnnotationQueryNode
from amsdal_glue_core.queries.final_query_statement import FinalQueryStatement
from amsdal_glue_core.queries.final_query_statement import JoinQueryNode
from amsdal_glue_core.queries.final_query_statement import QueryStatementNode

from amsdal_glue.queries.polars_operator_constructor import polars_operator_constructor


class PolarsFinalQueryDataExecutorMixin:
    def has_subquery_annotations(self, query: FinalQueryStatement) -> bool:
        """
        Checks if the query has subquery annotations.

        Args:
            query (FinalQueryStatement): The final query statement.

        Returns:
            bool: True if the query has subquery annotations, False otherwise.
        """
        return any(isinstance(annotation.value, QueryStatementNode) for annotation in (query.annotations or []))

    def process_results(self, data: list[dict[str, Any]]) -> list[Data]:
        """
        Processes the results of the query execution.

        Args:
            data (list[dict[str, Any]]): The data returned from the query execution.

        Returns:
            list[Data]: The processed data.
        """
        _first_item = data[0] if data else {}

        # check columns duplications

        for key in _first_item:
            if ':' in key:
                msg = f'Column name {key.split(":", 1)[1]} is duplicated'
                raise ValueError(msg)

        return [Data(data=_item) for _item in data] if data is not None else []

    def _build_sql_context(self, query: FinalQueryStatement) -> pl.SQLContext:
        """
        Builds the SQL context for the query.

        Args:
            query (FinalQueryStatement): The final query statement.

        Returns:
            pl.SQLContext: The SQL context for the query.
        """
        _frames: dict[str, pl.LazyFrame] = {}

        _name, _frame = self._get_frame_from_table(query.table)
        _frames[_name] = _frame

        _join: JoinQueryNode
        for _join in query.joins or []:
            _name, _frame = self._get_frame_from_table(_join.table)
            _frames[_name] = _frame

        _annotation: AnnotationQueryNode
        for _annotation in query.annotations or []:
            if isinstance(_annotation.value, ValueAnnotation | ExpressionAnnotation):
                continue

            _name, _frame = self._get_frame_from_table(_annotation.value)
            _frames[_name] = _frame

        return pl.SQLContext(frames=_frames)

    def _build_sql(self, query: FinalQueryStatement) -> str:
        """
        Builds the SQL query string.

        Args:
            query (FinalQueryStatement): The final query statement.

        Returns:
            str: The SQL query string.
        """
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
        """
        Retrieves the frame from the table.

        Args:
            table (QueryStatementNode): The query statement node representing the table.

        Returns:
            tuple[str, pl.LazyFrame]: The name and the frame of the table.
        """
        return (
            table.alias,
            self._build_frame_from_result(table.query_node.result),
        )

    def _build_frame_from_result(self, result: Any) -> pl.LazyFrame:
        """
        Builds the frame from the result.

        Args:
            result (Any): The result of the query execution.

        Returns:
            pl.LazyFrame: The frame built from the result.

        Raises:
            RuntimeError: If the result is None.
        """
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
        """
        Builds the SQL selection statement.

        Args:
            only (list[FieldReference | FieldReferenceAliased] | None): The fields to be selected.
            annotations (list[AnnotationQueryNode] | None): The annotations for the query.
            aggregations (list[AggregationQuery] | None): The aggregations for the query.

        Returns:
            str: The SQL selection statement.
        """
        _stmt = [self._build_field_reference_stmt(_item) for _item in only or []]

        for annotation in annotations or []:
            if isinstance(annotation.value, QueryStatementNode):
                msg = 'PolarsFinalQueryExecutor does not support subquery annotations'
                raise TypeError(msg)

            if isinstance(annotation.value, ExpressionAnnotation):
                _expression = self._build_expression(annotation.value.expression)
                _val = f'({_expression})'
                _stmt.append(f'{_val} AS {annotation.value.alias}')
            else:
                _val = repr(annotation.value.value)
                _stmt.append(f'{_val} AS {annotation.value.alias}')

        for aggregation in aggregations or []:
            _aggr_field = self._build_field_reference_stmt(aggregation.expression.field)
            _stmt.append(f'{aggregation.expression.name}({_aggr_field}) AS {aggregation.alias}')

        return ', '.join(filter(None, _stmt))

    def _build_field(self, field: Field) -> str:
        """
        Builds the field string.

        Args:
            field (Field): The field to be built.

        Returns:
            str: The field string.
        """
        parts = []

        while field:
            parts.append(field.name)
            field = field.child  # type: ignore[assignment]

        return '__'.join(parts)

    def _build_field_reference_stmt(
        self,
        field: FieldReference | FieldReferenceAliased,
    ) -> str:
        """
        Builds the field reference statement.

        Args:
            field (FieldReference | FieldReferenceAliased): The field reference.

        Returns:
            str: The field reference statement.
        """
        _item_stmt = f'{field.table_name}.{self._build_field(field.field)}'

        if isinstance(field, FieldReferenceAliased):
            _item_stmt += f' AS {field.alias}'

        return _item_stmt

    def _build_expression(self, expression: Expression) -> str:
        if isinstance(expression, CombinedExpression):
            _left = self._build_expression(expression.left)
            _right = self._build_expression(expression.right)
            return f'{_left} {expression.operator} {_right}'

        if isinstance(expression, FieldReference):
            return self._build_field_reference_stmt(expression)

        if isinstance(expression, FieldReferenceExpression):
            return self._build_field_reference_stmt(expression.field_reference)

        if isinstance(expression, Value):
            return repr(expression)

        msg = f'Unsupported expression type: {type(expression)}'
        raise TypeError(msg)

    def _sql_build_joins(
        self,
        joins: list[JoinQueryNode] | None,
    ) -> str:
        """
        Builds the SQL join statement.

        Args:
            joins (list[JoinQueryNode] | None): The join nodes.

        Returns:
            str: The SQL join statement.
        """
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
        """
        Builds the SQL conditions statement.

        Args:
            conditions (Conditions): The conditions for the query.

        Returns:
            str: The SQL conditions statement.
        """
        _stmt = []

        for condition in conditions.children:
            if isinstance(condition, Conditions):
                _stmt.append(f'({self._sql_build_conditions(condition)})')
                continue

            _stmt.append(
                polars_operator_constructor(
                    left=condition.left,
                    lookup=condition.lookup,
                    right=condition.right,
                    transform=get_pg_transform(),
                )
            )

        return f' {conditions.connector.value} '.join(_stmt)

    def _sql_build_where(
        self,
        where: Conditions | None,
    ) -> str:
        """
        Builds the SQL where statement.

        Args:
            where (Conditions | None): The where conditions.

        Returns:
            str: The SQL where statement.
        """
        if not where:
            return ''

        return f'WHERE {self._sql_build_conditions(where)}'

    def _sql_build_group_by(
        self,
        group_by: list[GroupByQuery] | None,
    ) -> str:
        """
        Builds the SQL group by statement.

        Args:
            group_by (list[GroupByQuery] | None): The group by queries.

        Returns:
            str: The SQL group by statement.
        """
        if not group_by:
            return ''

        _stmt = [self._build_field_reference_stmt(_item.field) for _item in group_by]

        return f'GROUP BY {", ".join(_stmt)}'

    def _sql_build_order_by(
        self,
        order_by: list[OrderByQuery] | None,
    ) -> str:
        """
        Builds the SQL order by statement.

        Args:
            order_by (list[OrderByQuery] | None): The order by queries.

        Returns:
            str: The SQL order by statement.
        """
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
        """
        Builds the SQL limit statement.

        Args:
            limit (LimitQuery | None): The limit query.

        Returns:
            str: The SQL limit statement.
        """
        if not limit:
            return ''

        _stmt = f'LIMIT {limit.limit}'

        if limit.offset:
            _stmt += f' OFFSET {limit.offset}'

        return _stmt


class PolarsFinalQueryDataExecutor(PolarsFinalQueryDataExecutorMixin, FinalDataQueryExecutor):
    """
    PolarsFinalQueryDataExecutor is responsible for executing final data queries using Polars.

    This executor is used when the [DefaultDataQueryPlanner][amsdal_glue.planners.DefaultDataQueryPlanner]
    splits the query to several subqueries and the [FinalDataQueryTask][amsdal_glue.tasks.FinalDataQueryTask]
    is created.

    Methods:
        execute(query_node: FinalDataQueryNode, transaction_id: str | None, lock_id: str | None) -> None:
            Executes the final data query node.
    """

    def execute(self, query_node: FinalDataQueryNode, transaction_id: str | None, lock_id: str | None) -> None:  # noqa: ARG002
        """
        Executes the final data query using Polars.

        Args:
            query_node (FinalDataQueryNode): The node representing the final data query.
            transaction_id (str | None): The ID of the transaction.
            lock_id (str | None): The ID of the lock.
        """
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


class AsyncPolarsFinalQueryDataExecutor(PolarsFinalQueryDataExecutorMixin, AsyncFinalDataQueryExecutor):
    """
    AsyncPolarsFinalQueryDataExecutor is responsible for executing final data queries using Polars.

    This executor is used when the [DefaultDataQueryPlanner][amsdal_glue.planners.DefaultDataQueryPlanner]
    splits the query to several subqueries and the [FinalDataQueryTask][amsdal_glue.tasks.FinalDataQueryTask]
    is created.

    Methods:
        execute(query_node: FinalDataQueryNode, transaction_id: str | None, lock_id: str | None) -> None:
            Executes the final data query node.
    """

    async def execute(self, query_node: FinalDataQueryNode, transaction_id: str | None, lock_id: str | None) -> None:  # noqa: ARG002
        """
        Executes the final data query using Polars.

        Args:
            query_node (FinalDataQueryNode): The node representing the final data query.
            transaction_id (str | None): The ID of the transaction.
            lock_id (str | None): The ID of the lock.
        """
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
