import contextlib
from datetime import datetime
from datetime import timedelta
from datetime import timezone
from typing import Any

from amsdal_glue_core.common.interfaces.connection import AsyncConnectionBase
from amsdal_glue_core.common.interfaces.connection import ConnectionBase
from amsdal_glue_core.common.interfaces.connection_pool import AsyncConnectionPoolBase
from amsdal_glue_core.common.interfaces.connection_pool import ConnectionPoolBase


class DefaultConnectionPool(ConnectionPoolBase):
    """
    DefaultConnectionPool manages a pool of connections, ensuring that connections are reused and not exceeded.
    It extends the ConnectionPoolBase class.

    Attributes:
        connections (dict[str | None, tuple[ConnectionBase, datetime]]): A dictionary of connections with
                                                                         their last used time.
        _max_connections (int): The maximum number of connections allowed.
        _expiration_time (int): The time in seconds after which a connection is considered expired.

    Example:
        This example demonstrates how to create SQLite-base connection pool with a maximum of 10 connections,
        supported by [SqliteConnection][amsdal_glue.SqliteConnection] connection:

        ```python
        from amsdal_glue import DefaultConnectionPool
        from amsdal_glue import SqliteConnection

        sqlite_connection_pool = DefaultConnectionPool(
            SqliteConnection,
            db_path='my_db.sqlite',
            max_connections=10,
        )
        ```

        Here is an example of how to create a Postgres-based connection
        with some parameters supported by [PostgresConnection][amsdal_glue.PostgresConnection] connection:

        ```python
        from amsdal_glue import DefaultConnectionPool
        from amsdal_glue import PostgresConnection

        pg_connection_pool = DefaultConnectionPool(
            PostgresConnection,
            dsn='postgres://db_user:db_password@localhost:5433/db_name',
            schema='public',
            timezone='UTC',
        )
        ```

    """

    @property
    def is_connected(self) -> bool:
        return all(connection.is_connected for connection, _ in self.connections.values())

    @property
    def is_alive(self) -> bool:
        return all(connection.is_alive for connection, _ in self.connections.values())

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


class DefaultAsyncConnectionPool(AsyncConnectionPoolBase):
    @property
    async def is_connected(self) -> bool:
        for connection, _ in self.connections.values():
            if not await connection.is_connected:
                return False
        return True

    @property
    async def is_alive(self) -> bool:
        for connection, _ in self.connections.values():
            if not await connection.is_alive:
                return False
        return True

    def __init__(
        self,
        connection_class: type[AsyncConnectionBase],
        *args: Any,
        max_connections: int = 10,
        expiration_time: int = 60,
        **kwargs: Any,
    ) -> None:
        """
        Initializes the DefaultConnectionPool with the given parameters.

        Args:
            connection_class (type[AsyncConnectionBase]): The class of the connection to be used.
            max_connections (int): The maximum number of connections allowed.
            expiration_time (int): The time in seconds after which a connection is considered expired.
            *args (Any): Additional positional arguments for the connection class.
            **kwargs (Any): Additional keyword arguments for the connection class.
        """
        super().__init__(connection_class, *args, **kwargs)
        self.connections: dict[str | None, tuple[AsyncConnectionBase, datetime]] = {}
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

    async def _get_available_connection(self) -> AsyncConnectionBase:
        """
        Retrieves an available connection from the pool or creates a new one if none are available.

        Returns:
            AsyncConnectionBase: An available connection.

        Raises:
            RuntimeError: If the maximum number of connections is reached.
        """
        for transaction_id, (connection, last_used) in list(self.connections.items()):
            if self._now() - last_used > timedelta(seconds=self._expiration_time):
                with contextlib.suppress(Exception):
                    await connection.rollback_transaction(transaction_id)

                self.connections.pop(transaction_id)

                return connection

        if len(self.connections) >= self._max_connections:
            msg = 'Max connections reached'
            raise RuntimeError(msg)

        connection = self._connection_class()
        await connection.connect(*self._connection_args, **self._connection_kwargs)

        return connection

    async def get_connection(self, transaction_id: str | None = None) -> AsyncConnectionBase:
        """
        Retrieves a connection for the given transaction ID or creates a new one if none are available.

        Args:
            transaction_id (str | None): The ID of the transaction.

        Returns:
            AsyncConnectionBase: A connection for the given transaction ID.
        """
        if transaction_id in self.connections:
            connection, _ = self.connections[transaction_id]

            self.connections[transaction_id] = (connection, self._now())

            return connection

        connection = await self._get_available_connection()

        self.connections[transaction_id] = (connection, self._now())

        return connection

    async def disconnect_connection(self, transaction_id: str | None = None) -> None:
        """
        Disconnects the connection for the given transaction ID.

        Args:
            transaction_id (str | None): The ID of the transaction.
        """
        if transaction_id in self.connections:
            connection, _ = self.connections.pop(transaction_id)

            if await connection.is_connected:
                await connection.disconnect()

    async def disconnect(self) -> None:
        """
        Disconnects all connections in the pool.
        """
        for connection, _ in self.connections.values():
            if await connection.is_connected:
                await connection.disconnect()

        self.connections.clear()
