from abc import ABC
from abc import abstractmethod
from typing import Any

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

    @property
    @abstractmethod
    def is_connected(self) -> bool:
        """bool: Indicates if the pool is connected."""
        ...

    @property
    @abstractmethod
    def is_alive(self) -> bool:
        """bool: Indicates if the pool is alive."""
        ...

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
