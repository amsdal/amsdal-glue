from typing import TYPE_CHECKING

from amsdal_glue_core.commands.mutation_nodes import DataMutationNode
from amsdal_glue_core.commands.planner.data_command_planner import AsyncDataCommandPlanner
from amsdal_glue_core.commands.planner.data_command_planner import DataCommandPlanner
from amsdal_glue_core.common.helpers.resolve_connection import resolve_async_connection
from amsdal_glue_core.common.helpers.resolve_connection import resolve_connection
from amsdal_glue_core.common.operations.commands import DataCommand
from amsdal_glue_core.common.workflows.chain import AsyncChainTask
from amsdal_glue_core.common.workflows.chain import ChainTask

from amsdal_glue.commands.tasks.data_mutation_tasks import AsyncDataMutationTask
from amsdal_glue.commands.tasks.data_mutation_tasks import DataMutationTask

if TYPE_CHECKING:
    from amsdal_glue_core.common.workflows.task import AsyncTask
    from amsdal_glue_core.common.workflows.task import Task


class DefaultDataCommandPlanner(DataCommandPlanner):
    """
    DefaultDataCommandPlanner is responsible for planning data commands by creating a chain of tasks
    that execute data mutations. It extends the DataCommandPlanner class.
    """

    def plan_data_command(self, command: DataCommand) -> ChainTask:
        """
        Plans the execution of a data command by creating a chain of tasks.

        Args:
            command (DataCommand): The data command containing mutations to be executed.

        Returns:
            ChainTask: A chain of tasks that execute the data mutations.
        """
        task_batches: list[Task] = []
        prev_connection = None

        for mutation in command.mutations:
            connection = resolve_connection(mutation.schema, command.root_transaction_id)

            if connection != prev_connection:
                task_batches.append(
                    DataMutationTask(
                        data_mutation_node=DataMutationNode(mutations=[]),
                    )
                )
                prev_connection = connection

            task_batches[-1].item.mutations.append(mutation)

        return ChainTask(tasks=task_batches)


class DefaultAsyncDataCommandPlanner(AsyncDataCommandPlanner):
    """
    DefaultAsyncDataCommandPlanner is responsible for planning data commands by creating a chain of tasks
    that execute data mutations. It extends the AsyncDataCommandPlanner class.
    """

    async def plan_data_command(self, command: DataCommand) -> AsyncChainTask:
        """
        Plans the execution of a data command by creating a chain of tasks.

        Args:
            command (DataCommand): The data command containing mutations to be executed.

        Returns:
            AsyncChainTask: A chain of tasks that execute the data mutations.
        """
        task_batches: list[AsyncTask] = []
        prev_connection = None

        for mutation in command.mutations:
            connection = await resolve_async_connection(mutation.schema, command.root_transaction_id)

            if connection != prev_connection:
                task_batches.append(
                    AsyncDataMutationTask(
                        data_mutation_node=DataMutationNode(mutations=[]),
                    )
                )
                prev_connection = connection

            task_batches[-1].item.mutations.append(mutation)

        return AsyncChainTask(tasks=task_batches)
