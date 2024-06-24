from amsdal_glue_core.common.data_models.conditions import Conditions
from amsdal_glue_core.common.services.managers.connection import ConnectionManager
from amsdal_glue_core.common.workflows.chain import ChainTask
from amsdal_glue_core.common.workflows.group import GroupTask
from amsdal_glue_core.queries.planner.query_planner.base import SchemaQueryPlanner

from amsdal_glue.queries.tasks.schema_tasks import FinalSchemaQueryTask
from amsdal_glue.queries.tasks.schema_tasks import SchemaQueryTask


class DefaultSchemaQueryPlanner(SchemaQueryPlanner):
    def plan_schema_query(self, filters: Conditions | None = None) -> ChainTask:
        from amsdal_glue_core.containers import Container

        connection_manager = Container.managers.get(ConnectionManager)
        tasks: list[SchemaQueryTask] = [
            SchemaQueryTask(
                connection=connection,
                filters=filters.copy() if filters else None,
            )
            for connection in connection_manager.connections.values()
        ]

        if len(tasks) == 1:
            return ChainTask(tasks=tasks)  # type: ignore[arg-type]

        group = GroupTask(tasks=tasks)  # type: ignore[arg-type]
        plan = ChainTask(tasks=[group])
        plan.final_task = FinalSchemaQueryTask(tasks=tasks)

        return plan
