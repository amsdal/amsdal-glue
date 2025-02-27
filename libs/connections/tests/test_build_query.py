import pytest
from amsdal_glue_core.common.data_models.aggregation import AggregationQuery
from amsdal_glue_core.common.data_models.annotation import AnnotationQuery
from amsdal_glue_core.common.data_models.annotation import ValueAnnotation
from amsdal_glue_core.common.data_models.conditions import Condition
from amsdal_glue_core.common.data_models.conditions import Conditions
from amsdal_glue_core.common.data_models.field_reference import Field
from amsdal_glue_core.common.data_models.field_reference import FieldReference
from amsdal_glue_core.common.data_models.field_reference import FieldReferenceAliased
from amsdal_glue_core.common.data_models.group_by import GroupByQuery
from amsdal_glue_core.common.data_models.join import JoinQuery
from amsdal_glue_core.common.data_models.limit import LimitQuery
from amsdal_glue_core.common.data_models.query import QueryStatement
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.data_models.sub_query import SubQueryStatement
from amsdal_glue_core.common.enums import FieldLookup
from amsdal_glue_core.common.enums import FilterConnector
from amsdal_glue_core.common.enums import JoinType
from amsdal_glue_core.common.enums import Version
from amsdal_glue_core.common.expressions.aggregation import Avg
from amsdal_glue_core.common.expressions.aggregation import Count
from amsdal_glue_core.common.expressions.aggregation import Max
from amsdal_glue_core.common.expressions.aggregation import Min
from amsdal_glue_core.common.expressions.aggregation import Sum
from amsdal_glue_core.common.expressions.field_reference import FieldReferenceExpression
from amsdal_glue_core.common.expressions.value import Value

from amsdal_glue_connections.sql.connections.postgres_connection import get_pg_transform
from amsdal_glue_connections.sql.sql_builders.query_builder import build_sql_query


def test_build_sql_query_simple() -> None:
    sql, value = build_sql_query(
        query=QueryStatement(
            table=SchemaReference(name='users', version=Version.LATEST),
        ),
        transform=get_pg_transform(),
    )

    assert sql == 'SELECT * FROM "users"'
    assert value == []


def test_build_sql_query_simple__only() -> None:
    sql, value = build_sql_query(
        query=QueryStatement(
            table=SchemaReference(name='users', version=Version.LATEST, alias='u'),
            only=[
                FieldReference(field=Field(name='full_name'), table_name='u'),
                FieldReferenceAliased(field=Field(name='age'), table_name='u', alias='user_age'),
            ],
        ),
        transform=get_pg_transform(),
    )

    assert sql == 'SELECT "u"."full_name", "u"."age" AS "user_age" FROM "users" AS "u"'
    assert value == []


def test_build_sql_query_simple_with_namespace__only() -> None:
    sql, value = build_sql_query(
        query=QueryStatement(
            table=SchemaReference(name='users', namespace='my_schema', version=Version.LATEST, alias='u'),
            only=[
                FieldReference(field=Field(name='full_name'), table_name='u'),
                FieldReferenceAliased(field=Field(name='age'), table_name='u', alias='user_age'),
            ],
        ),
        transform=get_pg_transform(),
    )

    assert sql == 'SELECT "u"."full_name", "u"."age" AS "user_age" FROM "my_schema"."users" AS "u"'
    assert value == []


def test_build_sql_query_simple__annotations() -> None:
    sql, value = build_sql_query(
        query=QueryStatement(
            table=SchemaReference(name='users', version=Version.LATEST, alias='u'),
            annotations=[
                AnnotationQuery(
                    value=SubQueryStatement(
                        query=QueryStatement(
                            table=SchemaReference(name='user_roles', version=Version.LATEST, alias='ur'),
                            only=[
                                FieldReference(field=Field(name='role'), table_name='ur'),
                            ],
                            limit=LimitQuery(limit=1),
                        ),
                        alias='role',
                    ),
                ),
                AnnotationQuery(
                    value=ValueAnnotation(
                        value=Value(100),
                        alias='max_age',
                    ),
                ),
                AnnotationQuery(
                    value=ValueAnnotation(
                        value=Value('hello'),
                        alias='custom_greeting',
                    ),
                ),
            ],
        ),
        transform=get_pg_transform(),
    )

    assert sql == (
        'SELECT '
        '(SELECT "ur"."role" FROM "user_roles" AS "ur" LIMIT 1) AS "role", '
        '%s AS "max_age", '
        '%s AS "custom_greeting" '
        'FROM "users" AS "u"'
    )
    assert value == [100, 'hello']


