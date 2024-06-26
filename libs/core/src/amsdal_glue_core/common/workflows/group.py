# mypy: disable-error-code="type-abstract"
from dataclasses import dataclass
from typing import Any

from amsdal_glue_core.common.executors.interfaces import ParallelExecutor
from amsdal_glue_core.common.workflows.task import Task


@dataclass(kw_only=True)
class GroupTask(Task):
    tasks: list[Task]

    def execute(self, transaction_id: str | None, lock_id: str | None):
        from amsdal_glue_core.containers import Container

        parallel_executor = Container.executors.get(ParallelExecutor)
        parallel_executor.execute_parallel(self.tasks, transaction_id=transaction_id, lock_id=lock_id)

    @property
    def item(self) -> Any:
        return [task.item for task in self.tasks]

    @property
    def result(self) -> Any:
        return [task.result for task in self.tasks]
