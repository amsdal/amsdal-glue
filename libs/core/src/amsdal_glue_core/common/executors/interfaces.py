from abc import ABC
from abc import abstractmethod
from typing import Any

from amsdal_glue_core.common.workflows.task import Task


class SequentialExecutor(ABC):
    """
    Interface for sequential executor.
    """

    @abstractmethod
    def execute_sequential(
        self,
        tasks: list[Task],
        final_task: Task | None,
    ) -> Any: ...


class ParallelExecutor(ABC):
    """
    Interface for parallel executor.
    """

    @abstractmethod
    def execute_parallel(
        self,
        tasks: list[Task],
    ): ...


class FinalExecutor(ABC):
    """
    Interface for final query executor.
    """

    @abstractmethod
    def execute(self, task: Task) -> None: ...
