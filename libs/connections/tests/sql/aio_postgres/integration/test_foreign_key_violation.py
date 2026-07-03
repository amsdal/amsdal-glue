"""Regression tests for FOREIGN KEY-constraint translation in the AsyncPostgres connection.

The execute() method must translate ``psycopg.errors.ForeignKeyViolation`` into
``ForeignKeyViolationError`` so callers can detect the situation (e.g. deleting a
row still referenced by another table) without parsing backend error messages.
Other psycopg errors must continue to surface as ``ConnectionError``.
"""

import pytest
from amsdal_glue_core.common.exceptions import AmsdalGlueError
from amsdal_glue_core.common.exceptions import ForeignKeyViolationError

from amsdal_glue_connections.sql.connections.postgres_connection import AsyncPostgresConnection


async def _create_parent_child_tables(connection: AsyncPostgresConnection) -> None:
    await connection.execute('CREATE TABLE parent (id INTEGER PRIMARY KEY)')
    await connection.execute('CREATE TABLE child (id INTEGER PRIMARY KEY, parent_id INTEGER REFERENCES parent(id))')
    await connection.execute('INSERT INTO parent (id) VALUES (1)')
    await connection.execute('INSERT INTO child (id, parent_id) VALUES (1, 1)')


async def test_foreign_key_violation_on_delete_is_translated(
    database_connection: AsyncPostgresConnection,
) -> None:
    await _create_parent_child_tables(database_connection)

    with pytest.raises(ForeignKeyViolationError):
        await database_connection.execute('DELETE FROM parent WHERE id = 1')


async def test_foreign_key_violation_on_insert_is_translated(
    database_connection: AsyncPostgresConnection,
) -> None:
    await database_connection.execute('CREATE TABLE parent (id INTEGER PRIMARY KEY)')
    await database_connection.execute(
        'CREATE TABLE child (id INTEGER PRIMARY KEY, parent_id INTEGER REFERENCES parent(id))'
    )

    with pytest.raises(ForeignKeyViolationError):
        await database_connection.execute('INSERT INTO child (id, parent_id) VALUES (1, 999)')


async def test_foreign_key_violation_is_amsdal_glue_error(
    database_connection: AsyncPostgresConnection,
) -> None:
    """Callers may catch the broader base type without losing constraint context."""
    await _create_parent_child_tables(database_connection)

    with pytest.raises(AmsdalGlueError):
        await database_connection.execute('DELETE FROM parent WHERE id = 1')
