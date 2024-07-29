from amsdal_glue_core.commands.planner.transaction_command_planner import TransactionCommandPlanner
from amsdal_glue_core.commands.transaction_node import ExecutionTransactionCommandNode
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.enums import Version
from amsdal_glue_core.common.operations.commands import TransactionCommand
from amsdal_glue_core.common.services.managers.connection import ConnectionManager
from amsdal_glue_core.common.services.managers.connection import ConnectionPoolBase
from amsdal_glue_core.common.workflows.chain import ChainTask
from amsdal_glue_core.common.workflows.group import GroupTask

from amsdal_glue.commands.tasks.transaction_tasks import TransactionCommandFinalTask
from amsdal_glue.commands.tasks.transaction_tasks import TransactionCommandTask


class DefaultTransactionCommandPlanner(TransactionCommandPlanner):
    """
    DefaultTransactionCommandPlanner is responsible for planning transaction commands by creating a chain of tasks
    that execute transaction operations. It extends the TransactionCommandPlanner class.
    """

    def plan_transaction(self, command: TransactionCommand) -> ChainTask:
        """
        Plans the execution of a transaction command by creating a chain of tasks.

        Args:
            command (TransactionCommand): The transaction command containing transaction operations to be executed.

        Returns:
            ChainTask: A chain of tasks that execute the transaction operations.
        """
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
        group_tasks = []
        schemas_per_connection: dict[ConnectionPoolBase, str] = {
            _connection: _schema_name for _schema_name, _connection in connection_manager.connections.items()
        }

        for _schema_name in schemas_per_connection.values():
            _command = TransactionCommand(
                lock_id=command.lock_id,
                transaction_id=command.transaction_id,
                root_transaction_id=command.root_transaction_id,
                parent_transaction_id=command.parent_transaction_id,
                schema=SchemaReference(
                    name=_schema_name,
                    version=Version.LATEST,
                ),
                action=command.action,
            )

            group_tasks.append(
                TransactionCommandTask(
                    transaction_command=ExecutionTransactionCommandNode(
                        command=_command,
                    ),
                ),
            )

        return ChainTask(
            tasks=[
                GroupTask(tasks=group_tasks),
            ],
            final_task=TransactionCommandFinalTask(tasks=group_tasks),
        )
