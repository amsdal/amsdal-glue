# mypy: disable-error-code="type-abstract"
from typing import Any

from amsdal_glue_core.common.executors.interfaces import ParallelExecutor
from amsdal_glue_core.common.executors.interfaces import SequentialExecutor
from amsdal_glue_core.common.workflows.chain import ChainTask
from amsdal_glue_core.common.workflows.group import GroupTask
from amsdal_glue_core.common.workflows.task import Task


class SequentialSyncExecutor(SequentialExecutor):
    def execute_sequential(
        self,
        tasks: list[Task],
        final_task: Task | None,
    ) -> Any:
        from amsdal_glue_core.containers import Container

        for task in tasks:
            if isinstance(task, ChainTask):
                self.execute_sequential(task.tasks, task.final_task)
            elif isinstance(task, GroupTask):
                parallel_executor = Container.executors.get(ParallelExecutor)
                parallel_executor.execute_parallel(task.tasks)
            else:
                task.execute()

        if final_task:
            final_task.execute()