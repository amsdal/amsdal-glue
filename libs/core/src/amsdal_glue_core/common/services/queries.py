from abc import ABC
from abc import abstractmethod

from amsdal_glue_core.common.data_models.results.data import DataResult
from amsdal_glue_core.common.data_models.results.schema import SchemaResult
from amsdal_glue_core.common.operations.queries import DataQueryOperation
from amsdal_glue_core.common.operations.queries import SchemaQueryOperation


class SchemaQueryService(ABC):
    @abstractmethod
    def execute(self, query_op: SchemaQueryOperation) -> SchemaResult: ...


class AsyncSchemaQueryService(ABC):
    @abstractmethod
    async def execute(self, query_op: SchemaQueryOperation) -> SchemaResult: ...


class DataQueryService(ABC):
    @abstractmethod
    def execute(self, query_op: DataQueryOperation) -> DataResult: ...


class AsyncDataQueryService(ABC):
    @abstractmethod
    async def execute(self, query_op: DataQueryOperation) -> DataResult: ...
