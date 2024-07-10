from amsdal_glue_core.commands.planner.transaction_command_planner import TransactionCommandPlanner
from amsdal_glue_core.commands.transaction_node import ExecutionTransactionCommandNode
from amsdal_glue_core.common.operations.commands import TransactionCommand
from amsdal_glue_core.common.services.managers.connection import ConnectionManager
from amsdal_glue_core.common.workflows.chain import ChainTask
from amsdal_glue_core.common.workflows.group import GroupTask

from amsdal_glue.commands.tasks.transaction_tasks import TransactionCommandFinalTask
from amsdal_glue.commands.tasks.transaction_tasks import TransactionCommandTask


class DefaultTransactionCommandPlanner(TransactionCommandPlanner):
    def plan_transaction(self, command: TransactionCommand) -> ChainTask:
        from amsdal_glue_core.containers import Container

        if command.schema:
            return ChainTask(
                tasks=[
                    TransactionCommandTask(
                        transaction_command=ExecutionTransactionCommandNode(
                            command=command,
                        ),
                    ),
                ],
            )

        connection_manager = Container.managers.get(ConnectionManager)
        schemas_per_connection = {}
        group_tasks = []

        for _schema_name, _connection in connection_manager.connections.items():
            schemas_per_connection[_connection] = _schema_name

        for _schema_name in schemas_per_connection.values():
            _command = TransactionCommand(
                lock_id=command.lock_id,
                transaction_id=command.transaction_id,
                parent_transaction_id=command.parent_transaction_id,
                schema=_schema_name,
                action=command.action,
            )

            group_tasks.append(
                TransactionCommandTask(
                    transaction_command=ExecutionTransactionCommandNode(
                        command=command,
                    ),
                ),
            )

        return ChainTask(
            tasks=[
                GroupTask(tasks=group_tasks),
            ],
            final_task=TransactionCommandFinalTask(tasks=group_tasks),
        )
