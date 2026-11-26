"""The `REGEXP` function of the SQLite connection, called directly in SQL.

`X REGEXP Y` is SQLite's call `regexp(Y, X)`: pattern first, value second. The function follows Django's
`_sqlite_regexp`: a NULL pattern or value gives NULL, any other value is matched as `str(value)`.
"""

import pytest

from amsdal_glue_connections.sql.connections.sqlite_connection import SqliteConnection


def _regexp(connection: SqliteConnection, value_sql: str, pattern: str | None) -> int | None:
    row = connection.connection.execute(f'SELECT {value_sql} REGEXP ?', (pattern,)).fetchone()
    return row[0]


@pytest.mark.parametrize(
    ('value_sql', 'pattern', 'expected'),
    [
        ("'Emil'", '^Em', 1),
        ("'Emil'", '^em', 0),
        ("'Emil'", '(?i)^em', 1),
        ('5', '^5$', 1),
        ('1.5', r'^1\.5$', 1),
        ("x'61'", "^b'a'$", 1),
        ('NULL', '^', None),
        ("'Emil'", None, None),
    ],
    ids=['match', 'no-match', 'inline-ignorecase', 'integer', 'real', 'blob', 'null-value', 'null-pattern'],
)
def test_regexp(
    database_connection: SqliteConnection, value_sql: str, pattern: str | None, expected: int | None
) -> None:
    assert _regexp(database_connection, value_sql, pattern) == expected
