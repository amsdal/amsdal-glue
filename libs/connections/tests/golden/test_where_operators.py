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
# Notable SQL choices noted per entry.
EXPECTED_PG: dict[str, tuple[str, list]] = {
    'EQ': ('SELECT * FROM "users" WHERE "users"."age" = %s', [18]),
    # Uses standard SQL <> instead of !=; semantically identical.
    'NEQ': ('SELECT * FROM "users" WHERE "users"."age" <> %s', [18]),
    'GT': ('SELECT * FROM "users" WHERE "users"."age" > %s', [18]),
    'GTE': ('SELECT * FROM "users" WHERE "users"."age" >= %s', [18]),
    'LT': ('SELECT * FROM "users" WHERE "users"."age" < %s', [18]),
    'LTE': ('SELECT * FROM "users" WHERE "users"."age" <= %s', [18]),
    # IN (%s, %s, %s) with flat params [1,2,3].
    'IN': ('SELECT * FROM "users" WHERE "users"."age" IN (%s, %s, %s)', [1, 2, 3]),
    # CONTAINS uses '%' wildcards (LIKE).
    'CONTAINS': ('SELECT * FROM "users" WHERE "users"."age"::text LIKE %s', ['%oo%']),
    # Uses native PostgreSQL ILIKE instead of LOWER(...) LIKE.
    'ICONTAINS': ('SELECT * FROM "users" WHERE "users"."age"::text ILIKE %s', ['%oo%']),
    'STARTSWITH': ('SELECT * FROM "users" WHERE "users"."age"::text LIKE %s', ['fo%']),
    'ISTARTSWITH': ('SELECT * FROM "users" WHERE "users"."age"::text ILIKE %s', ['fo%']),
    'ENDSWITH': ('SELECT * FROM "users" WHERE "users"."age"::text LIKE %s', ['%oo']),
    'IENDSWITH': ('SELECT * FROM "users" WHERE "users"."age"::text ILIKE %s', ['%oo']),
    'REGEX': ('SELECT * FROM "users" WHERE "users"."age" ~ %s', ['^foo']),
    'IREGEX': ('SELECT * FROM "users" WHERE "users"."age" ~* %s', ['^foo']),
}

# All SQLite entries use ANSI double-quote identifiers.
# Additional SQL-level notes per entry.
EXPECTED_LITE: dict[str, tuple[str, list]] = {
    'EQ': ('SELECT * FROM "users" WHERE "users"."age" = ?', [18]),
    # Uses <> (standard) instead of !=.
    'NEQ': ('SELECT * FROM "users" WHERE "users"."age" <> ?', [18]),
    'GT': ('SELECT * FROM "users" WHERE "users"."age" > ?', [18]),
    'GTE': ('SELECT * FROM "users" WHERE "users"."age" >= ?', [18]),
    'LT': ('SELECT * FROM "users" WHERE "users"."age" < ?', [18]),
    'LTE': ('SELECT * FROM "users" WHERE "users"."age" <= ?', [18]),
    'IN': ('SELECT * FROM "users" WHERE "users"."age" IN (?, ?, ?)', [1, 2, 3]),
    # Case-sensitive text match lowers to the case-sensitive glob(...) form (SQLite LIKE is
    # case-insensitive); GLOB is case-sensitive. See test_text_match_glob_lowering.py.
    'CONTAINS': ('SELECT * FROM "users" WHERE glob(?, CAST("users"."age" AS text)) = 1', ['*oo*']),
    # Uses LIKE LOWER + ESCAPE with ANSI quotes.
    'ICONTAINS': (
        'SELECT * FROM "users" WHERE LOWER(CAST("users"."age" AS text)) LIKE LOWER(?) ESCAPE \'\\\'',
        ['%oo%'],
    ),
    'STARTSWITH': ('SELECT * FROM "users" WHERE glob(?, CAST("users"."age" AS text)) = 1', ['fo*']),
    'ISTARTSWITH': (
        'SELECT * FROM "users" WHERE LOWER(CAST("users"."age" AS text)) LIKE LOWER(?) ESCAPE \'\\\'',
        ['fo%'],
    ),
    'ENDSWITH': ('SELECT * FROM "users" WHERE glob(?, CAST("users"."age" AS text)) = 1', ['*oo']),
    'IENDSWITH': (
        'SELECT * FROM "users" WHERE LOWER(CAST("users"."age" AS text)) LIKE LOWER(?) ESCAPE \'\\\'',
        ['%oo'],
    ),
    'REGEX': ('SELECT * FROM "users" WHERE "users"."age" REGEXP ?', ['^foo']),
    # Uses REGEXP '(?i)' || ? (POSIX inline flag) instead of LOWER(...) REGEXP.
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
    # ANSI double quotes.
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


def test_isnotnull_pg() -> None:
    q = QueryStatement(
        table=SchemaReference(name='users', version=Version.LATEST),
        where=Conditions(
            Condition(
                left=FieldReferenceExpression(
                    field_reference=FieldReference(field=Field(name='deleted_at'), table_name='users'),
                ),
                lookup=FieldLookup.ISNULL,
                right=Value(value=False),
            ),
        ),
    )
    assert pg(q) == ('SELECT * FROM "users" WHERE "users"."deleted_at" IS NOT NULL', [])


def test_isnotnull_sqlite() -> None:
    q = QueryStatement(
        table=SchemaReference(name='users', version=Version.LATEST),
        where=Conditions(
            Condition(
                left=FieldReferenceExpression(
                    field_reference=FieldReference(field=Field(name='deleted_at'), table_name='users'),
                ),
                lookup=FieldLookup.ISNULL,
                right=Value(value=False),
            ),
        ),
    )
    assert lite(q) == ('SELECT * FROM "users" WHERE "users"."deleted_at" IS NOT NULL', [])


def test_where_contains_pg_wildcard_correct_behaviour() -> None:
    # PG CONTAINS uses '%' LIKE wildcards.
    sql, params = pg(_where(FieldLookup.CONTAINS, 'oo'))
    assert (sql, params) == ('SELECT * FROM "users" WHERE "users"."age"::text LIKE %s', ['%oo%'])
