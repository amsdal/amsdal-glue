from amsdal_glue_core.common.data_models.annotation import AnnotationQuery
from amsdal_glue_core.common.data_models.annotation import ExpressionAnnotation
from amsdal_glue_core.common.data_models.annotation import ValueAnnotation
from amsdal_glue_core.common.data_models.field_reference import Field
from amsdal_glue_core.common.data_models.field_reference import FieldReference
from amsdal_glue_core.common.data_models.query import QueryStatement
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.data_models.sub_query import SubQueryStatement
from amsdal_glue_core.common.enums import Version
from amsdal_glue_core.common.expressions.field_reference import FieldReferenceExpression
from amsdal_glue_core.common.expressions.value import Value

from ._harness import lite
from ._harness import pg


def test_value_annotation_pg() -> None:
    q = QueryStatement(
        table=SchemaReference(name='users', version=Version.LATEST),
        annotations=[AnnotationQuery(value=ValueAnnotation(value=Value(value=1), alias='one'))],
    )
    assert pg(q) == ('SELECT %s AS "one" FROM "users"', [1])


def test_value_annotation_lite() -> None:
    q = QueryStatement(
        table=SchemaReference(name='users', version=Version.LATEST),
        annotations=[AnnotationQuery(value=ValueAnnotation(value=Value(value=1), alias='one'))],
    )
    assert lite(q) == ("SELECT ? AS 'one' FROM 'users'", [1])


def test_expression_annotation_pg() -> None:
    q = QueryStatement(
        table=SchemaReference(name='users', version=Version.LATEST),
        annotations=[
            AnnotationQuery(
                value=ExpressionAnnotation(
                    expression=FieldReferenceExpression(
                        field_reference=FieldReference(field=Field(name='age'), table_name='users'),
                    ),
                    alias='years',
                ),
            ),
        ],
    )
    assert pg(q) == ('SELECT ("users"."age") AS "years" FROM "users"', [])


def test_expression_annotation_lite() -> None:
    q = QueryStatement(
        table=SchemaReference(name='users', version=Version.LATEST),
        annotations=[
            AnnotationQuery(
                value=ExpressionAnnotation(
                    expression=FieldReferenceExpression(
                        field_reference=FieldReference(field=Field(name='age'), table_name='users'),
                    ),
                    alias='years',
                ),
            ),
        ],
    )
    assert lite(q) == ("SELECT ('users'.'age') AS 'years' FROM 'users'", [])


def test_subquery_annotation_pg() -> None:
    sub = SubQueryStatement(
        query=QueryStatement(table=SchemaReference(name='orders', version=Version.LATEST)),
        alias='order_q',
    )
    q = QueryStatement(
        table=SchemaReference(name='users', version=Version.LATEST),
        annotations=[AnnotationQuery(value=sub)],
    )
    assert pg(q) == ('SELECT (SELECT * FROM "orders") AS "order_q" FROM "users"', [])


def test_subquery_annotation_lite() -> None:
    sub = SubQueryStatement(
        query=QueryStatement(table=SchemaReference(name='orders', version=Version.LATEST)),
        alias='order_q',
    )
    q = QueryStatement(
        table=SchemaReference(name='users', version=Version.LATEST),
        annotations=[AnnotationQuery(value=sub)],
    )
    assert lite(q) == ("SELECT (SELECT * FROM 'orders') AS 'order_q' FROM 'users'", [])
