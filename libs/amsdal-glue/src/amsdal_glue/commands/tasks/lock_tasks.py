from dataclasses import dataclass
from typing import Any

from amsdal_glue_core.commands.lock_command_node import ExecutionLockCommand
from amsdal_glue_core.common.workflows.task import AsyncTask
from amsdal_glue_core.common.workflows.task import Task


@dataclass(kw_only=True)
class LockCommandTask(Task):
    """
    LockCommandTask is responsible for executing lock command tasks.
    It extends the Task class.

    Attributes:
        lock_command (ExecutionLockCommand): The lock command to be executed.
    """

    lock_command: ExecutionLockCommand

    def execute(self, transaction_id: str | None, lock_id: str | None) -> None:
        """
        Executes the lock command task.

        Args:
            transaction_id (str | None): The ID of the transaction.
            lock_id (str | None): The ID of the lock.
        """
        from amsdal_glue_core.commands.executors.lock_command_executor import LockCommandNodeExecutor

        _command_executor = LockCommandNodeExecutor()
        _command_executor.execute(self.lock_command, transaction_id=transaction_id, lock_id=lock_id)

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
        Returns the result of the lock command.

        Returns:
            Any: The result of the lock command.
        """
        return self.lock_command.result

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
        lock_command (ExecutionLockCommand): The lock command to be executed.
    """

    lock_command: ExecutionLockCommand

    async def execute(self, transaction_id: str | None, lock_id: str | None) -> None:
        """
        Executes the lock command task.

        Args:
            transaction_id (str | None): The ID of the transaction.
            lock_id (str | None): The ID of the lock.
        """
        from amsdal_glue_core.commands.executors.lock_command_executor import AsyncLockCommandNodeExecutor

        _command_executor = AsyncLockCommandNodeExecutor()
        await _command_executor.execute(self.lock_command, transaction_id=transaction_id, lock_id=lock_id)

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
        Returns the result of the lock command.

        Returns:
            Any: The result of the lock command.
        """
        return self.lock_command.result

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