def test_build_sql_query_simple_with_namespace__annotations() -> None:
    sql, value = build_sql_query(
        query=QueryStatement(
            table=SchemaReference(name='users', namespace='ns1', version=Version.LATEST, alias='u'),
            annotations=[
                AnnotationQuery(
                    value=SubQueryStatement(
                        query=QueryStatement(
                            table=SchemaReference(
                                name='user_roles', namespace='ns2', version=Version.LATEST, alias='ur'
                            ),
                            only=[
                                FieldReference(field=Field(name='role'), table_name='ur'),
                            ],
                            limit=LimitQuery(limit=1),
                        ),
                        alias='role',
                    ),
                ),
                AnnotationQuery(
                    value=ValueAnnotation(
                        value=Value(100),
                        alias='max_age',
                    ),
                ),
                AnnotationQuery(
                    value=ValueAnnotation(
                        value=Value('hello'),
                        alias='custom_greeting',
                    ),
                ),
            ],
        ),
        transform=get_pg_transform(),
    )

    assert sql == (
        'SELECT '
        '(SELECT "ur"."role" FROM "ns2"."user_roles" AS "ur" LIMIT 1) AS "role", '
        '%s AS "max_age", '
        '%s AS "custom_greeting" '
        'FROM "ns1"."users" AS "u"'
    )
    assert value == [100, 'hello']


def test_build_sql_query_simple__aggregations() -> None:
    sql, value = build_sql_query(
        query=QueryStatement(
            table=SchemaReference(name='users', version=Version.LATEST, alias='u'),
            aggregations=[
                AggregationQuery(
                    expression=Sum(field=FieldReference(field=Field(name='amount'), table_name='u')),
                    alias='total_amount',
                ),
                AggregationQuery(
                    expression=Min(field=FieldReference(field=Field(name='amount'), table_name='u')),
                    alias='min_amount',
                ),
                AggregationQuery(
                    expression=Max(field=FieldReference(field=Field(name='amount'), table_name='u')),
                    alias='max_amount',
                ),
                AggregationQuery(
                    expression=Count(field=FieldReference(field=Field(name='id'), table_name='u')),
                    alias='total_count',
                ),
                AggregationQuery(
                    expression=Avg(field=FieldReference(field=Field(name='id'), table_name='u')),
                    alias='avg_count',
                ),
            ],
        ),
        transform=get_pg_transform(),
    )

    assert sql == (
        'SELECT '
        'SUM("u"."amount") AS "total_amount", '
        'MIN("u"."amount") AS "min_amount", '
        'MAX("u"."amount") AS "max_amount", '
        'COUNT("u"."id") AS "total_count", '
        'AVG("u"."id") AS "avg_count" '
        'FROM "users" AS "u"'
    )
    assert value == []


def test_build_sql_query_simple__where() -> None:
    sql, value = build_sql_query(
        query=QueryStatement(
            table=SchemaReference(name='users', version=Version.LATEST, alias='u'),
            where=Conditions(
                Condition(
                    left=FieldReferenceExpression(
                        field_reference=FieldReference(field=Field(name='age'), table_name='u')
                    ),
                    lookup=FieldLookup.GTE,
                    right=Value(18),
                ),
                Conditions(
                    Condition(
                        left=FieldReferenceExpression(
                            field_reference=FieldReference(field=Field(name='name'), table_name='u')
                        ),
                        lookup=FieldLookup.CONTAINS,
                        right=Value('John'),
                    ),
                    Condition(
                        left=FieldReferenceExpression(
                            field_reference=FieldReference(field=Field(name='email'), table_name='u')
                        ),
                        lookup=FieldLookup.ISTARTSWITH,
                        right=Value('john'),
                    ),
                    connector=FilterConnector.OR,
                ),
            ),
        ),
        transform=get_pg_transform(),
    )

    assert sql == (
        'SELECT * FROM "users" AS "u" WHERE ("u"."age" >= %s AND "u"."name" LIKE %s) OR '
        '("u"."age" >= %s AND LOWER("u"."email") LIKE %s)'
    )
    assert value == [18, '*John*', 18, 'john%']


