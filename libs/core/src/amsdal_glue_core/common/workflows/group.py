# mypy: disable-error-code="type-abstract"
from dataclasses import dataclass
from typing import Any

from amsdal_glue_core.common.executors.interfaces import AsyncParallelExecutor
from amsdal_glue_core.common.executors.interfaces import ParallelExecutor
from amsdal_glue_core.common.workflows.task import AsyncTask
from amsdal_glue_core.common.workflows.task import Task


@dataclass(kw_only=True)
class GroupTask(Task):
    """
    Represents a group of tasks to be executed in parallel.

    Attributes:
        tasks (list[Task]): The list of tasks to be executed.

    Methods:
        execute(transaction_id: str | None, lock_id: str | None) -> None:
            Executes the group of tasks in parallel using the ParallelExecutor.

        item() -> Any:
            Returns the items of the tasks in the group.

        result() -> Any:
            Returns the results of the tasks in the group.
    """

    tasks: list[Task]
    executor: ParallelExecutor | None = None

    def execute(self, transaction_id: str | None, lock_id: str | None):
        """
        Executes the group of tasks in parallel using the ParallelExecutor.

        Parameters:
            transaction_id (str | None): The transaction ID to be used during execution.
            lock_id (str | None): The lock ID to be used during execution.
        """
        from amsdal_glue_core.containers import Container

        parallel_executor = self.executor or Container.executors.get(ParallelExecutor)
        parallel_executor.execute_parallel(self.tasks, transaction_id=transaction_id, lock_id=lock_id)

    @property
    def item(self) -> Any:
        """
        Returns the items of the tasks in the group.

        Returns:
            Any: The items of the tasks in the group.
        """
        return [task.item for task in self.tasks]

    @property
    def result(self) -> Any:
        """
        Returns the results of the tasks in the group.

        Returns:
            Any: The results of the tasks in the group.
        """
        return [task.result for task in self.tasks]


@dataclass(kw_only=True)
class AsyncGroupTask(AsyncTask):
    """
    Represents a group of tasks to be executed in parallel.

    Attributes:
        tasks (list[Task]): The list of tasks to be executed.

    Methods:
        execute(transaction_id: str | None, lock_id: str | None) -> None:
            Executes the group of tasks in parallel using the AsyncParallelExecutor.

        item() -> Any:
            Returns the items of the tasks in the group.

        result() -> Any:
            Returns the results of the tasks in the group.
    """

    tasks: list[AsyncTask]
    executor: AsyncParallelExecutor | None = None

    async def execute(self, transaction_id: str | None, lock_id: str | None):
        """
        Executes the group of tasks in parallel using the AsyncParallelExecutor.

        Parameters:
            transaction_id (str | None): The transaction ID to be used during execution.
            lock_id (str | None): The lock ID to be used during execution.
        """
        from amsdal_glue_core.containers import Container

        parallel_executor = self.executor or Container.executors.get(AsyncParallelExecutor)
        await parallel_executor.execute_parallel(self.tasks, transaction_id=transaction_id, lock_id=lock_id)

    @property
    def item(self) -> Any:
        """
        Returns the items of the tasks in the group.

        Returns:
            Any: The items of the tasks in the group.
        """
        return [task.item for task in self.tasks]

    @property
    def result(self) -> Any:
        """
        Returns the results of the tasks in the group.

        Returns:
            Any: The results of the tasks in the group.
        """
        return [task.result for task in self.tasks]
