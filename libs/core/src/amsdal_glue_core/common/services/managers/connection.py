from abc import ABC
from abc import abstractmethod
from typing import Any

from amsdal_glue_core.common.enums import ConnectionAlias
from amsdal_glue_core.common.helpers.singleton import Singleton
from amsdal_glue_core.common.interfaces.connection import ConnectionBase


class ConnectionPoolBase(ABC):
    """Abstract base class for managing a pool of database connections.

    Args:
        connection_class (type[ConnectionBase]): The class of the connection to manage.
        *args (Any): Positional arguments to pass to the connection class.
        **kwargs (Any): Keyword arguments to pass to the connection class.

    Methods:
        get_connection(transaction_id: str | None = None) -> ConnectionBase:
            Retrieves a connection from the pool.
        disconnect_connection(transaction_id: str | None = None) -> None:
            Disconnects a specific connection from the pool.
        disconnect() -> None:
            Disconnects all connections in the pool.
    """

    def __init__(self, connection_class: type[ConnectionBase], *args: Any, **kwargs: Any) -> None:
        self._connection_args = args
        self._connection_kwargs = kwargs
        self._connection_class = connection_class

    @abstractmethod
    def get_connection(self, transaction_id: str | None = None) -> ConnectionBase:
        """Retrieves a connection from the pool.

        Args:
            transaction_id (str | None): The transaction ID for the connection.

        Returns:
            ConnectionBase: The connection instance.
        """
        ...

    @abstractmethod
    def disconnect_connection(self, transaction_id: str | None = None) -> None:
        """Disconnects a specific connection from the pool.

        Args:
            transaction_id (str | None): The transaction ID for the connection.
        """
        ...

    @abstractmethod
    def disconnect(self) -> None:
        """Disconnects all connections in the pool."""
        ...


class ConnectionManager(metaclass=Singleton):
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
