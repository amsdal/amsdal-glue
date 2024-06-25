import contextlib
from datetime import datetime
from datetime import timedelta
from datetime import timezone
from typing import Any

from amsdal_glue_core.common.interfaces.connection import ConnectionBase
from amsdal_glue_core.common.services.managers.connection import ConnectionPoolBase


class DefaultConnectionPool(ConnectionPoolBase):
    def __init__(
        self,
        connection_class: type[ConnectionBase],
        *args: Any,
        max_connections: int = 10,
        expiration_time: int = 60,
        **kwargs: Any,
    ) -> None:
        super().__init__(connection_class, *args, **kwargs)
        self.connections: dict[str | None, tuple[ConnectionBase, datetime]] = {}
        self._max_connections = max_connections
        self._expiration_time = expiration_time

    def _now(self) -> datetime:
        return datetime.now(tz=timezone.utc)

    def _get_available_connection(self) -> ConnectionBase:
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
        if transaction_id in self.connections:
            connection, _ = self.connections[transaction_id]

            self.connections[transaction_id] = (connection, self._now())

            return connection

        connection = self._get_available_connection()

        self.connections[transaction_id] = (connection, self._now())

        return connection

    def disconnect(self) -> None:
        for connection, _ in self.connections.values():
            if connection.is_connected:
                connection.disconnect()

        self.connections.clear()
