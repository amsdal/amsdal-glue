# mypy: disable-error-code="type-abstract"
from amsdal_glue_core.common.executors.interfaces import ParallelExecutor
from amsdal_glue_core.common.executors.interfaces import SequentialExecutor
from amsdal_glue_core.common.workflows.chain import ChainTask
from amsdal_glue_core.common.workflows.group import GroupTask
from amsdal_glue_core.common.workflows.task import Task


class ThreadParallelExecutor(ParallelExecutor):
    """
    ThreadParallelExecutor is responsible for executing tasks in parallel using threads.
    """

    def execute_parallel(
        self,
        tasks: list[Task],
        transaction_id: str | None,
        lock_id: str | None,
    ):
        """
        Executes the given list of tasks in parallel using threads.

        Args:
            tasks (list[Task]): The list of tasks to be executed in parallel.
            transaction_id (str | None): The transaction ID to be used during execution.
            lock_id (str | None): The lock ID to be used during execution.
        """
        from concurrent.futures import ThreadPoolExecutor

        from amsdal_glue import Container

        current_container = Container.__current_container__

        with ThreadPoolExecutor() as pool_executor:
            pool_executor.map(
                lambda task: self.map_fn(current_container, task, transaction_id=transaction_id, lock_id=lock_id),
                tasks,
            )

    def map_fn(
        self,
        container_name: str | None,
        task: Task,
        transaction_id: str | None,
        lock_id: str | None,
    ) -> None:
        """
        Maps and executes a single task, handling different task types.

        Args:
            container_name (str | None): The name of the container
            task (Task): The task to be executed.
            transaction_id (str | None): The transaction ID to be used during execution.
            lock_id (str | None): The lock ID to be used during execution.
        """
        from amsdal_glue import Container

        Container.__current_container__ = container_name  # type: ignore[assignment]

        if isinstance(task, ChainTask):
            executor = Container.executors.get(SequentialExecutor)
            executor.execute_sequential(task.tasks, task.final_task, transaction_id=transaction_id, lock_id=lock_id)
        elif isinstance(task, GroupTask):
            self.execute_parallel(task.tasks, transaction_id=transaction_id, lock_id=lock_id)
        else:
            task.execute(transaction_id=transaction_id, lock_id=lock_id)