@pytest.mark.parametrize('join_type', [JoinType.INNER, JoinType.LEFT, JoinType.RIGHT, JoinType.FULL])
def test_build_sql_query_simple__joins(join_type) -> None:
    sql, value = build_sql_query(
        query=QueryStatement(
            table=SchemaReference(name='users', version=Version.LATEST, alias='u'),
            joins=[
                JoinQuery(
                    table=SchemaReference(name='user_roles', version=Version.LATEST, alias='ur'),
                    on=Conditions(
                        Condition(
                            left=FieldReferenceExpression(
                                field_reference=FieldReference(field=Field(name='user_id'), table_name='ur')
                            ),
                            lookup=FieldLookup.EQ,
                            right=FieldReferenceExpression(
                                field_reference=FieldReference(field=Field(name='id'), table_name='u')
                            ),
                        ),
                    ),
                    join_type=join_type,
                ),
            ],
        ),
        transform=get_pg_transform(),
    )

    assert (
        sql == f'SELECT * FROM "users" AS "u" {join_type.value} JOIN "user_roles" AS "ur" ON "ur"."user_id" = "u"."id"'  # noqa: S608
    )
    assert value == []


@pytest.mark.parametrize('join_type', [JoinType.INNER, JoinType.LEFT, JoinType.RIGHT, JoinType.FULL])
def test_build_sql_query_simple_with_namespace__joins(join_type) -> None:
    sql, value = build_sql_query(
        query=QueryStatement(
            table=SchemaReference(name='users', namespace='ns1', version=Version.LATEST, alias='u'),
            joins=[
                JoinQuery(
                    table=SchemaReference(name='user_roles', namespace='ns2', version=Version.LATEST, alias='ur'),
                    on=Conditions(
                        Condition(
                            left=FieldReferenceExpression(
                                field_reference=FieldReference(field=Field(name='user_id'), table_name='ur')
                            ),
                            lookup=FieldLookup.EQ,
                            right=FieldReferenceExpression(
                                field_reference=FieldReference(field=Field(name='id'), table_name='u')
                            ),
                        ),
                    ),
                    join_type=join_type,
                ),
            ],
        ),
        transform=get_pg_transform(),
    )

    assert sql == (
        f'SELECT * FROM "ns1"."users" AS "u" {join_type.value} JOIN '  # noqa: S608
        '"ns2"."user_roles" AS "ur" ON "ur"."user_id" = "u"."id"'
    )
    assert value == []


def test_build_sql_query_simple__group_by() -> None:
    sql, value = build_sql_query(
        query=QueryStatement(
            table=SchemaReference(name='users', version=Version.LATEST, alias='u'),
            aggregations=[
                AggregationQuery(
                    expression=Sum(field=FieldReference(field=Field(name='amount'), table_name='u')),
                    alias='amount_per_role',
                ),
            ],
            group_by=[
                GroupByQuery(field=FieldReference(field=Field(name='role_id'), table_name='u')),
            ],
        ),
        transform=get_pg_transform(),
    )

    assert sql == 'SELECT SUM("u"."amount") AS "amount_per_role" FROM "users" AS "u" GROUP BY "u"."role_id"'
    assert value == []


def test_build_sql_query_simple__limit() -> None:
    sql, value = build_sql_query(
        query=QueryStatement(
            table=SchemaReference(name='users', version=Version.LATEST, alias='u'),
            limit=LimitQuery(limit=10, offset=20),
        ),
        transform=get_pg_transform(),
    )

    assert sql == 'SELECT * FROM "users" AS "u" LIMIT 10 OFFSET 20'
    assert value == []


