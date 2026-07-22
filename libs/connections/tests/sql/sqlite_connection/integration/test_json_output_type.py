"""``output_type`` JSON semantics on SQLite -- must return exactly what Postgres returns.

SQLite has no JSON type: `->` yields TEXT holding JSON, and `->>` yields the native SQL value. So the
same AST that Postgres renders as `payload->'age' >= $1` cannot be rendered literally here -- SQLite
orders INTEGER below TEXT, which makes `payload->'age' > 1000000` silently true. The generator lowers
the nested access to the form that reproduces Postgres' answer instead.

The expected id sets are imported verbatim from the shared case module, so this suite and the
Postgres one assert against the same literals.
"""

import pytest

from tests.sql.json_output_type_cases import CASES
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
