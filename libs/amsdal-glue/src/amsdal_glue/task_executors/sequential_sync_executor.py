# mypy: disable-error-code="type-abstract"
from typing import Any

from amsdal_glue_core.common.executors.interfaces import AsyncParallelExecutor
from amsdal_glue_core.common.executors.interfaces import AsyncSequentialExecutor
from amsdal_glue_core.common.executors.interfaces import ParallelExecutor
from amsdal_glue_core.common.executors.interfaces import SequentialExecutor
from amsdal_glue_core.common.workflows.chain import AsyncChainTask
from amsdal_glue_core.common.workflows.chain import ChainTask
from amsdal_glue_core.common.workflows.group import AsyncGroupTask
from amsdal_glue_core.common.workflows.group import GroupTask
from amsdal_glue_core.common.workflows.task import AsyncTask
from amsdal_glue_core.common.workflows.task import Task


class SequentialSyncExecutor(SequentialExecutor):
    """
    SequentialSyncExecutor is responsible for executing tasks sequentially.
    """

    def execute_sequential(
        self,
        tasks: list[Task],
        final_task: Task | None,
        transaction_id: str | None,
        lock_id: str | None,
    ) -> Any:
        """
        Executes the given list of tasks sequentially.

        Args:
            tasks (list[Task]): The list of tasks to be executed sequentially.
            final_task (Task | None): The final task to be executed after all tasks.
            transaction_id (str | None): The transaction ID to be used during execution.
            lock_id (str | None): The lock ID to be used during execution.

        Returns:
            Any: The result of the final task execution.
        """
        from amsdal_glue_core.containers import Container

        for task in tasks:
            if isinstance(task, ChainTask):
                self.execute_sequential(task.tasks, task.final_task, transaction_id=transaction_id, lock_id=lock_id)
            elif isinstance(task, GroupTask):
                parallel_executor = Container.executors.get(ParallelExecutor)
                parallel_executor.execute_parallel(task.tasks, transaction_id=transaction_id, lock_id=lock_id)
            else:
                task.execute(transaction_id=transaction_id, lock_id=lock_id)

        if final_task:
            final_task.execute(transaction_id=transaction_id, lock_id=lock_id)


class AsyncSequentialSyncExecutor(AsyncSequentialExecutor):
    """
    AsyncSequentialSyncExecutor is responsible for executing tasks sequentially.
    """

    async def execute_sequential(
        self,
        tasks: list[AsyncTask],
        final_task: AsyncTask | None,
        transaction_id: str | None,
        lock_id: str | None,
    ) -> Any:
        """
        Executes the given list of tasks sequentially.

        Args:
            tasks (list[AsyncTask]): The list of tasks to be executed sequentially.
            final_task (AsyncTask | None): The final task to be executed after all tasks.
            transaction_id (str | None): The transaction ID to be used during execution.
            lock_id (str | None): The lock ID to be used during execution.

        Returns:
            Any: The result of the final task execution.
        """
        from amsdal_glue_core.containers import Container

        for task in tasks:
            if isinstance(task, AsyncChainTask):
                await self.execute_sequential(
                    task.tasks, task.final_task, transaction_id=transaction_id, lock_id=lock_id
                )
            elif isinstance(task, AsyncGroupTask):
                parallel_executor = Container.executors.get(AsyncParallelExecutor)
                await parallel_executor.execute_parallel(task.tasks, transaction_id=transaction_id, lock_id=lock_id)
            else:
                await task.execute(transaction_id=transaction_id, lock_id=lock_id)

        if final_task:
            await final_task.execute(transaction_id=transaction_id, lock_id=lock_id)
