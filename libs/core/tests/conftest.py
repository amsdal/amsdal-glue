from typing import Any
from unittest import mock

import pytest

from amsdal_glue_core.common.enums import ConnectionAlias
from amsdal_glue_core.common.interfaces.connection import AsyncConnectionBase
from amsdal_glue_core.common.interfaces.connection import ConnectionBase
from amsdal_glue_core.common.interfaces.connection_manager import AsyncConnectionManager
from amsdal_glue_core.common.interfaces.connection_manager import ConnectionManager
from amsdal_glue_core.common.interfaces.connection_pool import AsyncConnectionPoolBase
from amsdal_glue_core.common.interfaces.connection_pool import ConnectionPoolBase

DEFAULT_SCHEMA_NAME = 'default_schema'


class MockConnectionPool(ConnectionPoolBase):
    def __init__(self, connection_class: type[ConnectionBase], *args: Any, **kwargs: Any) -> None:  # noqa: ARG002
        self._connection_args = args
        self._connection_kwargs = kwargs
        self.connection = mock.Mock()

    @property
    def is_connected(self) -> bool:
        return True

    @property
    def is_alive(self) -> bool:
        return True

    def get_connection(self, transaction_id: str | None = None) -> ConnectionBase:  # noqa: ARG002
        return self.connection

    def disconnect_connection(self, transaction_id: str | None = None) -> None:
        pass

    def disconnect(self) -> None:
        pass


class MockConnectionManager(ConnectionManager):
    def __init__(self):
        self.connection_pool = MockConnectionPool(ConnectionBase)  # type: ignore[type-abstract]

    def register_connection_pool(self, connection: ConnectionPoolBase, schema_name: str | None = None) -> None:
        pass

    def has_multiple_models_connections(self, connection_alias: ConnectionAlias) -> bool:  # noqa: ARG002
        return False

    def get_connection_pool(self, schema_name: str) -> ConnectionPoolBase:  # noqa: ARG002
        return self.connection_pool

    def disconnect_all(self) -> None:
        pass

    def __call__(self) -> ConnectionManager:
        return self


class MockAsyncConnectionPool(AsyncConnectionPoolBase):
    def __init__(self, connection_class: type[AsyncConnectionBase], *args: Any, **kwargs: Any) -> None:  # noqa: ARG002
        self._connection_args = args
        self._connection_kwargs = kwargs
        self.connection = mock.AsyncMock()

    @property
    async def is_connected(self) -> bool:
        return True

    @property
    async def is_alive(self) -> bool:
        return True

    async def get_connection(self, transaction_id: str | None = None) -> AsyncConnectionBase:  # noqa: ARG002
        return self.connection

    async def disconnect_connection(self, transaction_id: str | None = None) -> None:
        pass

    async def disconnect(self) -> None:
        pass


class MockAsyncConnectionManager(AsyncConnectionManager):
    def __init__(self):
        self.connection_pool = MockAsyncConnectionPool(AsyncConnectionBase)  # type: ignore[type-abstract]

    def register_connection_pool(self, connection: AsyncConnectionPoolBase, schema_name: str | None = None) -> None:
        pass

    def has_multiple_models_connections(self, connection_alias: ConnectionAlias) -> bool:  # noqa: ARG002
        return False

    def get_connection_pool(self, schema_name: str) -> AsyncConnectionPoolBase:  # noqa: ARG002
        return self.connection_pool

    async def disconnect_all(self) -> None:
        pass

    def __call__(self) -> AsyncConnectionManager:
        return self


@pytest.fixture
def mock_connection_manager() -> MockConnectionManager:
    return MockConnectionManager()


@pytest.fixture
def mock_async_connection_manager() -> MockAsyncConnectionManager:
    return MockAsyncConnectionManager()
