# mypy: disable-error-code="type-abstract"
from typing import TYPE_CHECKING

from amsdal_glue_core.common.interfaces.connection_manager import AsyncConnectionManager
from amsdal_glue_core.common.interfaces.connection_manager import ConnectionManager

if TYPE_CHECKING:
    from amsdal_glue_core.queries.schema_query_nodes import SchemaQueryNode


class SchemaQueryNodeExecutor:
    """Executes a node in the schema query tree.

    This class implements the business logic for executing a single node of a schema query tree.

    Methods:
        execute(query_node: SchemaQueryNode, transaction_id: str | None, lock_id: str | None) -> None:
            Executes the given schema query node.
    """

    def execute(self, query_node: 'SchemaQueryNode', transaction_id: str | None, lock_id: str | None) -> None:  # noqa: ARG002
        """Executes the given schema query node.

        Args:
            query_node (SchemaQueryNode): The schema query node to be executed.
            transaction_id (str | None): The transaction ID to be used during execution.
            lock_id (str | None): The lock ID to be used during execution.
        """
        from amsdal_glue_core.containers import Container

        connection_manager = Container.managers.get(ConnectionManager)
        connection = connection_manager.get_connection_pool(query_node.schema_name_connection).get_connection(
            transaction_id
        )
        query_node.result = connection.query_schema(query_node.filters)


class AsyncSchemaQueryNodeExecutor:
    """Executes a node in the schema query tree.

    This class implements the business logic for executing a single node of a schema query tree.

    Methods:
        execute(query_node: SchemaQueryNode, transaction_id: str | None, lock_id: str | None) -> None:
            Executes the given schema query node.
    """

    async def execute(self, query_node: 'SchemaQueryNode', transaction_id: str | None, lock_id: str | None) -> None:  # noqa: ARG002
        """Executes the given schema query node.

        Args:
            query_node (SchemaQueryNode): The schema query node to be executed.
            transaction_id (str | None): The transaction ID to be used during execution.
            lock_id (str | None): The lock ID to be used during execution.
        """
        from amsdal_glue_core.containers import Container

        connection_manager = Container.managers.get(AsyncConnectionManager)
        connection = await connection_manager.get_connection_pool(query_node.schema_name_connection).get_connection(
            transaction_id
        )
        query_node.result = await connection.query_schema(query_node.filters)
