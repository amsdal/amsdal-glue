"""Nested SubQueryStatement: outer references aliased columns from deep inner subqueries."""

from amsdal_glue_core.common.data_models.field_reference import Field
from amsdal_glue_core.common.data_models.field_reference import FieldReference
from amsdal_glue_core.common.data_models.field_reference import FieldReferenceAliased
from amsdal_glue_core.common.data_models.query import QueryStatement
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.data_models.sub_query import SubQueryStatement

from amsdal_glue_connections.sql.connections.sqlite_connection import get_sqlite_transform
from amsdal_glue_connections.sql.sql_builders.query_builder import build_sql_query


def test_three_level_nested_subquery_qualified_column_resolves() -> None:
    inner = QueryStatement(
        only=[
            FieldReferenceAliased(
                field=Field(name='name'),
                table_name='Inner',
                alias='sr_2__inner__name',
            )
        ],
        table=SchemaReference(name='Inner'),
    )
    middle = QueryStatement(
        only=[
            FieldReferenceAliased(
                field=Field(name='sr_2__inner__name'),
                table_name='middle',
                alias='sr_1__middle__sr_2__inner__name',
            )
        ],
        table=SubQueryStatement(query=inner, alias='middle'),
    )
    outer = QueryStatement(
        only=[
            FieldReference(
                field=Field(name='sr_1__middle__sr_2__inner__name'),
                table_name='outer',
            )
        ],
        table=SubQueryStatement(query=middle, alias='outer'),
    )

    sql, _ = build_sql_query(query=outer, transform=get_sqlite_transform())

    assert "'outer'.'sr_1__middle__sr_2__inner__name'" in sql
    assert "'middle'.'sr_2__inner__name' AS 'sr_1__middle__sr_2__inner__name'" in sql
    assert "'Inner'.'name' AS 'sr_2__inner__name'" in sql


def test_multi_version_alias_pattern_renders() -> None:
    """Alias contains __<v[:8]> hex suffix — common in amsdal_models historical builder."""
    inner = QueryStatement(
        only=[
            FieldReferenceAliased(
                field=Field(name='name'),
                table_name='Inner',
                alias='sr_2__abc12345__name',
            )
        ],
        table=SchemaReference(name='Inner'),
    )
    outer = QueryStatement(
        only=[
            FieldReference(
                field=Field(name='sr_2__abc12345__name'),
                table_name='sr_1__abc12345',
            )
        ],
        table=SubQueryStatement(query=inner, alias='sr_1__abc12345'),
    )

    sql, _ = build_sql_query(query=outer, transform=get_sqlite_transform())

    assert "'sr_1__abc12345'.'sr_2__abc12345__name'" in sql
