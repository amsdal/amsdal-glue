from amsdal_glue_core.commands.planner.transaction_command_planner import TransactionCommandPlanner
from amsdal_glue_core.commands.transaction_node import ExecutionTransactionCommandNode
from amsdal_glue_core.common.operations.commands import TransactionCommand
from amsdal_glue_core.common.workflows.chain import ChainTask

from amsdal_glue.commands.tasks.transaction_tasks import TransactionCommandTask


class DefaultTransactionCommandPlanner(TransactionCommandPlanner):
    def plan_transaction(self, command: TransactionCommand) -> ChainTask:
        return ChainTask(
            tasks=[
                TransactionCommandTask(
                    transaction_command=ExecutionTransactionCommandNode(
                        command=command,
                    ),
                ),
            ],
        )
