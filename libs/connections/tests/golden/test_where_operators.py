import pytest
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

from ._harness import lite
from ._harness import pg


def _where(lookup: FieldLookup, right: object) -> QueryStatement:
    return QueryStatement(
        table=SchemaReference(name='users', version=Version.LATEST),
        where=Conditions(
            Condition(
                left=FieldReferenceExpression(
                    field_reference=FieldReference(field=Field(name='age'), table_name='users'),
                ),
                lookup=lookup,
                right=Value(value=right),
            ),
        ),
    )


# (lookup, right_value) — one row per operator.
CASES = [
    (FieldLookup.EQ, 18),
    (FieldLookup.NEQ, 18),
    (FieldLookup.GT, 18),
    (FieldLookup.GTE, 18),
    (FieldLookup.LT, 18),
    (FieldLookup.LTE, 18),
    (FieldLookup.IN, [1, 2, 3]),
    (FieldLookup.CONTAINS, 'oo'),
    (FieldLookup.ICONTAINS, 'oo'),
    (FieldLookup.STARTSWITH, 'fo'),
    (FieldLookup.ISTARTSWITH, 'fo'),
    (FieldLookup.ENDSWITH, 'oo'),
    (FieldLookup.IENDSWITH, 'oo'),
    (FieldLookup.REGEX, '^foo'),
    (FieldLookup.IREGEX, '^foo'),
]

# EXPECTED_PG / EXPECTED_LITE: Map FieldLookup.name -> (sql, params).
#
# Re-baselined against the Rust generator (differences noted per entry).
EXPECTED_PG: dict[str, tuple[str, list]] = {
    'EQ': ('SELECT * FROM "users" WHERE "users"."age" = %s', [18]),
    # Rust uses standard SQL <> instead of !=; semantically identical — re-baselined.
    'NEQ': ('SELECT * FROM "users" WHERE "users"."age" <> %s', [18]),
    'GT': ('SELECT * FROM "users" WHERE "users"."age" > %s', [18]),
    'GTE': ('SELECT * FROM "users" WHERE "users"."age" >= %s', [18]),
    'LT': ('SELECT * FROM "users" WHERE "users"."age" < %s', [18]),
    'LTE': ('SELECT * FROM "users" WHERE "users"."age" <= %s', [18]),
    # Rust generates IN (%s, %s, %s) with flat params [1,2,3] — correct SQL; re-baselined.
    # Old Python builder used = ANY(%s) with triple-nested params [[[1,2,3]]] (bug).
    'IN': ('SELECT * FROM "users" WHERE "users"."age" IN (%s, %s, %s)', [1, 2, 3]),
    # Rust fixed the CONTAINS wildcard: now uses '%' wildcards (correct LIKE); re-baselined.
    'CONTAINS': ('SELECT * FROM "users" WHERE "users"."age" LIKE %s', ['%oo%']),
    # Rust uses native PostgreSQL ILIKE instead of LOWER(...) LIKE — valid; re-baselined.
    'ICONTAINS': ('SELECT * FROM "users" WHERE "users"."age" ILIKE %s', ['%oo%']),
    'STARTSWITH': ('SELECT * FROM "users" WHERE "users"."age" LIKE %s', ['fo%']),
    'ISTARTSWITH': ('SELECT * FROM "users" WHERE "users"."age" ILIKE %s', ['fo%']),
    'ENDSWITH': ('SELECT * FROM "users" WHERE "users"."age" LIKE %s', ['%oo']),
    'IENDSWITH': ('SELECT * FROM "users" WHERE "users"."age" ILIKE %s', ['%oo']),
    'REGEX': ('SELECT * FROM "users" WHERE "users"."age" ~ %s', ['^foo']),
    'IREGEX': ('SELECT * FROM "users" WHERE "users"."age" ~* %s', ['^foo']),
}

