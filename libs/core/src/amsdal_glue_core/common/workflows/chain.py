# mypy: disable-error-code="type-abstract"
from dataclasses import dataclass
from typing import Any

from amsdal_glue_core.common.executors.interfaces import AsyncSequentialExecutor
from amsdal_glue_core.common.executors.interfaces import SequentialExecutor
from amsdal_glue_core.common.workflows.task import AsyncTask
from amsdal_glue_core.common.workflows.task import Task


@dataclass(kw_only=True)
class ChainTask(Task):
    """
    Represents a chain of tasks to be executed sequentially.

    Attributes:
        tasks (list[Task]): The list of tasks to be executed.
        final_task (Task | None): The final task to be executed after the chain of tasks.

    Methods:
        execute(transaction_id: str | None, lock_id: str | None) -> None:
            Executes the chain of tasks sequentially using the SequentialExecutor.

        item() -> Any:
            Returns the item of the final task or the last task in the chain.

        result() -> Any:
            Returns the result of the final task or the last task in the chain.
    """

    tasks: list[Task]
    final_task: Task | None = None
    executor: SequentialExecutor | None = None

    def execute(self, transaction_id: str | None, lock_id: str | None) -> None:
        """
        Executes the chain of tasks sequentially using the SequentialExecutor.

        Parameters:
            transaction_id (str | None): The transaction ID to be used during execution.
            lock_id (str | None): The lock ID to be used during execution.
        """

        from amsdal_glue_core.containers import Container

        executor = self.executor or Container.executors.get(SequentialExecutor)
        executor.execute_sequential(
            self.tasks,
            final_task=self.final_task,
            transaction_id=transaction_id,
            lock_id=lock_id,
        )

    @property
    def item(self) -> Any:
        """
        Returns the item of the final task or the last task in the chain.

        Returns:
            Any: The item of the final task or the last task in the chain.
        """
        if self.final_task:
            return self.final_task.item
        return self.tasks[-1].item

    @property
    def result(self) -> Any:
        """
        Returns the result of the final task or the last task in the chain.

        Returns:
            Any: The result of the final task or the last task in the chain.
        """
        return self.final_task.result if self.final_task else self.tasks[-1].result


@dataclass(kw_only=True)
class AsyncChainTask(AsyncTask):
    """
    Represents a chain of tasks to be executed sequentially.

    Attributes:
        tasks (list[AsyncTask]): The list of tasks to be executed.
        final_task (AsyncTask | None): The final task to be executed after the chain of tasks.

    Methods:
        execute(transaction_id: str | None, lock_id: str | None) -> None:
            Executes the chain of tasks sequentially using the SequentialExecutor.

        item() -> Any:
            Returns the item of the final task or the last task in the chain.

        result() -> Any:
            Returns the result of the final task or the last task in the chain.
    """

    tasks: list[AsyncTask]
    final_task: AsyncTask | None = None
    executor: AsyncSequentialExecutor | None = None

    async def execute(self, transaction_id: str | None, lock_id: str | None) -> None:
        """
        Executes the chain of tasks sequentially using the AsyncSequentialExecutor.

        Parameters:
            transaction_id (str | None): The transaction ID to be used during execution.
            lock_id (str | None): The lock ID to be used during execution.
        """

        from amsdal_glue_core.containers import Container

        executor = self.executor or Container.executors.get(AsyncSequentialExecutor)
        await executor.execute_sequential(
            self.tasks,
            final_task=self.final_task,
            transaction_id=transaction_id,
            lock_id=lock_id,
        )

    @property
    def item(self) -> Any:
        """
        Returns the item of the final task or the last task in the chain.

        Returns:
            Any: The item of the final task or the last task in the chain.
        """
        if self.final_task:
            return self.final_task.item
        return self.tasks[-1].item

    @property
    def result(self) -> Any:
        """
        Returns the result of the final task or the last task in the chain.

        Returns:
            Any: The result of the final task or the last task in the chain.
        """
        return self.final_task.result if self.final_task else self.tasks[-1].result
