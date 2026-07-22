"""Default SELECT projection: bare `*` vs qualified `<table>.*` with joins.

A default projection (`only=None`) over a query WITH joins must qualify the star to the base
table/subquery (`SELECT "Company".*`), not emit a bare `SELECT *`. A bare star expands to every
joined table's columns, so tables sharing a column name (e.g. `partition_key`) yield a duplicated
result column that the downstream executor rejects. With no joins, or when the base alias is empty,
the bare `SELECT *` is kept. An explicit `only=` is never touched.
"""

from amsdal_glue_connections._sql_core import SqlGenerator
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

_lite = SqlGenerator('sqlite', param_style='qmark')


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

    sql, _ = _lite.compile_query(query)

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

    sql, _ = _lite.compile_query(query)

    assert sql.startswith('SELECT "Company".* ')


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

    sql, _ = _lite.compile_query(query)

    assert sql.startswith('SELECT "c".* ')


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

    sql, _ = _lite.compile_query(query)

    assert sql.startswith('SELECT "c".* ')


def test_explicit_only_unchanged_regression() -> None:
    """Explicit `only=` is not touched by the new default-projection logic."""
    # Double-quoted identifiers.
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

    sql, _ = _lite.compile_query(query)

    assert '"Company"."name"' in sql
    assert '*' not in sql.split('FROM')[0]


def test_subquery_from_empty_alias_falls_back_to_plain_asterisk() -> None:
    """`SubQueryStatement.alias=''` emits `SELECT *` (no table qualifier)."""
    inner = QueryStatement(table=SchemaReference(name='Company'))
    query = QueryStatement(
        only=None,
        table=SubQueryStatement(query=inner, alias=''),
        joins=[
            JoinQuery(
                table=SchemaReference(name='Employee', alias='rev_1'),
                on=_trivial_on(),
                join_type=JoinType.INNER,
            )
        ],
    )

    sql, _ = _lite.compile_query(query)

    projection = sql.split('FROM')[0]
    assert 'SELECT *' in projection


def test_only_field_reference_aliased_unchanged() -> None:
    """Aliased projection survives unchanged."""
    # Double-quoted identifiers.
    query = QueryStatement(
        only=[FieldReferenceAliased(field=Field(name='name'), table_name='Company', alias='company_name')],
        table=SchemaReference(name='Company'),
        joins=None,
    )

    sql, _ = _lite.compile_query(query)

    assert '"Company"."name" AS "company_name"' in sql
