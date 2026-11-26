"""`regex` / `iregex` on the async SQLite connection: the same `REGEXP` function as the sync one.

Runs the shared cases, NULL handling, negation, an invalid pattern and a reconnect through the async
connection, as the sync suite (``sqlite_connection/integration/test_regex_lookups.py``) does.
"""

from pathlib import Path

import pytest
from amsdal_glue_core.common.data_models.query import QueryStatement
from amsdal_glue_core.common.enums import FieldLookup

from amsdal_glue_connections.sql.connections.sqlite_connection import AsyncSqliteConnection
from tests.sql.regex_cases import CASES
from tests.sql.regex_cases import INSERT_ROWS
from tests.sql.regex_cases import match
from tests.sql.regex_cases import PYTHON_RE_SYNTAX_CASE
from tests.sql.regex_cases import ROWS
from tests.sql.regex_cases import SCHEMA_COMMAND


async def _seed(connection: AsyncSqliteConnection) -> None:
    await connection.run_schema_command(SCHEMA_COMMAND)
    await connection.run_mutations(INSERT_ROWS)


async def _ids(connection: AsyncSqliteConnection, statement: QueryStatement) -> set[int]:
    return {row.data['id'] for row in await connection.query(statement)}


@pytest.mark.parametrize(
    ('statement', 'expected'),
    [(statement, expected) for _, statement, expected in [*CASES, PYTHON_RE_SYNTAX_CASE]],
    ids=[case_id for case_id, *_ in [*CASES, PYTHON_RE_SYNTAX_CASE]],
)
async def test_regex_lookup(
    database_connection: AsyncSqliteConnection,
    statement: QueryStatement,
    expected: set[int],
) -> None:
    await _seed(database_connection)

    assert await _ids(database_connection, statement) == expected


async def test_negated_lookup_excludes_matches_and_null(database_connection: AsyncSqliteConnection) -> None:
    await _seed(database_connection)
    non_null = {row['id'] for row in ROWS if row['text'] is not None}

    assert await _ids(database_connection, match(FieldLookup.IREGEX, r'^JOHN', negated=True)) == non_null - {1, 2, 3}


async def test_null_pattern_matches_nothing(database_connection: AsyncSqliteConnection) -> None:
    await _seed(database_connection)

    assert await _ids(database_connection, match(FieldLookup.REGEX, None)) == set()
    assert await _ids(database_connection, match(FieldLookup.REGEX, None, negated=True)) == set()


async def test_invalid_pattern_raises(database_connection: AsyncSqliteConnection) -> None:
    await _seed(database_connection)

    # glue wraps every SQLite error of a query in `ConnectionError`; SQLite only reports that the function raised.
    with pytest.raises(ConnectionError, match='user-defined function raised exception'):
        await database_connection.query(match(FieldLookup.REGEX, '('))


async def test_regexp_is_registered_again_after_a_reconnect(tmp_path: Path) -> None:
    db_path = tmp_path / 'reconnect.db'
    connection = AsyncSqliteConnection()
    await connection.connect(db_path=db_path)
    await _seed(connection)
    await connection.disconnect()

    await connection.connect(db_path=db_path)
    try:
        assert await _ids(connection, match(FieldLookup.REGEX, r'^john')) == {2, 3}
    finally:
        await connection.disconnect()
