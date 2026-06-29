import pytest

from amsdal_glue_core.common.data_models.field_reference import Field
from amsdal_glue_core.common.data_models.field_reference import FieldReference
from amsdal_glue_core.common.data_models.field_reference import FieldReferenceAliased
from amsdal_glue_core.common.data_models.query import QueryStatement
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.enums import Version

from ._harness import lite
from ._harness import pg


def _ref(name: str, table: str = 'users') -> FieldReference:
    return FieldReference(field=Field(name=name), table_name=table)


def test_select_star_pg() -> None:
    q = QueryStatement(table=SchemaReference(name='users', version=Version.LATEST))
    assert pg(q) == ('SELECT * FROM "users"', [])


def test_select_only_columns_pg() -> None:
    q = QueryStatement(
        table=SchemaReference(name='users', version=Version.LATEST),
        only=[_ref('id'), _ref('name')],
    )
    assert pg(q) == ('SELECT "users"."id", "users"."name" FROM "users"', [])


def test_select_aliased_column_pg() -> None:
    q = QueryStatement(
        table=SchemaReference(name='users', version=Version.LATEST),
        only=[FieldReferenceAliased(field=Field(name='name'), table_name='users', alias='full_name')],
    )
    assert pg(q) == ('SELECT "users"."name" AS "full_name" FROM "users"', [])


def test_select_distinct_pg() -> None:
    # KNOWN-DIVERGENCE (migration): current builder silently ignores distinct — no DISTINCT emitted.
    # Correct SQL should be: 'SELECT DISTINCT * FROM "users"'. This locked value characterises the
    # CURRENT bug and is EXPECTED TO CHANGE when the Rust/qcraft generator implements DISTINCT;
    # re-baseline this test at that point.
    q = QueryStatement(table=SchemaReference(name='users', version=Version.LATEST), distinct=True)
    assert pg(q) == ('SELECT * FROM "users"', [])


@pytest.mark.xfail(strict=True, reason='correct behaviour — to be fixed by qcraft/Rust migration; see §3-D1')
def test_select_distinct_star_pg_correct_behaviour() -> None:
    # D1: distinct=True with empty only must emit DISTINCT, not be dropped.
    q = QueryStatement(table=SchemaReference(name='users', version=Version.LATEST), distinct=True)
    assert pg(q) == ('SELECT DISTINCT * FROM "users"', [])


def test_select_distinct_on_pg() -> None:
    # KNOWN-DIVERGENCE (migration): current builder silently ignores distinct — no DISTINCT emitted.
    # Correct SQL should be: 'SELECT DISTINCT ON ("users"."country") * FROM "users"'. This locked
    # value characterises the CURRENT bug and is EXPECTED TO CHANGE when the Rust/qcraft generator
    # implements DISTINCT; re-baseline this test at that point.
    # Note: xfail does not apply here because the builder fails SILENTLY (returns wrong SQL) rather
    # than raising an exception.
    q = QueryStatement(
        table=SchemaReference(name='users', version=Version.LATEST),
        distinct=[_ref('country')],
    )
    assert pg(q) == ('SELECT * FROM "users"', [])


@pytest.mark.xfail(strict=True, reason='correct behaviour — to be fixed by qcraft/Rust migration; see §3-D1')
def test_select_distinct_on_star_pg_correct_behaviour() -> None:
    # D1: PG DISTINCT ON with empty only must emit DISTINCT ON, not be dropped.
    q = QueryStatement(
        table=SchemaReference(name='users', version=Version.LATEST),
        distinct=[_ref('country')],
    )
    assert pg(q) == ('SELECT DISTINCT ON ("users"."country") * FROM "users"', [])


def test_select_star_sqlite() -> None:
    q = QueryStatement(table=SchemaReference(name='users', version=Version.LATEST))
    assert lite(q) == ("SELECT * FROM 'users'", [])


def test_select_only_columns_sqlite() -> None:
    q = QueryStatement(
        table=SchemaReference(name='users', version=Version.LATEST),
        only=[_ref('id'), _ref('name')],
    )
    assert lite(q) == ("SELECT 'users'.'id', 'users'.'name' FROM 'users'", [])


def test_select_aliased_column_sqlite() -> None:
    q = QueryStatement(
        table=SchemaReference(name='users', version=Version.LATEST),
        only=[FieldReferenceAliased(field=Field(name='name'), table_name='users', alias='full_name')],
    )
    assert lite(q) == ("SELECT 'users'.'name' AS 'full_name' FROM 'users'", [])


def test_select_distinct_sqlite() -> None:
    # KNOWN-DIVERGENCE (migration): current builder silently ignores distinct — no DISTINCT emitted.
    # Correct SQL should be: "SELECT DISTINCT * FROM 'users'". This locked value characterises the
    # CURRENT bug and is EXPECTED TO CHANGE when the Rust/qcraft generator implements DISTINCT;
    # re-baseline this test at that point.
    q = QueryStatement(table=SchemaReference(name='users', version=Version.LATEST), distinct=True)
    assert lite(q) == ("SELECT * FROM 'users'", [])


@pytest.mark.xfail(strict=True, reason='correct behaviour — to be fixed by qcraft/Rust migration; see §3-D1')
def test_select_distinct_star_sqlite_correct_behaviour() -> None:
    # D1: SQLite distinct=True with empty only must emit DISTINCT.
    q = QueryStatement(table=SchemaReference(name='users', version=Version.LATEST), distinct=True)
    assert lite(q) == ("SELECT DISTINCT * FROM 'users'", [])
