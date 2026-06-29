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
EXPECTED_PG: dict[str, tuple[str, list]] = {
    'EQ': ('SELECT * FROM "users" WHERE "users"."age" = %s', [18]),
    'NEQ': ('SELECT * FROM "users" WHERE "users"."age" != %s', [18]),
    'GT': ('SELECT * FROM "users" WHERE "users"."age" > %s', [18]),
    'GTE': ('SELECT * FROM "users" WHERE "users"."age" >= %s', [18]),
    'LT': ('SELECT * FROM "users" WHERE "users"."age" < %s', [18]),
    'LTE': ('SELECT * FROM "users" WHERE "users"."age" <= %s', [18]),
    # KNOWN-DIVERGENCE (migration): params are triply-nested [[[ ]]] due to a wrapping bug in
    # pg_operator_constructor's IN branch (right_values = [_values] where _values already is a list).
    # The correct params should be [[1, 2, 3]] so that psycopg3 passes [1, 2, 3] to = ANY(%s).
    # This will change when the Rust/qcraft generator fixes the IN param construction.
    'IN': ('SELECT * FROM "users" WHERE "users"."age" = ANY(%s)', [[[1, 2, 3]]]),
    # KNOWN-DIVERGENCE (migration): CONTAINS uses LIKE with '*' wildcards ('*oo*') instead of '%'
    # wildcards ('%oo%'). PostgreSQL LIKE only recognises '%' and '_' as wildcards; '*' matches
    # a literal asterisk, so this query silently returns no rows when it should return rows
    # containing 'oo'. Correct SQL: WHERE "users"."age" LIKE %s with params ['%oo%'].
    # This will change when the Rust/qcraft generator fixes CONTAINS for the PG dialect.
    'CONTAINS': ('SELECT * FROM "users" WHERE "users"."age" LIKE %s', ['*oo*']),
    'ICONTAINS': ('SELECT * FROM "users" WHERE LOWER("users"."age") LIKE %s', ['%oo%']),
    'STARTSWITH': ('SELECT * FROM "users" WHERE "users"."age" LIKE %s', ['fo%']),
    'ISTARTSWITH': ('SELECT * FROM "users" WHERE LOWER("users"."age") LIKE %s', ['fo%']),
    'ENDSWITH': ('SELECT * FROM "users" WHERE "users"."age" LIKE %s', ['%oo']),
    'IENDSWITH': ('SELECT * FROM "users" WHERE LOWER("users"."age") LIKE %s', ['%oo']),
    'REGEX': ('SELECT * FROM "users" WHERE "users"."age" ~ %s', ['^foo']),
    'IREGEX': ('SELECT * FROM "users" WHERE "users"."age" ~* %s', ['^foo']),
}

EXPECTED_LITE: dict[str, tuple[str, list]] = {
    'EQ': ("SELECT * FROM 'users' WHERE 'users'.'age' = ?", [18]),
    'NEQ': ("SELECT * FROM 'users' WHERE 'users'.'age' != ?", [18]),
    'GT': ("SELECT * FROM 'users' WHERE 'users'.'age' > ?", [18]),
    'GTE': ("SELECT * FROM 'users' WHERE 'users'.'age' >= ?", [18]),
    'LT': ("SELECT * FROM 'users' WHERE 'users'.'age' < ?", [18]),
    'LTE': ("SELECT * FROM 'users' WHERE 'users'.'age' <= ?", [18]),
    'IN': ("SELECT * FROM 'users' WHERE 'users'.'age' IN (?, ?, ?)", [1, 2, 3]),
    'CONTAINS': ("SELECT * FROM 'users' WHERE 'users'.'age' GLOB ?", ['*oo*']),
    'ICONTAINS': ("SELECT * FROM 'users' WHERE LOWER('users'.'age') LIKE LOWER(?)", ['%oo%']),
    'STARTSWITH': ("SELECT * FROM 'users' WHERE 'users'.'age' GLOB ?", ['fo*']),
    'ISTARTSWITH': ("SELECT * FROM 'users' WHERE LOWER('users'.'age') LIKE LOWER(?)", ['fo%']),
    'ENDSWITH': ("SELECT * FROM 'users' WHERE 'users'.'age' GLOB ?", ['*oo']),
    'IENDSWITH': ("SELECT * FROM 'users' WHERE LOWER('users'.'age') LIKE LOWER(?)", ['%oo']),
    'REGEX': ("SELECT * FROM 'users' WHERE 'users'.'age' REGEXP ?", ['^foo']),
    'IREGEX': ("SELECT * FROM 'users' WHERE LOWER('users'.'age') REGEXP ?", ['^foo']),
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
    assert lite(q) == ("SELECT * FROM 'users' WHERE 'users'.'deleted_at' IS NULL", [])
