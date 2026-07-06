from unittest import mock

import psycopg
from psycopg import sql

from amsdal_glue_connections.sql.connections.postgres_connection import PostgresConnection


def _search_path_stmt(fake_conn: mock.Mock) -> sql.Composed:
    composed = [c.args[0] for c in fake_conn.execute.call_args_list if isinstance(c.args[0], sql.Composable)]
    assert composed, 'search_path was not set via psycopg SQL composition'
    stmt = composed[-1]
    assert isinstance(stmt, sql.Composed)
    return stmt


def test__connect_sets_search_path_via_identifier_composition(monkeypatch: object) -> None:
    """``SET search_path`` must be built with ``sql.Identifier`` composition, not an f-string."""
    fake_conn = mock.Mock()
    monkeypatch.setattr(psycopg, 'connect', mock.Mock(return_value=fake_conn))  # type: ignore[attr-defined]

    connection = PostgresConnection()
    connection.connect(dsn='postgresql://localhost/x', schema='amsdal_test_ns')

    stmt = _search_path_stmt(fake_conn)
    assert stmt.as_string(None) == 'SET search_path TO "amsdal_test_ns"'
    assert connection._schema == 'amsdal_test_ns'  # noqa: SLF001


def test__connect_escapes_malicious_schema(monkeypatch: object) -> None:
    """A schema containing SQL metacharacters stays inside a quoted identifier (no injection)."""
    fake_conn = mock.Mock()
    monkeypatch.setattr(psycopg, 'connect', mock.Mock(return_value=fake_conn))  # type: ignore[attr-defined]

    connection = PostgresConnection()
    connection.connect(dsn='postgresql://localhost/x', schema='evil"; DROP TABLE users; --')

    stmt = _search_path_stmt(fake_conn)
    assert stmt.as_string(None) == 'SET search_path TO "evil""; DROP TABLE users; --"'


def test__connect_without_schema_defaults_to_public(monkeypatch: object) -> None:
    fake_conn = mock.Mock()
    monkeypatch.setattr(psycopg, 'connect', mock.Mock(return_value=fake_conn))  # type: ignore[attr-defined]

    connection = PostgresConnection()
    connection.connect(dsn='postgresql://localhost/x')

    assert connection._schema == 'public'  # noqa: SLF001
    # No search_path statement should be issued when no schema is requested.
    assert not [c for c in fake_conn.execute.call_args_list if isinstance(c.args[0], sql.Composable)]