# All SQLite entries re-baselined: ANSI double-quote identifiers (old builder used single quotes).
# Additional SQL-level changes noted per entry.
EXPECTED_LITE: dict[str, tuple[str, list]] = {
    'EQ': ('SELECT * FROM "users" WHERE "users"."age" = ?', [18]),
    # Rust uses <> (standard) instead of !=; re-baselined.
    'NEQ': ('SELECT * FROM "users" WHERE "users"."age" <> ?', [18]),
    'GT': ('SELECT * FROM "users" WHERE "users"."age" > ?', [18]),
    'GTE': ('SELECT * FROM "users" WHERE "users"."age" >= ?', [18]),
    'LT': ('SELECT * FROM "users" WHERE "users"."age" < ?', [18]),
    'LTE': ('SELECT * FROM "users" WHERE "users"."age" <= ?', [18]),
    'IN': ('SELECT * FROM "users" WHERE "users"."age" IN (?, ?, ?)', [1, 2, 3]),
    # Rust uses LIKE + ESCAPE instead of GLOB; % wildcards; re-baselined.
    'CONTAINS': ('SELECT * FROM "users" WHERE "users"."age" LIKE ? ESCAPE \'\\\'', ['%oo%']),
    # Rust uses LIKE LOWER + ESCAPE with ANSI quotes; re-baselined.
    'ICONTAINS': ('SELECT * FROM "users" WHERE LOWER("users"."age") LIKE LOWER(?) ESCAPE \'\\\'', ['%oo%']),
    'STARTSWITH': ('SELECT * FROM "users" WHERE "users"."age" LIKE ? ESCAPE \'\\\'', ['fo%']),
    'ISTARTSWITH': ('SELECT * FROM "users" WHERE LOWER("users"."age") LIKE LOWER(?) ESCAPE \'\\\'', ['fo%']),
    'ENDSWITH': ('SELECT * FROM "users" WHERE "users"."age" LIKE ? ESCAPE \'\\\'', ['%oo']),
    'IENDSWITH': ('SELECT * FROM "users" WHERE LOWER("users"."age") LIKE LOWER(?) ESCAPE \'\\\'', ['%oo']),
    'REGEX': ('SELECT * FROM "users" WHERE "users"."age" REGEXP ?', ['^foo']),
    # Rust uses REGEXP '(?i)' || ? (POSIX inline flag) instead of LOWER(...) REGEXP; re-baselined.
    'IREGEX': ('SELECT * FROM "users" WHERE "users"."age" REGEXP \'(?i)\' || ?', ['^foo']),
}


@pytest.mark.parametrize(('lookup', 'right'), CASES, ids=[c[0].name for c in CASES])
def test_where_operator_pg(lookup: FieldLookup, right: object) -> None:
    assert pg(_where(lookup, right)) == EXPECTED_PG[lookup.name]


@pytest.mark.parametrize(('lookup', 'right'), CASES, ids=[c[0].name for c in CASES])
def test_where_operator_sqlite(lookup: FieldLookup, right: object) -> None:
    assert lite(_where(lookup, right)) == EXPECTED_LITE[lookup.name]


def test_isnull_pg() -> None:
    q = QueryStatement(
        table=SchemaReference(name='users', version=Version.LATEST),
        where=Conditions(
            Condition(
                left=FieldReferenceExpression(
                    field_reference=FieldReference(field=Field(name='deleted_at'), table_name='users'),
                ),
                lookup=FieldLookup.ISNULL,
                right=Value(value=True),
            ),
        ),
    )
    assert pg(q) == ('SELECT * FROM "users" WHERE "users"."deleted_at" IS NULL', [])


def test_isnull_sqlite() -> None:
    # ANSI double quotes — valid; re-baselined.
    q = QueryStatement(
        table=SchemaReference(name='users', version=Version.LATEST),
        where=Conditions(
            Condition(
                left=FieldReferenceExpression(
                    field_reference=FieldReference(field=Field(name='deleted_at'), table_name='users'),
                ),
                lookup=FieldLookup.ISNULL,
                right=Value(value=True),
            ),
        ),
    )
    assert lite(q) == ('SELECT * FROM "users" WHERE "users"."deleted_at" IS NULL', [])


@pytest.mark.xfail(strict=True, reason='Rust no longer emits = ANY(%s); test documents superseded expectation')
def test_where_in_pg_params_correct_behaviour() -> None:
    # D2 (superseded): original concern was = ANY(%s) needing [[1,2,3]] for psycopg3.
    # Rust instead emits IN (%s,%s,%s) with [1,2,3] — correct, so = ANY form never appears.
    # Kept as xfail to preserve the historical record; the assertion cannot pass.
    sql, params = pg(_where(FieldLookup.IN, [1, 2, 3]))
    assert (sql, params) == ('SELECT * FROM "users" WHERE "users"."age" = ANY(%s)', [[1, 2, 3]])


def test_where_contains_pg_wildcard_correct_behaviour() -> None:
    # Rust fixed PG CONTAINS to use '%' LIKE wildcards — no longer an xfail.
    sql, params = pg(_where(FieldLookup.CONTAINS, 'oo'))
    assert (sql, params) == ('SELECT * FROM "users" WHERE "users"."age" LIKE %s', ['%oo%'])
