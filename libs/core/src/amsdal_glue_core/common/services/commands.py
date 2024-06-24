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
    @abstractmethod
    def execute(self, command: SchemaCommand) -> SchemaResult: ...


class AsyncSchemaCommandService(ABC):
    @abstractmethod
    async def execute_async(self, command: SchemaCommand) -> SchemaResult: ...


class DataCommandService(ABC):
    @abstractmethod
    def execute(self, command: DataCommand) -> DataResult: ...


class AsyncDataCommandService(ABC):
    @abstractmethod
    async def execute_async(self, command: DataCommand) -> DataResult: ...


class LockCommandService(ABC):
    @abstractmethod
    def execute(self, command: LockCommand) -> LockResult: ...


class AsyncLockCommandService(ABC):
    @abstractmethod
    async def execute_async(self, command: LockCommand) -> LockResult: ...


class TransactionCommandService(ABC):
    @abstractmethod
    def execute(self, command: TransactionCommand) -> TransactionResult: ...


class AsyncTransactionCommandService(ABC):
    @abstractmethod
    async def execute_async(self, command: TransactionCommand) -> TransactionResult: ...
