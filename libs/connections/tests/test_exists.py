"""SQL emission for the `Exists` boolean Expression."""

from amsdal_glue_core.common.data_models.annotation import AnnotationQuery
from amsdal_glue_core.common.data_models.annotation import ExpressionAnnotation
from amsdal_glue_core.common.data_models.conditions import Condition
from amsdal_glue_core.common.data_models.conditions import Conditions
from amsdal_glue_core.common.data_models.field_reference import Field
from amsdal_glue_core.common.data_models.field_reference import FieldReference
from amsdal_glue_core.common.data_models.join import JoinQuery
from amsdal_glue_core.common.data_models.query import QueryStatement
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.enums import FieldLookup
from amsdal_glue_core.common.enums import FilterConnector
from amsdal_glue_core.common.enums import JoinType
from amsdal_glue_core.common.expressions.exists import Exists
from amsdal_glue_core.common.expressions.field_reference import FieldReferenceExpression
from amsdal_glue_core.common.expressions.value import Value

from amsdal_glue_connections.sql.connections.sqlite_connection import get_sqlite_transform
from amsdal_glue_connections.sql.sql_builders.build_expression import build_expression
from amsdal_glue_connections.sql.sql_builders.query_builder import build_conditions
from amsdal_glue_connections.sql.sql_builders.query_builder import build_sql_query


def _correlated_subquery() -> QueryStatement:
    return QueryStatement(
        only=[FieldReference(field=Field(name='1'), table_name='')],
        table=SchemaReference(name='Employee'),
        where=Conditions(
            Condition(
                left=FieldReferenceExpression(
                    field_reference=FieldReference(
                        field=Field(name='company_id'),
                        table_name='Employee',
                    )
                ),
                lookup=FieldLookup.EQ,
                right=FieldReferenceExpression(
                    field_reference=FieldReference(
                        field=Field(name='id'),
                        table_name='Company',
                    )
                ),
            )
        ),
    )


def test_exists_renders_via_build_expression() -> None:
    sql, _ = build_expression(Exists(query=_correlated_subquery()), transform=get_sqlite_transform())

    assert sql.startswith('EXISTS (SELECT')
    assert 'company_id' in sql
    assert 'Company' in sql


def test_not_exists_renders_via_build_expression() -> None:
    sql, _ = build_expression(
        Exists(query=_correlated_subquery(), negated=True),
        transform=get_sqlite_transform(),
    )

    assert sql.startswith('NOT EXISTS (')


def test_exists_inside_conditions_children_renders_in_where() -> None:
    where = Conditions(Exists(query=_correlated_subquery()))

    sql, _ = build_conditions(where, transform=get_sqlite_transform())

    assert sql.startswith('EXISTS (')


def test_not_exists_inside_conditions_combined_with_other_condition() -> None:
    where = Conditions(
        Condition(
            left=FieldReferenceExpression(
                field_reference=FieldReference(
                    field=Field(name='name'),
                    table_name='Company',
                )
            ),
            lookup=FieldLookup.EQ,
            right=Value(value='Acme'),
        ),
        Exists(query=_correlated_subquery(), negated=True),
        connector=FilterConnector.AND,
    )

    sql, _ = build_conditions(where, transform=get_sqlite_transform())

    assert 'name' in sql
    assert 'NOT EXISTS (' in sql
    assert ' AND ' in sql


def test_exists_in_top_level_query_where() -> None:
    """End-to-end: SQL builder integrates Exists in WHERE."""
    query = QueryStatement(
        only=None,
        table=SchemaReference(name='Company'),
        where=Conditions(Exists(query=_correlated_subquery(), negated=True)),
    )

    sql, _ = build_sql_query(query=query, transform=get_sqlite_transform())

    assert 'WHERE NOT EXISTS (' in sql


def test_exists_as_annotation_in_select() -> None:
    """`SELECT ..., EXISTS(...) AS has_alice FROM ...`."""
    query = QueryStatement(
        only=[FieldReference(field=Field(name='name'), table_name='Company')],
        table=SchemaReference(name='Company'),
        annotations=[
            AnnotationQuery(
                value=ExpressionAnnotation(
                    expression=Exists(query=_correlated_subquery()),
                    alias='has_alice',
                )
            )
        ],
    )

    sql, _ = build_sql_query(query=query, transform=get_sqlite_transform())

    assert 'EXISTS (' in sql
    assert 'has_alice' in sql


def test_exists_in_join_on_clause() -> None:
    """`JOIN ... ON EXISTS (...)` — rare but valid."""
    query = QueryStatement(
        only=None,
        table=SchemaReference(name='Company'),
        joins=[
            JoinQuery(
                table=SchemaReference(name='Employee', alias='e'),
                on=Conditions(Exists(query=_correlated_subquery())),
                join_type=JoinType.INNER,
            )
        ],
    )

    sql, _ = build_sql_query(query=query, transform=get_sqlite_transform())

    assert 'INNER JOIN' in sql
    assert 'ON EXISTS (' in sql


def test_exists_inside_condition_left_with_eq_value() -> None:
    """Awkward but valid: `WHERE EXISTS(...) = TRUE`."""
    where = Conditions(
        Condition(
            left=Exists(query=_correlated_subquery()),
            lookup=FieldLookup.EQ,
            right=Value(value=True),
        )
    )

    sql, _ = build_conditions(where, transform=get_sqlite_transform())

    assert 'EXISTS (' in sql
    assert '= ?' in sql
