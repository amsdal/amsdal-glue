from typing import TYPE_CHECKING

from amsdal_glue_core.common.enums import TransactionAction
from amsdal_glue_core.common.helpers.resolve_connection import resolve_connection
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
        _connection = resolve_connection(command_node.command.schema, transaction_id)

        if command_node.command.action == TransactionAction.COMMIT:
            command_node.result = _connection.commit_transaction(command_node.command)

        elif command_node.command.action == TransactionAction.ROLLBACK:
            command_node.result = _connection.rollback_transaction(command_node.command)

        elif command_node.command.action == TransactionAction.BEGIN:
            command_node.result = _connection.begin_transaction(command_node.command)

        elif command_node.command.action == TransactionAction.REVERT:
            command_node.result = _connection.revert_transaction(command_node.command)
