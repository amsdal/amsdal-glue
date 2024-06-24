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
    ):
        with ThreadPoolExecutor() as pool_executor:
            pool_executor.map(lambda task: self.map_fn(task), tasks)

    def map_fn(
        self,
        task: Task,
    ) -> None:
        from amsdal_glue_core.containers import Container

        if isinstance(task, ChainTask):
            executor = Container.executors.get(SequentialExecutor)
            executor.execute_sequential(task.tasks, task.final_task)
        elif isinstance(task, GroupTask):
            self.execute_parallel(task.tasks)
        else:
            task.execute()