def test_build_sql_query_complex() -> None:
    sql, value = build_sql_query(
        query=QueryStatement(
            table=SubQueryStatement(
                query=QueryStatement(
                    table=SchemaReference(name='users', version=Version.LATEST, alias='u'),
                    where=Conditions(
                        Condition(
                            left=FieldReferenceExpression(
                                field_reference=FieldReference(field=Field(name='age'), table_name='u')
                            ),
                            lookup=FieldLookup.GTE,
                            right=Value(18),
                        ),
                    ),
                ),
                alias='sub',
            ),
        ),
        transform=get_pg_transform(),
    )

    assert sql == 'SELECT * FROM (SELECT * FROM "users" AS "u" WHERE "u"."age" >= %s) AS "sub"'
    assert value == [18]


def test_build_sql_query_complex_with_namespace() -> None:
    sql, value = build_sql_query(
        query=QueryStatement(
            table=SubQueryStatement(
                query=QueryStatement(
                    table=SchemaReference(name='users', namespace='ns1', version=Version.LATEST, alias='u'),
                    where=Conditions(
                        Condition(
                            left=FieldReferenceExpression(
                                field_reference=FieldReference(field=Field(name='age'), table_name='u')
                            ),
                            lookup=FieldLookup.GTE,
                            right=Value(18),
                        ),
                    ),
                ),
                alias='sub',
            ),
        ),
        transform=get_pg_transform(),
    )

    assert sql == 'SELECT * FROM (SELECT * FROM "ns1"."users" AS "u" WHERE "u"."age" >= %s) AS "sub"'
    assert value == [18]


def test_build_sql_query_complex_joins() -> None:
    sql, value = build_sql_query(
        query=QueryStatement(
            table=SubQueryStatement(
                query=QueryStatement(
                    table=SchemaReference(name='users', version=Version.LATEST, alias='u'),
                    where=Conditions(
                        Condition(
                            left=FieldReferenceExpression(
                                field_reference=FieldReference(field=Field(name='age'), table_name='u')
                            ),
                            lookup=FieldLookup.GTE,
                            right=Value(18),
                        ),
                    ),
                ),
                alias='sub',
            ),
            joins=[
                JoinQuery(
                    table=SubQueryStatement(
                        query=QueryStatement(
                            table=SchemaReference(name='user_roles', version=Version.LATEST, alias='ur'),
                            only=[
                                FieldReference(field=Field(name='role'), table_name='ur'),
                            ],
                            where=Conditions(
                                Condition(
                                    left=FieldReferenceExpression(
                                        field_reference=FieldReference(field=Field(name='role'), table_name='ur')
                                    ),
                                    lookup=FieldLookup.STARTSWITH,
                                    right=Value('staff_'),
                                ),
                            ),
                        ),
                        alias='ur',
                    ),
                    on=Conditions(
                        Condition(
                            left=FieldReferenceExpression(
                                field_reference=FieldReference(field=Field(name='user_id'), table_name='ur')
                            ),
                            lookup=FieldLookup.EQ,
                            right=FieldReferenceExpression(
                                field_reference=FieldReference(field=Field(name='id'), table_name='sub')
                            ),
                        ),
                    ),
                    join_type=JoinType.LEFT,
                ),
            ],
        ),
        transform=get_pg_transform(),
    )

    assert sql == (
        'SELECT * FROM '
        '(SELECT * FROM "users" AS "u" WHERE "u"."age" >= %s) AS "sub" '
        'LEFT JOIN (SELECT "ur"."role" FROM "user_roles" AS "ur" WHERE "ur"."role" LIKE %s) AS "ur" '
        'ON "ur"."user_id" = "sub"."id"'
    )
    assert value == [18, 'staff_%']


