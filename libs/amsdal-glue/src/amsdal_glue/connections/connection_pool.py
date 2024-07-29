import contextlib
from datetime import datetime
from datetime import timedelta
from datetime import timezone
from typing import Any

from amsdal_glue_core.common.interfaces.connection import ConnectionBase
from amsdal_glue_core.common.services.managers.connection import ConnectionPoolBase


class DefaultConnectionPool(ConnectionPoolBase):
    """
    DefaultConnectionPool manages a pool of connections, ensuring that connections are reused and not exceeded.
    It extends the ConnectionPoolBase class.

    Attributes:
        connections (dict[str | None, tuple[ConnectionBase, datetime]]): A dictionary of connections with
                                                                         their last used time.
        _max_connections (int): The maximum number of connections allowed.
        _expiration_time (int): The time in seconds after which a connection is considered expired.
    """

    def __init__(
        self,
        connection_class: type[ConnectionBase],
        *args: Any,
        max_connections: int = 10,
        expiration_time: int = 60,
        **kwargs: Any,
    ) -> None:
        """
        Initializes the DefaultConnectionPool with the given parameters.

        Args:
            connection_class (type[ConnectionBase]): The class of the connection to be used.
            max_connections (int): The maximum number of connections allowed.
            expiration_time (int): The time in seconds after which a connection is considered expired.
            *args (Any): Additional positional arguments for the connection class.
            **kwargs (Any): Additional keyword arguments for the connection class.
        """
        super().__init__(connection_class, *args, **kwargs)
        self.connections: dict[str | None, tuple[ConnectionBase, datetime]] = {}
        self._max_connections = max_connections
        self._expiration_time = expiration_time

    @staticmethod
    def _now() -> datetime:
        """
        Returns the current datetime in UTC.

        Returns:
            datetime: The current datetime in UTC.
        """
        return datetime.now(tz=timezone.utc)

    def _get_available_connection(self) -> ConnectionBase:
        """
        Retrieves an available connection from the pool or creates a new one if none are available.

        Returns:
            ConnectionBase: An available connection.

        Raises:
            RuntimeError: If the maximum number of connections is reached.
        """
        for transaction_id, (connection, last_used) in list(self.connections.items()):
            if self._now() - last_used > timedelta(seconds=self._expiration_time):
                with contextlib.suppress(Exception):
                    connection.rollback_transaction(transaction_id)

                self.connections.pop(transaction_id)

                return connection

        if len(self.connections) >= self._max_connections:
            msg = 'Max connections reached'
            raise RuntimeError(msg)

        connection = self._connection_class()
        connection.connect(*self._connection_args, **self._connection_kwargs)

        return connection

    def get_connection(self, transaction_id: str | None = None) -> ConnectionBase:
        """
        Retrieves a connection for the given transaction ID or creates a new one if none are available.

        Args:
            transaction_id (str | None): The ID of the transaction.

        Returns:
            ConnectionBase: A connection for the given transaction ID.
        """
        if transaction_id in self.connections:
            connection, _ = self.connections[transaction_id]

            self.connections[transaction_id] = (connection, self._now())

            return connection

        connection = self._get_available_connection()

        self.connections[transaction_id] = (connection, self._now())

        return connection

    def disconnect_connection(self, transaction_id: str | None = None) -> None:
        """
        Disconnects the connection for the given transaction ID.

        Args:
            transaction_id (str | None): The ID of the transaction.
        """
        if transaction_id in self.connections:
            connection, _ = self.connections.pop(transaction_id)

            if connection.is_connected:
                connection.disconnect()

    def disconnect(self) -> None:
        """
        Disconnects all connections in the pool.
        """
        for connection, _ in self.connections.values():
            if connection.is_connected:
                connection.disconnect()

        self.connections.clear()
