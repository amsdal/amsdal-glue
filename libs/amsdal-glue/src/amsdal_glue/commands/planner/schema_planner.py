# mypy: disable-error-code="type-abstract"
from collections import defaultdict

from amsdal_glue_core.commands.mutation_nodes import SchemaCommandNode
from amsdal_glue_core.commands.planner.schema_command_planner import AsyncSchemaCommandPlanner
from amsdal_glue_core.commands.planner.schema_command_planner import SchemaCommandPlanner
from amsdal_glue_core.common.interfaces.connection_manager import AsyncConnectionManager
from amsdal_glue_core.common.interfaces.connection_manager import ConnectionManager
from amsdal_glue_core.common.operations.commands import SchemaCommand
from amsdal_glue_core.common.workflows.chain import AsyncChainTask
from amsdal_glue_core.common.workflows.chain import ChainTask

from amsdal_glue.commands.tasks.schema_mutation_tasks import AsyncFinalSchemaCommandTask
from amsdal_glue.commands.tasks.schema_mutation_tasks import AsyncSchemaCommandTask
from amsdal_glue.commands.tasks.schema_mutation_tasks import FinalSchemaCommandTask
from amsdal_glue.commands.tasks.schema_mutation_tasks import SchemaCommandTask


class DefaultSchemaCommandPlanner(SchemaCommandPlanner):
    """
    DefaultSchemaCommandPlanner is responsible for planning schema commands by creating a chain of tasks
    that execute schema mutations. It extends the SchemaCommandPlanner class.
    """

    def plan_schema_command(self, command: SchemaCommand) -> ChainTask:
        """
        Plans the execution of a schema command by creating a chain of tasks.

        Args:
            command (SchemaCommand): The schema command containing mutations to be executed.

        Returns:
            ChainTask: A chain of tasks that execute the schema mutations.
        """
        from amsdal_glue_core.containers import Container

        mutations_per_connection = defaultdict(list)
        connection_manager = Container.managers.get(ConnectionManager)

        for mutation in command.mutations:
            _schema_name = mutation.get_schema_name()
            _connection = connection_manager.get_connection_pool(_schema_name)
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
                        root_transaction_id=command.root_transaction_id,
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


class DefaultAsyncSchemaCommandPlanner(AsyncSchemaCommandPlanner):
    """
    DefaultAsyncSchemaCommandPlanner is responsible for planning schema commands by creating a chain of tasks
    that execute schema mutations. It extends the AsyncSchemaCommandPlanner class.
    """

    def plan_schema_command(self, command: SchemaCommand) -> AsyncChainTask:
        """
        Plans the execution of a schema command by creating a chain of tasks.

        Args:
            command (SchemaCommand): The schema command containing mutations to be executed.

        Returns:
            AsyncChainTask: A chain of tasks that execute the schema mutations.
        """
        from amsdal_glue_core.containers import Container

        mutations_per_connection = defaultdict(list)
        connection_manager = Container.managers.get(AsyncConnectionManager)

        for mutation in command.mutations:
            _schema_name = mutation.get_schema_name()
            _connection = connection_manager.get_connection_pool(_schema_name)
            mutations_per_connection[_connection].append(mutation)

        if len(mutations_per_connection) > 1:
            return AsyncChainTask(
                tasks=[
                    AsyncSchemaCommandTask(
                        command_node=SchemaCommandNode(command=command),
                    ),
                ],
            )

        _tasks = [
            AsyncSchemaCommandTask(
                command_node=SchemaCommandNode(
                    command=SchemaCommand(
                        lock_id=command.lock_id,
                        root_transaction_id=command.root_transaction_id,
                        transaction_id=command.transaction_id,
                        mutations=mutations,
                    ),
                ),
            )
            for mutations in mutations_per_connection.values()
        ]

        return AsyncChainTask(
            tasks=_tasks,  # type: ignore[arg-type]
            final_task=AsyncFinalSchemaCommandTask(tasks=_tasks),
        )
