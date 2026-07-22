from amsdal_glue_core.common.data_models.distinct import DistinctClause
from amsdal_glue_core.common.data_models.field_reference import Field
from amsdal_glue_core.common.data_models.field_reference import FieldReference
from amsdal_glue_core.common.data_models.field_reference import FieldReferenceAliased
from amsdal_glue_core.common.data_models.query import QueryStatement
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.enums import Version

from ._harness import lite
from ._harness import pg

# NOTE: SQLite identifiers are ANSI double-quoted.
# DISTINCT / DISTINCT ON are correctly emitted.


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
    q = QueryStatement(table=SchemaReference(name='users', version=Version.LATEST), distinct=DistinctClause())
    assert pg(q) == ('SELECT DISTINCT * FROM "users"', [])


def test_select_distinct_on_pg() -> None:
    q = QueryStatement(
        table=SchemaReference(name='users', version=Version.LATEST),
        distinct=DistinctClause(on_fields=[_ref('country')]),
    )
    assert pg(q) == ('SELECT DISTINCT ON ("users"."country") * FROM "users"', [])


def test_select_star_sqlite() -> None:
    q = QueryStatement(table=SchemaReference(name='users', version=Version.LATEST))
    assert lite(q) == ('SELECT * FROM "users"', [])


def test_select_only_columns_sqlite() -> None:
    q = QueryStatement(
        table=SchemaReference(name='users', version=Version.LATEST),
        only=[_ref('id'), _ref('name')],
    )
    assert lite(q) == ('SELECT "users"."id", "users"."name" FROM "users"', [])


def test_select_aliased_column_sqlite() -> None:
    q = QueryStatement(
        table=SchemaReference(name='users', version=Version.LATEST),
        only=[FieldReferenceAliased(field=Field(name='name'), table_name='users', alias='full_name')],
    )
    assert lite(q) == ('SELECT "users"."name" AS "full_name" FROM "users"', [])


def test_select_distinct_sqlite() -> None:
    q = QueryStatement(table=SchemaReference(name='users', version=Version.LATEST), distinct=DistinctClause())
    assert lite(q) == ('SELECT DISTINCT * FROM "users"', [])
