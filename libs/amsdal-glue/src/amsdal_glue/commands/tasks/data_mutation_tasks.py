from dataclasses import dataclass
from typing import Any

from amsdal_glue_core.commands.executors.data_command_executor import AsyncDataCommandNodeExecutor
from amsdal_glue_core.commands.executors.data_command_executor import DataCommandNodeExecutor
from amsdal_glue_core.commands.mutation_nodes import DataMutationNode
from amsdal_glue_core.common.workflows.task import AsyncTask
from amsdal_glue_core.common.workflows.task import Task


@dataclass(kw_only=True)
class DataMutationTask(Task):
    """
    DataMutationTask is responsible for executing data mutation tasks.
    It extends the Task class.
    """

    data_mutation_node: DataMutationNode

    def execute(self, transaction_id: str | None, lock_id: str | None) -> None:
        """
        Executes the data mutation task.

        Args:
            transaction_id (str | None): The ID of the transaction.
            lock_id (str | None): The ID of the lock.
        """
        _query_executor = DataCommandNodeExecutor()
        _query_executor.execute(self.data_mutation_node, transaction_id=transaction_id, lock_id=lock_id)

    @property
    def item(self) -> Any:
        """
        Returns the data mutation node.

        Returns:
            Any: The data mutation node.
        """
        return self.data_mutation_node

    @property
    def result(self) -> Any:
        """
        Returns the result of the data mutation.

        Returns:
            Any: The result of the data mutation.
        """
        return self.data_mutation_node.result


@dataclass(kw_only=True)
class AsyncDataMutationTask(AsyncTask):
    """
    AsyncDataMutationTask is responsible for executing data mutation tasks.
    It extends the AsyncTask class.
    """

    data_mutation_node: DataMutationNode

    async def execute(self, transaction_id: str | None, lock_id: str | None) -> None:
        """
        Executes the data mutation task.

        Args:
            transaction_id (str | None): The ID of the transaction.
            lock_id (str | None): The ID of the lock.
        """
        _query_executor = AsyncDataCommandNodeExecutor()
        await _query_executor.execute(self.data_mutation_node, transaction_id=transaction_id, lock_id=lock_id)

    @property
    def item(self) -> Any:
        """
        Returns the data mutation node.

        Returns:
            Any: The data mutation node.
        """
        return self.data_mutation_node

    @property
    def result(self) -> Any:
        """
        Returns the result of the data mutation.

        Returns:
            Any: The result of the data mutation.
        """
        return self.data_mutation_node.result
