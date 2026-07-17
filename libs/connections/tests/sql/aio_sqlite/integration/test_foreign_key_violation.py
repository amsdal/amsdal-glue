"""Regression tests for FOREIGN KEY-constraint translation in the AsyncSQLite connection.

The execute() method must translate ``aiosqlite.IntegrityError`` raised on a
FOREIGN KEY violation into ``ForeignKeyViolationError``. UNIQUE violations must keep
raising ``UniqueViolationError`` and every other ``aiosqlite.Error`` must continue
to surface as ``ConnectionError``.
"""

import pytest
from amsdal_glue_core.common.exceptions import AmsdalGlueError
from amsdal_glue_core.common.exceptions import ForeignKeyViolationError

from amsdal_glue_connections.sql.connections.sqlite_connection import AsyncSqliteConnection


async def _create_parent_child_tables(connection: AsyncSqliteConnection) -> None:
    await connection.execute('PRAGMA foreign_keys = ON')
    await connection.execute('CREATE TABLE parent (id INTEGER PRIMARY KEY)')
    await connection.execute('CREATE TABLE child (id INTEGER PRIMARY KEY, parent_id INTEGER REFERENCES parent(id))')
    await connection.execute('INSERT INTO parent (id) VALUES (1)')
    await connection.execute('INSERT INTO child (id, parent_id) VALUES (1, 1)')


async def test_foreign_key_violation_on_delete_is_translated(
    database_connection: AsyncSqliteConnection,
) -> None:
    await _create_parent_child_tables(database_connection)

    with pytest.raises(ForeignKeyViolationError) as exc_info:
        await database_connection.execute('DELETE FROM parent WHERE id = 1')

    assert 'FOREIGN KEY constraint failed' in str(exc_info.value)


async def test_foreign_key_violation_on_insert_is_translated(
    database_connection: AsyncSqliteConnection,
) -> None:
    await database_connection.execute('PRAGMA foreign_keys = ON')
    await database_connection.execute('CREATE TABLE parent (id INTEGER PRIMARY KEY)')
    await database_connection.execute(
        'CREATE TABLE child (id INTEGER PRIMARY KEY, parent_id INTEGER REFERENCES parent(id))'
    )

    with pytest.raises(ForeignKeyViolationError):
        await database_connection.execute('INSERT INTO child (id, parent_id) VALUES (1, 999)')


async def test_foreign_key_violation_is_amsdal_glue_error(
    database_connection: AsyncSqliteConnection,
) -> None:
    """Callers may catch the broader base type without losing constraint context."""
    await _create_parent_child_tables(database_connection)

    with pytest.raises(AmsdalGlueError):
        await database_connection.execute('DELETE FROM parent WHERE id = 1')
