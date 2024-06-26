from abc import ABC
from abc import abstractmethod
from typing import Any

from amsdal_glue_core.commands.lock_command_node import ExecutionLockCommand
from amsdal_glue_core.common.data_models.conditions import Conditions
from amsdal_glue_core.common.data_models.data import Data
from amsdal_glue_core.common.data_models.query import QueryStatement
from amsdal_glue_core.common.data_models.schema import Schema
from amsdal_glue_core.common.interfaces.connectable import Connectable
from amsdal_glue_core.common.operations.commands import SchemaCommand
from amsdal_glue_core.common.operations.commands import TransactionCommand
from amsdal_glue_core.common.operations.mutations.data import DataMutation


class ConnectionBase(Connectable, ABC):
    @abstractmethod
    def query(self, query: QueryStatement) -> list[Data]: ...

    @abstractmethod
    def query_schema(self, filters: Conditions | None = None) -> list[Schema]: ...

    @abstractmethod
    def run_mutations(self, mutations: list[DataMutation]) -> list[list[Data] | None]: ...

    @abstractmethod
    def acquire_lock(self, lock: ExecutionLockCommand) -> Any: ...

    @abstractmethod
    def release_lock(self, lock: ExecutionLockCommand) -> Any: ...

    @abstractmethod
    def commit_transaction(self, transaction: TransactionCommand | str | None) -> Any: ...

    @abstractmethod
    def rollback_transaction(self, transaction: TransactionCommand | str | None) -> Any: ...

    @abstractmethod
    def begin_transaction(self, transaction: TransactionCommand | str | None) -> Any: ...

    @abstractmethod
    def revert_transaction(self, transaction: TransactionCommand | str | None) -> Any: ...

    @abstractmethod
    def run_schema_command(self, command: SchemaCommand) -> list[Schema | None]: ...
