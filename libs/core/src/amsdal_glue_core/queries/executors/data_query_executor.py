# mypy: disable-error-code="type-abstract"
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.data_models.sub_query import SubQueryStatement
from amsdal_glue_core.common.interfaces.connection import AsyncConnectionBase
from amsdal_glue_core.common.interfaces.connection import ConnectionBase
from amsdal_glue_core.common.interfaces.connection_manager import AsyncConnectionManager
from amsdal_glue_core.common.interfaces.connection_manager import ConnectionManager
from amsdal_glue_core.queries.data_query_nodes import DataQueryNode


class DataQueryNodeExecutor:
    """Executes a node in the data query tree.

    This class implements the business logic for executing a single node of a data query tree.

    Methods:
        execute(query: DataQueryNode, transaction_id: str | None, lock_id: str | None) -> None:
            Executes the given data query node.
    """

    def __init__(self) -> None:
        from amsdal_glue_core.containers import Container

        self.connection_manager = Container.managers.get(ConnectionManager)

    def execute(self, query: DataQueryNode, transaction_id: str | None, lock_id: str | None) -> None:  # noqa: ARG002
        """Executes the given data query node.

        Args:
            query (DataQueryNode): The data query node to be executed.
            transaction_id (str | None): The transaction ID to be used during execution.
            lock_id (str | None): The lock ID to be used during execution.
        """
        _query = query.query
        _connection = self.resolve_connection(_query.table, transaction_id)

        query.result = _connection.query(_query)

    def resolve_connection(
        self,
        table: SchemaReference | SubQueryStatement,
        transaction_id: str | None,
    ) -> ConnectionBase:
        """Resolves the connection for the given table.

        Args:
            table (SchemaReference | SubQueryStatement): The table for which to resolve the connection.
            transaction_id (str | None): The transaction ID to be used during execution.

        Returns:
            ConnectionBase: The resolved connection.
        """
        if isinstance(table, SchemaReference):
            return self.connection_manager.get_connection_pool(table.name).get_connection(transaction_id)

        if isinstance(table, SubQueryStatement):
            return self.resolve_connection(table.query.table, transaction_id)

        msg = f'QueryNodeExecutor does not support queries with {type(table)} as table.'
        raise RuntimeError(msg)


class AsyncDataQueryNodeExecutor:
    """Executes a node in the data query tree.

    This class implements the business logic for executing a single node of a data query tree.

    Methods:
        execute(query: DataQueryNode, transaction_id: str | None, lock_id: str | None) -> None:
            Executes the given data query node.
    """

    def __init__(self) -> None:
        from amsdal_glue_core.containers import Container

        self.connection_manager = Container.managers.get(AsyncConnectionManager)

    async def execute(self, query: DataQueryNode, transaction_id: str | None, lock_id: str | None) -> None:  # noqa: ARG002
        """Executes the given data query node.

        Args:
            query (DataQueryNode): The data query node to be executed.
            transaction_id (str | None): The transaction ID to be used during execution.
            lock_id (str | None): The lock ID to be used during execution.
        """
        _query = query.query
        _connection = await self.resolve_connection(_query.table, transaction_id)

        query.result = await _connection.query(_query)

    async def resolve_connection(
        self,
        table: SchemaReference | SubQueryStatement,
        transaction_id: str | None,
    ) -> AsyncConnectionBase:
        """Resolves the connection for the given table.

        Args:
            table (SchemaReference | SubQueryStatement): The table for which to resolve the connection.
            transaction_id (str | None): The transaction ID to be used during execution.

        Returns:
            ConnectionBase: The resolved connection.
        """
        if isinstance(table, SchemaReference):
            return await self.connection_manager.get_connection_pool(table.name).get_connection(transaction_id)

        if isinstance(table, SubQueryStatement):
            return await self.resolve_connection(table.query.table, transaction_id)

        msg = f'QueryNodeExecutor does not support queries with {type(table)} as table.'
        raise RuntimeError(msg)
