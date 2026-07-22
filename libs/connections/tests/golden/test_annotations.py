from amsdal_glue_core.common.data_models.field_reference import Field
from amsdal_glue_core.common.data_models.field_reference import FieldReference
from amsdal_glue_core.common.data_models.query import QueryStatement
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.data_models.select_expression import SelectExpression
from amsdal_glue_core.common.data_models.sub_query import SubQueryStatement
from amsdal_glue_core.common.enums import Version
from amsdal_glue_core.common.expressions.field_reference import FieldReferenceExpression
from amsdal_glue_core.common.expressions.value import Value

from ._harness import lite
from ._harness import pg

# NOTE (evolved model): annotations=[AnnotationQuery(...)] is gone.  The new
# QueryStatement uses `only` (projection list) + `expressions` (extra SELECT
# items).  A pure annotation with no other columns is expressed as
# only=[] + expressions=[SelectExpression(expression=<value>, alias='...')].
# Without only=[] the generator emits SELECT *, <expr> — wrong projection.


def test_value_annotation_pg() -> None:
    q = QueryStatement(
        table=SchemaReference(name='users', version=Version.LATEST),
        only=[],
        expressions=[SelectExpression(expression=Value(value=1), alias='one')],
    )
    assert pg(q) == ('SELECT %s AS "one" FROM "users"', [1])


def test_value_annotation_lite() -> None:
    # SQLite uses ANSI double-quote identifiers.
    q = QueryStatement(
        table=SchemaReference(name='users', version=Version.LATEST),
        only=[],
        expressions=[SelectExpression(expression=Value(value=1), alias='one')],
    )
    assert lite(q) == ('SELECT ? AS "one" FROM "users"', [1])


def test_expression_annotation_pg() -> None:
    # No cosmetic parentheses around field references; SQL semantics unchanged.
    q = QueryStatement(
        table=SchemaReference(name='users', version=Version.LATEST),
        only=[],
        expressions=[
            SelectExpression(
                expression=FieldReferenceExpression(
                    field_reference=FieldReference(field=Field(name='age'), table_name='users'),
                ),
                alias='years',
            ),
        ],
    )
    assert pg(q) == ('SELECT "users"."age" AS "years" FROM "users"', [])


def test_expression_annotation_lite() -> None:
    # ANSI double quotes + no cosmetic parens.
    q = QueryStatement(
        table=SchemaReference(name='users', version=Version.LATEST),
        only=[],
        expressions=[
            SelectExpression(
                expression=FieldReferenceExpression(
                    field_reference=FieldReference(field=Field(name='age'), table_name='users'),
                ),
                alias='years',
            ),
        ],
    )
    assert lite(q) == ('SELECT "users"."age" AS "years" FROM "users"', [])


def test_subquery_annotation_pg() -> None:
    sub = SubQueryStatement(
        query=QueryStatement(table=SchemaReference(name='orders', version=Version.LATEST)),
        alias='order_q',
    )
    q = QueryStatement(
        table=SchemaReference(name='users', version=Version.LATEST),
        only=[],
        expressions=[SelectExpression(expression=sub, alias='order_q')],
    )
    assert pg(q) == ('SELECT (SELECT * FROM "orders") AS "order_q" FROM "users"', [])


def test_subquery_annotation_lite() -> None:
    # ANSI double quotes.
    sub = SubQueryStatement(
        query=QueryStatement(table=SchemaReference(name='orders', version=Version.LATEST)),
        alias='order_q',
    )
    q = QueryStatement(
        table=SchemaReference(name='users', version=Version.LATEST),
        only=[],
        expressions=[SelectExpression(expression=sub, alias='order_q')],
    )
    assert lite(q) == ('SELECT (SELECT * FROM "orders") AS "order_q" FROM "users"', [])
