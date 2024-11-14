from typing import TYPE_CHECKING

from amsdal_glue_core.common.enums import LockAction
from amsdal_glue_core.common.helpers.resolve_connection import resolve_async_connection
from amsdal_glue_core.common.helpers.resolve_connection import resolve_connection

if TYPE_CHECKING:
    from amsdal_glue_core.commands.lock_command_node import ExecutionLockCommand


class LockCommandNodeExecutor:
    """Executes a node in the lock command tree.

    This class implements the business logic for executing a single node of a lock command tree.

    Methods:
        execute(command: ExecutionLockCommand, transaction_id: str | None, lock_id: str | None) -> None:
            Executes the given lock command node.
    """

    def execute(self, command: 'ExecutionLockCommand', transaction_id: str | None, lock_id: str | None) -> None:  # noqa: ARG002
        """Executes the given lock command node.

        Args:
            command (ExecutionLockCommand): The lock command node to be executed.
            transaction_id (str | None): The transaction ID to be used during execution.
            lock_id (str | None): The lock ID to be used during execution.
        """
        lock_object = command.locked_object
        _connection = resolve_connection(lock_object.schema, transaction_id)

        if command.action == LockAction.ACQUIRE:
            command.result = _connection.acquire_lock(command)

        else:
            command.result = _connection.release_lock(command)


class AsyncLockCommandNodeExecutor:
    """Executes a node in the lock command tree.

    This class implements the business logic for executing a single node of a lock command tree.

    Methods:
        execute(command: ExecutionLockCommand, transaction_id: str | None, lock_id: str | None) -> None:
            Executes the given lock command node.
    """

    async def execute(self, command: 'ExecutionLockCommand', transaction_id: str | None, lock_id: str | None) -> None:  # noqa: ARG002
        """Executes the given lock command node.

        Args:
            command (ExecutionLockCommand): The lock command node to be executed.
            transaction_id (str | None): The transaction ID to be used during execution.
            lock_id (str | None): The lock ID to be used during execution.
        """
        lock_object = command.locked_object
        _connection = await resolve_async_connection(lock_object.schema, transaction_id)

        if command.action == LockAction.ACQUIRE:
            command.result = await _connection.acquire_lock(command)

        else:
            command.result = await _connection.release_lock(command)
