from abc import ABC
from abc import abstractmethod
from typing import Any

from amsdal_glue_core.commands.lock_command_node import ExecutionLockCommand
from amsdal_glue_core.common.data_models.conditions import Conditions
from amsdal_glue_core.common.data_models.data import Data
from amsdal_glue_core.common.data_models.query import QueryStatement
from amsdal_glue_core.common.data_models.schema import Schema
from amsdal_glue_core.common.interfaces.connectable import AsyncConnectable
from amsdal_glue_core.common.interfaces.connectable import Connectable
from amsdal_glue_core.common.operations.commands import SchemaCommand
from amsdal_glue_core.common.operations.commands import TransactionCommand
from amsdal_glue_core.common.operations.mutations.data import DataMutation


class ConnectionBase(Connectable, ABC):
    """Abstract base class for database connections."""

    debug_mode: bool = False

    @abstractmethod
    def query(self, query: QueryStatement) -> list[Data]:
        """Executes a query and returns the result.

        Args:
            query (QueryStatement): The query to execute.

        Returns:
            list[Data]: The result of the query.
        """

    @abstractmethod
    def query_schema(self, filters: Conditions | None = None) -> list[Schema]:
        """Queries the schema with optional filters.

        Args:
            filters (Conditions | None): Optional filters for the schema query.

        Returns:
            list[Schema]: The result of the schema query.
        """

    @abstractmethod
    def run_mutations(self, mutations: list[DataMutation]) -> list[list[Data] | None]:
        """Executes a list of data mutations.

        Args:
            mutations (list[DataMutation]): The list of data mutations to execute.

        Returns:
            list[list[Data] | None]: The result of the mutations.
        """

    @abstractmethod
    def acquire_lock(self, lock: ExecutionLockCommand) -> Any:
        """Acquires a lock.

        Args:
            lock (ExecutionLockCommand): The lock command to execute.

        Returns:
            Any: The result of the lock acquisition.
        """

    @abstractmethod
    def release_lock(self, lock: ExecutionLockCommand) -> Any:
        """Releases a lock.

        Args:
            lock (ExecutionLockCommand): The lock command to execute.

        Returns:
            Any: The result of the lock release.
        """

    @abstractmethod
    def commit_transaction(self, transaction: TransactionCommand | str | None) -> Any:
        """Commits a transaction.

        Args:
            transaction (TransactionCommand | str | None): The transaction to commit.

        Returns:
            Any: The result of the transaction commit.
        """

    @abstractmethod
    def rollback_transaction(self, transaction: TransactionCommand | str | None) -> Any:
        """Rolls back a transaction.

        Args:
            transaction (TransactionCommand | str | None): The transaction to roll back.

        Returns:
            Any: The result of the transaction rollback.
        """

    @abstractmethod
    def begin_transaction(self, transaction: TransactionCommand | str | None) -> Any:
        """Begins a transaction.

        Args:
            transaction (TransactionCommand | str | None): The transaction to begin.

        Returns:
            Any: The result of the transaction begin.
        """

    @abstractmethod
    def revert_transaction(self, transaction: TransactionCommand | str | None) -> Any:
        """Reverts a transaction.

        Args:
            transaction (TransactionCommand | str | None): The transaction to revert.

        Returns:
            Any: The result of the transaction revert.
        """

    @abstractmethod
    def run_schema_command(self, command: SchemaCommand) -> list[Schema | None]:
        """Executes a schema command.

        Args:
            command (SchemaCommand): The schema command to execute.

        Returns:
            list[Schema | None]: The result of the schema command.
        """

    @property
    def debug_queries(self) -> bool:
        """
        Returns the debug queries flag.

        Returns:
            bool: True if debug queries are enabled, False otherwise.
        """
        return self.debug_mode

    @property
    @abstractmethod
    def queries(self) -> list[str]:
        """
        Returns the queries executed on this connection.

        Returns:
            list[str]: The queries executed.
        """
        ...


class AsyncConnectionBase(AsyncConnectable, ABC):
    """Abstract base class for async database connections."""

    debug_mode: bool = False

    @abstractmethod
    async def query(self, query: QueryStatement) -> list[Data]:
        """Executes a query and returns the result.

        Args:
            query (QueryStatement): The query to execute.

        Returns:
            list[Data]: The result of the query.
        """

    @abstractmethod
    async def query_schema(self, filters: Conditions | None = None) -> list[Schema]:
        """Queries the schema with optional filters.

        Args:
            filters (Conditions | None): Optional filters for the schema query.

        Returns:
            list[Schema]: The result of the schema query.
        """

    @abstractmethod
    async def run_mutations(self, mutations: list[DataMutation]) -> list[list[Data] | None]:
        """Executes a list of data mutations.

        Args:
            mutations (list[DataMutation]): The list of data mutations to execute.

        Returns:
            list[list[Data] | None]: The result of the mutations.
        """

    @abstractmethod
    async def acquire_lock(self, lock: ExecutionLockCommand) -> Any:
        """Acquires a lock.

        Args:
            lock (ExecutionLockCommand): The lock command to execute.

        Returns:
            Any: The result of the lock acquisition.
        """

    @abstractmethod
    async def release_lock(self, lock: ExecutionLockCommand) -> Any:
        """Releases a lock.

        Args:
            lock (ExecutionLockCommand): The lock command to execute.

        Returns:
            Any: The result of the lock release.
        """

    @abstractmethod
    async def commit_transaction(self, transaction: TransactionCommand | str | None) -> Any:
        """Commits a transaction.

        Args:
            transaction (TransactionCommand | str | None): The transaction to commit.

        Returns:
            Any: The result of the transaction commit.
        """

    @abstractmethod
    async def rollback_transaction(self, transaction: TransactionCommand | str | None) -> Any:
        """Rolls back a transaction.

        Args:
            transaction (TransactionCommand | str | None): The transaction to roll back.

        Returns:
            Any: The result of the transaction rollback.
        """

    @abstractmethod
    async def begin_transaction(self, transaction: TransactionCommand | str | None) -> Any:
        """Begins a transaction.

        Args:
            transaction (TransactionCommand | str | None): The transaction to begin.

        Returns:
            Any: The result of the transaction begin.
        """

    @abstractmethod
    async def revert_transaction(self, transaction: TransactionCommand | str | None) -> Any:
        """Reverts a transaction.

        Args:
            transaction (TransactionCommand | str | None): The transaction to revert.

        Returns:
            Any: The result of the transaction revert.
        """

    @abstractmethod
    async def run_schema_command(self, command: SchemaCommand) -> list[Schema | None]:
        """Executes a schema command.

        Args:
            command (SchemaCommand): The schema command to execute.

        Returns:
            list[Schema | None]: The result of the schema command.
        """

    @property
    def debug_queries(self) -> bool:
        """
        Returns the debug queries flag.

        Returns:
            bool: True if debug queries are enabled, False otherwise.
        """
        return self.debug_mode

    @property
    @abstractmethod
    def queries(self) -> list[str]:
        """
        Returns the queries executed on this connection.

        Returns:
            list[str]: The queries executed.
        """
        ...
