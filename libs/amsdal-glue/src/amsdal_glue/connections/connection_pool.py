import asyncio
import contextlib
import logging
import threading
from datetime import datetime
from datetime import timedelta
from datetime import timezone
from time import monotonic
from typing import Any

from amsdal_glue_core.common.interfaces.connection import AsyncConnectionBase
from amsdal_glue_core.common.interfaces.connection import ConnectionBase
from amsdal_glue_core.common.interfaces.connection_pool import AsyncConnectionPoolBase
from amsdal_glue_core.common.interfaces.connection_pool import ConnectionPoolBase

logger = logging.getLogger(__name__)

DEFAULT_MAX_CONNECTIONS = 10
DEFAULT_EXPIRATION_TIME = 60
DEFAULT_TRANSACTION_EXPIRATION_TIME = 900
DEFAULT_ACQUISITION_TIMEOUT = 0.0
# Joining a transaction that is still opening its connection is not a capacity problem, so it is
# waited out regardless of ``acquisition_timeout``.
CREATION_WAIT_TIMEOUT = 30.0

MAX_CONNECTIONS_REACHED_MSG = 'Max connections reached'


class DefaultConnectionPool(ConnectionPoolBase):
    """
    DefaultConnectionPool manages a pool of connections, ensuring that connections are reused and not exceeded.
    It extends the ConnectionPoolBase class.

    A connection is bound to the transaction it was acquired for and returns to the pool only when that
    transaction ends (see ``disconnect_connection``). A connection that is never released - a crashed or
    cancelled request, for example - is reclaimed once it stays untouched for
    ``transaction_expiration_time`` seconds, which is logged as a warning since it always means a leak
    somewhere upstream.

    Attributes:
        connections (dict[str | None, tuple[ConnectionBase, datetime]]): A dictionary of connections with
                                                                         their last used time.
        _idle_connections (list[tuple[ConnectionBase, datetime]]): Released connections kept open for reuse.
        _max_connections (int): The maximum number of connections allowed.
        _expiration_time (float): The time in seconds after which an idle connection is closed.
        _transaction_expiration_time (float): The time in seconds after which a transaction-bound connection
                                              is considered leaked and is reclaimed.
        _acquisition_timeout (float): The time in seconds to wait for a free slot before giving up.

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
    def _all_connections(self) -> list[ConnectionBase]:
        """Every connection the pool owns: handed out plus idle and waiting for reuse."""
        return [connection for connection, _ in self.connections.values()] + [
            connection for connection, _ in self._idle_connections
        ]

    @property
    def is_connected(self) -> bool:
        return all(connection.is_connected for connection in self._all_connections)

    @property
    def is_alive(self) -> bool:
        return all(connection.is_alive for connection in self._all_connections)

    def __init__(
        self,
        connection_class: type[ConnectionBase],
        *args: Any,
        max_connections: int = DEFAULT_MAX_CONNECTIONS,
        expiration_time: float = DEFAULT_EXPIRATION_TIME,
        transaction_expiration_time: float = DEFAULT_TRANSACTION_EXPIRATION_TIME,
        acquisition_timeout: float = DEFAULT_ACQUISITION_TIMEOUT,
        reuse_connections: bool = True,
        **kwargs: Any,
    ) -> None:
        """
        Initializes the DefaultConnectionPool with the given parameters.

        Args:
            connection_class (type[ConnectionBase]): The class of the connection to be used.
            max_connections (int): The maximum number of connections allowed.
            expiration_time (float): The time in seconds after which an IDLE connection is closed
                instead of being handed out again.
            transaction_expiration_time (float): The time in seconds after which a transaction-bound
                connection is considered leaked and can be reclaimed.
            acquisition_timeout (float): The time in seconds to wait for a free slot before raising.
                Zero - the default - fails as soon as the pool is full.
            reuse_connections (bool): Whether a released connection is kept open for the next
                caller. Disable it when a release must close the underlying handle.
            *args (Any): Additional positional arguments for the connection class.
            **kwargs (Any): Additional keyword arguments for the connection class.
        """
        super().__init__(connection_class, *args, **kwargs)
        self.connections: dict[str | None, tuple[ConnectionBase, datetime]] = {}
        self._idle_connections: list[tuple[ConnectionBase, datetime]] = []
        self._max_connections = max_connections
        self._expiration_time = expiration_time
        self._transaction_expiration_time = transaction_expiration_time
        self._acquisition_timeout = acquisition_timeout
        self._reuse_connections = reuse_connections
        self._condition = threading.Condition()
        # Slots promised to callers that are still opening their connection: not in ``connections``
        # yet, but they must count against ``max_connections`` all the same.
        self._reserved = 0
        # Transactions whose connection is being opened right now, so that a concurrent caller of the
        # same transaction waits for that one connection instead of opening a second one.
        self._creating: set[str | None] = set()

    @staticmethod
    def _now() -> datetime:
        """
        Returns the current datetime in UTC.

        Returns:
            datetime: The current datetime in UTC.
        """
        return datetime.now(tz=timezone.utc)

    def _owned(self) -> int:
        """Number of connections the pool has committed to. Must be called while holding the lock."""
        return len(self.connections) + len(self._idle_connections) + self._reserved

    def _take_idle(self, stale: list[ConnectionBase]) -> ConnectionBase | None:
        """
        Takes a reusable idle connection, setting the expired ones aside for the caller to close.

        Idle connections are released by `disconnect_connection` at the end of a transaction, so they
        carry no open transaction and can be handed straight back out. Reusing one skips a physical
        connect and whatever per-connection setup the driver does on top of it - on the historical
        connections that includes a full schema introspection.

        Must be called while holding the lock.
        """
        while self._idle_connections:
            connection, released_at = self._idle_connections.pop()

            if self._now() - released_at > timedelta(seconds=self._expiration_time):
                stale.append(connection)

                continue

            return connection

        return None

    def _take_leaked(self) -> tuple[str | None, ConnectionBase] | None:
        """
        Takes the connection of a transaction that was never released. Must be called while holding the lock.

        This is a safety net, not a scheduling mechanism: a transaction that is merely slow keeps its
        connection, so `transaction_expiration_time` has to stay well above the slowest transaction.
        """
        for transaction_id, (connection, last_used) in list(self.connections.items()):
            if self._now() - last_used > timedelta(seconds=self._transaction_expiration_time):
                del self.connections[transaction_id]

                return transaction_id, connection

        return None

    def _recycle(self, transaction_id: str | None, connection: ConnectionBase) -> ConnectionBase:
        """Rolls back whatever the previous owner left behind, replacing the connection if that fails."""
        logger.warning(
            'Reclaiming the connection of transaction %s: it was not released within %s seconds. '
            'This means the transaction was never committed or rolled back.',
            transaction_id,
            self._transaction_expiration_time,
        )

        try:
            connection.rollback_transaction(transaction_id)
        except Exception:  # noqa: BLE001
            logger.warning('Discarding a connection that failed to roll back on reclaim.', exc_info=True)
            self._discard(connection)

            return self._create()

        return connection

    def _create(self) -> ConnectionBase:
        connection = self._connection_class()
        connection.connect(*self._connection_args, **self._connection_kwargs)

        return connection

    def _discard(self, connection: ConnectionBase) -> None:
        """Closes a connection the pool is not going to track any more."""
        with contextlib.suppress(Exception):
            if connection.is_connected:
                connection.disconnect()

    def _wait_for_slot(self, deadline: float) -> bool:
        """Waits for another caller to free a slot. Must be called while holding the lock."""
        remaining = deadline - monotonic()

        return remaining > 0 and self._condition.wait(remaining)

    def _finish_creation(self, transaction_id: str | None, connection: ConnectionBase | None) -> None:
        """Publishes a freshly opened connection, or gives its slot back when the open failed."""
        with self._condition:
            self._reserved -= 1
            self._creating.discard(transaction_id)

            if connection is not None:
                self.connections[transaction_id] = (connection, self._now())

            self._condition.notify_all()

    def _max_connections_error(self) -> str:
        return (
            f'{MAX_CONNECTIONS_REACHED_MSG}: no connection became available within '
            f'{self._acquisition_timeout} seconds (limit: {self._max_connections})'
        )

    def get_connection(self, transaction_id: str | None = None) -> ConnectionBase:
        """
        Retrieves a connection for the given transaction ID or creates a new one if none are available.

        Args:
            transaction_id (str | None): The ID of the transaction.

        Returns:
            ConnectionBase: A connection for the given transaction ID.

        Raises:
            RuntimeError: If no connection became available within `acquisition_timeout` seconds.
        """
        deadline = monotonic() + self._acquisition_timeout
        stale: list[ConnectionBase] = []

        try:
            while True:
                with self._condition:
                    existing = self.connections.get(transaction_id)

                    if existing is not None:
                        connection, _ = existing
                        self.connections[transaction_id] = (connection, self._now())

                        return connection

                    if transaction_id in self._creating:
                        creation_deadline = max(deadline, monotonic() + CREATION_WAIT_TIMEOUT)

                        if not self._wait_for_slot(creation_deadline):
                            raise RuntimeError(self._max_connections_error())

                        continue

                    idle = self._take_idle(stale)

                    if idle is not None:
                        self.connections[transaction_id] = (idle, self._now())

                        return idle

                    leaked = self._take_leaked()

                    if leaked is None and self._owned() >= self._max_connections:
                        if not self._wait_for_slot(deadline):
                            raise RuntimeError(self._max_connections_error())

                        continue

                    self._reserved += 1
                    self._creating.add(transaction_id)

                try:
                    connection = self._recycle(*leaked) if leaked else self._create()
                except BaseException:
                    self._finish_creation(transaction_id, None)
                    raise

                self._finish_creation(transaction_id, connection)

                return connection
        finally:
            for connection in stale:
                self._discard(connection)

    def disconnect_connection(self, transaction_id: str | None = None) -> None:
        """
        Releases the connection for the given transaction ID.

        The connection is kept open and parked for the next caller unless the pool was built
        with ``reuse_connections=False``. Either way it is closed by ``disconnect()``, and an
        idle connection that goes stale is closed rather than handed out again.

        Args:
            transaction_id (str | None): The ID of the transaction.
        """
        with self._condition:
            entry = self.connections.pop(transaction_id, None)

            if entry is not None and self._reuse_connections and entry[0].is_connected:
                self._idle_connections.append((entry[0], self._now()))
                entry = None

            self._condition.notify_all()

        if entry is None:
            return

        connection, _ = entry

        if connection.is_connected:
            connection.disconnect()

    def disconnect(self) -> None:
        """
        Disconnects all connections in the pool, idle ones included.
        """
        with self._condition:
            connections = self._all_connections
            self.connections.clear()
            self._idle_connections.clear()
            self._condition.notify_all()

        for connection in connections:
            if connection.is_connected:
                connection.disconnect()


class DefaultAsyncConnectionPool(AsyncConnectionPoolBase):
    """Async counterpart of [DefaultConnectionPool][amsdal_glue.DefaultConnectionPool].

    See [DefaultConnectionPool][amsdal_glue.DefaultConnectionPool] for the pooling rules: a released
    connection is parked for reuse, the capacity is enforced across concurrently awaiting callers, and a
    transaction-bound connection is only reclaimed once it looks leaked.
    """

    @property
    def _all_connections(self) -> list[AsyncConnectionBase]:
        """Every connection the pool owns: handed out plus idle and waiting for reuse."""
        return [connection for connection, _ in self.connections.values()] + [
            connection for connection, _ in self._idle_connections
        ]

    @property
    async def is_connected(self) -> bool:
        for connection in self._all_connections:
            if not await connection.is_connected:
                return False
        return True

    @property
    async def is_alive(self) -> bool:
        for connection in self._all_connections:
            if not await connection.is_alive:
                return False
        return True

    def __init__(
        self,
        connection_class: type[AsyncConnectionBase],
        *args: Any,
        max_connections: int = DEFAULT_MAX_CONNECTIONS,
        expiration_time: float = DEFAULT_EXPIRATION_TIME,
        transaction_expiration_time: float = DEFAULT_TRANSACTION_EXPIRATION_TIME,
        acquisition_timeout: float = DEFAULT_ACQUISITION_TIMEOUT,
        reuse_connections: bool = True,
        **kwargs: Any,
    ) -> None:
        """
        Initializes the DefaultAsyncConnectionPool with the given parameters.

        Args:
            connection_class (type[AsyncConnectionBase]): The class of the connection to be used.
            max_connections (int): The maximum number of connections allowed.
            expiration_time (float): The time in seconds after which an IDLE connection is closed
                instead of being handed out again.
            transaction_expiration_time (float): The time in seconds after which a transaction-bound
                connection is considered leaked and can be reclaimed.
            acquisition_timeout (float): The time in seconds to wait for a free slot before raising.
                Zero - the default - fails as soon as the pool is full.
            reuse_connections (bool): Whether a released connection is kept open for the next
                caller. Disable it when a release must close the underlying handle.
            *args (Any): Additional positional arguments for the connection class.
            **kwargs (Any): Additional keyword arguments for the connection class.
        """
        super().__init__(connection_class, *args, **kwargs)
        self.connections: dict[str | None, tuple[AsyncConnectionBase, datetime]] = {}
        self._idle_connections: list[tuple[AsyncConnectionBase, datetime]] = []
        self._max_connections = max_connections
        self._expiration_time = expiration_time
        self._transaction_expiration_time = transaction_expiration_time
        self._acquisition_timeout = acquisition_timeout
        self._reuse_connections = reuse_connections
        self._condition: asyncio.Condition | None = None
        self._condition_loop: asyncio.AbstractEventLoop | None = None
        self._reserved = 0
        self._creating: set[str | None] = set()

    def _get_condition(self) -> asyncio.Condition:
        """Returns the condition bound to the running loop, re-creating it if the loop changed."""
        loop = asyncio.get_running_loop()

        if self._condition is None or self._condition_loop is not loop:
            self._condition = asyncio.Condition()
            self._condition_loop = loop

        return self._condition

    @staticmethod
    def _now() -> datetime:
        """
        Returns the current datetime in UTC.

        Returns:
            datetime: The current datetime in UTC.
        """
        return datetime.now(tz=timezone.utc)

    def _owned(self) -> int:
        """Number of connections the pool has committed to. Must be called while holding the condition."""
        return len(self.connections) + len(self._idle_connections) + self._reserved

    def _take_idle(self, stale: list[AsyncConnectionBase]) -> AsyncConnectionBase | None:
        """
        Takes a reusable idle connection, setting the expired ones aside for the caller to close.

        See the sync pool for why a released connection is safe to hand straight back out.
        Must be called while holding the condition.
        """
        while self._idle_connections:
            connection, released_at = self._idle_connections.pop()

            if self._now() - released_at > timedelta(seconds=self._expiration_time):
                stale.append(connection)

                continue

            return connection

        return None

    def _take_leaked(self) -> tuple[str | None, AsyncConnectionBase] | None:
        """
        Takes the connection of a transaction that was never released. Must be called while holding the condition.

        This is a safety net, not a scheduling mechanism: a transaction that is merely slow keeps its
        connection, so `transaction_expiration_time` has to stay well above the slowest transaction.
        """
        for transaction_id, (connection, last_used) in list(self.connections.items()):
            if self._now() - last_used > timedelta(seconds=self._transaction_expiration_time):
                del self.connections[transaction_id]

                return transaction_id, connection

        return None

    async def _recycle(self, transaction_id: str | None, connection: AsyncConnectionBase) -> AsyncConnectionBase:
        """Rolls back whatever the previous owner left behind, replacing the connection if that fails."""
        logger.warning(
            'Reclaiming the connection of transaction %s: it was not released within %s seconds. '
            'This means the transaction was never committed or rolled back.',
            transaction_id,
            self._transaction_expiration_time,
        )

        try:
            await connection.rollback_transaction(transaction_id)
        except Exception:  # noqa: BLE001
            logger.warning('Discarding a connection that failed to roll back on reclaim.', exc_info=True)
            await self._discard(connection)

            return await self._create()

        return connection

    async def _create(self) -> AsyncConnectionBase:
        connection = self._connection_class()
        await connection.connect(*self._connection_args, **self._connection_kwargs)

        return connection

    async def _discard(self, connection: AsyncConnectionBase) -> None:
        """Closes a connection the pool is not going to track any more."""
        with contextlib.suppress(Exception):
            if await connection.is_connected:
                await connection.disconnect()

    async def _wait_for_slot(self, condition: asyncio.Condition, deadline: float) -> bool:
        """Waits for another caller to free a slot. Must be called while holding the condition."""
        remaining = deadline - asyncio.get_running_loop().time()

        if remaining <= 0:
            return False

        try:
            await asyncio.wait_for(condition.wait(), remaining)
        except (TimeoutError, asyncio.TimeoutError):
            return False

        return True

    async def _finish_creation(self, transaction_id: str | None, connection: AsyncConnectionBase | None) -> None:
        """Publishes a freshly opened connection, or gives its slot back when the open failed."""
        condition = self._get_condition()

        async with condition:
            self._reserved -= 1
            self._creating.discard(transaction_id)

            if connection is not None:
                self.connections[transaction_id] = (connection, self._now())

            condition.notify_all()

    def _max_connections_error(self) -> str:
        return (
            f'{MAX_CONNECTIONS_REACHED_MSG}: no connection became available within '
            f'{self._acquisition_timeout} seconds (limit: {self._max_connections})'
        )

    async def get_connection(self, transaction_id: str | None = None) -> AsyncConnectionBase:
        """
        Retrieves a connection for the given transaction ID or creates a new one if none are available.

        Args:
            transaction_id (str | None): The ID of the transaction.

        Returns:
            AsyncConnectionBase: A connection for the given transaction ID.

        Raises:
            RuntimeError: If no connection became available within `acquisition_timeout` seconds.
        """
        condition = self._get_condition()
        deadline = asyncio.get_running_loop().time() + self._acquisition_timeout
        stale: list[AsyncConnectionBase] = []

        try:
            while True:
                async with condition:
                    existing = self.connections.get(transaction_id)

                    if existing is not None:
                        connection, _ = existing
                        self.connections[transaction_id] = (connection, self._now())

                        return connection

                    if transaction_id in self._creating:
                        creation_deadline = max(
                            deadline,
                            asyncio.get_running_loop().time() + CREATION_WAIT_TIMEOUT,
                        )

                        if not await self._wait_for_slot(condition, creation_deadline):
                            raise RuntimeError(self._max_connections_error())

                        continue

                    idle = self._take_idle(stale)

                    if idle is not None:
                        self.connections[transaction_id] = (idle, self._now())

                        return idle

                    leaked = self._take_leaked()

                    if leaked is None and self._owned() >= self._max_connections:
                        if not await self._wait_for_slot(condition, deadline):
                            raise RuntimeError(self._max_connections_error())

                        continue

                    self._reserved += 1
                    self._creating.add(transaction_id)

                try:
                    connection = await self._recycle(*leaked) if leaked else await self._create()
                except BaseException:
                    await self._finish_creation(transaction_id, None)
                    raise

                await self._finish_creation(transaction_id, connection)

                return connection
        finally:
            for connection in stale:
                await self._discard(connection)

    async def disconnect_connection(self, transaction_id: str | None = None) -> None:
        """
        Releases the connection for the given transaction ID.

        The connection is kept open and parked for the next caller unless the pool was built
        with ``reuse_connections=False``. Either way it is closed by ``disconnect()``, and an
        idle connection that goes stale is closed rather than handed out again.

        Args:
            transaction_id (str | None): The ID of the transaction.
        """
        condition = self._get_condition()

        async with condition:
            entry = self.connections.pop(transaction_id, None)

            if entry is not None and self._reuse_connections and await entry[0].is_connected:
                self._idle_connections.append((entry[0], self._now()))
                entry = None

            condition.notify_all()

        if entry is None:
            return

        connection, _ = entry

        if await connection.is_connected:
            await connection.disconnect()

    async def disconnect(self) -> None:
        """
        Disconnects all connections in the pool, idle ones included.
        """
        condition = self._get_condition()

        async with condition:
            connections = self._all_connections
            self.connections.clear()
            self._idle_connections.clear()
            condition.notify_all()

        for connection in connections:
            if await connection.is_connected:
                await connection.disconnect()
