from dataclasses import dataclass
from typing import Any

from amsdal_glue_core.common.data_models.schema import Schema
from amsdal_glue_core.common.workflows.task import AsyncTask
from amsdal_glue_core.common.workflows.task import Task
from amsdal_glue_core.queries.executors.schema_query_executor import AsyncSchemaQueryNodeExecutor
from amsdal_glue_core.queries.executors.schema_query_executor import SchemaQueryNodeExecutor
from amsdal_glue_core.queries.schema_query_nodes import SchemaQueryNode


@dataclass(kw_only=True)
class SchemaQueryTask(Task):
    """
    SchemaQueryTask is responsible for executing a schema query node.
    It extends the Task class.

    Attributes:
        schema_query_node (SchemaQueryNode): The schema query node to be executed.
    """

    def __init__(self, schema_query_node: SchemaQueryNode):
        """
        Initializes the SchemaQueryTask with the given schema query node.

        Args:
            schema_query_node (SchemaQueryNode): The schema query node to be executed.
        """
        self.schema_query_node = schema_query_node

    def execute(self, transaction_id: str | None, lock_id: str | None) -> None:
        """
        Executes the schema query node.

        Args:
            transaction_id (str | None): The ID of the transaction.
            lock_id (str | None): The ID of the lock.
        """
        _query_executor = SchemaQueryNodeExecutor()
        _query_executor.execute(self.schema_query_node, transaction_id=transaction_id, lock_id=lock_id)

    @property
    def item(self) -> Any:
        """
        Returns the schema query node.

        Returns:
            Any: The schema query node.
        """
        return self.schema_query_node

    @property
    def result(self) -> list[Schema] | None:
        """
        Returns the result of the schema query node execution.

        Returns:
            list[Schema] | None: The result of the schema query node execution.
        """
        return self.schema_query_node.result


@dataclass(kw_only=True)
class AsyncSchemaQueryTask(AsyncTask):
    """
    AsyncSchemaQueryTask is responsible for executing a schema query node.
    It extends the AsyncTask class.

    Attributes:
        schema_query_node (SchemaQueryNode): The schema query node to be executed.
    """

    def __init__(self, schema_query_node: SchemaQueryNode):
        """
        Initializes the SchemaQueryTask with the given schema query node.

        Args:
            schema_query_node (SchemaQueryNode): The schema query node to be executed.
        """
        self.schema_query_node = schema_query_node

    async def execute(self, transaction_id: str | None, lock_id: str | None) -> None:
        """
        Executes the schema query node.

        Args:
            transaction_id (str | None): The ID of the transaction.
            lock_id (str | None): The ID of the lock.
        """
        _query_executor = AsyncSchemaQueryNodeExecutor()
        await _query_executor.execute(self.schema_query_node, transaction_id=transaction_id, lock_id=lock_id)

    @property
    def item(self) -> Any:
        """
        Returns the schema query node.

        Returns:
            Any: The schema query node.
        """
        return self.schema_query_node

    @property
    def result(self) -> list[Schema] | None:
        """
        Returns the result of the schema query node execution.

        Returns:
            list[Schema] | None: The result of the schema query node execution.
        """
        return self.schema_query_node.result


class FinalSchemaQueryTask(Task):
    """
    FinalSchemaQueryTask is responsible for executing a final schema query node.
    It extends the Task class.

    Attributes:
        tasks (list[SchemaQueryTask]): The list of schema query tasks to be executed.
        _results (list[Schema]): The results of the schema query tasks execution.
    """

    def __init__(self, tasks: list[SchemaQueryTask]):
        """
        Initializes the FinalSchemaQueryTask with the given list of schema query tasks.

        Args:
            tasks (list[SchemaQueryTask]): The list of schema query tasks to be executed.
        """
        self._tasks = tasks
        self._results: list[Schema] = []

    @property
    def item(self) -> Any:
        """
        Returns the list of schema query nodes.

        Returns:
            Any: The list of schema query nodes.
        """
        return [task.item for task in self._tasks]

    @property
    def result(self) -> list[Schema]:
        """
        Returns the results of the schema query tasks execution.

        Returns:
            list[Schema]: The results of the schema query tasks execution.
        """
        return self._results

    def execute(self, transaction_id: str | None, lock_id: str | None) -> None:  # noqa: ARG002
        """
        Executes the final schema query tasks.

        Args:
            transaction_id (str | None): The ID of the transaction.
            lock_id (str | None): The ID of the lock.
        """
        self._results = []

        for task in self._tasks:
            self._results.extend(task.result or [])


class AsyncFinalSchemaQueryTask(AsyncTask):
    """
    AsyncFinalSchemaQueryTask is responsible for executing a final schema query node.
    It extends the AsyncTask class.

    Attributes:
        tasks (list[AsyncSchemaQueryTask]): The list of schema query tasks to be executed.
        _results (list[Schema]): The results of the schema query tasks execution.
    """

    def __init__(self, tasks: list[AsyncSchemaQueryTask]):
        """
        Initializes the FinalSchemaQueryTask with the given list of schema query tasks.

        Args:
            tasks (list[AsyncSchemaQueryTask]): The list of schema query tasks to be executed.
        """
        self._tasks = tasks
        self._results: list[Schema] = []

    @property
    def item(self) -> Any:
        """
        Returns the list of schema query nodes.

        Returns:
            Any: The list of schema query nodes.
        """
        return [task.item for task in self._tasks]

    @property
    def result(self) -> list[Schema]:
        """
        Returns the results of the schema query tasks execution.

        Returns:
            list[Schema]: The results of the schema query tasks execution.
        """
        return self._results

    async def execute(self, transaction_id: str | None, lock_id: str | None) -> None:  # noqa: ARG002
        """
        Executes the final schema query tasks.

        Args:
            transaction_id (str | None): The ID of the transaction.
            lock_id (str | None): The ID of the lock.
        """
        self._results = []

        for task in self._tasks:
            self._results.extend(task.result or [])
