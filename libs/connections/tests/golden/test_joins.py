import pytest
from amsdal_glue_core.common.data_models.conditions import Condition
from amsdal_glue_core.common.data_models.conditions import Conditions
from amsdal_glue_core.common.data_models.field_reference import Field
from amsdal_glue_core.common.data_models.field_reference import FieldReference
from amsdal_glue_core.common.data_models.join import JoinQuery
from amsdal_glue_core.common.data_models.query import QueryStatement
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.data_models.sub_query import SubQueryStatement
from amsdal_glue_core.common.enums import FieldLookup
from amsdal_glue_core.common.enums import JoinType
from amsdal_glue_core.common.enums import Version
from amsdal_glue_core.common.expressions.field_reference import FieldReferenceExpression

from ._harness import lite
from ._harness import pg


def _on() -> Conditions:
    return Conditions(
        Condition(
            left=FieldReferenceExpression(
                field_reference=FieldReference(field=Field(name='id'), table_name='users'),
            ),
            lookup=FieldLookup.EQ,
            right=FieldReferenceExpression(
                field_reference=FieldReference(field=Field(name='user_id'), table_name='orders'),
            ),
        ),
    )


def _q(join_type: JoinType) -> QueryStatement:
    return QueryStatement(
        table=SchemaReference(name='users', version=Version.LATEST),
        joins=[
            JoinQuery(
                table=SchemaReference(name='orders', version=Version.LATEST),
                on=_on(),
                join_type=join_type,
            ),
        ],
    )


EXPECTED_PG: dict[str, tuple[str, list]] = {
    'INNER': ('SELECT "users".* FROM "users" INNER JOIN "orders" ON "users"."id" = "orders"."user_id"', []),
    'LEFT': ('SELECT "users".* FROM "users" LEFT JOIN "orders" ON "users"."id" = "orders"."user_id"', []),
    'RIGHT': ('SELECT "users".* FROM "users" RIGHT JOIN "orders" ON "users"."id" = "orders"."user_id"', []),
    'FULL': ('SELECT "users".* FROM "users" FULL JOIN "orders" ON "users"."id" = "orders"."user_id"', []),
}

# KNOWN-DIVERGENCE (migration): SQLite only supports RIGHT JOIN since v3.39.0 and does not
# support FULL JOIN at all. The builder emits RIGHT/FULL JOIN SQL without raising; asserting
# the current output here. These tests characterise a build-time quirk: the SQL may fail at
# execute time on older SQLite or for FULL joins on any SQLite version.
EXPECTED_LITE: dict[str, tuple[str, list]] = {
    'INNER': ("SELECT 'users'.* FROM 'users' INNER JOIN 'orders' ON 'users'.'id' = 'orders'.'user_id'", []),
    'LEFT': ("SELECT 'users'.* FROM 'users' LEFT JOIN 'orders' ON 'users'.'id' = 'orders'.'user_id'", []),
    'RIGHT': ("SELECT 'users'.* FROM 'users' RIGHT JOIN 'orders' ON 'users'.'id' = 'orders'.'user_id'", []),
    'FULL': ("SELECT 'users'.* FROM 'users' FULL JOIN 'orders' ON 'users'.'id' = 'orders'.'user_id'", []),
}


@pytest.mark.parametrize('join_type', list(JoinType), ids=[j.name for j in JoinType])
def test_join_pg(join_type: JoinType) -> None:
    sql, params = pg(_q(join_type))
    assert (sql, params) == EXPECTED_PG[join_type.name]


@pytest.mark.parametrize('join_type', list(JoinType), ids=[j.name for j in JoinType])
def test_join_lite(join_type: JoinType) -> None:
    # KNOWN-DIVERGENCE (migration): RIGHT and FULL join types are emitted by the builder
    # without error but RIGHT JOIN requires SQLite >= 3.39.0 and FULL JOIN is unsupported
    # by SQLite entirely. The assertions below lock in the current builder output.
    sql, params = lite(_q(join_type))
    assert (sql, params) == EXPECTED_LITE[join_type.name]


