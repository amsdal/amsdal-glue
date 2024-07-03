from abc import ABC
from abc import abstractmethod
from typing import Any

from amsdal_glue_core.common.enums import ConnectionAlias
from amsdal_glue_core.common.helpers.singleton import Singleton
from amsdal_glue_core.common.interfaces.connection import ConnectionBase


class ConnectionPoolBase(ABC):
    def __init__(self, connection_class: type[ConnectionBase], *args: Any, **kwargs: Any) -> None:
        self._connection_args = args
        self._connection_kwargs = kwargs
        self._connection_class = connection_class

    @abstractmethod
    def get_connection(self, transaction_id: str | None = None) -> ConnectionBase: ...

    @abstractmethod
    def disconnect(self) -> None: ...


class ConnectionManager(metaclass=Singleton):
    def __init__(self) -> None:
        self.connections: dict[str, ConnectionPoolBase] = {}

    def register_connection_pool(self, connection: ConnectionPoolBase, schema_name: str | None = None) -> None:
        self.connections[schema_name or ConnectionAlias.DEFAULT] = connection

    def has_multiple_models_connections(self, connection_alias: ConnectionAlias) -> bool:
        return connection_alias == ConnectionAlias.DEFAULT and len(self.connections) > 1

    def get_connection_pool(self, schema_name: str) -> ConnectionPoolBase:
        return self.connections.get(schema_name) or self.connections[ConnectionAlias.DEFAULT]

    def disconnect_all(self) -> None:
        for connection in self.connections.values():
            connection.disconnect()

        self.connections.clear()

    def __del__(self) -> None:
        self.disconnect_all()
