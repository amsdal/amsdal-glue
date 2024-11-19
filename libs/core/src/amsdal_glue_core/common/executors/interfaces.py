from abc import ABC
from abc import abstractmethod
from typing import Any

from amsdal_glue_core.common.workflows.task import AsyncTask
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
    ) -> Any:
        """Executes the given tasks sequentially.

        Args:
            tasks (list[Task]): The list of tasks to be executed.
            final_task (Task | None): The final task to be executed.
            transaction_id (str | None): The transaction ID to be used during execution.
            lock_id (str | None): The lock ID to be used during execution.

        Returns:
            Any: The result of the execution.
        """
        ...


class AsyncSequentialExecutor(ABC):
    """
    Interface for sequential executor.
    """

    @abstractmethod
    async def execute_sequential(
        self,
        tasks: list[AsyncTask],
        final_task: AsyncTask | None,
        transaction_id: str | None,
        lock_id: str | None,
    ) -> Any:
        """Executes the given tasks sequentially.

        Args:
            tasks (list[AsyncTask]): The list of tasks to be executed.
            final_task (AsyncTask | None): The final task to be executed.
            transaction_id (str | None): The transaction ID to be used during execution.
            lock_id (str | None): The lock ID to be used during execution.

        Returns:
            Any: The result of the execution.
        """
        ...


class ParallelExecutor(ABC):
    """
    Interface for parallel executor.

    Methods:
        execute_parallel(tasks: list[Task], transaction_id: str | None, lock_id: str | None) -> Any:
            Executes the given tasks in parallel.
    """

    @abstractmethod
    def execute_parallel(
        self,
        tasks: list[Task],
        transaction_id: str | None,
        lock_id: str | None,
    ) -> Any:
        """Executes the given tasks in parallel.

        Args:
            tasks (list[Task]): The list of tasks to be executed.
            transaction_id (str | None): The transaction ID to be used during execution.
            lock_id (str | None): The lock ID to be used during execution.

        Returns:
            Any: The result of the execution.
        """
        ...


class AsyncParallelExecutor(ABC):
    """
    Interface for parallel executor.

    Methods:
        execute_parallel(tasks: list[AsyncTask], transaction_id: str | None, lock_id: str | None) -> Any:
            Executes the given tasks in parallel.
    """

    @abstractmethod
    async def execute_parallel(
        self,
        tasks: list[AsyncTask],
        transaction_id: str | None,
        lock_id: str | None,
    ) -> Any:
        """Executes the given tasks in parallel.

        Args:
            tasks (list[AsyncTask]): The list of tasks to be executed.
            transaction_id (str | None): The transaction ID to be used during execution.
            lock_id (str | None): The lock ID to be used during execution.

        Returns:
            Any: The result of the execution.
        """
        ...


class FinalDataQueryExecutor(ABC):
    """
    Interface for final data query executor.

    Methods:
        execute(query_node: FinalDataQueryNode, transaction_id: str | None, lock_id: str | None) -> None:
            Executes the given final data query node.
    """

    @abstractmethod
    def execute(
        self,
        query_node: FinalDataQueryNode,
        transaction_id: str | None,
        lock_id: str | None,
    ) -> None:
        """Executes the given final data query node.

        Args:
            query_node (FinalDataQueryNode): The final data query node to be executed.
            transaction_id (str | None): The transaction ID to be used during execution.
            lock_id (str | None): The lock ID to be used during execution.
        """
        ...


class AsyncFinalDataQueryExecutor(ABC):
    """
    Interface for final data query executor.

    Methods:
        execute(query_node: FinalDataQueryNode, transaction_id: str | None, lock_id: str | None) -> None:
            Executes the given final data query node.
    """

    @abstractmethod
    async def execute(
        self,
        query_node: FinalDataQueryNode,
        transaction_id: str | None,
        lock_id: str | None,
    ) -> None:
        """Executes the given final data query node.

        Args:
            query_node (FinalDataQueryNode): The final data query node to be executed.
            transaction_id (str | None): The transaction ID to be used during execution.
            lock_id (str | None): The lock ID to be used during execution.
        """
        ...
