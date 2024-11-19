import asyncio

from amsdal_glue_core.common.enums import ConnectionAlias

from amsdal_glue.interfaces import AsyncConnectionManager
from amsdal_glue.interfaces import AsyncConnectionPoolBase
from amsdal_glue.interfaces import ConnectionManager
from amsdal_glue.interfaces import ConnectionPoolBase


class DefaultConnectionManager(ConnectionManager):
    """Manages multiple connection pools for different schemas.

    Methods:
        register_connection_pool(connection: ConnectionPoolBase, schema_name: str | None = None) -> None:
            Registers a connection pool for a specific schema.
        has_multiple_models_connections(connection_alias: ConnectionAlias) -> bool:
            Checks if there are multiple model connections for the given alias.
        get_connection_pool(schema_name: str) -> ConnectionPoolBase:
            Retrieves the connection pool for a specific schema.
        disconnect_all() -> None:
            Disconnects all registered connection pools.

    Example:
        Always use [Container][amsdal_glue.Container] to register and retrieve the connection manager.

        Register a ConnectionManager instance:

        ```python
        from amsdal_glue import Container
        from amsdal_glue import Singleton
        from amsdal_glue import ConnectionManager

        Container.managers.register(ConnectionManagerBase, Singleton(ConnectionManager))
        ```

        Retrieve the ConnectionManager instance:

        ```python
        from amsdal_glue import Container
        from amsdal_glue import ConnectionManager

        connection_manager = Container.managers.get(ConnectionManager)
        ```

        The ConnectionManager class provides methods to register and retrieve
        [DefaultConnectionPool][amsdal_glue.DefaultConnectionPool] for different schemas.

        Register a connection pool for a specific schema `users`:

        ```python
        from amsdal_glue import Container
        from amsdal_glue import ConnectionManager
        from amsdal_glue import DefaultConnectionPool
        from amsdal_glue import PostgresConnection

        connection_manager = Container.managers.get(ConnectionManager)
        connection_manager.register_connection_pool(
            DefaultConnectionPool(
                PostgresConnection,
                dsn='postgres://db_user:db_password@localhost:5433/db_name',
            ),
            schema_name='users',
        )
        ```

        Retrieve the connection pool for the schema `users`:

        ```python
        from amsdal_glue import Container
        from amsdal_glue import ConnectionManager

        connection_manager = Container.managers.get(ConnectionManager)
        connection_pool = connection_manager.get_connection_pool('users')
        ```
    """

    def __init__(self) -> None:
        self.connections: dict[str, ConnectionPoolBase] = {}

    def register_connection_pool(self, connection: ConnectionPoolBase, schema_name: str | None = None) -> None:
        """Registers a connection pool for a specific schema.

        Args:
            connection (ConnectionPoolBase): The connection pool to register.
            schema_name (str | None): The schema name for the connection pool.
        """
        self.connections[schema_name or ConnectionAlias.DEFAULT] = connection

    def has_multiple_models_connections(self, connection_alias: ConnectionAlias) -> bool:
        """Checks if there are multiple model connections for the given alias.

        Args:
            connection_alias (ConnectionAlias): The connection alias to check.

        Returns:
            bool: True if there are multiple model connections, False otherwise.
        """
        return connection_alias == ConnectionAlias.DEFAULT and len(self.connections) > 1

    def get_connection_pool(self, schema_name: str) -> ConnectionPoolBase:
        """Retrieves the connection pool for a specific schema.

        Args:
            schema_name (str): The schema name for the connection pool.

        Returns:
            ConnectionPoolBase: The connection pool instance.
        """
        return self.connections.get(schema_name) or self.connections[ConnectionAlias.DEFAULT]

    def disconnect_all(self) -> None:
        """Disconnects all registered connection pools."""
        for connection in self.connections.values():
            connection.disconnect()

        self.connections.clear()

    def __del__(self) -> None:
        self.disconnect_all()


class DefaultAsyncConnectionManager(AsyncConnectionManager):
    def __init__(self) -> None:
        self.connections: dict[str, AsyncConnectionPoolBase] = {}

    def register_connection_pool(self, connection: AsyncConnectionPoolBase, schema_name: str | None = None) -> None:
        """Registers a connection pool for a specific schema.

        Args:
            connection (AsyncConnectionPoolBase): The connection pool to register.
            schema_name (str | None): The schema name for the connection pool.
        """
        self.connections[schema_name or ConnectionAlias.DEFAULT] = connection

    def has_multiple_models_connections(self, connection_alias: ConnectionAlias) -> bool:
        """Checks if there are multiple model connections for the given alias.

        Args:
            connection_alias (ConnectionAlias): The connection alias to check.

        Returns:
            bool: True if there are multiple model connections, False otherwise.
        """
        return connection_alias == ConnectionAlias.DEFAULT and len(self.connections) > 1

    def get_connection_pool(self, schema_name: str) -> AsyncConnectionPoolBase:
        """Retrieves the connection pool for a specific schema.

        Args:
            schema_name (str): The schema name for the connection pool.

        Returns:
            AsyncConnectionPoolBase: The connection pool instance.
        """
        return self.connections.get(schema_name) or self.connections[ConnectionAlias.DEFAULT]

    async def disconnect_all(self) -> None:
        """Disconnects all registered connection pools."""

        for connection in self.connections.values():
            await connection.disconnect()

        self.connections.clear()

    def __del__(self) -> None:
        # Close connection when this object is destroyed
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                loop.create_task(self.disconnect_all())  # noqa: RUF006
            else:
                loop.run_until_complete(self.disconnect_all())
        except Exception:  # noqa: BLE001, S110
            pass
