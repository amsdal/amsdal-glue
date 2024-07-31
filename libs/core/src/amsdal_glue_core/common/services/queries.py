from abc import ABC
from abc import abstractmethod

from amsdal_glue_core.common.data_models.results.data import DataResult
from amsdal_glue_core.common.data_models.results.schema import SchemaResult
from amsdal_glue_core.common.operations.queries import DataQueryOperation
from amsdal_glue_core.common.operations.queries import SchemaQueryOperation


class SchemaQueryService(ABC):
    """
    Abstract base class for executing schema query operations.

    Methods:
        execute(query_op: SchemaQueryOperation) -> SchemaResult:
            Executes the given schema query operation and returns the result.
    """

    @abstractmethod
    def execute(self, query_op: SchemaQueryOperation) -> SchemaResult:
        """
        Executes the given schema query operation.

        Args:
            query_op (SchemaQueryOperation): The schema query operation to execute.

        Returns:
            SchemaResult: The result of the schema query operation.
        """
        ...


class AsyncSchemaQueryService(ABC):
    """
    Abstract base class for executing schema query operations asynchronously.

    Methods:
        execute(query_op: SchemaQueryOperation) -> SchemaResult:
            Asynchronously executes the given schema query operation and returns the result.
    """

    @abstractmethod
    async def execute(self, query_op: SchemaQueryOperation) -> SchemaResult:
        """
        Asynchronously executes the given schema query operation.

        Args:
            query_op (SchemaQueryOperation): The schema query operation to execute.

        Returns:
            SchemaResult: The result of the schema query operation.
        """
        ...


class DataQueryService(ABC):
    """
    Abstract base class for executing data query operations.

    Methods:
        execute(query_op: DataQueryOperation) -> DataResult:
            Executes the given data query operation and returns the result.
    """

    @abstractmethod
    def execute(self, query_op: DataQueryOperation) -> DataResult:
        """
        Executes the given data query operation.

        Args:
            query_op (DataQueryOperation): The data query operation to execute.

        Returns:
            DataResult: The result of the data query operation.
        """
        ...


class AsyncDataQueryService(ABC):
    """
    Abstract base class for executing data query operations asynchronously.

    Methods:
        execute(query_op: DataQueryOperation) -> DataResult:
            Asynchronously executes the given data query operation and returns the result.
    """

    @abstractmethod
    async def execute(self, query_op: DataQueryOperation) -> DataResult:
        """
        Asynchronously executes the given data query operation.

        Args:
            query_op (DataQueryOperation): The data query operation to execute.

        Returns:
            DataResult: The result of the data query operation.
        """
        ...
