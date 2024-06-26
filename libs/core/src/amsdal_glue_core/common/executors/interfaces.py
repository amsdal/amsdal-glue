from abc import ABC
from abc import abstractmethod
from typing import Any

from amsdal_glue_core.common.workflows.task import Task
from amsdal_glue_core.queries.data_query_nodes import FinalDataQueryNode


class SequentialExecutor(ABC):
    """
    Interface for sequential executor.
    """

    @abstractmethod
    def execute_sequential(
        self,
        tasks: list[Task],
        final_task: Task | None,
        transaction_id: str | None,
        lock_id: str | None,
    ) -> Any: ...


class ParallelExecutor(ABC):
    """
    Interface for parallel executor.
    """

    @abstractmethod
    def execute_parallel(self, tasks: list[Task], transaction_id: str | None, lock_id: str | None): ...


class FinalDataQueryExecutor(ABC):
    """
    Interface for final data query executor.
    """

    @abstractmethod
    def execute(self, query_node: FinalDataQueryNode, transaction_id: str | None, lock_id: str | None) -> None: ...
