from dataclasses import dataclass
from typing import Any

from amsdal_glue_core.commands.lock_command_node import ExecutionLockCommand
from amsdal_glue_core.common.workflows.task import Task


@dataclass(kw_only=True)
class LockCommandTask(Task):
    lock_command: ExecutionLockCommand

    def execute(self, transaction_id: str | None, lock_id: str | None) -> None:
        from amsdal_glue_core.commands.executors.lock_command_executor import LockCommandNodeExecutor

        _command_executor = LockCommandNodeExecutor()
        _command_executor.execute(self.lock_command, transaction_id=transaction_id, lock_id=lock_id)

    @property
    def item(self) -> Any:
        return self.lock_command

    @property
    def result(self) -> Any:
        return self.lock_command.result

    def __repr__(self) -> str:
        return f'LockCommandTask<{self.lock_command}>'

    def __hash__(self) -> int:
        return hash(id(self))
