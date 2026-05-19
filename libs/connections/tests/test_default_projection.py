"""Default SELECT projection: bare `*` vs qualified `<table>.*` with joins."""

from amsdal_glue_core.common.data_models.conditions import Condition
from amsdal_glue_core.common.data_models.conditions import Conditions
from amsdal_glue_core.common.data_models.field_reference import Field
from amsdal_glue_core.common.data_models.field_reference import FieldReference
from amsdal_glue_core.common.data_models.field_reference import FieldReferenceAliased
from amsdal_glue_core.common.data_models.join import JoinQuery
from amsdal_glue_core.common.data_models.query import QueryStatement
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.data_models.sub_query import SubQueryStatement
from amsdal_glue_core.common.enums import FieldLookup
from amsdal_glue_core.common.enums import JoinType
from amsdal_glue_core.common.expressions.field_reference import FieldReferenceExpression
from amsdal_glue_core.common.expressions.value import Value

from amsdal_glue_connections.sql.connections.sqlite_connection import get_sqlite_transform
from amsdal_glue_connections.sql.sql_builders.query_builder import build_sql_query


def _trivial_on() -> Conditions:
    return Conditions(
        Condition(
            left=FieldReferenceExpression(
                field_reference=FieldReference(
                    field=Field(name='id'),
                    table_name='Company',
                )
            ),
            lookup=FieldLookup.EQ,
            right=Value(value=1),
        )
    )


def test_only_none_no_joins_keeps_plain_asterisk() -> None:
    query = QueryStatement(only=None, table=SchemaReference(name='Company'), joins=None)

    sql, _ = build_sql_query(query=query, transform=get_sqlite_transform())

    assert sql.startswith('SELECT * ')


def test_only_none_with_join_qualifies_to_base_table_name() -> None:
    query = QueryStatement(
        only=None,
        table=SchemaReference(name='Company'),
        joins=[
            JoinQuery(
                table=SchemaReference(name='Employee', alias='rev_1'),
                on=_trivial_on(),
                join_type=JoinType.INNER,
            )
        ],
    )

    sql, _ = build_sql_query(query=query, transform=get_sqlite_transform())

    assert sql.startswith("SELECT 'Company'.* ")


def test_only_none_with_join_qualifies_to_base_table_alias_when_set() -> None:
    query = QueryStatement(
        only=None,
        table=SchemaReference(name='Company', alias='c'),
        joins=[
            JoinQuery(
                table=SchemaReference(name='Employee', alias='rev_1'),
                on=_trivial_on(),
                join_type=JoinType.INNER,
            )
        ],
    )

    sql, _ = build_sql_query(query=query, transform=get_sqlite_transform())

    assert sql.startswith("SELECT 'c'.* ")


def test_subquery_from_with_join_qualifies_to_subquery_alias() -> None:
    inner = QueryStatement(table=SchemaReference(name='Company'))
    query = QueryStatement(
        only=None,
        table=SubQueryStatement(query=inner, alias='c'),
        joins=[
            JoinQuery(
                table=SchemaReference(name='Employee', alias='rev_1'),
                on=_trivial_on(),
                join_type=JoinType.INNER,
            )
        ],
    )

    sql, _ = build_sql_query(query=query, transform=get_sqlite_transform())

    assert sql.startswith("SELECT 'c'.* ")


def test_explicit_only_unchanged_regression() -> None:
    """Explicit `only=` is not touched by the new default-projection logic."""
    query = QueryStatement(
        only=[FieldReference(field=Field(name='name'), table_name='Company')],
        table=SchemaReference(name='Company'),
        joins=[
            JoinQuery(
                table=SchemaReference(name='Employee', alias='rev_1'),
                on=_trivial_on(),
                join_type=JoinType.INNER,
            )
        ],
    )

    sql, _ = build_sql_query(query=query, transform=get_sqlite_transform())

    assert "SELECT 'Company'.'name'" in sql
    assert '*' not in sql.split('FROM')[0]


def test_only_field_reference_aliased_unchanged() -> None:
    """Aliased projection survives unchanged."""
    query = QueryStatement(
        only=[FieldReferenceAliased(field=Field(name='name'), table_name='Company', alias='company_name')],
        table=SchemaReference(name='Company'),
        joins=None,
    )

    sql, _ = build_sql_query(query=query, transform=get_sqlite_transform())

    assert "'Company'.'name' AS 'company_name'" in sql
