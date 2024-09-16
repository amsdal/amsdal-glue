from collections.abc import Generator
from unittest import mock

import pytest

from amsdal_glue_connections.sql.connections.postgres_connection import PostgresConnection


class MockPostgresConnection(PostgresConnection):
    def __init__(self):
        self.execute_mock = mock.Mock()
        self.cursor_mock = mock.Mock()
        self.cursor_mock.execute = self.execute_mock
        self._connection = mock.Mock()
        self._connection.cursor.return_value = self.cursor_mock
        self._connection.execute = self.cursor_mock.execute

    @property
    def connection(self) -> mock.Mock:
        return self._connection  # type: ignore[return-value]

    def set_cursor_mock(self, cursor_mock: mock.Mock) -> None:
        self.cursor_mock = cursor_mock
        self._connection.cursor.return_value = self.cursor_mock  # type: ignore[union-attr]
        self._connection.execute.return_value = self.cursor_mock  # type: ignore[union-attr]


@pytest.fixture(scope='function')
def database_connection() -> Generator[PostgresConnection, None, None]:
    connection = MockPostgresConnection()

    yield connection
