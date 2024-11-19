from abc import ABC
from abc import abstractmethod

from amsdal_glue_core.common.enums import ConnectionAlias
from amsdal_glue_core.common.interfaces.connection_pool import AsyncConnectionPoolBase
from amsdal_glue_core.common.interfaces.connection_pool import ConnectionPoolBase


class ConnectionManager(ABC):
    connections: dict[str, ConnectionPoolBase]

    @abstractmethod
    def register_connection_pool(self, connection: ConnectionPoolBase, schema_name: str | None = None) -> None:
        """Registers a connection pool for a specific schema.

        Args:
            connection (ConnectionPoolBase): The connection pool to register.
            schema_name (str | None): The schema name for the connection pool.
        """
        ...

    @abstractmethod
    def has_multiple_models_connections(self, connection_alias: ConnectionAlias) -> bool:
        """Checks if there are multiple model connections for the given alias.

        Args:
            connection_alias (ConnectionAlias): The connection alias to check.

        Returns:
            bool: True if there are multiple model connections, False otherwise.
        """
        ...

    @abstractmethod
    def get_connection_pool(self, schema_name: str) -> ConnectionPoolBase:
        """Retrieves the connection pool for a specific schema.

        Args:
            schema_name (str): The schema name for the connection pool.

        Returns:
            ConnectionPoolBase: The connection pool instance.
        """
        ...

    @abstractmethod
    def disconnect_all(self) -> None:
        """Disconnects all registered connection pools."""
        ...


class AsyncConnectionManager(ABC):
    connections: dict[str, AsyncConnectionPoolBase]

    @abstractmethod
    def register_connection_pool(self, connection: AsyncConnectionPoolBase, schema_name: str | None = None) -> None:
        """Registers a connection pool for a specific schema.

        Args:
            connection (AsyncConnectionPoolBase): The connection pool to register.
            schema_name (str | None): The schema name for the connection pool.
        """
        ...

    @abstractmethod
    def has_multiple_models_connections(self, connection_alias: ConnectionAlias) -> bool:
        """Checks if there are multiple model connections for the given alias.

        Args:
            connection_alias (ConnectionAlias): The connection alias to check.

        Returns:
            bool: True if there are multiple model connections, False otherwise.
        """
        ...

    @abstractmethod
    def get_connection_pool(self, schema_name: str) -> AsyncConnectionPoolBase:
        """Retrieves the connection pool for a specific schema.

        Args:
            schema_name (str): The schema name for the connection pool.

        Returns:
            AsyncConnectionPoolBase: The connection pool instance.
        """
        ...

    @abstractmethod
    async def disconnect_all(self) -> None:
        """Disconnects all registered connection pools."""
        ...
