from amsdal_glue_core.common.data_models.query import QueryStatement
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.data_models.sub_query import SubQueryStatement
from amsdal_glue_core.common.workflows.chain import AsyncChainTask
from amsdal_glue_core.common.workflows.chain import ChainTask
from amsdal_glue_core.common.workflows.group import AsyncGroupTask
from amsdal_glue_core.common.workflows.group import GroupTask
from amsdal_glue_core.queries.data_query_nodes import DataQueryNode
from amsdal_glue_core.queries.data_query_nodes import FinalDataQueryNode
from amsdal_glue_core.queries.final_query_statement import AnnotationQueryNode
from amsdal_glue_core.queries.final_query_statement import FinalQueryStatement
from amsdal_glue_core.queries.final_query_statement import JoinQueryNode
from amsdal_glue_core.queries.final_query_statement import QueryStatementNode
from amsdal_glue_core.queries.helpers import has_multiple_connections
from amsdal_glue_core.queries.planner.data_query_planner import AsyncDataQueryPlanner
from amsdal_glue_core.queries.planner.data_query_planner import DataQueryPlanner

from amsdal_glue.queries.tasks.query_tasks import AsyncDataQueryTask
from amsdal_glue.queries.tasks.query_tasks import AsyncFinalDataQueryTask
from amsdal_glue.queries.tasks.query_tasks import DataQueryTask
from amsdal_glue.queries.tasks.query_tasks import FinalDataQueryTask


class DefaultDataQueryPlannerMixin:
    chain_task_class: type[ChainTask] | type[AsyncChainTask]
    group_task_class: type[GroupTask] | type[AsyncGroupTask]
    data_query_task_class: type[DataQueryTask] | type[AsyncDataQueryTask]
    final_data_query_task_class: type[FinalDataQueryTask] | type[AsyncFinalDataQueryTask]

    is_async: bool = False

    def plan_data_query(self, query: QueryStatement) -> ChainTask | AsyncChainTask:
        """
        Plans the execution of a data query by creating a chain of tasks.

        Args:
            query (QueryStatement): The data query statement to be executed.

        Returns:
            ChainTask: A chain of tasks that execute the data query.
        """
        plan = self.chain_task_class(tasks=[])

        if has_multiple_connections(query, is_async=self.is_async):
            group_workflow = self.group_task_class(tasks=[])
            from_alias, from_node, from_task = self.construct_query(query.table)

            final_query = FinalQueryStatement(
                only=query.only,
                table=QueryStatementNode(
                    alias=from_alias,
                    query_node=from_node,  # type: ignore[arg-type]
                ),
                aggregations=query.aggregations,
                group_by=query.group_by,
                where=query.where,
                order_by=query.order_by,
                limit=query.limit,
            )
            group_workflow.tasks.append(from_task)  # type: ignore[arg-type]

            for join in list(query.joins or []):
                _join_alias, _join_node, _join_task = self.construct_query(join.table)
                _joins = final_query.joins or []
                _joins.append(
                    JoinQueryNode(
                        table=QueryStatementNode(
                            alias=_join_alias,
                            query_node=_join_node,  # type: ignore[arg-type]
                        ),
                        on=join.on,
                        join_type=join.join_type,
                    ),
                )
                final_query.joins = _joins
                group_workflow.tasks.append(_join_task)  # type: ignore[arg-type]

            for annotation in list(query.annotations or []):
                if isinstance(annotation.value, SubQueryStatement):
                    _ann_alias, _ann_node, _ann_task = self.construct_query(annotation.value)
                    _annotations = final_query.annotations or []
                    _annotations.append(
                        AnnotationQueryNode(
                            value=QueryStatementNode(
                                alias=_ann_alias,
                                query_node=_ann_node,  # type: ignore[arg-type]
                            ),
                        ),
                    )
                    final_query.annotations = _annotations
                    group_workflow.tasks.append(_ann_task)  # type: ignore[arg-type]
                else:
                    _annotations = final_query.annotations or []
                    _annotations.append(
                        AnnotationQueryNode(
                            value=annotation.value,
                        ),
                    )
                    final_query.annotations = _annotations

            plan.tasks.append(group_workflow)  # type: ignore[arg-type]
            # Last query in the chain is the root query

            plan.final_task = self.final_data_query_task_class(
                query_node=FinalDataQueryNode(
                    query=final_query,
                ),
            )
        else:
            _final_query = DataQueryNode(query=query)
            plan.tasks.append(self.data_query_task_class(query_node=_final_query))  # type: ignore[arg-type]

        return plan

    def construct_query(
        self,
        table: SchemaReference | SubQueryStatement,
    ) -> tuple[str, DataQueryNode | FinalDataQueryNode, ChainTask | AsyncChainTask]:
        """
        Constructs a query node and a chain of tasks for the given table.

        Args:
            table (SchemaReference | SubQueryStatement): The table or subquery statement.

        Returns:
            tuple[str, DataQueryNode | FinalDataQueryNode, ChainTask | AsyncChainTask]: The alias, query node,
            and chain of tasks.
        """
        if isinstance(table, SubQueryStatement):
            _query = table.query

            if has_multiple_connections(_query, is_async=self.is_async):
                nested_plan = self.plan_data_query(_query)

                if nested_plan.final_task:
                    return table.alias, nested_plan.final_task.item, nested_plan
                return table.alias, nested_plan.tasks[-1].item, nested_plan

            _alias = table.alias
            _table = _query.table
        else:
            _table = table
            _alias = table.alias or table.name

        if isinstance(_table, SchemaReference):
            _query_stmt = QueryStatement(table=_table)
            _node = DataQueryNode(query=_query_stmt)

            return _alias, _node, self.chain_task_class(tasks=[self.data_query_task_class(query_node=_node)])  # type: ignore[list-item]

        msg = f'Unsupported table type: {type(_table)}'
        raise ValueError(msg)


class DefaultDataQueryPlanner(DefaultDataQueryPlannerMixin, DataQueryPlanner):
    """
    DefaultDataQueryPlanner is responsible for planning data queries by creating a chain of tasks
    that execute data queries. It extends the DataQueryPlanner class.
    """

    chain_task_class = ChainTask
    group_task_class = GroupTask
    data_query_task_class = DataQueryTask
    final_data_query_task_class = FinalDataQueryTask
    is_async = False

    def plan_data_query(self, query: QueryStatement) -> ChainTask:
        """
        Plans the execution of a data query by creating a chain of tasks.

        Args:
            query (QueryStatement): The data query statement to be executed.

        Returns:
            ChainTask: A chain of tasks that execute the data query.
        """
        return super().plan_data_query(query)  # type: ignore[return-value]


class DefaultAsyncDataQueryPlanner(DefaultDataQueryPlannerMixin, AsyncDataQueryPlanner):
    """
    DefaultAsyncDataQueryPlanner is responsible for planning data queries by creating a chain of tasks
    that execute data queries. It extends the AsyncDataQueryPlanner class.
    """

    chain_task_class = AsyncChainTask
    group_task_class = AsyncGroupTask
    data_query_task_class = AsyncDataQueryTask
    final_data_query_task_class = AsyncFinalDataQueryTask
    is_async = True

    def plan_data_query(self, query: QueryStatement) -> AsyncChainTask:
        """
        Plans the execution of a data query by creating a chain of tasks.

        Args:
            query (QueryStatement): The data query statement to be executed.

        Returns:
            AsyncChainTask: A chain of tasks that execute the data query.
        """
        return super().plan_data_query(query)  # type: ignore[return-value]
