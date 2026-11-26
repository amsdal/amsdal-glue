"""`regex` / `iregex` on the async SQLite connection: the same `REGEXP` function as the sync one.

The sync suite (``sqlite_connection/integration/test_regex_lookups.py``) covers the function's edge cases;
this runs the shared cases through the async connection.
"""

from pathlib import Path

import pytest
from amsdal_glue_core.common.data_models.query import QueryStatement
from amsdal_glue_core.common.enums import FieldLookup

from amsdal_glue_connections.sql.connections.sqlite_connection import AsyncSqliteConnection
from tests.sql.regex_cases import CASES
from tests.sql.regex_cases import INSERT_ROWS
from tests.sql.regex_cases import match
from tests.sql.regex_cases import SCHEMA_COMMAND


async def _ids(connection: AsyncSqliteConnection, statement: QueryStatement) -> set[int]:
    return {row.data['id'] for row in await connection.query(statement)}


@pytest.mark.parametrize(
    ('statement', 'expected'),
    [(statement, sqlite) for _, statement, _, sqlite in CASES],
    ids=[case_id for case_id, *_ in CASES],
)
async def test_regex_lookup(
    database_connection: AsyncSqliteConnection,
    statement: QueryStatement,
    expected: set[int],
) -> None:
    await database_connection.run_schema_command(SCHEMA_COMMAND)
    await database_connection.run_mutations(INSERT_ROWS)

    assert await _ids(database_connection, statement) == expected


async def test_regexp_is_registered_again_after_a_reconnect(tmp_path: Path) -> None:
    db_path = tmp_path / 'reconnect.db'
    connection = AsyncSqliteConnection()
    await connection.connect(db_path=db_path)
    await connection.run_schema_command(SCHEMA_COMMAND)
    await connection.run_mutations(INSERT_ROWS)
    await connection.disconnect()

    await connection.connect(db_path=db_path)
    try:
        assert await _ids(connection, match(FieldLookup.REGEX, r'^emil')) == {2}
    finally:
        await connection.disconnect()
