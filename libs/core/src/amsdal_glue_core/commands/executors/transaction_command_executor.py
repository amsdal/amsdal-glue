from typing import TYPE_CHECKING

from amsdal_glue_core.common.enums import TransactionAction
from amsdal_glue_core.common.helpers.resolve_connection import resolve_connection_pool
from amsdal_glue_core.common.helpers.singleton import Singleton

if TYPE_CHECKING:
    from amsdal_glue_core.commands.transaction_node import ExecutionTransactionCommandNode


class TransactionNodeExecutor(metaclass=Singleton):
    def execute(
        self,
        command_node: 'ExecutionTransactionCommandNode',
        transaction_id: str | None,
        lock_id: str | None,  # noqa: ARG002
    ) -> None:
        if not command_node.command.schema:
            msg = 'Schema is required for transaction command'
            raise ValueError(msg)

        connection_pool = resolve_connection_pool(table=command_node.command.schema)
        _connection = connection_pool.get_connection(transaction_id=transaction_id)

        if command_node.command.action == TransactionAction.COMMIT:
            command_node.result = _connection.commit_transaction(command_node.command)

        elif command_node.command.action == TransactionAction.ROLLBACK:
            command_node.result = _connection.rollback_transaction(command_node.command)

        elif command_node.command.action == TransactionAction.BEGIN:
            command_node.result = _connection.begin_transaction(command_node.command)

        elif command_node.command.action == TransactionAction.REVERT:
            command_node.result = _connection.revert_transaction(command_node.command)

        if (
            command_node.command.action
            in [TransactionAction.COMMIT, TransactionAction.ROLLBACK, TransactionAction.REVERT]
        ) and command_node.command.parent_transaction_id is None:
            connection_pool.disconnect_connection(transaction_id=transaction_id)
