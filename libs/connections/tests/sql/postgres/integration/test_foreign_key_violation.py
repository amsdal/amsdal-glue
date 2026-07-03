"""Regression tests for FOREIGN KEY-constraint translation in the Postgres connection.

The execute() method must translate ``psycopg.errors.ForeignKeyViolation`` into
``ForeignKeyViolationError`` so callers can detect the situation (e.g. deleting a
row still referenced by another table) without parsing backend error messages.
Other psycopg errors must continue to surface as ``ConnectionError``.
"""

import pytest
from amsdal_glue_core.common.exceptions import AmsdalGlueError
from amsdal_glue_core.common.exceptions import ForeignKeyViolationError

from amsdal_glue_connections.sql.connections.postgres_connection import PostgresConnection


def _create_parent_child_tables(connection: PostgresConnection) -> None:
    connection.execute('CREATE TABLE parent (id INTEGER PRIMARY KEY)')
    connection.execute('CREATE TABLE child (id INTEGER PRIMARY KEY, parent_id INTEGER REFERENCES parent(id))')
    connection.execute('INSERT INTO parent (id) VALUES (1)')
    connection.execute('INSERT INTO child (id, parent_id) VALUES (1, 1)')


def test_foreign_key_violation_on_delete_is_translated(database_connection: PostgresConnection) -> None:
    _create_parent_child_tables(database_connection)

    with pytest.raises(ForeignKeyViolationError):
        database_connection.execute('DELETE FROM parent WHERE id = 1')


def test_foreign_key_violation_on_insert_is_translated(database_connection: PostgresConnection) -> None:
    database_connection.execute('CREATE TABLE parent (id INTEGER PRIMARY KEY)')
    database_connection.execute('CREATE TABLE child (id INTEGER PRIMARY KEY, parent_id INTEGER REFERENCES parent(id))')

    with pytest.raises(ForeignKeyViolationError):
        database_connection.execute('INSERT INTO child (id, parent_id) VALUES (1, 999)')


def test_foreign_key_violation_is_amsdal_glue_error(database_connection: PostgresConnection) -> None:
    """Callers may catch the broader base type without losing constraint context."""
    _create_parent_child_tables(database_connection)

    with pytest.raises(AmsdalGlueError):
        database_connection.execute('DELETE FROM parent WHERE id = 1')
