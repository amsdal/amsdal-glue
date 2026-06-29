import pytest
from amsdal_glue_core.common.data_models.aggregation import AggregationQuery
from amsdal_glue_core.common.data_models.field_reference import Field
from amsdal_glue_core.common.data_models.field_reference import FieldReference
from amsdal_glue_core.common.data_models.group_by import GroupByQuery
from amsdal_glue_core.common.data_models.query import QueryStatement
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.enums import Version
from amsdal_glue_core.common.expressions.aggregation import Avg
from amsdal_glue_core.common.expressions.aggregation import Count
from amsdal_glue_core.common.expressions.aggregation import Max
from amsdal_glue_core.common.expressions.aggregation import Min
from amsdal_glue_core.common.expressions.aggregation import Sum

from ._harness import lite
from ._harness import pg


def _ref(name: str, table: str = 'orders') -> FieldReference:
    return FieldReference(field=Field(name=name), table_name=table)


AGGS = [
    ('count', Count(field=_ref('id'))),
    ('sum', Sum(field=_ref('amount'))),
    ('avg', Avg(field=_ref('amount'))),
    ('min', Min(field=_ref('amount'))),
    ('max', Max(field=_ref('amount'))),
]

EXPECTED_AGG_PG: dict[str, tuple[str, list]] = {
    'count': ('SELECT COUNT("orders"."id") AS "count_value" FROM "orders"', []),
    'sum': ('SELECT SUM("orders"."amount") AS "sum_value" FROM "orders"', []),
    'avg': ('SELECT AVG("orders"."amount") AS "avg_value" FROM "orders"', []),
    'min': ('SELECT MIN("orders"."amount") AS "min_value" FROM "orders"', []),
    'max': ('SELECT MAX("orders"."amount") AS "max_value" FROM "orders"', []),
}

EXPECTED_AGG_LITE: dict[str, tuple[str, list]] = {
    'count': ("SELECT COUNT('orders'.'id') AS 'count_value' FROM 'orders'", []),
    'sum': ("SELECT SUM('orders'.'amount') AS 'sum_value' FROM 'orders'", []),
    'avg': ("SELECT AVG('orders'.'amount') AS 'avg_value' FROM 'orders'", []),
    'min': ("SELECT MIN('orders'.'amount') AS 'min_value' FROM 'orders'", []),
    'max': ("SELECT MAX('orders'.'amount') AS 'max_value' FROM 'orders'", []),
}


@pytest.mark.parametrize(('name', 'expr'), AGGS, ids=[a[0] for a in AGGS])
def test_aggregation_pg(name: str, expr: object) -> None:
    q = QueryStatement(
        table=SchemaReference(name='orders', version=Version.LATEST),
        aggregations=[AggregationQuery(expression=expr, alias=f'{name}_value')],  # type: ignore[arg-type]
    )
    assert pg(q) == EXPECTED_AGG_PG[name]


@pytest.mark.parametrize(('name', 'expr'), AGGS, ids=[a[0] for a in AGGS])
def test_aggregation_lite(name: str, expr: object) -> None:
    q = QueryStatement(
        table=SchemaReference(name='orders', version=Version.LATEST),
        aggregations=[AggregationQuery(expression=expr, alias=f'{name}_value')],  # type: ignore[arg-type]
    )
    assert lite(q) == EXPECTED_AGG_LITE[name]


def test_group_by_single_pg() -> None:
    q = QueryStatement(
        table=SchemaReference(name='orders', version=Version.LATEST),
        group_by=[GroupByQuery(field=_ref('customer_id'))],
        aggregations=[AggregationQuery(expression=Count(field=_ref('id')), alias='cnt')],
    )
    assert pg(q) == (
        'SELECT COUNT("orders"."id") AS "cnt" FROM "orders" GROUP BY "orders"."customer_id"',
        [],
    )


def test_group_by_single_lite() -> None:
    q = QueryStatement(
        table=SchemaReference(name='orders', version=Version.LATEST),
        group_by=[GroupByQuery(field=_ref('customer_id'))],
        aggregations=[AggregationQuery(expression=Count(field=_ref('id')), alias='cnt')],
    )
    assert lite(q) == (
        "SELECT COUNT('orders'.'id') AS 'cnt' FROM 'orders' GROUP BY 'orders'.'customer_id'",
        [],
    )


def test_group_by_multi_pg() -> None:
    # KNOWN-DIVERGENCE (migration): builder emits `SELECT *` with no aggregations/only-fields,
    # which is invalid PostgreSQL — non-grouped columns in SELECT violate SQL standard GROUP BY
    # rules and PostgreSQL will reject it. The correct SQL would be:
    #   SELECT "orders"."customer_id", "orders"."status"
    #   FROM "orders" GROUP BY "orders"."customer_id", "orders"."status"
    # The `SELECT *` here is a synthetic-input artifact (no `only`/aggregations were provided).
    # Assertion kept as-is to characterise current builder output.
    q = QueryStatement(
        table=SchemaReference(name='orders', version=Version.LATEST),
        group_by=[GroupByQuery(field=_ref('customer_id')), GroupByQuery(field=_ref('status'))],
    )
    assert pg(q) == (
        'SELECT * FROM "orders" GROUP BY "orders"."customer_id", "orders"."status"',
        [],
    )


def test_group_by_multi_lite() -> None:
    # SQLite permissively allows SELECT * with GROUP BY (executes, picks an arbitrary row per
    # group for non-grouped columns) — no divergence marker needed.
    q = QueryStatement(
        table=SchemaReference(name='orders', version=Version.LATEST),
        group_by=[GroupByQuery(field=_ref('customer_id')), GroupByQuery(field=_ref('status'))],
    )
    assert lite(q) == (
        "SELECT * FROM 'orders' GROUP BY 'orders'.'customer_id', 'orders'.'status'",
        [],
    )


def test_group_by_multi_agg_pg() -> None:
    # Realistic case: multi-field GROUP BY combined with an aggregation.
    q = QueryStatement(
        table=SchemaReference(name='orders', version=Version.LATEST),
        group_by=[GroupByQuery(field=_ref('customer_id')), GroupByQuery(field=_ref('status'))],
        aggregations=[AggregationQuery(expression=Count(field=_ref('id')), alias='cnt')],
    )
    assert pg(q) == (
        'SELECT COUNT("orders"."id") AS "cnt" FROM "orders" GROUP BY "orders"."customer_id", "orders"."status"',
        [],
    )


def test_group_by_multi_agg_lite() -> None:
    # Realistic case: multi-field GROUP BY combined with an aggregation.
    q = QueryStatement(
        table=SchemaReference(name='orders', version=Version.LATEST),
        group_by=[GroupByQuery(field=_ref('customer_id')), GroupByQuery(field=_ref('status'))],
        aggregations=[AggregationQuery(expression=Count(field=_ref('id')), alias='cnt')],
    )
    assert lite(q) == (
        "SELECT COUNT('orders'.'id') AS 'cnt' FROM 'orders' GROUP BY 'orders'.'customer_id', 'orders'.'status'",
        [],
    )
