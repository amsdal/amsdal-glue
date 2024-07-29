from amsdal_glue_core.common.data_models.conditions import Conditions
from amsdal_glue_core.common.services.managers.connection import ConnectionManager
from amsdal_glue_core.common.workflows.chain import ChainTask
from amsdal_glue_core.common.workflows.group import GroupTask
from amsdal_glue_core.queries.planner.schema_query_planner import SchemaQueryPlanner
from amsdal_glue_core.queries.schema_query_nodes import SchemaQueryNode

from amsdal_glue.queries.tasks.schema_tasks import FinalSchemaQueryTask
from amsdal_glue.queries.tasks.schema_tasks import SchemaQueryTask


class DefaultSchemaQueryPlanner(SchemaQueryPlanner):
    """
    DefaultSchemaQueryPlanner is responsible for planning schema queries by creating a chain of tasks
    that execute schema queries. It extends the SchemaQueryPlanner class.
    """

    def plan_schema_query(self, filters: Conditions | None = None) -> ChainTask:
        """
        Plans the execution of a schema query by creating a chain of tasks.

        Args:
            filters (Conditions | None): The conditions to filter the schema query.

        Returns:
            ChainTask: A chain of tasks that execute the schema query.
        """
        from amsdal_glue_core.containers import Container

        connection_manager = Container.managers.get(ConnectionManager)
        connections_map = {
            connection: schema_name for schema_name, connection in connection_manager.connections.items()
        }
        tasks: list[SchemaQueryTask] = [
            SchemaQueryTask(
                schema_query_node=SchemaQueryNode(
                    schema_name_connection=schema_name,
                    filters=filters.copy() if filters else None,
                ),
            )
            for schema_name in connections_map.values()
        ]

        if len(tasks) == 1:
            return ChainTask(tasks=tasks)  # type: ignore[arg-type]

        group = GroupTask(tasks=tasks)  # type: ignore[arg-type]
        plan = ChainTask(tasks=[group])
        plan.final_task = FinalSchemaQueryTask(tasks=tasks)

        return plan
