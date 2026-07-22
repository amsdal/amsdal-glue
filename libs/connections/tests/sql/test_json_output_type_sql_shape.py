"""The SQL each dialect must emit for a nested JSON field, keyed by ``output_type``.

Fast (no database). The behavioral suites cover the *answers*; this pins the *shape*, so a future
change cannot quietly swap the SQLite lowering back to a `->` chain (which silently mis-orders
numbers) or to a `json_extract(col, '$.a.b')` path (which silently misses keys containing a dot).

Whitespace is normalised away -- the operators and the parameters are what matter.
"""

import pytest
from amsdal_glue_connections._sql_core import SqlGenerator
from amsdal_glue_core.common.enums import FieldLookup
from amsdal_glue_core.common.enums import ScalarType
from amsdal_glue_core.common.expressions.value import Value

from tests.sql.json_output_type_cases import cond
from tests.sql.json_output_type_cases import query
from tests.sql.json_output_type_cases import ref

J = ScalarType.JSONB


def _compile(dialect: str, statement) -> tuple[str, list]:
    style = 'format' if dialect == 'postgres' else 'qmark'
    sql, params = SqlGenerator(dialect, param_style=style).compile_query(statement)

    return ''.join(sql.split()), list(params)


# --- extraction shape ----------------------------------------------------------------------------


@pytest.mark.parametrize(
    ('output_type', 'expected'),
    [
        # Default: compare the JSON value as JSON -- Postgres' native jsonb comparison.
        (None, '"payload"->\'age\''),
        (ScalarType.JSONB, '"payload"->\'age\''),
        # TEXT: switch the LAST operator to `->>`.
        (ScalarType.TEXT, '"payload"->>\'age\''),
        # A typed extraction casts the text form. The parentheses matter: `::` binds tighter than
        # `->>` in Postgres, so `p->>'age'::bigint` would parse as `p ->> ('age'::bigint)` and fail.
        (ScalarType.BIGINT, '."payload"->>\'age\')::bigint'),
    ],
)
def test_postgres_nested_extraction(output_type, expected) -> None:
    sql, _ = _compile(
        'postgres', query(cond(ref('payload', 'age', output_type=output_type), FieldLookup.GTE, Value(18)))
    )

    assert expected in sql


@pytest.mark.parametrize(
    ('output_type', 'expected', 'forbidden'),
    [
        # `->>` yields the NATIVE value, which is the only way SQLite orders numbers correctly.
        (None, '"payload"->>\'age\'', '"payload"->\'age\''),
        (ScalarType.JSONB, '"payload"->>\'age\'', '"payload"->\'age\''),
        # A typed extraction casts the native form. `bigint` carries INTEGER affinity in SQLite.
        (ScalarType.BIGINT, 'CAST("JsonOutputType"."payload"->>\'age\'ASbigint)', None),
    ],
)
def test_sqlite_nested_extraction(output_type, expected, forbidden) -> None:
    sql, _ = _compile('sqlite', query(cond(ref('payload', 'age', output_type=output_type), FieldLookup.GTE, Value(18))))

    assert expected in sql

    if forbidden is not None:
        assert forbidden not in sql


def test_sqlite_text_extraction_reproduces_postgres_text() -> None:
    """SQLite's `->>` gives INTEGER 36 / 1 for a JSON number / boolean; Postgres' gives '36' / 'true'.

    Only a `json_type`-driven CASE reproduces Postgres for every scalar kind, so that is what the
    TEXT lowering must emit. It is built on `->` (not `->>`) because `->>` collapses JSON null into
    SQL NULL, which would make the 'null' branch unreachable.
    """
    sql, _ = _compile(
        'sqlite',
        query(cond(ref('payload', 'age', output_type=ScalarType.TEXT), FieldLookup.GTE, Value('18'))),
    )

    assert 'json_type("JsonOutputType"."payload"->\'age\')' in sql
    assert "='null'THENNULL" in sql
    assert '=\'text\'THEN"JsonOutputType"."payload"->>\'age\'' in sql
    assert 'ELSE"JsonOutputType"."payload"->\'age\'END' in sql


def test_nested_two_level_path() -> None:
    # Only the LAST operator differs by dialect: Postgres keeps `->` (compare as JSON), SQLite ends in
    # `->>` (the native value). Inner-operand parentheses are qcraft's and do not matter here, so they
    # are stripped before the check.
    pg_sql, _ = _compile('postgres', query(cond(ref('payload', 'meta', 'k'), FieldLookup.GTE, Value(4))))
    sq_sql, _ = _compile('sqlite', query(cond(ref('payload', 'meta', 'k'), FieldLookup.GTE, Value(4))))

    assert "\"payload\"->'meta'->'k'" in pg_sql.replace('(', '').replace(')', '')
    assert "\"payload\"->'meta'->>'k'" in sq_sql.replace('(', '').replace(')', '')


