"""SQL emission for the `Exists` boolean Expression."""

from amsdal_glue_connections._sql_core import SqlGenerator
from amsdal_glue_core.common.data_models.conditions import Condition
from amsdal_glue_core.common.data_models.conditions import Conditions
from amsdal_glue_core.common.data_models.field_reference import Field
from amsdal_glue_core.common.data_models.field_reference import FieldReference
from amsdal_glue_core.common.data_models.join import JoinQuery
from amsdal_glue_core.common.data_models.query import QueryStatement
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.data_models.select_expression import SelectExpression
from amsdal_glue_core.common.data_models.sub_query import SubQueryStatement
from amsdal_glue_core.common.enums import FieldLookup
from amsdal_glue_core.common.enums import FilterConnector
from amsdal_glue_core.common.enums import JoinType
from amsdal_glue_core.common.expressions.exists import Exists
from amsdal_glue_core.common.expressions.field_reference import FieldReferenceExpression
from amsdal_glue_core.common.expressions.value import Value

_lite = SqlGenerator('sqlite', param_style='qmark')


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


def _exists(negated: bool = False) -> Exists:  # noqa: FBT001, FBT002
    # §7: Exists(query=sub) → Exists(subquery=SubQueryStatement(query=sub, alias=''))
    return Exists(subquery=SubQueryStatement(query=_correlated_subquery(), alias=''), negated=negated)


def test_exists_renders_via_build_expression() -> None:
    # EXISTS is rendered via compile_query in a WHERE clause.
    # EXISTS( has no space before the paren.
    query = QueryStatement(
        table=SchemaReference(name='Company'),
        where=Conditions(_exists()),
    )
    sql, _ = _lite.compile_query(query)

    assert 'EXISTS(SELECT' in sql
    assert 'company_id' in sql
    assert 'Company' in sql


def test_not_exists_renders_via_build_expression() -> None:
    query = QueryStatement(
        table=SchemaReference(name='Company'),
        where=Conditions(_exists(negated=True)),
    )
    sql, _ = _lite.compile_query(query)

    assert 'NOT EXISTS(' in sql


def test_exists_inside_conditions_children_renders_in_where() -> None:
    query = QueryStatement(
        table=SchemaReference(name='Company'),
        where=Conditions(_exists()),
    )
    sql, _ = _lite.compile_query(query)

    assert 'EXISTS(' in sql


def test_not_exists_inside_conditions_combined_with_other_condition() -> None:
    query = QueryStatement(
        table=SchemaReference(name='Company'),
        where=Conditions(
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
            _exists(negated=True),
            connector=FilterConnector.AND,
        ),
    )
    sql, _ = _lite.compile_query(query)

    assert 'name' in sql
    assert 'NOT EXISTS(' in sql
    assert ' AND ' in sql


def test_exists_in_top_level_query_where() -> None:
    """End-to-end: SqlGenerator integrates Exists in WHERE."""
    query = QueryStatement(
        only=None,
        table=SchemaReference(name='Company'),
        where=Conditions(_exists(negated=True)),
    )
    sql, _ = _lite.compile_query(query)

    # Rust wraps negated EXISTS in parens: WHERE (NOT EXISTS(...))
    assert 'NOT EXISTS(' in sql
    assert 'WHERE' in sql


def test_exists_as_annotation_in_select() -> None:
    """`SELECT ..., EXISTS(...) AS has_alice FROM ...`."""
    # §7: annotations=[AnnotationQuery(ExpressionAnnotation(...))] →
    #     expressions=[SelectExpression(...)] (only= keeps the column projection).
    query = QueryStatement(
        only=[FieldReference(field=Field(name='name'), table_name='Company')],
        table=SchemaReference(name='Company'),
        expressions=[
            SelectExpression(
                expression=_exists(),
                alias='has_alice',
            )
        ],
    )
    sql, _ = _lite.compile_query(query)

    assert 'EXISTS(' in sql
    assert 'has_alice' in sql


def test_exists_in_join_on_clause() -> None:
    """`JOIN ... ON EXISTS (...)` — rare but valid."""
    query = QueryStatement(
        only=None,
        table=SchemaReference(name='Company'),
        joins=[
            JoinQuery(
                table=SchemaReference(name='Employee', alias='e'),
                on=Conditions(_exists()),
                join_type=JoinType.INNER,
            )
        ],
    )
    sql, _ = _lite.compile_query(query)

    assert 'INNER JOIN' in sql
    assert 'ON EXISTS(' in sql


def test_exists_inside_condition_left_with_eq_value() -> None:
    """Awkward but valid: `WHERE EXISTS(...) = TRUE`."""
    query = QueryStatement(
        table=SchemaReference(name='Company'),
        where=Conditions(
            Condition(
                left=_exists(),
                lookup=FieldLookup.EQ,
                right=Value(value=True),
            )
        ),
    )
    sql, _ = _lite.compile_query(query)

    assert 'EXISTS(' in sql
    assert '= ?' in sql
