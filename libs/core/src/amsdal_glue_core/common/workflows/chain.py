# mypy: disable-error-code="type-abstract"
from dataclasses import dataclass
from typing import Any

from amsdal_glue_core.common.executors.interfaces import SequentialExecutor
from amsdal_glue_core.common.workflows.task import Task


@dataclass(kw_only=True)
class ChainTask(Task):
    tasks: list[Task]
    final_task: Task | None = None

    def execute(self, transaction_id: str | None, lock_id: str | None):
        from amsdal_glue_core.containers import Container

        executor = Container.executors.get(SequentialExecutor)
        executor.execute_sequential(
            self.tasks,
            final_task=self.final_task,
            transaction_id=transaction_id,
            lock_id=lock_id,
        )

    @property
    def item(self) -> Any:
        if self.final_task:
            return self.final_task.item
        return self.tasks[-1].item

    @property
    def result(self) -> Any:
        """
        Get result of task execution.
        """
        return self.final_task.result if self.final_task else self.tasks[-1].result
