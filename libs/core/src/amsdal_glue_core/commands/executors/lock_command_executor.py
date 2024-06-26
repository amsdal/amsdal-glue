from typing import TYPE_CHECKING

from amsdal_glue_core.common.enums import LockAction
from amsdal_glue_core.common.helpers.resolve_connection import resolve_connection
from amsdal_glue_core.common.helpers.singleton import Singleton

if TYPE_CHECKING:
    from amsdal_glue_core.commands.lock_command_node import ExecutionLockCommand


class LockCommandNodeExecutor(metaclass=Singleton):
    def execute(self, command: 'ExecutionLockCommand', transaction_id: str | None, lock_id: str | None) -> None:  # noqa: ARG002
        lock_object = command.locked_object
        _connection = resolve_connection(lock_object.schema, transaction_id)

        if command.action == LockAction.ACQUIRE:
            command.result = _connection.acquire_lock(command)

        else:
            command.result = _connection.release_lock(command)