def test_sqlite_key_containing_a_dot_is_not_a_json_path() -> None:
    """`json_extract(col, '$.a.b')` would read the key `a.b` as two levels and silently return NULL.

    The `->`/`->>` chain takes the key as an ordinary string literal, so it has no such ambiguity.
    """
    sql, _ = _compile('sqlite', query(cond(ref('payload', 'a.b'), FieldLookup.EQ, Value(1))))

    assert '"payload"->>\'a.b\'' in sql
    assert '$.' not in sql


def test_non_nested_jsonb_output_type_is_identity() -> None:
    """A whole JSON column already IS JSON -- casting it is wrong.

    In SQLite `CAST(col AS jsonb)` would even give the column NUMERIC affinity.
    """
    for dialect in ('postgres', 'sqlite'):
        sql, _ = _compile(
            dialect, query(cond(ref('payload', output_type=J), FieldLookup.EQ, Value({'a': 1}, output_type=J)))
        )

        assert 'CAST' not in sql.upper() or '::' not in sql


# --- parameter shape -----------------------------------------------------------------------------


def test_postgres_json_value_param_is_marked_for_the_binding_layer() -> None:
    """Postgres needs `psycopg.types.json.Jsonb(x)`. Rust cannot build that (it is a psycopg object),
    so the param crosses back as a dialect-neutral marker the connection wraps.
    """
    from amsdal_glue_core.common.data_models.json_value import JsonValue

    _, params = _compile('postgres', query(cond(ref('payload', 'age'), FieldLookup.GTE, Value(18, output_type=J))))

    assert params == [JsonValue(18, ScalarType.JSONB)]


def test_sqlite_scalar_json_value_binds_raw_against_a_native_extraction() -> None:
    """`payload ->> 'age'` yields INTEGER 36, so the parameter must be the raw 18 -- not '18'.

    Binding the JSON text here would compare INTEGER to TEXT, and SQLite orders every INTEGER below
    every TEXT, which is exactly the always-true bug this whole change exists to kill.
    """
    _, params = _compile('sqlite', query(cond(ref('payload', 'age'), FieldLookup.GTE, Value(18, output_type=J))))

    assert params == [18]


def test_sqlite_container_json_value_is_normalised_by_json() -> None:
    """SQLite re-renders JSON minified (`{"k":1}`), while ``json.dumps`` writes `{"k": 1}`.

    Comparing the raw texts silently returns zero rows, so the parameter goes through `json(?)`.

    This is the NESTED-container branch: the counterpart is a `col->'meta'` extraction, which yields
    TEXT, so the parameter must stay TEXT too (`json(?)`). It deliberately does NOT switch to `jsonb()`
    -- SQLite never treats a TEXT value as equal to a binary JSONB blob, so `col->'meta' = jsonb(?)`
    would match nothing. (Whole-column equality, where BOTH sides are wrapped, does use `jsonb()`.)
    """
    from amsdal_glue_core.common.data_models.json_value import JsonValue

    sql, params = _compile(
        'sqlite', query(cond(ref('payload', 'meta'), FieldLookup.EQ, Value({'k': 1}, output_type=J)))
    )

    assert 'json(?)' in sql
    assert 'jsonb(?)' not in sql
    assert params == [JsonValue({'k': 1}, ScalarType.JSONB)]


def test_sqlite_whole_column_comparison_normalises_both_sides() -> None:
    """The stored text carries ``json.dumps`` spacing, so the column needs `jsonb()` too."""
    sql, _ = _compile('sqlite', query(cond(ref('payload'), FieldLookup.EQ, Value({'a': 1}, output_type=J))))

    assert 'jsonb("JsonOutputType"."payload")=jsonb(?)' in sql


def test_json_value_param_shape_is_symmetric_for_a_reversed_condition() -> None:
    """The rule keys on the operand kinds, not on which side the Value happens to sit."""
    _, params = _compile('sqlite', query(cond(Value(18, output_type=J), FieldLookup.GT, ref('payload', 'age'))))

    assert params == [18]


def test_in_list_applies_the_rule_to_every_element() -> None:
    _, params = _compile('sqlite', query(cond(ref('payload', 'age'), FieldLookup.IN, Value([18, 36], output_type=J))))

    assert params == [18, 36]
