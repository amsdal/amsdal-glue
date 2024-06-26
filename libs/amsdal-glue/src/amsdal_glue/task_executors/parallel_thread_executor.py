# mypy: disable-error-code="type-abstract"
from concurrent.futures import ThreadPoolExecutor

from amsdal_glue_core.common.executors.interfaces import ParallelExecutor
from amsdal_glue_core.common.executors.interfaces import SequentialExecutor
from amsdal_glue_core.common.workflows.chain import ChainTask
from amsdal_glue_core.common.workflows.group import GroupTask
from amsdal_glue_core.common.workflows.task import Task


class ThreadParallelExecutor(ParallelExecutor):
    def execute_parallel(
        self,
        tasks: list[Task],
        transaction_id: str | None,
        lock_id: str | None,
    ):
        with ThreadPoolExecutor() as pool_executor:
            pool_executor.map(lambda task: self.map_fn(task, transaction_id=transaction_id, lock_id=lock_id), tasks)

    def map_fn(
        self,
        task: Task,
        transaction_id: str | None,
        lock_id: str | None,
    ) -> None:
        from amsdal_glue_core.containers import Container

        if isinstance(task, ChainTask):
            executor = Container.executors.get(SequentialExecutor)
            executor.execute_sequential(task.tasks, task.final_task, transaction_id=transaction_id, lock_id=lock_id)
        elif isinstance(task, GroupTask):
            self.execute_parallel(task.tasks, transaction_id=transaction_id, lock_id=lock_id)
        else:
            task.execute(transaction_id=transaction_id, lock_id=lock_id)
