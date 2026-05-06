"""Regression tests for UNIQUE-constraint translation in the AsyncSQLite connection.

The execute() method must translate ``aiosqlite.IntegrityError`` raised on a
UNIQUE or PRIMARY-KEY collision into ``UniqueViolationError``. All other
``aiosqlite.Error`` subclasses must continue to surface as ``ConnectionError``.
"""

import pytest
from amsdal_glue_core.common.exceptions import AmsdalGlueError
from amsdal_glue_core.common.exceptions import UniqueViolationError

from amsdal_glue_connections.sql.connections.sqlite_connection import AsyncSqliteConnection


async def _create_table_with_unique_email(connection: AsyncSqliteConnection) -> None:
    await connection.execute('CREATE TABLE users (  id INTEGER PRIMARY KEY,  email VARCHAR(100) UNIQUE)')


async def test_unique_violation_is_translated(database_connection: AsyncSqliteConnection) -> None:
    await _create_table_with_unique_email(database_connection)
    await database_connection.execute("INSERT INTO users (id, email) VALUES (1, 'a@example.com')")

    with pytest.raises(UniqueViolationError) as exc_info:
        await database_connection.execute("INSERT INTO users (id, email) VALUES (2, 'a@example.com')")

    assert 'UNIQUE constraint failed' in str(exc_info.value)


async def test_primary_key_collision_is_translated(database_connection: AsyncSqliteConnection) -> None:
    await _create_table_with_unique_email(database_connection)
    await database_connection.execute("INSERT INTO users (id, email) VALUES (1, 'a@example.com')")

    with pytest.raises(UniqueViolationError):
        await database_connection.execute("INSERT INTO users (id, email) VALUES (1, 'b@example.com')")


async def test_unique_violation_is_amsdal_glue_error(database_connection: AsyncSqliteConnection) -> None:
    """Callers may catch the broader base type without losing constraint context."""
    await _create_table_with_unique_email(database_connection)
    await database_connection.execute("INSERT INTO users (id, email) VALUES (1, 'a@example.com')")

    with pytest.raises(AmsdalGlueError):
        await database_connection.execute("INSERT INTO users (id, email) VALUES (2, 'a@example.com')")


async def test_non_unique_integrity_error_is_connection_error(database_connection: AsyncSqliteConnection) -> None:
    """NOT NULL violations must keep raising ConnectionError, not UniqueViolationError."""
    await database_connection.execute('CREATE TABLE items (  id INTEGER PRIMARY KEY,  name VARCHAR(100) NOT NULL)')

    with pytest.raises(ConnectionError):
        await database_connection.execute('INSERT INTO items (id, name) VALUES (1, NULL)')


async def test_other_sql_error_is_connection_error(database_connection: AsyncSqliteConnection) -> None:
    """Syntax / operational errors must continue to surface as ConnectionError."""
    with pytest.raises(ConnectionError):
        await database_connection.execute('SELECT * FROM nonexistent_table_xyz')
