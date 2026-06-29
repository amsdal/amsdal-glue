"""Build helpers for golden-master SQL characterization tests.

Each helper turns a glue AST node into the exact (sql, params) the current
string-concatenation builders produce, for one dialect. The returned tuple is
asserted against a captured literal in the feature tests.
"""

from typing import Any

from amsdal_glue_connections.sql.connections.postgres_connection import get_pg_transform
from amsdal_glue_connections.sql.connections.postgres_connection.async_connection import AsyncPostgresConnection
from amsdal_glue_connections.sql.connections.postgres_connection.sync_connection import PostgresConnection
from amsdal_glue_connections.sql.connections.sqlite_connection import get_sqlite_transform
from amsdal_glue_connections.sql.connections.sqlite_connection.sync_connection import SqliteConnection
from amsdal_glue_connections.sql.sql_builders.command_builder import build_sql_data_command
from amsdal_glue_connections.sql.sql_builders.query_builder import build_sql_query


def pg(query: Any) -> tuple[str, list[Any]]:
    return build_sql_query(query=query, transform=get_pg_transform())


def lite(query: Any) -> tuple[str, list[Any]]:
    return build_sql_query(query=query, transform=get_sqlite_transform())


def pg_cmd(mutation: Any) -> tuple[str, list[Any]]:
    return build_sql_data_command(mutation=mutation, transform=get_pg_transform())


def lite_cmd(mutation: Any) -> tuple[str, list[Any]]:
    return build_sql_data_command(mutation=mutation, transform=get_sqlite_transform())


# DDL / lock / transaction SQL is built INLINE inside the connection and sent straight to
# execute() — Postgres does NOT route DDL through build_schema_mutation, and it quotes
# identifiers with double quotes ("users"). The true oracle is what reaches execute().
# Recording connections drive the real connection path with an execute() that records
# (sql, params) instead of hitting a DB. No live DB needed for build->execute paths.
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


def pg_ddl(mutation: Any) -> list[tuple[str, list[Any]]]:
    conn = _RecordingPG()
    conn._run_schema_mutation(mutation)  # noqa: SLF001
    return conn.captured


def lite_ddl(mutation: Any) -> list[tuple[str, list[Any]]]:
    conn = _RecordingSqlite()
    conn._run_schema_mutation(mutation)  # noqa: SLF001
    return conn.captured


class _RecordingAsyncPG(AsyncPostgresConnection):
    def __init__(self) -> None:
        super().__init__()
        self.captured: list[tuple[str, list[Any]]] = []

    async def execute(self, query: str, *args: Any) -> Any:  # type: ignore[override]
        self.captured.append((query, list(args)))
        return None


def pg_record() -> _RecordingPG:
    """Postgres connection whose execute() records (sql, params). For lock/transaction
    characterization (Task 14): call the connection method, then read .captured."""
    return _RecordingPG()


def lite_record() -> _RecordingSqlite:
    """SQLite recording connection — same usage as pg_record()."""
    return _RecordingSqlite()


def pg_async_record() -> _RecordingAsyncPG:
    """Async Postgres recording connection — execute() records (sql, params).
    Call an async connection method, then read .captured. No live DB needed."""
    return _RecordingAsyncPG()
