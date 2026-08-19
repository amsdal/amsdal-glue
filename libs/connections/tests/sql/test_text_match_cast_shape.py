"""The SQL shape of text-match lookups on a whole JSON column.

Fast (no database). Postgres stores JSON columns as ``jsonb``, which has no ``LIKE`` operator
(``operator does not exist: jsonb ~~ unknown``), so every LIKE-family comparison must cast its
left side to text. The behavioral suites pin the answers; this pins the shape, so the cast cannot
quietly disappear and 500 every array/dictionary filter on Postgres again.
"""

import pytest
from amsdal_glue_connections._sql_core import SqlGenerator
from amsdal_glue_core.common.enums import FieldLookup
from amsdal_glue_core.common.expressions.value import Value

from tests.sql.json_output_type_cases import cond
from tests.sql.json_output_type_cases import query
from tests.sql.json_output_type_cases import ref

TEXT_MATCH_LOOKUPS = [
    FieldLookup.CONTAINS,
    FieldLookup.ICONTAINS,
    FieldLookup.STARTSWITH,
    FieldLookup.ISTARTSWITH,
    FieldLookup.ENDSWITH,
    FieldLookup.IENDSWITH,
]


def _compile(dialect: str, statement) -> str:
    style = 'format' if dialect == 'postgres' else 'qmark'
    sql, _ = SqlGenerator(dialect, param_style=style).compile_query(statement)

    return ''.join(sql.split())


@pytest.mark.parametrize('lookup', TEXT_MATCH_LOOKUPS, ids=[lookup.value for lookup in TEXT_MATCH_LOOKUPS])
def test_postgres_text_match_casts_column_to_text(lookup) -> None:
    sql = _compile('postgres', query(cond(ref('payload'), lookup, Value('Emil'))))

    assert '::text' in sql, sql
    assert 'LIKE' in sql, sql


def test_postgres_eq_keeps_bare_column() -> None:
    """The cast is a text-match concern only; equality must stay the native jsonb comparison."""
    sql = _compile('postgres', query(cond(ref('payload'), FieldLookup.EQ, Value('x'))))

    assert '::text' not in sql, sql


def test_sqlite_contains_still_uses_glob() -> None:
    """The SQLite case-sensitivity lowering must survive the cast."""
    sql = _compile('sqlite', query(cond(ref('payload'), FieldLookup.CONTAINS, Value('Emil'))))

    assert 'glob(' in sql, sql


@pytest.mark.parametrize('lookup', [FieldLookup.REGEX, FieldLookup.IREGEX], ids=['REGEX', 'IREGEX'])
def test_postgres_regex_casts_column_to_text(lookup) -> None:
    """`~`/`~*` have no jsonb operator either -- same failure mode as LIKE."""
    sql = _compile('postgres', query(cond(ref('payload'), lookup, Value('^Emil'))))

    assert '::text' in sql, sql
    assert '~' in sql, sql


@pytest.mark.parametrize('lookup', TEXT_MATCH_LOOKUPS, ids=[lookup.value for lookup in TEXT_MATCH_LOOKUPS])
def test_postgres_nested_text_match_uses_text_extraction(lookup) -> None:
    """A nested field must switch to `->>` (unquoted text), NOT `(col->'k')::text`.

    `(payload->'name')::text` is the QUOTED JSON serialization (`"Emil"`), so STARTSWITH/ENDSWITH
    would silently miss every row on Postgres while matching on SQLite's unquoted `->>`.
    """
    sql = _compile('postgres', query(cond(ref('payload', 'name'), lookup, Value('Emil'))))

    assert "->>'name'" in sql, sql
    assert "->'name')::text" not in sql, sql
