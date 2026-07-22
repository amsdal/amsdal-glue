from amsdal_glue_core.common.data_models.field_reference import Field
from amsdal_glue_core.common.data_models.field_reference import FieldReference
from amsdal_glue_core.common.data_models.limit import LimitQuery
from amsdal_glue_core.common.data_models.order_by import OrderByQuery
from amsdal_glue_core.common.data_models.query import QueryStatement
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.enums import OrderDirection
from amsdal_glue_core.common.enums import Version
from amsdal_glue_core.common.expressions.field_reference import FieldReferenceExpression
from amsdal_glue_core.common.expressions.func import Func

from ._harness import lite
from ._harness import pg


def _ref(name: str) -> FieldReference:
    return FieldReference(field=Field(name=name), table_name='users')


def _ref_expr(name: str) -> FieldReferenceExpression:
    return FieldReferenceExpression(field_reference=_ref(name))


# ---------------------------------------------------------------------------
# ORDER BY ASC
# ---------------------------------------------------------------------------


def test_order_by_asc_pg() -> None:
    q = QueryStatement(
        table=SchemaReference(name='users', version=Version.LATEST),
        order_by=[
            OrderByQuery(
                expression=FieldReferenceExpression(field_reference=_ref('name')), direction=OrderDirection.ASC
            )
        ],
    )
    assert pg(q) == ('SELECT * FROM "users" ORDER BY "users"."name" ASC', [])


def test_order_by_asc_sqlite() -> None:
    q = QueryStatement(
        table=SchemaReference(name='users', version=Version.LATEST),
        order_by=[
            OrderByQuery(
                expression=FieldReferenceExpression(field_reference=_ref('name')), direction=OrderDirection.ASC
            )
        ],
    )
    # SQLite uses ANSI double-quoted identifiers.
    assert lite(q) == ('SELECT * FROM "users" ORDER BY "users"."name" ASC', [])


# ---------------------------------------------------------------------------
# ORDER BY DESC
# ---------------------------------------------------------------------------


def test_order_by_desc_pg() -> None:
    q = QueryStatement(
        table=SchemaReference(name='users', version=Version.LATEST),
        order_by=[
            OrderByQuery(
                expression=FieldReferenceExpression(field_reference=_ref('created_at')), direction=OrderDirection.DESC
            )
        ],
    )
    assert pg(q) == ('SELECT * FROM "users" ORDER BY "users"."created_at" DESC', [])


def test_order_by_desc_sqlite() -> None:
    q = QueryStatement(
        table=SchemaReference(name='users', version=Version.LATEST),
        order_by=[
            OrderByQuery(
                expression=FieldReferenceExpression(field_reference=_ref('created_at')), direction=OrderDirection.DESC
            )
        ],
    )
    # SQLite uses ANSI double-quoted identifiers.
    assert lite(q) == ('SELECT * FROM "users" ORDER BY "users"."created_at" DESC', [])


# ---------------------------------------------------------------------------
# ORDER BY multiple fields
# ---------------------------------------------------------------------------


def test_order_by_multi_pg() -> None:
    q = QueryStatement(
        table=SchemaReference(name='users', version=Version.LATEST),
        order_by=[
            OrderByQuery(
                expression=FieldReferenceExpression(field_reference=_ref('name')), direction=OrderDirection.ASC
            ),
            OrderByQuery(
                expression=FieldReferenceExpression(field_reference=_ref('created_at')), direction=OrderDirection.DESC
            ),
        ],
    )
    assert pg(q) == ('SELECT * FROM "users" ORDER BY "users"."name" ASC, "users"."created_at" DESC', [])


def test_order_by_multi_sqlite() -> None:
    q = QueryStatement(
        table=SchemaReference(name='users', version=Version.LATEST),
        order_by=[
            OrderByQuery(
                expression=FieldReferenceExpression(field_reference=_ref('name')), direction=OrderDirection.ASC
            ),
            OrderByQuery(
                expression=FieldReferenceExpression(field_reference=_ref('created_at')), direction=OrderDirection.DESC
            ),
        ],
    )
    # SQLite uses ANSI double-quoted identifiers.
    assert lite(q) == ('SELECT * FROM "users" ORDER BY "users"."name" ASC, "users"."created_at" DESC', [])


