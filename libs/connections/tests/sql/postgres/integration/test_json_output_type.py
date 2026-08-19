"""``output_type`` JSON semantics on Postgres -- the reference dialect.

Postgres must render exactly what the AST describes: a nested field reference with the default
(JSONB) ``output_type`` is a `->` chain compared against a `jsonb` parameter; ``output_type=TEXT``
switches the last operator to `->>`; any other scalar type adds a cast.

The expected id sets live in ``tests.sql.json_output_type_cases`` and are shared verbatim with the
SQLite suite, so the two engines are pinned to the same answers.
"""

import pytest

from tests.sql.json_output_type_cases import CASES
from tests.sql.json_output_type_cases import NON_ASCII_ROWS
from tests.sql.json_output_type_cases import NON_ASCII_TABLE
from tests.sql.json_output_type_cases import NON_ASCII_TEXT_MATCH_CASES
from tests.sql.json_output_type_cases import PG_REGEX_CASES
from tests.sql.json_output_type_cases import register_and_seed
from tests.sql.json_output_type_cases import ROWS
from tests.sql.json_output_type_cases import SCALAR_CASES
from tests.sql.json_output_type_cases import SCALAR_ROWS
from tests.sql.json_output_type_cases import SCALAR_TABLE
from tests.sql.json_output_type_cases import TABLE


@pytest.mark.parametrize(
    ('statement', 'expected'),
    [(statement, expected) for _, statement, expected in CASES],
    ids=[case_id for case_id, _, _ in CASES],
)
def test_json_output_type(database_connection, statement, expected) -> None:
    register_and_seed(database_connection, TABLE, ROWS)

    result = database_connection.query(statement)

    assert {row.data['id'] for row in result} == expected


@pytest.mark.parametrize(
    ('statement', 'expected'),
    [(statement, expected) for _, statement, expected in SCALAR_CASES],
    ids=[case_id for case_id, _, _ in SCALAR_CASES],
)
def test_json_output_type_scalar_column(database_connection, statement, expected) -> None:
    register_and_seed(database_connection, SCALAR_TABLE, SCALAR_ROWS)

    result = database_connection.query(statement)

    assert {row.data['id'] for row in result} == expected


@pytest.mark.parametrize(
    ('statement', 'expected'),
    [(statement, expected) for _, statement, expected in PG_REGEX_CASES],
    ids=[case_id for case_id, _, _ in PG_REGEX_CASES],
)
def test_json_regex_lookups(database_connection, statement, expected) -> None:
    register_and_seed(database_connection, TABLE, ROWS)

    result = database_connection.query(statement)

    assert {row.data['id'] for row in result} == expected


@pytest.mark.parametrize(
    ('statement', 'expected'),
    [(statement, expected[0]) for _, statement, *expected in NON_ASCII_TEXT_MATCH_CASES],
    ids=[case_id for case_id, _, _, _ in NON_ASCII_TEXT_MATCH_CASES],
)
def test_non_ascii_text_match(database_connection, statement, expected) -> None:
    """Pin the Postgres half of the non-ASCII text-match divergence (see the shared case module)."""
    register_and_seed(database_connection, NON_ASCII_TABLE, NON_ASCII_ROWS)

    result = database_connection.query(statement)

    assert {row.data['id'] for row in result} == expected
