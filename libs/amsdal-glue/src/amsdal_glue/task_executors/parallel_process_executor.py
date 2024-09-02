# mypy: disable-error-code="type-abstract"
from amsdal_glue_core.common.executors.interfaces import ParallelExecutor
from amsdal_glue_core.common.executors.interfaces import SequentialExecutor
from amsdal_glue_core.common.workflows.chain import ChainTask
from amsdal_glue_core.common.workflows.group import GroupTask
from amsdal_glue_core.common.workflows.task import Task


class ProcessParallelExecutor(ParallelExecutor):
    """
    ProcessParallelExecutor is responsible for executing tasks in parallel using processes.
    """

    def execute_parallel(
        self,
        tasks: list[Task],
        transaction_id: str | None,
        lock_id: str | None,
    ) -> None:
        """
        Executes the given list of tasks in parallel using processes.

        Args:
            tasks (list[Task]): The list of tasks to be executed in parallel.
            transaction_id (str | None): The transaction ID to be used during execution.
            lock_id (str | None): The lock ID to be used during execution.
        """
        from concurrent.futures import ProcessPoolExecutor

        from amsdal_glue import Container

        state = Container.serialize_state()

        with ProcessPoolExecutor() as pool_executor:
            pool_executor.map(
                lambda task: self.map_fn(state, task, transaction_id=transaction_id, lock_id=lock_id),
                tasks,
            )

    def map_fn(
        self,
        state: bytes,
        task: Task,
        transaction_id: str | None,
        lock_id: str | None,
    ) -> None:
        """
        Maps and executes a single task, handling different task types.

        Args:
            state (bytes): The serialized state of the container
            task (Task): The task to be executed.
            transaction_id (str | None): The transaction ID to be used during execution.
            lock_id (str | None): The lock ID to be used during execution.
        """
        from amsdal_glue import Container

        Container.deserialize_state(state)

        if isinstance(task, ChainTask):
            executor = Container.executors.get(SequentialExecutor)
            executor.execute_sequential(task.tasks, task.final_task, transaction_id=transaction_id, lock_id=lock_id)
        elif isinstance(task, GroupTask):
            self.execute_parallel(task.tasks, transaction_id=transaction_id, lock_id=lock_id)
        else:
            task.execute(transaction_id=transaction_id, lock_id=lock_id)
