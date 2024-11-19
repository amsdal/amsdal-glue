from dataclasses import dataclass
from typing import Any

from amsdal_glue_core.commands.executors.schema_command_executor import AsyncSchemaCommandNodeExecutor
from amsdal_glue_core.commands.executors.schema_command_executor import SchemaCommandNodeExecutor
from amsdal_glue_core.commands.mutation_nodes import SchemaCommandNode
from amsdal_glue_core.common.operations.commands import SchemaCommand
from amsdal_glue_core.common.workflows.task import AsyncTask
from amsdal_glue_core.common.workflows.task import Task


@dataclass(kw_only=True)
class SchemaCommandTask(Task):
    """
    SchemaCommandTask is responsible for executing schema command tasks.
    It extends the Task class.

    Attributes:
        command_node (SchemaCommandNode): The schema command node to be executed.
    """

    command_node: SchemaCommandNode

    def __post_init__(self) -> None:
        """
        Initializes the SchemaCommandTask by setting up the executor.
        """
        self._executor = SchemaCommandNodeExecutor()

    def execute(self, transaction_id: str | None, lock_id: str | None) -> None:
        """
        Executes the schema command task.

        Args:
            transaction_id (str | None): The ID of the transaction.
            lock_id (str | None): The ID of the lock.
        """
        self._executor.execute(self.command_node, transaction_id=transaction_id, lock_id=lock_id)

    @property
    def item(self) -> Any:
        """
        Returns the schema command.

        Returns:
            Any: The schema command.
        """
        return self.command_node.command

    @property
    def result(self) -> list[Any] | None:
        """
        Returns the result of the schema command.

        Returns:
            list[Any] | None: The result of the schema command.
        """
        return self.command_node.result


@dataclass(kw_only=True)
class AsyncSchemaCommandTask(AsyncTask):
    """
    AsyncSchemaCommandTask is responsible for executing schema command tasks.
    It extends the AsyncTask class.

    Attributes:
        command_node (SchemaCommandNode): The schema command node to be executed.
    """

    command_node: SchemaCommandNode

    def __post_init__(self) -> None:
        """
        Initializes the SchemaCommandTask by setting up the executor.
        """
        self._executor = AsyncSchemaCommandNodeExecutor()

    async def execute(self, transaction_id: str | None, lock_id: str | None) -> None:
        """
        Executes the schema command task.

        Args:
            transaction_id (str | None): The ID of the transaction.
            lock_id (str | None): The ID of the lock.
        """
        await self._executor.execute(self.command_node, transaction_id=transaction_id, lock_id=lock_id)

    @property
    def item(self) -> Any:
        """
        Returns the schema command.

        Returns:
            Any: The schema command.
        """
        return self.command_node.command

    @property
    def result(self) -> list[Any] | None:
        """
        Returns the result of the schema command.

        Returns:
            list[Any] | None: The result of the schema command.
        """
        return self.command_node.result


@dataclass(kw_only=True)
class FinalSchemaCommandTask(Task):
    """
    FinalSchemaCommandTask processes and aggregates the results of previously executed tasks.
    It extends the Task class.

    Attributes:
        tasks (list[SchemaCommandTask]): The list of schema command tasks to be executed.
    """

    tasks: list[SchemaCommandTask]

    def __post_init__(self) -> None:
        """
        Initializes the FinalSchemaCommandTask by setting up the result attribute.
        """
        self._result: SchemaCommandNode | None = None

    def execute(self, transaction_id: str | None, lock_id: str | None) -> None:  # noqa: ARG002
        """
        Runs aggregation of the results of the schema command tasks.

        Args:
            transaction_id (str | None): The ID of the transaction.
            lock_id (str | None): The ID of the lock.
        """
        if not self.tasks:
            return

        _command = SchemaCommand(
            lock_id=self.tasks[0].item.lock_id,
            root_transaction_id=self.tasks[0].item.root_transaction_id,
            transaction_id=self.tasks[0].item.transaction_id,
            mutations=[],
        )
        _result = []

        for task in self.tasks:
            _command.mutations.extend(task.item.mutations)
            _results = [task.result[i] if task.result else None for i in range(len(task.item.mutations))]
            _result.extend(_results)

        self._result = SchemaCommandNode(
            command=_command,
            result=_result,
        )

    @property
    def item(self) -> Any:
        """
        Returns the list of schema command items.

        Returns:
            Any: The list of schema command items.
        """
        return [task.item for task in self.tasks]

    @property
    def result(self) -> list[Any] | None:
        """
        Returns the result of the schema command tasks.

        Returns:
            list[Any] | None: The result of the schema command tasks.
        """
        return self._result.result if self._result else None


@dataclass(kw_only=True)
class AsyncFinalSchemaCommandTask(AsyncTask):
    """
    AsyncFinalSchemaCommandTask processes and aggregates the results of previously executed tasks.
    It extends the AsyncTask class.

    Attributes:
        tasks (list[AsyncSchemaCommandTask]): The list of schema command tasks to be executed.
    """

    tasks: list[AsyncSchemaCommandTask]

    def __post_init__(self) -> None:
        """
        Initializes the AsyncFinalSchemaCommandTask by setting up the result attribute.
        """
        self._result: SchemaCommandNode | None = None

    async def execute(self, transaction_id: str | None, lock_id: str | None) -> None:  # noqa: ARG002
        """
        Runs aggregation of the results of the schema command tasks.

        Args:
            transaction_id (str | None): The ID of the transaction.
            lock_id (str | None): The ID of the lock.
        """
        if not self.tasks:
            return

        _command = SchemaCommand(
            lock_id=self.tasks[0].item.lock_id,
            root_transaction_id=self.tasks[0].item.root_transaction_id,
            transaction_id=self.tasks[0].item.transaction_id,
            mutations=[],
        )
        _result = []

        for task in self.tasks:
            _command.mutations.extend(task.item.mutations)
            _results = [task.result[i] if task.result else None for i in range(len(task.item.mutations))]
            _result.extend(_results)

        self._result = SchemaCommandNode(
            command=_command,
            result=_result,
        )

    @property
    def item(self) -> Any:
        """
        Returns the list of schema command items.

        Returns:
            Any: The list of schema command items.
        """
        return [task.item for task in self.tasks]

    @property
    def result(self) -> list[Any] | None:
        """
        Returns the result of the schema command tasks.

        Returns:
            list[Any] | None: The result of the schema command tasks.
        """
        return self._result.result if self._result else None
