"""Case-sensitive text-match lowering to SQLite `glob(...)`.

SQLite `LIKE` is case-INsensitive for ASCII, so the qcraft default (`LIKE ?`) makes
`STARTSWITH='Test'` wrongly match `'test'`. GLOB is case-sensitive, so the
SQLite lowering pass rewrites the case-sensitive text-match
variants (CONTAINS / STARTSWITH / ENDSWITH) into the `glob(pattern, col) = 1` form,
which is case-sensitive; the case-insensitive `I` variants stay `LOWER(col) LIKE LOWER(?)`.
Postgres is unaffected (its `LIKE` is already case-sensitive).
"""

from amsdal_glue_connections._sql_core import SqlGenerator
from amsdal_glue_core.common.data_models.conditions import Condition
from amsdal_glue_core.common.data_models.conditions import Conditions
from amsdal_glue_core.common.data_models.field_reference import Field
from amsdal_glue_core.common.data_models.field_reference import FieldReference
from amsdal_glue_core.common.data_models.query import QueryStatement
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.enums import FieldLookup
from amsdal_glue_core.common.enums import Version
from amsdal_glue_core.common.expressions.field_reference import FieldReferenceExpression
from amsdal_glue_core.common.expressions.value import Value

_lite = SqlGenerator('sqlite', param_style='qmark')
_pg = SqlGenerator('postgresql', param_style='format')


def _query(lookup: FieldLookup, right: object, *, negate: bool = False) -> QueryStatement:
    return QueryStatement(
        table=SchemaReference(name='t', version=Version.LATEST),
        where=Conditions(
            Condition(
                left=FieldReferenceExpression(
                    field_reference=FieldReference(field=Field(name='name'), table_name='t'),
                ),
                lookup=lookup,
                right=Value(value=right),
                negate=negate,
            ),
        ),
    )


# SQLite: the 3 case-sensitive variants become `glob(pattern, col) = 1`.
EXPECTED_LITE = {
    'CONTAINS': ('SELECT * FROM "t" WHERE glob(?, CAST("t"."name" AS text)) = 1', ['*Test*']),
    'STARTSWITH': ('SELECT * FROM "t" WHERE glob(?, CAST("t"."name" AS text)) = 1', ['Test*']),
    'ENDSWITH': ('SELECT * FROM "t" WHERE glob(?, CAST("t"."name" AS text)) = 1', ['*Test']),
    # I-variants are NOT rewritten by the glob pass: they stay LOWER(col) LIKE LOWER(?) ESCAPE '\'.
    # The CAST(... AS text) is unrelated to this pass -- it comes from `extract.rs::text_match_left`,
    # which casts every text-match left side so a JSON column is comparable with LIKE.
    'ICONTAINS': ('SELECT * FROM "t" WHERE LOWER(CAST("t"."name" AS text)) LIKE LOWER(?) ESCAPE \'\\\'', ['%Test%']),
    'ISTARTSWITH': ('SELECT * FROM "t" WHERE LOWER(CAST("t"."name" AS text)) LIKE LOWER(?) ESCAPE \'\\\'', ['Test%']),
    'IENDSWITH': ('SELECT * FROM "t" WHERE LOWER(CAST("t"."name" AS text)) LIKE LOWER(?) ESCAPE \'\\\'', ['%Test']),
}

# Postgres: none of the 6 are rewritten -- the glob pass is SQLite-only and PG LIKE is already
# case-sensitive. The `::text` is `extract.rs::text_match_left`, not this pass.
EXPECTED_PG = {
    'CONTAINS': ('SELECT * FROM "t" WHERE "t"."name"::text LIKE %s', ['%Test%']),
    'STARTSWITH': ('SELECT * FROM "t" WHERE "t"."name"::text LIKE %s', ['Test%']),
    'ENDSWITH': ('SELECT * FROM "t" WHERE "t"."name"::text LIKE %s', ['%Test']),
    'ICONTAINS': ('SELECT * FROM "t" WHERE "t"."name"::text ILIKE %s', ['%Test%']),
    'ISTARTSWITH': ('SELECT * FROM "t" WHERE "t"."name"::text ILIKE %s', ['Test%']),
    'IENDSWITH': ('SELECT * FROM "t" WHERE "t"."name"::text ILIKE %s', ['%Test']),
}


def test_sqlite_case_sensitive_text_match_uses_glob() -> None:
    for lookup in ('CONTAINS', 'STARTSWITH', 'ENDSWITH'):
        assert _lite.compile_query(_query(FieldLookup[lookup], 'Test')) == EXPECTED_LITE[lookup]


def test_sqlite_case_insensitive_text_match_not_lowered_to_glob() -> None:
    for lookup in ('ICONTAINS', 'ISTARTSWITH', 'IENDSWITH'):
        assert _lite.compile_query(_query(FieldLookup[lookup], 'Test')) == EXPECTED_LITE[lookup]


def test_postgres_text_match_not_lowered_to_glob() -> None:
    for lookup, expected in EXPECTED_PG.items():
        assert _pg.compile_query(_query(FieldLookup[lookup], 'Test')) == expected


def test_sqlite_negated_startswith_wraps_glob_in_not() -> None:
    # exclude(name__startswith='Test') -> NOT (glob(...) = 1).
    assert _lite.compile_query(_query(FieldLookup.STARTSWITH, 'Test', negate=True)) == (
        'SELECT * FROM "t" WHERE NOT (glob(?, CAST("t"."name" AS text)) = 1)',
        ['Test*'],
    )


def test_sqlite_percent_is_literal_under_glob() -> None:
    # `%` is a LIKE metachar but a LITERAL under GLOB — no escaping, matches a real '10%'.
    assert _lite.compile_query(_query(FieldLookup.CONTAINS, '10%')) == (
        'SELECT * FROM "t" WHERE glob(?, CAST("t"."name" AS text)) = 1',
        ['*10%*'],
    )


def test_sqlite_glob_metachars_are_escaped() -> None:
    # `*` is a GLOB wildcard — escaped to `[*]` so the search term stays literal.
    assert _lite.compile_query(_query(FieldLookup.CONTAINS, '10*')) == (
        'SELECT * FROM "t" WHERE glob(?, CAST("t"."name" AS text)) = 1',
        ['*10[*]*'],
    )