def test_build_sql_query_complex_joins_with_namespace() -> None:
    sql, value = build_sql_query(
        query=QueryStatement(
            table=SubQueryStatement(
                query=QueryStatement(
                    table=SchemaReference(name='users', namespace='ns1', version=Version.LATEST, alias='u'),
                    where=Conditions(
                        Condition(
                            left=FieldReferenceExpression(
                                field_reference=FieldReference(field=Field(name='age'), table_name='u')
                            ),
                            lookup=FieldLookup.GTE,
                            right=Value(18),
                        ),
                    ),
                ),
                alias='sub',
            ),
            joins=[
                JoinQuery(
                    table=SubQueryStatement(
                        query=QueryStatement(
                            table=SchemaReference(
                                name='user_roles',
                                namespace='ns2',
                                version=Version.LATEST,
                                alias='ur',
                            ),
                            only=[
                                FieldReference(field=Field(name='role'), table_name='ur'),
                            ],
                            where=Conditions(
                                Condition(
                                    left=FieldReferenceExpression(
                                        field_reference=FieldReference(field=Field(name='role'), table_name='ur')
                                    ),
                                    lookup=FieldLookup.STARTSWITH,
                                    right=Value('staff_'),
                                ),
                            ),
                        ),
                        alias='ur',
                    ),
                    on=Conditions(
                        Condition(
                            left=FieldReferenceExpression(
                                field_reference=FieldReference(field=Field(name='user_id'), table_name='ur')
                            ),
                            lookup=FieldLookup.EQ,
                            right=FieldReferenceExpression(
                                field_reference=FieldReference(field=Field(name='id'), table_name='sub')
                            ),
                        ),
                    ),
                    join_type=JoinType.LEFT,
                ),
            ],
        ),
        transform=get_pg_transform(),
    )

    assert sql == (
        'SELECT * FROM '
        '(SELECT * FROM "ns1"."users" AS "u" WHERE "u"."age" >= %s) AS "sub" '
        'LEFT JOIN (SELECT "ur"."role" FROM "ns2"."user_roles" AS "ur" WHERE "ur"."role" LIKE %s) AS "ur" '
        'ON "ur"."user_id" = "sub"."id"'
    )
    assert value == [18, 'staff_%']


def test_build_sql_query_complex_with_namespaces_without_aliases() -> None:
    sql, value = build_sql_query(
        query=QueryStatement(
            table=SubQueryStatement(
                query=QueryStatement(
                    table=SchemaReference(name='users', namespace='ns1', version=Version.LATEST),
                    where=Conditions(
                        Condition(
                            left=FieldReferenceExpression(
                                field_reference=FieldReference(
                                    field=Field(name='age'), table_name='users', namespace='ns1'
                                )
                            ),
                            lookup=FieldLookup.GTE,
                            right=Value(18),
                        ),
                    ),
                ),
                alias='sub',
            ),
            joins=[
                JoinQuery(
                    table=SubQueryStatement(
                        query=QueryStatement(
                            table=SchemaReference(name='user_roles', namespace='ns2', version=Version.LATEST),
                            only=[
                                FieldReference(field=Field(name='role'), table_name='user_roles', namespace='ns2'),
                            ],
                            where=Conditions(
                                Condition(
                                    left=FieldReferenceExpression(
                                        field_reference=FieldReference(
                                            field=Field(name='role'),
                                            table_name='user_roles',
                                            namespace='ns2',
                                        )
                                    ),
                                    lookup=FieldLookup.STARTSWITH,
                                    right=Value('staff_'),
                                ),
                            ),
                        ),
                        alias='ur',
                    ),
                    on=Conditions(
                        Condition(
                            left=FieldReferenceExpression(
                                field_reference=FieldReference(field=Field(name='user_id'), table_name='ur')
                            ),
                            lookup=FieldLookup.EQ,
                            right=FieldReferenceExpression(
                                field_reference=FieldReference(field=Field(name='id'), table_name='sub')
                            ),
                        ),
                    ),
                    join_type=JoinType.LEFT,
                ),
            ],
        ),
        transform=get_pg_transform(),
    )

    assert sql == (
        'SELECT * FROM '
        '(SELECT * FROM "ns1"."users" WHERE "ns1"."users"."age" >= %s) AS "sub" '
        'LEFT JOIN ('
        'SELECT "ns2"."user_roles"."role" FROM "ns2"."user_roles" WHERE "ns2"."user_roles"."role" LIKE %s) AS "ur" '
        'ON "ur"."user_id" = "sub"."id"'
    )
    assert value == [18, 'staff_%']
