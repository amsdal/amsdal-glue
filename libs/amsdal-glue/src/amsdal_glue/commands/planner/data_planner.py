from typing import TYPE_CHECKING

from amsdal_glue_core.commands.mutation_nodes import DataMutationNode
from amsdal_glue_core.commands.planner.data_command_planner import DataCommandPlanner
from amsdal_glue_core.common.helpers.resolve_connection import resolve_connection
from amsdal_glue_core.common.operations.commands import DataCommand
from amsdal_glue_core.common.workflows.chain import ChainTask

from amsdal_glue.commands.tasks.data_mutation_tasks import DataMutationTask

if TYPE_CHECKING:
    from amsdal_glue_core.common.workflows.task import Task


class DefaultDataCommandPlanner(DataCommandPlanner):
    def plan_data_command(self, command: DataCommand) -> ChainTask:
        task_batches: list[Task] = []
        prev_connection = None

        for mutation in command.mutations:
            connection = resolve_connection(mutation.schema, command.transaction_id)

            if connection != prev_connection:
                task_batches.append(
                    DataMutationTask(
                        data_mutation_node=DataMutationNode(mutations=[]),
                    )
                )
                prev_connection = connection

            task_batches[-1].item.mutations.append(mutation)

        return ChainTask(tasks=task_batches)
