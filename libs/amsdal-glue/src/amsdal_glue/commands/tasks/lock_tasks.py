from dataclasses import dataclass
from dataclasses import field
from typing import Any

from amsdal_glue_core.common.operations.commands import LockCommand
from amsdal_glue_core.common.workflows.task import AsyncTask
from amsdal_glue_core.common.workflows.task import Task


@dataclass(kw_only=True)
class LockCommandTask(Task):
    """
    LockCommandTask is responsible for executing lock command tasks.
    It extends the Task class.

    Attributes:
        lock_command (LockCommand): The grouped lock command to be executed.
    """

    lock_command: LockCommand
    _result: Any = field(init=False, default=None)

    def execute(self, transaction_id: str | None, lock_id: str | None) -> None:
        """
        Executes the lock command task.

        Args:
            transaction_id (str | None): The ID of the transaction.
            lock_id (str | None): The ID of the lock.
        """
        from amsdal_glue_core.commands.executors.lock_command_executor import LockCommandNodeExecutor

        _command_executor = LockCommandNodeExecutor()
        self._result = _command_executor.execute(self.lock_command, transaction_id=transaction_id, lock_id=lock_id)

    @property
    def item(self) -> Any:
        """
        Returns the lock command.

        Returns:
            Any: The lock command.
        """
        return self.lock_command

    @property
    def result(self) -> Any:
        """
        Returns the result of the lock command execution.

        Returns:
            Any: The result of the lock command.
        """
        return self._result

    def __repr__(self) -> str:
        """
        Returns a string representation of the LockCommandTask.

        Returns:
            str: A string representation of the LockCommandTask.
        """
        return f'LockCommandTask<{self.lock_command}>'

    def __hash__(self) -> int:
        """
        Returns the hash of the LockCommandTask.

        Returns:
            int: The hash of the LockCommandTask.
        """
        return hash(id(self))


@dataclass(kw_only=True)
class AsyncLockCommandTask(AsyncTask):
    """
    AsyncLockCommandTask is responsible for executing lock command tasks.
    It extends the AsyncTask class.

    Attributes:
        lock_command (LockCommand): The grouped lock command to be executed.
    """

    lock_command: LockCommand
    _result: Any = field(init=False, default=None)

    async def execute(self, transaction_id: str | None, lock_id: str | None) -> None:
        """
        Executes the lock command task asynchronously.

        Args:
            transaction_id (str | None): The ID of the transaction.
            lock_id (str | None): The ID of the lock.
        """
        from amsdal_glue_core.commands.executors.lock_command_executor import AsyncLockCommandNodeExecutor

        _command_executor = AsyncLockCommandNodeExecutor()
        self._result = await _command_executor.execute(
            self.lock_command, transaction_id=transaction_id, lock_id=lock_id
        )

    @property
    def item(self) -> Any:
        """
        Returns the lock command.

        Returns:
            Any: The lock command.
        """
        return self.lock_command

    @property
    def result(self) -> Any:
        """
        Returns the result of the lock command execution.

        Returns:
            Any: The result of the lock command.
        """
        return self._result

    def __repr__(self) -> str:
        """
        Returns a string representation of the AsyncLockCommandTask.

        Returns:
            str: A string representation of the AsyncLockCommandTask.
        """
        return f'LockCommandTask<{self.lock_command}>'

    def __hash__(self) -> int:
        """
        Returns the hash of the AsyncLockCommandTask.

        Returns:
            int: The hash of the AsyncLockCommandTask.
        """
        return hash(id(self))