# ---------------------------------------------------------------------------
# LIMIT only
# ---------------------------------------------------------------------------


def test_limit_only_pg() -> None:
    q = QueryStatement(table=SchemaReference(name='users', version=Version.LATEST), limit=LimitQuery(limit=10))
    # LIMIT is parameterized (LIMIT %s, value in params).
    assert pg(q) == ('SELECT * FROM "users" LIMIT %s', [10])


def test_limit_only_sqlite() -> None:
    q = QueryStatement(table=SchemaReference(name='users', version=Version.LATEST), limit=LimitQuery(limit=10))
    # LIMIT is parameterized and identifiers are double-quoted.
    assert lite(q) == ('SELECT * FROM "users" LIMIT ?', [10])


# ---------------------------------------------------------------------------
# LIMIT + OFFSET
# ---------------------------------------------------------------------------


def test_limit_offset_pg() -> None:
    q = QueryStatement(
        table=SchemaReference(name='users', version=Version.LATEST),
        limit=LimitQuery(limit=10, offset=20),
    )
    # LIMIT/OFFSET values are parameterized.
    assert pg(q) == ('SELECT * FROM "users" LIMIT %s OFFSET %s', [10, 20])


def test_limit_offset_sqlite() -> None:
    q = QueryStatement(
        table=SchemaReference(name='users', version=Version.LATEST),
        limit=LimitQuery(limit=10, offset=20),
    )
    # LIMIT/OFFSET values are parameterized and identifiers are double-quoted.
    assert lite(q) == ('SELECT * FROM "users" LIMIT ? OFFSET ?', [10, 20])


# ---------------------------------------------------------------------------
# ORDER BY an arbitrary expression (expression-only OrderByQuery, no `field`)
# ---------------------------------------------------------------------------


def test_order_by_expression_upper_pg() -> None:
    # OrderByQuery is expression-only: ordering by a function needs no dummy field.
    q = QueryStatement(
        table=SchemaReference(name='users', version=Version.LATEST),
        order_by=[
            OrderByQuery(
                expression=Func(name='UPPER', args=[_ref_expr('name')]),
                direction=OrderDirection.ASC,
            ),
        ],
    )
    assert pg(q) == ('SELECT * FROM "users" ORDER BY UPPER("users"."name") ASC', [])


def test_order_by_expression_upper_sqlite() -> None:
    q = QueryStatement(
        table=SchemaReference(name='users', version=Version.LATEST),
        order_by=[
            OrderByQuery(
                expression=Func(name='UPPER', args=[_ref_expr('name')]),
                direction=OrderDirection.ASC,
            ),
        ],
    )
    assert lite(q) == ('SELECT * FROM "users" ORDER BY UPPER("users"."name") ASC', [])


def test_order_by_plain_field_via_expression_renders_identically() -> None:
    # A plain field wrapped in FieldReferenceExpression renders exactly like the
    # legacy `field=`-based ORDER BY did — no SQL change.
    q = QueryStatement(
        table=SchemaReference(name='users', version=Version.LATEST),
        order_by=[OrderByQuery(expression=_ref_expr('name'), direction=OrderDirection.ASC)],
    )
    assert pg(q) == ('SELECT * FROM "users" ORDER BY "users"."name" ASC', [])
    assert lite(q) == ('SELECT * FROM "users" ORDER BY "users"."name" ASC', [])


# ---------------------------------------------------------------------------
# Empty ORDER BY — an empty order-by list must NOT render a column-less `ORDER BY`
# (invalid SQL: "incomplete input"). It is omitted entirely, on both dialects.
# ---------------------------------------------------------------------------


def test_empty_order_by_omits_clause_pg() -> None:
    q = QueryStatement(table=SchemaReference(name='users', version=Version.LATEST), order_by=[])

    sql, _ = pg(q)

    assert sql == 'SELECT * FROM "users"'
    assert 'ORDER BY' not in sql


def test_empty_order_by_omits_clause_sqlite() -> None:
    q = QueryStatement(table=SchemaReference(name='users', version=Version.LATEST), order_by=[])

    sql, _ = lite(q)

    assert sql == 'SELECT * FROM "users"'
    assert 'ORDER BY' not in sql
