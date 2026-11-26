"""`regex` / `iregex` on SQLite, through the `REGEXP` function the connection registers (Python `re`).

Runs the shared cases in ``tests.sql.regex_cases`` and one in Python `re` syntax; the tests below cover what
only the SQLite function decides: NULL handling, negation, an invalid pattern, a reconnect.
"""

from pathlib import Path

import pytest
from amsdal_glue_core.common.data_models.query import QueryStatement
from amsdal_glue_core.common.enums import FieldLookup

from amsdal_glue_connections.sql.connections.sqlite_connection import SqliteConnection
from tests.sql.regex_cases import CASES
from tests.sql.regex_cases import INSERT_ROWS
from tests.sql.regex_cases import match
from tests.sql.regex_cases import PYTHON_RE_SYNTAX_CASE
from tests.sql.regex_cases import ROWS
from tests.sql.regex_cases import SCHEMA_COMMAND


def _seed(connection: SqliteConnection) -> None:
    connection.run_schema_command(SCHEMA_COMMAND)
    connection.run_mutations(INSERT_ROWS)


def _ids(connection: SqliteConnection, statement: QueryStatement) -> set[int]:
    return {row.data['id'] for row in connection.query(statement)}


@pytest.mark.parametrize(
    ('statement', 'expected'),
    [(statement, expected) for _, statement, expected in [*CASES, PYTHON_RE_SYNTAX_CASE]],
    ids=[case_id for case_id, *_ in [*CASES, PYTHON_RE_SYNTAX_CASE]],
)
def test_regex_lookup(database_connection: SqliteConnection, statement: QueryStatement, expected: set[int]) -> None:
    _seed(database_connection)

    assert _ids(database_connection, statement) == expected


def test_negated_lookup_excludes_matches_and_null(database_connection: SqliteConnection) -> None:
    _seed(database_connection)
    non_null = {row['id'] for row in ROWS if row['text'] is not None}

    assert _ids(database_connection, match(FieldLookup.IREGEX, r'^JOHN', negated=True)) == non_null - {1, 2, 3}


def test_null_pattern_matches_nothing(database_connection: SqliteConnection) -> None:
    _seed(database_connection)

    assert _ids(database_connection, match(FieldLookup.REGEX, None)) == set()
    assert _ids(database_connection, match(FieldLookup.REGEX, None, negated=True)) == set()


def test_invalid_pattern_raises(database_connection: SqliteConnection) -> None:
    _seed(database_connection)

    # glue wraps every SQLite error of a query in `ConnectionError`; SQLite only reports that the function raised.
    with pytest.raises(ConnectionError, match='user-defined function raised exception'):
        database_connection.query(match(FieldLookup.REGEX, '('))


def test_regexp_is_registered_again_after_a_reconnect(tmp_path: Path) -> None:
    db_path = tmp_path / 'reconnect.db'
    connection = SqliteConnection()
    connection.connect(db_path=db_path)
    _seed(connection)
    connection.disconnect()

    connection.connect(db_path=db_path)
    try:
        assert _ids(connection, match(FieldLookup.REGEX, r'^john')) == {2, 3}
    finally:
        connection.disconnect()
