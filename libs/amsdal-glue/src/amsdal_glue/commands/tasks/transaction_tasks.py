from dataclasses import dataclass
from typing import Any

from amsdal_glue_core.commands.transaction_node import ExecutionTransactionCommandNode
from amsdal_glue_core.common.operations.commands import TransactionCommand
from amsdal_glue_core.common.workflows.task import AsyncTask
from amsdal_glue_core.common.workflows.task import Task


@dataclass(kw_only=True)
class TransactionCommandTask(Task):
    """
    TransactionCommandTask is responsible for executing transaction command tasks.
    It extends the Task class.

    Attributes:
        transaction_command (ExecutionTransactionCommandNode): The transaction command to be executed.
    """

    transaction_command: ExecutionTransactionCommandNode

    def execute(self, transaction_id: str | None, lock_id: str | None) -> None:
        """
        Executes the transaction command task.

        Args:
            transaction_id (str | None): The ID of the transaction.
            lock_id (str | None): The ID of the lock.
        """
        from amsdal_glue_core.commands.executors.transaction_command_executor import TransactionNodeExecutor

        _command_executor = TransactionNodeExecutor()
        _command_executor.execute(self.transaction_command, transaction_id=transaction_id, lock_id=lock_id)

    @property
    def item(self) -> Any:
        """
        Returns the transaction command.

        Returns:
            Any: The transaction command.
        """
        return self.transaction_command

    @property
    def result(self) -> Any:
        """
        Returns the result of the transaction command.

        Returns:
            Any: The result of the transaction command.
        """
        return self.transaction_command.result

    def __repr__(self) -> str:
        """
        Returns a string representation of the TransactionCommandTask.

        Returns:
            str: A string representation of the TransactionCommandTask.
        """
        return f'TransactionCommandTask<{self.transaction_command}>'

    def __hash__(self) -> int:
        """
        Returns the hash of the TransactionCommandTask.

        Returns:
            int: The hash of the TransactionCommandTask.
        """
        return hash(id(self))


@dataclass(kw_only=True)
class AsyncTransactionCommandTask(AsyncTask):
    """
    AsyncTransactionCommandTask is responsible for executing transaction command tasks.
    It extends the AsyncTask class.

    Attributes:
        transaction_command (ExecutionTransactionCommandNode): The transaction command to be executed.
    """

    transaction_command: ExecutionTransactionCommandNode

    async def execute(self, transaction_id: str | None, lock_id: str | None) -> None:
        """
        Executes the transaction command task.

        Args:
            transaction_id (str | None): The ID of the transaction.
            lock_id (str | None): The ID of the lock.
        """
        from amsdal_glue_core.commands.executors.transaction_command_executor import AsyncTransactionNodeExecutor

        _command_executor = AsyncTransactionNodeExecutor()
        await _command_executor.execute(self.transaction_command, transaction_id=transaction_id, lock_id=lock_id)

    @property
    def item(self) -> Any:
        """
        Returns the transaction command.

        Returns:
            Any: The transaction command.
        """
        return self.transaction_command

    @property
    def result(self) -> Any:
        """
        Returns the result of the transaction command.

        Returns:
            Any: The result of the transaction command.
        """
        return self.transaction_command.result

    def __repr__(self) -> str:
        """
        Returns a string representation of the TransactionCommandTask.

        Returns:
            str: A string representation of the TransactionCommandTask.
        """
        return f'TransactionCommandTask<{self.transaction_command}>'

    def __hash__(self) -> int:
        """
        Returns the hash of the TransactionCommandTask.

        Returns:
            int: The hash of the TransactionCommandTask.
        """
        return hash(id(self))


@dataclass(kw_only=True)
class TransactionCommandFinalTask(Task):
    """
    TransactionCommandFinalTask processes and aggregates the results of previously executed transaction command tasks.
    It extends the Task class.

    Attributes:
        tasks (list[TransactionCommandTask]): The list of transaction command tasks to be executed.
    """

    tasks: list[TransactionCommandTask]

    def __post_init__(self) -> None:
        """
        Initializes the TransactionCommandFinalTask by setting up the result attribute.
        """
        self._result: ExecutionTransactionCommandNode | None = None

    def execute(self, transaction_id: str | None, lock_id: str | None) -> None:  # noqa: ARG002
        """
        Executes the series of transaction command tasks and aggregates their results.

        Args:
            transaction_id (str | None): The ID of the transaction.
            lock_id (str | None): The ID of the lock.
        """
        if not self.tasks:
            return

        _command = TransactionCommand(
            lock_id=self.tasks[0].item.command.lock_id,
            transaction_id=self.tasks[0].item.command.transaction_id,
            action=self.tasks[0].item.command.action,
            parent_transaction_id=self.tasks[0].item.command.parent_transaction_id,
        )
        _result = None

        for task in self.tasks:
            _result = _result and task.result if _result else task.result

        self._result = ExecutionTransactionCommandNode(
            command=_command,
            result=_result,
        )

    @property
    def item(self) -> Any:
        """
        Returns the list of transaction command items.

        Returns:
            Any: The list of transaction command items.
        """
        return [task.item for task in self.tasks]

    @property
    def result(self) -> list[Any] | None:
        """
        Returns the aggregated result of the transaction command tasks.

        Returns:
            list[Any] | None: The aggregated result of the transaction command tasks.
        """
        return self._result.result if self._result else None


@dataclass(kw_only=True)
class AsyncTransactionCommandFinalTask(AsyncTask):
    """
    TransactionCommandFinalTask processes and aggregates the results of previously executed transaction command tasks.
    It extends the Task class.

    Attributes:
        tasks (list[TransactionCommandTask]): The list of transaction command tasks to be executed.
    """

    tasks: list[AsyncTransactionCommandTask]

    def __post_init__(self) -> None:
        """
        Initializes the TransactionCommandFinalTask by setting up the result attribute.
        """
        self._result: ExecutionTransactionCommandNode | None = None

    async def execute(self, transaction_id: str | None, lock_id: str | None) -> None:  # noqa: ARG002
        """
        Executes the series of transaction command tasks and aggregates their results.

        Args:
            transaction_id (str | None): The ID of the transaction.
            lock_id (str | None): The ID of the lock.
        """
        if not self.tasks:
            return

        _command = TransactionCommand(
            lock_id=self.tasks[0].item.command.lock_id,
            transaction_id=self.tasks[0].item.command.transaction_id,
            action=self.tasks[0].item.command.action,
            parent_transaction_id=self.tasks[0].item.command.parent_transaction_id,
        )
        _result = None

        for task in self.tasks:
            _result = _result and task.result if _result else task.result

        self._result = ExecutionTransactionCommandNode(
            command=_command,
            result=_result,
        )

    @property
    def item(self) -> Any:
        """
        Returns the list of transaction command items.

        Returns:
            Any: The list of transaction command items.
        """
        return [task.item for task in self.tasks]

    @property
    def result(self) -> list[Any] | None:
        """
        Returns the aggregated result of the transaction command tasks.

        Returns:
            list[Any] | None: The aggregated result of the transaction command tasks.
        """
        return self._result.result if self._result else None
