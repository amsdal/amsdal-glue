"""`regex` / `iregex` on PostgreSQL: the PostgreSQL half of the shared cases in ``tests.sql.regex_cases``."""

import pytest
from amsdal_glue_core.common.data_models.query import QueryStatement

from amsdal_glue_connections.sql.connections.postgres_connection import PostgresConnection
from tests.sql.regex_cases import CASES
from tests.sql.regex_cases import INSERT_ROWS
from tests.sql.regex_cases import SCHEMA_COMMAND


@pytest.mark.parametrize(
    ('statement', 'expected'),
    [(statement, postgres) for _, statement, postgres, _ in CASES],
    ids=[case_id for case_id, *_ in CASES],
)
def test_regex_lookup(database_connection: PostgresConnection, statement: QueryStatement, expected: set[int]) -> None:
    database_connection.run_schema_command(SCHEMA_COMMAND)
    database_connection.run_mutations(INSERT_ROWS)

    result = database_connection.query(statement)

    assert {row.data['id'] for row in result} == expected