def test_multiple_joins_pg() -> None:
    q = QueryStatement(
        table=SchemaReference(name='users', version=Version.LATEST),
        joins=[
            JoinQuery(table=SchemaReference(name='orders', version=Version.LATEST), on=_on(), join_type=JoinType.LEFT),
            JoinQuery(
                table=SchemaReference(name='payments', version=Version.LATEST),
                on=Conditions(
                    Condition(
                        left=FieldReferenceExpression(
                            field_reference=FieldReference(field=Field(name='id'), table_name='orders'),
                        ),
                        lookup=FieldLookup.EQ,
                        right=FieldReferenceExpression(
                            field_reference=FieldReference(field=Field(name='order_id'), table_name='payments'),
                        ),
                    ),
                ),
                join_type=JoinType.INNER,
            ),
        ],
    )
    assert pg(q) == (
        'SELECT "users".* FROM "users" LEFT JOIN "orders" ON "users"."id" = "orders"."user_id"'
        ' INNER JOIN "payments" ON "orders"."id" = "payments"."order_id"',
        [],
    )


def test_multiple_joins_lite() -> None:
    q = QueryStatement(
        table=SchemaReference(name='users', version=Version.LATEST),
        joins=[
            JoinQuery(table=SchemaReference(name='orders', version=Version.LATEST), on=_on(), join_type=JoinType.LEFT),
            JoinQuery(
                table=SchemaReference(name='payments', version=Version.LATEST),
                on=Conditions(
                    Condition(
                        left=FieldReferenceExpression(
                            field_reference=FieldReference(field=Field(name='id'), table_name='orders'),
                        ),
                        lookup=FieldLookup.EQ,
                        right=FieldReferenceExpression(
                            field_reference=FieldReference(field=Field(name='order_id'), table_name='payments'),
                        ),
                    ),
                ),
                join_type=JoinType.INNER,
            ),
        ],
    )
    assert lite(q) == (
        "SELECT 'users'.* FROM 'users' LEFT JOIN 'orders' ON 'users'.'id' = 'orders'.'user_id'"
        " INNER JOIN 'payments' ON 'orders'.'id' = 'payments'.'order_id'",
        [],
    )


def test_subquery_join_pg() -> None:
    subq = SubQueryStatement(
        query=QueryStatement(
            table=SchemaReference(name='orders', version=Version.LATEST),
        ),
        alias='o',
    )
    q = QueryStatement(
        table=SchemaReference(name='users', version=Version.LATEST),
        joins=[
            JoinQuery(
                table=subq,
                on=Conditions(
                    Condition(
                        left=FieldReferenceExpression(
                            field_reference=FieldReference(field=Field(name='id'), table_name='users'),
                        ),
                        lookup=FieldLookup.EQ,
                        right=FieldReferenceExpression(
                            field_reference=FieldReference(field=Field(name='user_id'), table_name='o'),
                        ),
                    ),
                ),
                join_type=JoinType.INNER,
            ),
        ],
    )
    assert pg(q) == (
        'SELECT "users".* FROM "users" INNER JOIN (SELECT * FROM "orders") AS "o" ON "users"."id" = "o"."user_id"',
        [],
    )


def test_subquery_join_lite() -> None:
    subq = SubQueryStatement(
        query=QueryStatement(
            table=SchemaReference(name='orders', version=Version.LATEST),
        ),
        alias='o',
    )
    q = QueryStatement(
        table=SchemaReference(name='users', version=Version.LATEST),
        joins=[
            JoinQuery(
                table=subq,
                on=Conditions(
                    Condition(
                        left=FieldReferenceExpression(
                            field_reference=FieldReference(field=Field(name='id'), table_name='users'),
                        ),
                        lookup=FieldLookup.EQ,
                        right=FieldReferenceExpression(
                            field_reference=FieldReference(field=Field(name='user_id'), table_name='o'),
                        ),
                    ),
                ),
                join_type=JoinType.INNER,
            ),
        ],
    )
    assert lite(q) == (
        "SELECT 'users'.* FROM 'users' INNER JOIN (SELECT * FROM 'orders') AS 'o' ON 'users'.'id' = 'o'.'user_id'",
        [],
    )
