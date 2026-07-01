import pytest
from amsdal_glue_core.common.data_models.field_reference import Field
from amsdal_glue_core.common.data_models.field_reference import FieldReference
from amsdal_glue_core.common.data_models.group_by import GroupByQuery
from amsdal_glue_core.common.data_models.query import QueryStatement
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.data_models.select_expression import SelectExpression
from amsdal_glue_core.common.enums import Version
from amsdal_glue_core.common.expressions.aggregation import Avg
from amsdal_glue_core.common.expressions.aggregation import Count
from amsdal_glue_core.common.expressions.aggregation import Max
from amsdal_glue_core.common.expressions.aggregation import Min
from amsdal_glue_core.common.expressions.aggregation import Sum
from amsdal_glue_core.common.expressions.field_reference import FieldReferenceExpression

from ._harness import lite
from ._harness import pg

# NOTE (evolved model): the new QueryStatement separates the projection (`only`) from extra select
# items (`expressions`). The old `aggregations=` REPLACED the projection; the new `expressions=`
# ADD to it, and `only=None` defaults to `*`. So a pure aggregation `SELECT COUNT(...) FROM t` is
# `only=[]` + `expressions=[SelectExpression(Count(...))]`. Without `only=[]` the Rust generator
# (correctly) emits `SELECT *, COUNT(...)`.


def _ref(name: str, table: str = 'orders') -> FieldReference:
    return FieldReference(field=Field(name=name), table_name=table)


def _fexpr(name: str, table: str = 'orders') -> FieldReferenceExpression:
    return FieldReferenceExpression(field_reference=_ref(name, table))


AGGS = [
    ('count', Count(expression=_fexpr('id'))),
    ('sum', Sum(expression=_fexpr('amount'))),
    ('avg', Avg(expression=_fexpr('amount'))),
    ('min', Min(expression=_fexpr('amount'))),
    ('max', Max(expression=_fexpr('amount'))),
]

EXPECTED_AGG_PG: dict[str, tuple[str, list]] = {
    'count': ('SELECT COUNT("orders"."id") AS "count_value" FROM "orders"', []),
    'sum': ('SELECT SUM("orders"."amount") AS "sum_value" FROM "orders"', []),
    'avg': ('SELECT AVG("orders"."amount") AS "avg_value" FROM "orders"', []),
    'min': ('SELECT MIN("orders"."amount") AS "min_value" FROM "orders"', []),
    'max': ('SELECT MAX("orders"."amount") AS "max_value" FROM "orders"', []),
}

# SQLite now uses ANSI double-quote identifiers (old Python builder used single quotes) — valid.
EXPECTED_AGG_LITE: dict[str, tuple[str, list]] = {
    'count': ('SELECT COUNT("orders"."id") AS "count_value" FROM "orders"', []),
    'sum': ('SELECT SUM("orders"."amount") AS "sum_value" FROM "orders"', []),
    'avg': ('SELECT AVG("orders"."amount") AS "avg_value" FROM "orders"', []),
    'min': ('SELECT MIN("orders"."amount") AS "min_value" FROM "orders"', []),
    'max': ('SELECT MAX("orders"."amount") AS "max_value" FROM "orders"', []),
}


@pytest.mark.parametrize(('name', 'expr'), AGGS, ids=[a[0] for a in AGGS])
def test_aggregation_pg(name: str, expr: object) -> None:
    q = QueryStatement(
        table=SchemaReference(name='orders', version=Version.LATEST),
        only=[],
        expressions=[SelectExpression(expression=expr, alias=f'{name}_value')],  # type: ignore[arg-type]
    )
    assert pg(q) == EXPECTED_AGG_PG[name]


@pytest.mark.parametrize(('name', 'expr'), AGGS, ids=[a[0] for a in AGGS])
def test_aggregation_lite(name: str, expr: object) -> None:
    q = QueryStatement(
        table=SchemaReference(name='orders', version=Version.LATEST),
        only=[],
        expressions=[SelectExpression(expression=expr, alias=f'{name}_value')],  # type: ignore[arg-type]
    )
    assert lite(q) == EXPECTED_AGG_LITE[name]


def test_group_by_single_pg() -> None:
    q = QueryStatement(
        table=SchemaReference(name='orders', version=Version.LATEST),
        only=[],
        group_by=[GroupByQuery(expression=_fexpr('customer_id'))],
        expressions=[SelectExpression(expression=Count(expression=_fexpr('id')), alias='cnt')],
    )
    assert pg(q) == (
        'SELECT COUNT("orders"."id") AS "cnt" FROM "orders" GROUP BY "orders"."customer_id"',
        [],
    )


def test_group_by_single_lite() -> None:
    q = QueryStatement(
        table=SchemaReference(name='orders', version=Version.LATEST),
        only=[],
        group_by=[GroupByQuery(expression=_fexpr('customer_id'))],
        expressions=[SelectExpression(expression=Count(expression=_fexpr('id')), alias='cnt')],
    )
    assert lite(q) == (
        'SELECT COUNT("orders"."id") AS "cnt" FROM "orders" GROUP BY "orders"."customer_id"',
        [],
    )


def test_group_by_multi_pg() -> None:
    # No explicit projection (only=None) → SELECT * (the synthetic input provides no columns).
    q = QueryStatement(
        table=SchemaReference(name='orders', version=Version.LATEST),
        group_by=[GroupByQuery(expression=_fexpr('customer_id')), GroupByQuery(expression=_fexpr('status'))],
    )
    assert pg(q) == (
        'SELECT * FROM "orders" GROUP BY "orders"."customer_id", "orders"."status"',
        [],
    )


def test_group_by_multi_lite() -> None:
    q = QueryStatement(
        table=SchemaReference(name='orders', version=Version.LATEST),
        group_by=[GroupByQuery(expression=_fexpr('customer_id')), GroupByQuery(expression=_fexpr('status'))],
    )
    assert lite(q) == (
        'SELECT * FROM "orders" GROUP BY "orders"."customer_id", "orders"."status"',
        [],
    )


def test_group_by_multi_agg_pg() -> None:
    q = QueryStatement(
        table=SchemaReference(name='orders', version=Version.LATEST),
        only=[],
        group_by=[GroupByQuery(expression=_fexpr('customer_id')), GroupByQuery(expression=_fexpr('status'))],
        expressions=[SelectExpression(expression=Count(expression=_fexpr('id')), alias='cnt')],
    )
    assert pg(q) == (
        'SELECT COUNT("orders"."id") AS "cnt" FROM "orders" GROUP BY "orders"."customer_id", "orders"."status"',
        [],
    )


def test_group_by_multi_agg_lite() -> None:
    q = QueryStatement(
        table=SchemaReference(name='orders', version=Version.LATEST),
        only=[],
        group_by=[GroupByQuery(expression=_fexpr('customer_id')), GroupByQuery(expression=_fexpr('status'))],
        expressions=[SelectExpression(expression=Count(expression=_fexpr('id')), alias='cnt')],
    )
    assert lite(q) == (
        'SELECT COUNT("orders"."id") AS "cnt" FROM "orders" GROUP BY "orders"."customer_id", "orders"."status"',
        [],
    )
