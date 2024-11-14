from typing import TYPE_CHECKING

from amsdal_glue_core.common.enums import TransactionAction
from amsdal_glue_core.common.helpers.resolve_connection import resolve_connection_pool
from amsdal_glue_core.common.interfaces.connection_pool import AsyncConnectionPoolBase
from amsdal_glue_core.common.interfaces.connection_pool import ConnectionPoolBase

if TYPE_CHECKING:
    from amsdal_glue_core.commands.transaction_node import ExecutionTransactionCommandNode


class TransactionNodeExecutor:
    """Executes a node in the transaction command tree.

    This class implements the business logic for executing a single node of a transaction command tree.

    Methods:
        execute(command_node: ExecutionTransactionCommandNode, transaction_id: str | None, lock_id: str | None) -> None:
            Executes the given transaction command node.
    """

    def execute(
        self,
        command_node: 'ExecutionTransactionCommandNode',
        transaction_id: str | None,
        lock_id: str | None,  # noqa: ARG002
    ) -> None:
        """Executes the given transaction command node.

        Args:
            command_node (ExecutionTransactionCommandNode): The transaction command node to be executed.
            transaction_id (str | None): The transaction ID to be used during execution.
            lock_id (str | None): The lock ID to be used during execution.
        """
        if not command_node.command.schema:
            msg = 'Schema is required for transaction command'
            raise ValueError(msg)

        connection_pool = resolve_connection_pool(table=command_node.command.schema)

        if not isinstance(connection_pool, ConnectionPoolBase):
            msg = 'Connection pool must be an instance of ConnectionPoolBase'
            raise TypeError(msg)

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


class AsyncTransactionNodeExecutor:
    """Executes a node in the transaction command tree.

    This class implements the business logic for executing a single node of a transaction command tree.

    Methods:
        execute(command_node: ExecutionTransactionCommandNode, transaction_id: str | None, lock_id: str | None) -> None:
            Executes the given transaction command node.
    """

    async def execute(
        self,
        command_node: 'ExecutionTransactionCommandNode',
        transaction_id: str | None,
        lock_id: str | None,  # noqa: ARG002
    ) -> None:
        """Executes the given transaction command node.

        Args:
            command_node (ExecutionTransactionCommandNode): The transaction command node to be executed.
            transaction_id (str | None): The transaction ID to be used during execution.
            lock_id (str | None): The lock ID to be used during execution.
        """
        if not command_node.command.schema:
            msg = 'Schema is required for transaction command'
            raise ValueError(msg)

        connection_pool = resolve_connection_pool(table=command_node.command.schema, is_async=True)

        if not isinstance(connection_pool, AsyncConnectionPoolBase):
            msg = 'Connection pool must be an instance of AsyncConnectionPoolBase'
            raise TypeError(msg)

        _connection = await connection_pool.get_connection(transaction_id=transaction_id)

        if command_node.command.action == TransactionAction.COMMIT:
            command_node.result = await _connection.commit_transaction(command_node.command)

        elif command_node.command.action == TransactionAction.ROLLBACK:
            command_node.result = await _connection.rollback_transaction(command_node.command)

        elif command_node.command.action == TransactionAction.BEGIN:
            command_node.result = await _connection.begin_transaction(command_node.command)

        elif command_node.command.action == TransactionAction.REVERT:
            command_node.result = await _connection.revert_transaction(command_node.command)

        if (
            command_node.command.action
            in [TransactionAction.COMMIT, TransactionAction.ROLLBACK, TransactionAction.REVERT]
        ) and command_node.command.parent_transaction_id is None:
            await connection_pool.disconnect_connection(transaction_id=transaction_id)
