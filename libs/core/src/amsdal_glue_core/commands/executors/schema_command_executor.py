# mypy: disable-error-code="type-abstract"
from amsdal_glue_core.commands.mutation_nodes import SchemaCommandNode
from amsdal_glue_core.common.interfaces.connection import AsyncConnectionBase
from amsdal_glue_core.common.interfaces.connection import ConnectionBase
from amsdal_glue_core.common.interfaces.connection_manager import AsyncConnectionManager
from amsdal_glue_core.common.interfaces.connection_manager import ConnectionManager
from amsdal_glue_core.common.operations.mutations.schema import SchemaMutation


class SchemaCommandNodeExecutor:
    """Executes a node in the schema command tree produced by the schema command planner.

    This class implements the business logic for executing a single node of a schema command tree.

    Attributes:
        connection_manager (ConnectionManager): Manages connections to the database.
    """

    def __init__(self) -> None:
        """Initializes the SchemaCommandNodeExecutor with a connection manager."""
        from amsdal_glue_core.containers import Container

        self.connection_manager = Container.managers.get(ConnectionManager)

    def execute(self, command_node: SchemaCommandNode, transaction_id: str | None, lock_id: str | None) -> None:  # noqa: ARG002
        """Executes the given schema command node.

        Args:
            command_node (SchemaCommandNode): The schema command node to be executed.
            transaction_id (str | None): The transaction ID to be used during execution.
            lock_id (str | None): The lock ID to be used during execution.
        """
        _command = command_node.command
        _connection = self.resolve_connection(_command.mutations, transaction_id)

        _connection.run_schema_command(_command)

    def resolve_connection(self, mutations: list[SchemaMutation], transaction_id: str | None) -> ConnectionBase:
        """Resolves the connection for the given schema mutations.

        Args:
            mutations (list[SchemaMutation]): The list of schema mutations to resolve the connection for.
            transaction_id (str | None): The transaction ID to be used during execution.

        Returns:
            ConnectionBase: The resolved connection for the schema mutations.

        Raises:
            ValueError: If no mutations are provided.
        """
        if not mutations:
            msg = 'No mutations to resolve connection for'
            raise ValueError(msg)

        return self.connection_manager.get_connection_pool(mutations[0].get_schema_name()).get_connection(
            transaction_id
        )


class AsyncSchemaCommandNodeExecutor:
    """Executes a node in the schema command tree produced by the schema command planner.

    This class implements the business logic for executing a single node of a schema command tree.

    Attributes:
        connection_manager (AsyncConnectionManager): Manages connections to the database.
    """

    def __init__(self) -> None:
        """Initializes the SchemaCommandNodeExecutor with a connection manager."""
        from amsdal_glue_core.containers import Container

        self.connection_manager = Container.managers.get(AsyncConnectionManager)

    async def execute(self, command_node: SchemaCommandNode, transaction_id: str | None, lock_id: str | None) -> None:  # noqa: ARG002
        """Executes the given schema command node.

        Args:
            command_node (SchemaCommandNode): The schema command node to be executed.
            transaction_id (str | None): The transaction ID to be used during execution.
            lock_id (str | None): The lock ID to be used during execution.
        """
        _command = command_node.command
        _connection = await self.resolve_connection(_command.mutations, transaction_id)

        await _connection.run_schema_command(_command)

    async def resolve_connection(
        self, mutations: list[SchemaMutation], transaction_id: str | None
    ) -> AsyncConnectionBase:
        """Resolves the connection for the given schema mutations.

        Args:
            mutations (list[SchemaMutation]): The list of schema mutations to resolve the connection for.
            transaction_id (str | None): The transaction ID to be used during execution.

        Returns:
            ConnectionBase: The resolved connection for the schema mutations.

        Raises:
            ValueError: If no mutations are provided.
        """
        if not mutations:
            msg = 'No mutations to resolve connection for'
            raise ValueError(msg)

        return await self.connection_manager.get_connection_pool(mutations[0].get_schema_name()).get_connection(
            transaction_id
        )
