"""Regression tests for UNIQUE-constraint translation in the AsyncPostgres connection.

The execute() method must translate ``psycopg.errors.UniqueViolation`` into
``UniqueViolationError`` so callers can detect duplicate-key conflicts without
parsing backend error messages. Other psycopg errors must continue to surface
as ``ConnectionError``.
"""

import pytest
from amsdal_glue_core.common.exceptions import AmsdalGlueError
from amsdal_glue_core.common.exceptions import UniqueViolationError

from amsdal_glue_connections.sql.connections.postgres_connection import AsyncPostgresConnection


async def _create_table_with_unique_email(connection: AsyncPostgresConnection) -> None:
    await connection.execute('CREATE TABLE users (  id SERIAL PRIMARY KEY,  email VARCHAR(100) UNIQUE)')


async def test_unique_violation_is_translated(database_connection: AsyncPostgresConnection) -> None:
    await _create_table_with_unique_email(database_connection)
    await database_connection.execute("INSERT INTO users (email) VALUES ('a@example.com')")

    with pytest.raises(UniqueViolationError):
        await database_connection.execute("INSERT INTO users (email) VALUES ('a@example.com')")


async def test_primary_key_collision_is_translated(database_connection: AsyncPostgresConnection) -> None:
    await database_connection.execute('CREATE TABLE items (  id INTEGER PRIMARY KEY,  label VARCHAR(50))')
    await database_connection.execute("INSERT INTO items (id, label) VALUES (1, 'x')")

    with pytest.raises(UniqueViolationError):
        await database_connection.execute("INSERT INTO items (id, label) VALUES (1, 'y')")


async def test_unique_violation_is_amsdal_glue_error(database_connection: AsyncPostgresConnection) -> None:
    """Callers may catch the broader base type without losing constraint context."""
    await _create_table_with_unique_email(database_connection)
    await database_connection.execute("INSERT INTO users (email) VALUES ('a@example.com')")

    with pytest.raises(AmsdalGlueError):
        await database_connection.execute("INSERT INTO users (email) VALUES ('a@example.com')")


async def test_non_unique_integrity_error_is_connection_error(database_connection: AsyncPostgresConnection) -> None:
    """NOT NULL violations must keep raising ConnectionError, not UniqueViolationError."""
    await database_connection.execute('CREATE TABLE items (  id SERIAL PRIMARY KEY,  name VARCHAR(100) NOT NULL)')

    with pytest.raises(ConnectionError):
        await database_connection.execute('INSERT INTO items (name) VALUES (NULL)')


async def test_other_sql_error_is_connection_error(database_connection: AsyncPostgresConnection) -> None:
    """Syntax / operational errors must continue to surface as ConnectionError."""
    with pytest.raises(ConnectionError):
        await database_connection.execute('SELECT * FROM nonexistent_table_xyz')
