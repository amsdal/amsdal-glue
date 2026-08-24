"""The SQLite registry views are per-connection, so they must be created per connection.

They were re-issued on every ``query_schema`` call instead: a suite that introspects
often paid several ``CREATE TEMPORARY VIEW`` round trips per call for views that were
already there. The DDL is idempotent, so correctness never suffered - only speed.
"""

from pathlib import Path
from typing import Any

from amsdal_glue_core.common.data_models.query import QueryStatement
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.enums import Version

from amsdal_glue_connections.sql.connections.sqlite_connection.base import TABLE_REGISTRY
from amsdal_glue_connections.sql.connections.sqlite_connection.sync_connection import SqliteConnection


class _CountingSqliteConnection(SqliteConnection):
    """Counts the registry-view DDL statements this connection issues."""

    view_ddls: int = 0

    def execute(self, query: str, *args: Any) -> Any:
        if query.lstrip().upper().startswith('CREATE TEMPORARY VIEW'):
            self.view_ddls += 1
        return super().execute(query, *args)


def _query_schema(connection: SqliteConnection) -> None:
    connection.query_schema(
        QueryStatement(table=SchemaReference(name=TABLE_REGISTRY, version=Version.LATEST)),
    )


def test_registry_views_created_once_per_connection(tmp_path: Path) -> None:
    connection = _CountingSqliteConnection()
    connection.connect(tmp_path / 'db.sqlite3')

    try:
        _query_schema(connection)
        after_first = connection.view_ddls
        assert after_first > 0, 'the first introspection must create the registry views'

        for _ in range(5):
            _query_schema(connection)

        assert connection.view_ddls == after_first, 'registry views must not be re-created per query_schema'
    finally:
        connection.disconnect()


def test_registry_views_recreated_after_reconnect(tmp_path: Path) -> None:
    """TEMPORARY views die with the connection, so a reconnect must recreate them."""
    db_path = tmp_path / 'db.sqlite3'
    connection = _CountingSqliteConnection()

    connection.connect(db_path)
    _query_schema(connection)
    after_first = connection.view_ddls
    connection.disconnect()

    connection.connect(db_path)
    try:
        _query_schema(connection)
        assert connection.view_ddls == after_first * 2, 'a reconnect must recreate the per-connection views'
        # And the views actually work after the reconnect.
        _query_schema(connection)
    finally:
        connection.disconnect()
