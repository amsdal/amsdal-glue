"""Build helpers for SQL generator tests.

Each helper turns a glue AST node into the exact (sql, params) the
SqlGenerator produces, for one dialect. The returned tuple is asserted
against a captured literal in the feature tests.
"""

from typing import Any

from amsdal_glue_connections._sql_core import SqlGenerator

from amsdal_glue_connections.sql.connections.postgres_connection.async_connection import AsyncPostgresConnection
from amsdal_glue_connections.sql.connections.postgres_connection.sync_connection import PostgresConnection
from amsdal_glue_connections.sql.connections.sqlite_connection.async_connection import AsyncSqliteConnection
from amsdal_glue_connections.sql.connections.sqlite_connection.sync_connection import SqliteConnection

_pg_gen = SqlGenerator('postgresql', param_style='format')
_lite_gen = SqlGenerator('sqlite', param_style='qmark')


def pg(query: Any) -> tuple[str, list[Any]]:
    return _pg_gen.compile_query(query)


def lite(query: Any) -> tuple[str, list[Any]]:
    return _lite_gen.compile_query(query)


def pg_cmd(mutation: Any) -> tuple[str, list[Any]]:
    return _pg_gen.compile_mutation(mutation)


def lite_cmd(mutation: Any) -> tuple[str, list[Any]]:
    return _lite_gen.compile_mutation(mutation)


def pg_ddl(mutation: Any) -> list[tuple[str, list[Any]]]:
    return _pg_gen.compile_schema_mutation(mutation)


def lite_ddl(mutation: Any) -> list[tuple[str, list[Any]]]:
    return _lite_gen.compile_schema_mutation(mutation)


# Recording connections drive the real connection execute() path — used by
# lock/transaction tests (test_lock.py). The connections
# have their own internal SqlGenerator, so no transform wiring is needed.
class _RecordingPG(PostgresConnection):
    def __init__(self) -> None:
        super().__init__()
        self.captured: list[tuple[str, list[Any]]] = []

    def execute(self, query: str, *args: Any) -> Any:
        self.captured.append((query, list(args)))
        return None


class _RecordingSqlite(SqliteConnection):
    def __init__(self) -> None:
        super().__init__()
        self.captured: list[tuple[str, list[Any]]] = []

    def execute(self, query: str, *args: Any) -> Any:
        self.captured.append((query, list(args)))
        return None


class _RecordingAsyncPG(AsyncPostgresConnection):
    def __init__(self) -> None:
        super().__init__()
        self.captured: list[tuple[str, list[Any]]] = []

    async def execute(self, query: str, *args: Any) -> Any:  # type: ignore[override]
        self.captured.append((query, list(args)))
        return None


class _RecordingAsyncSqlite(AsyncSqliteConnection):
    def __init__(self) -> None:
        super().__init__()
        self.captured: list[tuple[str, list[Any]]] = []

    async def execute(self, query: str, *args: Any) -> Any:  # type: ignore[override]
        self.captured.append((query, list(args)))
        return None


def pg_record() -> _RecordingPG:
    """Postgres connection whose execute() records (sql, params). For lock/transaction
    tests: call the connection method, then read .captured."""
    return _RecordingPG()


def lite_record() -> _RecordingSqlite:
    """SQLite recording connection — same usage as pg_record()."""
    return _RecordingSqlite()


def pg_async_record() -> _RecordingAsyncPG:
    """Async Postgres recording connection — execute() records (sql, params).
    Call an async connection method, then read .captured. No live DB needed."""
    return _RecordingAsyncPG()


def lite_async_record() -> _RecordingAsyncSqlite:
    """Async SQLite recording connection — execute() records (sql, params).
    Call an async connection method, then read .captured. No live DB needed."""
    return _RecordingAsyncSqlite()
