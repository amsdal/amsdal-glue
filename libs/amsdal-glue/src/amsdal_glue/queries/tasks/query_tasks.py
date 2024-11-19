# mypy: disable-error-code="type-abstract"
from typing import Any

from amsdal_glue_core.common.executors.interfaces import AsyncFinalDataQueryExecutor
from amsdal_glue_core.common.executors.interfaces import FinalDataQueryExecutor
from amsdal_glue_core.common.workflows.task import AsyncTask
from amsdal_glue_core.common.workflows.task import Task
from amsdal_glue_core.queries.data_query_nodes import DataQueryNode
from amsdal_glue_core.queries.data_query_nodes import FinalDataQueryNode
from amsdal_glue_core.queries.executors.data_query_executor import AsyncDataQueryNodeExecutor
from amsdal_glue_core.queries.executors.data_query_executor import DataQueryNodeExecutor


class DataQueryTask(Task):
    """
    DataQueryTask is responsible for executing a data query node.
    It extends the Task class.

    Attributes:
        query_node (DataQueryNode): The data query node to be executed.
        executor (DataQueryNodeExecutor): The executor responsible for executing the data query node.
    """

    def __init__(self, query_node: DataQueryNode):
        """
        Initializes the DataQueryTask with the given query node.

        Args:
            query_node (DataQueryNode): The data query node to be executed.
        """
        self.query_node = query_node
        self.executor = DataQueryNodeExecutor()

    def execute(self, transaction_id: str | None, lock_id: str | None):
        """
        Executes the data query node.

        Args:
            transaction_id (str | None): The ID of the transaction.
            lock_id (str | None): The ID of the lock.
        """
        self.executor.execute(self.query_node, transaction_id=transaction_id, lock_id=lock_id)

    @property
    def item(self) -> Any:
        """
        Returns the data query node.

        Returns:
            Any: The data query node.
        """
        return self.query_node

    @property
    def result(self) -> Any:
        """
        Returns the result of the data query node execution.

        Returns:
            Any: The result of the data query node execution.
        """
        return self.query_node.result


class AsyncDataQueryTask(AsyncTask):
    """
    AsyncDataQueryTask is responsible for executing a data query node.
    It extends the AsyncTask class.

    Attributes:
        query_node (DataQueryNode): The data query node to be executed.
        executor (AsyncDataQueryNodeExecutor): The executor responsible for executing the data query node.
    """

    def __init__(self, query_node: DataQueryNode):
        """
        Initializes the DataQueryTask with the given query node.

        Args:
            query_node (DataQueryNode): The data query node to be executed.
        """
        self.query_node = query_node
        self.executor = AsyncDataQueryNodeExecutor()

    async def execute(self, transaction_id: str | None, lock_id: str | None):
        """
        Executes the data query node.

        Args:
            transaction_id (str | None): The ID of the transaction.
            lock_id (str | None): The ID of the lock.
        """
        await self.executor.execute(self.query_node, transaction_id=transaction_id, lock_id=lock_id)

    @property
    def item(self) -> Any:
        """
        Returns the data query node.

        Returns:
            Any: The data query node.
        """
        return self.query_node

    @property
    def result(self) -> Any:
        """
        Returns the result of the data query node execution.

        Returns:
            Any: The result of the data query node execution.
        """
        return self.query_node.result


class FinalDataQueryTask(Task):
    """
    FinalDataQueryTask is responsible for executing a final data query node.
    It extends the Task class.

    Attributes:
        query_node (FinalDataQueryNode): The final data query node to be executed.
        executor (FinalDataQueryExecutor): The executor responsible for executing the final data query node.
    """

    def __init__(self, query_node: FinalDataQueryNode):
        """
        Initializes the FinalDataQueryTask with the given query node.

        Args:
            query_node (FinalDataQueryNode): The final data query node to be executed.
        """
        from amsdal_glue_core.containers import Container

        self.query_node = query_node
        self.executor = Container.executors.get(FinalDataQueryExecutor)

    def execute(self, transaction_id: str | None, lock_id: str | None) -> None:
        """
        Executes the final data query node.

        Args:
            transaction_id (str | None): The ID of the transaction.
            lock_id (str | None): The ID of the lock.
        """
        self.executor.execute(self.query_node, transaction_id=transaction_id, lock_id=lock_id)

    @property
    def item(self) -> Any:
        """
        Returns the final data query node.

        Returns:
            Any: The final data query node.
        """
        return self.query_node

    @property
    def result(self) -> Any:
        """
        Returns the result of the final data query node execution.

        Returns:
            Any: The result of the final data query node execution.
        """
        return self.query_node.result


class AsyncFinalDataQueryTask(AsyncTask):
    """
    AsyncFinalDataQueryTask is responsible for executing a final data query node.
    It extends the AsyncTask class.

    Attributes:
        query_node (FinalDataQueryNode): The final data query node to be executed.
        executor (AsyncFinalDataQueryExecutor): The executor responsible for executing the final data query node.
    """

    def __init__(self, query_node: FinalDataQueryNode):
        """
        Initializes the FinalDataQueryTask with the given query node.

        Args:
            query_node (FinalDataQueryNode): The final data query node to be executed.
        """
        from amsdal_glue_core.containers import Container

        self.query_node = query_node
        self.executor = Container.executors.get(AsyncFinalDataQueryExecutor)

    async def execute(self, transaction_id: str | None, lock_id: str | None) -> None:
        """
        Executes the final data query node.

        Args:
            transaction_id (str | None): The ID of the transaction.
            lock_id (str | None): The ID of the lock.
        """
        await self.executor.execute(self.query_node, transaction_id=transaction_id, lock_id=lock_id)

    @property
    def item(self) -> Any:
        """
        Returns the final data query node.

        Returns:
            Any: The final data query node.
        """
        return self.query_node

    @property
    def result(self) -> Any:
        """
        Returns the result of the final data query node execution.

        Returns:
            Any: The result of the final data query node execution.
        """
        return self.query_node.result
