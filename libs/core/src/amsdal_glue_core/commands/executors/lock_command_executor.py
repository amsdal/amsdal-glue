# mypy: disable-error-code="type-abstract"
from typing import Any

from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.enums import LockAction
from amsdal_glue_core.common.helpers.resolve_connection import resolve_async_connection
from amsdal_glue_core.common.helpers.resolve_connection import resolve_connection
from amsdal_glue_core.common.operations.commands import LockCommand


class LockCommandNodeExecutor:
    """Executes a grouped lock command (one task per connection group).

    Resolves the connection from the group's homogeneous references:
    - ``SchemaReference`` group → existing ``resolve_connection`` (schema routing).
    - ``LockIdentifier`` group → strict pool resolve (raises on unknown pool).

    Methods:
        execute(command: LockCommand, transaction_id: str | None, lock_id: str | None) -> Any:
            Executes the given lock command and returns the connection result.
    """

    def execute(self, command: LockCommand, transaction_id: str | None, lock_id: str | None) -> Any:  # noqa: ARG002
        """Executes the given lock command.

        Args:
            command (LockCommand): The lock command to be executed.
            transaction_id (str | None): The transaction ID to be used during execution.
            lock_id (str | None): The lock ID to be used during execution.

        Returns:
            Any: The result of the acquire or release call.
        """
        first_ref = command.locked_objects[0].reference

        if isinstance(first_ref, SchemaReference):
            _connection = resolve_connection(first_ref, transaction_id)
        else:
            # LockIdentifier group — strict pool resolve: unknown pool RAISES (§8.4).
            # Do NOT fall back to DEFAULT — that would lock the wrong DB.
            # (first_ref is narrowed to LockIdentifier here — the only non-SchemaReference variant.)
            from amsdal_glue_core.common.interfaces.connection_manager import ConnectionManager
            from amsdal_glue_core.containers import Container

            manager = Container.managers.get(ConnectionManager)
            pool = manager.connections.get(first_ref.pool)
            if pool is None:
                msg = (
                    f"Lock pool '{first_ref.pool}' is not registered. "
                    'Cannot route advisory lock — refusing to fall back to DEFAULT pool.'
                )
                raise RuntimeError(msg)
            _connection = pool.get_connection(transaction_id=transaction_id)

        if command.action == LockAction.ACQUIRE:
            return _connection.acquire_lock(command)
        return _connection.release_lock(command)


class AsyncLockCommandNodeExecutor:
    """Async version of LockCommandNodeExecutor.

    Methods:
        execute(command: LockCommand, transaction_id: str | None, lock_id: str | None) -> Any:
            Executes the given lock command asynchronously and returns the connection result.
    """

    async def execute(self, command: LockCommand, transaction_id: str | None, lock_id: str | None) -> Any:  # noqa: ARG002
        """Executes the given lock command asynchronously.

        Args:
            command (LockCommand): The lock command to be executed.
            transaction_id (str | None): The transaction ID to be used during execution.
            lock_id (str | None): The lock ID to be used during execution.

        Returns:
            Any: The result of the acquire or release call.
        """
        first_ref = command.locked_objects[0].reference

        if isinstance(first_ref, SchemaReference):
            _connection = await resolve_async_connection(first_ref, transaction_id)
        else:
            # LockIdentifier group — strict pool resolve: unknown pool RAISES (§8.4).
            # (first_ref is narrowed to LockIdentifier here — the only non-SchemaReference variant.)
            from amsdal_glue_core.common.interfaces.connection_manager import AsyncConnectionManager
            from amsdal_glue_core.containers import Container

            manager = Container.managers.get(AsyncConnectionManager)
            pool = manager.connections.get(first_ref.pool)
            if pool is None:
                msg = (
                    f"Lock pool '{first_ref.pool}' is not registered. "
                    'Cannot route advisory lock — refusing to fall back to DEFAULT pool.'
                )
                raise RuntimeError(msg)
            _connection = await pool.get_connection(transaction_id=transaction_id)

        if command.action == LockAction.ACQUIRE:
            return await _connection.acquire_lock(command)
        return await _connection.release_lock(command)
