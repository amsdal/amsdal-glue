from abc import ABC
from abc import abstractmethod

from amsdal_glue_core.common.data_models.results.data import DataResult
from amsdal_glue_core.common.data_models.results.data import LockResult
from amsdal_glue_core.common.data_models.results.data import TransactionResult
from amsdal_glue_core.common.data_models.results.schema import SchemaResult
from amsdal_glue_core.common.operations.commands import DataCommand
from amsdal_glue_core.common.operations.commands import LockCommand
from amsdal_glue_core.common.operations.commands import SchemaCommand
from amsdal_glue_core.common.operations.commands import TransactionCommand


class SchemaCommandService(ABC):
    """
    Abstract base class for executing schema command operations.

    Methods:
        execute(command: SchemaCommand) -> SchemaResult:
            Executes the given schema command and returns the result.
    """

    @abstractmethod
    def execute(self, command: SchemaCommand) -> SchemaResult:
        """
        Executes the given schema command.

        Args:
            command (SchemaCommand): The schema command to execute.

        Returns:
            SchemaResult: The result of the schema command.
        """
        ...


class AsyncSchemaCommandService(ABC):
    """
    Abstract base class for executing schema command operations asynchronously.

    Methods:
        execute_async(command: SchemaCommand) -> SchemaResult:
            Asynchronously executes the given schema command and returns the result.
    """

    @abstractmethod
    async def execute(self, command: SchemaCommand) -> SchemaResult:
        """
        Asynchronously executes the given schema command.

        Args:
            command (SchemaCommand): The schema command to execute.

        Returns:
            SchemaResult: The result of the schema command.
        """
        ...


class DataCommandService(ABC):
    """
    Abstract base class for executing data command operations.

    Methods:
        execute(command: DataCommand) -> DataResult:
            Executes the given data command and returns the result.
    """

    @abstractmethod
    def execute(self, command: DataCommand) -> DataResult:
        """
        Executes the given data command.

        Args:
            command (DataCommand): The data command to execute.

        Returns:
            DataResult: The result of the data command.
        """
        ...


class AsyncDataCommandService(ABC):
    """
    Abstract base class for executing data command operations asynchronously.

    Methods:
        execute_async(command: DataCommand) -> DataResult:
            Asynchronously executes the given data command and returns the result.
    """

    @abstractmethod
    async def execute(self, command: DataCommand) -> DataResult:
        """
        Asynchronously executes the given data command.

        Args:
            command (DataCommand): The data command to execute.

        Returns:
            DataResult: The result of the data command.
        """
        ...


class LockCommandService(ABC):
    """
    Abstract base class for executing lock command operations.

    Methods:
        execute(command: LockCommand) -> LockResult:
            Executes the given lock command and returns the result.
    """

    @abstractmethod
    def execute(self, command: LockCommand) -> LockResult:
        """
        Executes the given lock command.

        Args:
            command (LockCommand): The lock command to execute.

        Returns:
            LockResult: The result of the lock command.
        """
        ...


class AsyncLockCommandService(ABC):
    """
    Abstract base class for executing lock command operations asynchronously.

    Methods:
        execute_async(command: LockCommand) -> LockResult:
            Asynchronously executes the given lock command and returns the result.
    """

    @abstractmethod
    async def execute(self, command: LockCommand) -> LockResult:
        """
        Asynchronously executes the given lock command.

        Args:
            command (LockCommand): The lock command to execute.

        Returns:
            LockResult: The result of the lock command.
        """
        ...


class TransactionCommandService(ABC):
    """
    Abstract base class for executing transaction command operations.

    Methods:
        execute(command: TransactionCommand) -> TransactionResult:
            Executes the given transaction command and returns the result.
    """

    @abstractmethod
    def execute(self, command: TransactionCommand) -> TransactionResult:
        """
        Executes the given transaction command.

        Args:
            command (TransactionCommand): The transaction command to execute.

        Returns:
            TransactionResult: The result of the transaction command.
        """
        ...


class AsyncTransactionCommandService(ABC):
    """
    Abstract base class for executing transaction command operations asynchronously.

    Methods:
        execute_async(command: TransactionCommand) -> TransactionResult:
            Asynchronously executes the given transaction command and returns the result.
    """

    @abstractmethod
    async def execute(self, command: TransactionCommand) -> TransactionResult:
        """
        Asynchronously executes the given transaction command.

        Args:
            command (TransactionCommand): The transaction command to execute.

        Returns:
            TransactionResult: The result of the transaction command.
        """
        ...
