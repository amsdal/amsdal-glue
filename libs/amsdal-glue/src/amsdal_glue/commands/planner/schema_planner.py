from collections import defaultdict

from amsdal_glue_core.commands.mutation_nodes import SchemaCommandNode
from amsdal_glue_core.commands.planner.schema_command_planner import SchemaCommandPlanner
from amsdal_glue_core.common.operations.commands import SchemaCommand
from amsdal_glue_core.common.services.managers.connection import ConnectionManager
from amsdal_glue_core.common.workflows.chain import ChainTask

from amsdal_glue.commands.tasks.schema_mutation_tasks import FinalSchemaCommandTask
from amsdal_glue.commands.tasks.schema_mutation_tasks import SchemaCommandTask


class DefaultSchemaCommandPlanner(SchemaCommandPlanner):
    def plan_schema_command(self, command: SchemaCommand) -> ChainTask:
        from amsdal_glue_core.containers import Container

        mutations_per_connection = defaultdict(list)
        connection_manager = Container.managers.get(ConnectionManager)

        for mutation in command.mutations:
            _schema_name = mutation.get_schema_name()
            _connection = connection_manager.get_connection(_schema_name)
            mutations_per_connection[_connection].append(mutation)

        if len(mutations_per_connection) > 1:
            return ChainTask(
                tasks=[
                    SchemaCommandTask(
                        command_node=SchemaCommandNode(command=command),
                    ),
                ],
            )

        _tasks = [
            SchemaCommandTask(
                command_node=SchemaCommandNode(
                    command=SchemaCommand(
                        lock_id=command.lock_id,
                        transaction_id=command.transaction_id,
                        mutations=mutations,
                    ),
                ),
            )
            for mutations in mutations_per_connection.values()
        ]

        return ChainTask(
            tasks=_tasks,  # type: ignore[arg-type]
            final_task=FinalSchemaCommandTask(tasks=_tasks),
        )