# libs/connections/tests/golden/test_expressions.py
"""Golden-master tests for expression rendering in the SQL generator.

Covers: Combined/arithmetic operators, Func (COALESCE/UPPER/…), RawExpression,
Cast, Case/WhenClause, Exists/NOT EXISTS, Window functions, vector operators,
JsonbArray, ArraySubquery, Collate, FTS helpers (SearchVector/SearchRank/
SearchHeadline), and aggregations with ORDER BY.

Each test calls our Rust-backed SqlGenerator and asserts the exact emitted
(sql, params) tuple — no live database required.
"""

import pytest
from amsdal_glue_connections._sql_core import SqlGenerator
from amsdal_glue_connections._sql_core import UnsupportedFeatureError
from amsdal_glue_core.common.data_models.conditions import Condition
from amsdal_glue_core.common.data_models.conditions import Conditions
from amsdal_glue_core.common.data_models.field_reference import Field
from amsdal_glue_core.common.data_models.field_reference import FieldReference
from amsdal_glue_core.common.data_models.order_by import OrderByQuery
from amsdal_glue_core.common.data_models.query import QueryStatement
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.data_models.select_expression import SelectExpression
from amsdal_glue_core.common.data_models.sub_query import SubQueryStatement
from amsdal_glue_core.common.enums import FieldLookup
from amsdal_glue_core.common.enums import OrderDirection
from amsdal_glue_core.common.enums import ScalarType
from amsdal_glue_core.common.enums import Version
from amsdal_glue_core.common.enums import WindowFrameType
from amsdal_glue_core.common.expressions.aggregation import Count
from amsdal_glue_core.common.expressions.aggregation import Sum
from amsdal_glue_core.common.expressions.array_subquery import ArraySubquery
from amsdal_glue_core.common.expressions.case import Case
from amsdal_glue_core.common.expressions.case import WhenClause
from amsdal_glue_core.common.expressions.cast import Cast
from amsdal_glue_core.common.expressions.collate import Collate
from amsdal_glue_core.common.expressions.combined import Combined
from amsdal_glue_core.common.expressions.exists import Exists
from amsdal_glue_core.common.expressions.field_reference import FieldReferenceExpression
from amsdal_glue_core.common.expressions.func import Func
from amsdal_glue_core.common.expressions.jsonb_array import JsonbArray
from amsdal_glue_core.common.expressions.raw import RawExpression
from amsdal_glue_core.common.expressions.search import SearchHeadline
from amsdal_glue_core.common.expressions.search import SearchQuery
from amsdal_glue_core.common.expressions.search import SearchRank
from amsdal_glue_core.common.expressions.search import SearchVector
from amsdal_glue_core.common.expressions.value import Value
from amsdal_glue_core.common.expressions.vector import CosineDistance
from amsdal_glue_core.common.expressions.vector import InnerProduct
from amsdal_glue_core.common.expressions.vector import L1Distance
from amsdal_glue_core.common.expressions.vector import L2Distance
from amsdal_glue_core.common.expressions.window import Window
from amsdal_glue_core.common.expressions.window import WindowFrame

from ._harness import lite
from ._harness import pg

# A separate generator for PostgreSQL dollar-sign param style (used in a few
# tests that specifically exercise $1/$2 placeholders).
_pg_dollar = SqlGenerator('postgresql', param_style='dollar')


def _ref(name: str, table: str) -> FieldReferenceExpression:
    return FieldReferenceExpression(
        field_reference=FieldReference(field=Field(name=name), table_name=table),
    )


# ---------------------------------------------------------------------------
# Combined / arithmetic
# ---------------------------------------------------------------------------


def test_arithmetic_multiply_in_select() -> None:
    q = QueryStatement(
        table=SchemaReference(name='orders', version=Version.LATEST),
        expressions=[
            SelectExpression(
                expression=Combined(
                    left=_ref('price', 'orders'),
                    operator='*',
                    right=_ref('quantity', 'orders'),
                ),
                alias='total',
            ),
        ],
    )
    assert pg(q) == (
        'SELECT *, "orders"."price" * "orders"."quantity" AS "total" FROM "orders"',
        [],
    )


def test_combined_multiply_in_where() -> None:
    q = QueryStatement(
        table=SchemaReference(name='orders', version=Version.LATEST),
        where=Conditions(
            Condition(
                left=Combined(
                    left=_ref('price', 'orders'),
                    operator='*',
                    right=_ref('quantity', 'orders'),
                ),
                lookup=FieldLookup.GT,
                right=Value(100),
            ),
        ),
    )
    assert pg(q) == (
        'SELECT * FROM "orders" WHERE "orders"."price" * "orders"."quantity" > %s',
        [100],
    )


def test_subtraction_in_select() -> None:
    q = QueryStatement(
        table=SchemaReference(name='orders', version=Version.LATEST),
        expressions=[
            SelectExpression(
                expression=Combined(
                    left=_ref('total', 'orders'),
                    operator='-',
                    right=_ref('discount', 'orders'),
                ),
                alias='net',
            ),
        ],
    )
    assert pg(q) == (
        'SELECT *, "orders"."total" - "orders"."discount" AS "net" FROM "orders"',
        [],
    )


def test_division_in_select() -> None:
    q = QueryStatement(
        table=SchemaReference(name='orders', version=Version.LATEST),
        expressions=[
            SelectExpression(
                expression=Combined(
                    left=_ref('total', 'orders'),
                    operator='/',
                    right=_ref('quantity', 'orders'),
                ),
                alias='unit_price',
            ),
        ],
    )
    assert pg(q) == (
        'SELECT *, "orders"."total" / "orders"."quantity" AS "unit_price" FROM "orders"',
        [],
    )


def test_modulo_in_select() -> None:
    # With format param_style the generator doubles bare '%' → '%%' to avoid
    # collision with the %s placeholder syntax.
    q = QueryStatement(
        table=SchemaReference(name='numbers', version=Version.LATEST),
        expressions=[
            SelectExpression(
                expression=Combined(
                    left=_ref('val', 'numbers'),
                    operator='%',
                    right=Value(2),
                ),
                alias='remainder',
            ),
        ],
    )
    assert pg(q) == (
        'SELECT *, "numbers"."val" %% %s AS "remainder" FROM "numbers"',
        [2],
    )


def test_string_concat_in_select() -> None:
    q = QueryStatement(
        table=SchemaReference(name='users', version=Version.LATEST),
        expressions=[
            SelectExpression(
                expression=Combined(
                    left=_ref('first_name', 'users'),
                    operator='||',
                    right=_ref('last_name', 'users'),
                ),
                alias='full_name',
            ),
        ],
    )
    assert pg(q) == (
        'SELECT *, "users"."first_name" || "users"."last_name" AS "full_name" FROM "users"',
        [],
    )


# ---------------------------------------------------------------------------
# Bitwise operators
# ---------------------------------------------------------------------------


def test_bitand_in_select() -> None:
    q = QueryStatement(
        table=SchemaReference(name='flags', version=Version.LATEST),
        expressions=[
            SelectExpression(
                expression=Combined(
                    left=_ref('mask', 'flags'),
                    operator='&',
                    right=Value(0xFF),
                ),
                alias='low_byte',
            ),
        ],
    )
    assert pg(q) == (
        'SELECT *, "flags"."mask" & %s AS "low_byte" FROM "flags"',
        [255],
    )


def test_bitor_in_select() -> None:
    q = QueryStatement(
        table=SchemaReference(name='flags', version=Version.LATEST),
        expressions=[
            SelectExpression(
                expression=Combined(
                    left=_ref('mask', 'flags'),
                    operator='|',
                    right=Value(0x0F),
                ),
                alias='merged',
            ),
        ],
    )
    assert pg(q) == (
        'SELECT *, "flags"."mask" | %s AS "merged" FROM "flags"',
        [15],
    )


def test_lshift_in_select() -> None:
    q = QueryStatement(
        table=SchemaReference(name='flags', version=Version.LATEST),
        expressions=[
            SelectExpression(
                expression=Combined(
                    left=_ref('val', 'flags'),
                    operator='<<',
                    right=Value(2),
                ),
                alias='shifted',
            ),
        ],
    )
    assert pg(q) == (
        'SELECT *, "flags"."val" << %s AS "shifted" FROM "flags"',
        [2],
    )


def test_rshift_in_select() -> None:
    q = QueryStatement(
        table=SchemaReference(name='flags', version=Version.LATEST),
        expressions=[
            SelectExpression(
                expression=Combined(
                    left=_ref('val', 'flags'),
                    operator='>>',
                    right=Value(2),
                ),
                alias='shifted',
            ),
        ],
    )
    assert pg(q) == (
        'SELECT *, "flags"."val" >> %s AS "shifted" FROM "flags"',
        [2],
    )


# ---------------------------------------------------------------------------
# Func
# ---------------------------------------------------------------------------


def test_func_coalesce() -> None:
    q = QueryStatement(
        table=SchemaReference(name='users', version=Version.LATEST),
        expressions=[
            SelectExpression(
                expression=Func(
                    name='COALESCE',
                    args=[_ref('nickname', 'users'), Value('anonymous')],
                ),
                alias='display_name',
            ),
        ],
    )
    assert pg(q) == (
        'SELECT *, COALESCE("users"."nickname", %s) AS "display_name" FROM "users"',
        ['anonymous'],
    )


def test_func_upper() -> None:
    q = QueryStatement(
        table=SchemaReference(name='users', version=Version.LATEST),
        expressions=[
            SelectExpression(
                expression=Func(
                    name='UPPER',
                    args=[_ref('name', 'users')],
                ),
                alias='upper_name',
            ),
        ],
    )
    assert pg(q) == (
        'SELECT *, UPPER("users"."name") AS "upper_name" FROM "users"',
        [],
    )


# ---------------------------------------------------------------------------
# RawExpression
# ---------------------------------------------------------------------------


def test_raw_in_select() -> None:
    q = QueryStatement(
        table=SchemaReference(name='users', version=Version.LATEST),
        expressions=[
            SelectExpression(
                expression=RawExpression('1 + 1'),
                alias='two',
            ),
        ],
    )
    assert pg(q) == ('SELECT *, 1 + 1 AS "two" FROM "users"', [])
    assert lite(q) == ('SELECT *, 1 + 1 AS "two" FROM "users"', [])


def test_raw_expression_params_as_list() -> None:
    """list params are accepted and threaded correctly into the output."""
    q = QueryStatement(
        table=SchemaReference(name='users', version=Version.LATEST),
        where=Conditions(
            Condition(
                left=_ref('score', 'users'),
                lookup=FieldLookup.GT,
                right=RawExpression('%s + %s', params=[10, 20]),  # type: ignore[arg-type]
            ),
        ),
    )
    sql, params = _pg_dollar.compile_query(q)
    assert sql == 'SELECT * FROM "users" WHERE "users"."score" > $1 + $2'
    assert params == [10, 20]


def test_raw_expression_params_as_tuple() -> None:
    """tuple params produce the same result as list params."""
    q = QueryStatement(
        table=SchemaReference(name='users', version=Version.LATEST),
        where=Conditions(
            Condition(
                left=_ref('score', 'users'),
                lookup=FieldLookup.GT,
                right=RawExpression('%s + %s', params=(10, 20)),
            ),
        ),
    )
    sql, params = _pg_dollar.compile_query(q)
    assert sql == 'SELECT * FROM "users" WHERE "users"."score" > $1 + $2'
    assert params == [10, 20]


def test_raw_expression_params_invalid_type_raises() -> None:
    q = QueryStatement(
        table=SchemaReference(name='users', version=Version.LATEST),
        where=Conditions(
            Condition(
                left=_ref('x', 'users'),
                lookup=FieldLookup.EQ,
                right=RawExpression('$1', params='not_a_sequence'),  # type: ignore[arg-type]
            ),
        ),
    )
    with pytest.raises(TypeError, match='must be a tuple or list'):
        pg(q)


# ---------------------------------------------------------------------------
# Cast
# ---------------------------------------------------------------------------


def test_cast_to_text_pg() -> None:
    q = QueryStatement(
        table=SchemaReference(name='users', version=Version.LATEST),
        expressions=[
            SelectExpression(
                expression=Cast(
                    expression=_ref('id', 'users'),
                    to_type=ScalarType.TEXT,
                ),
                alias='id_text',
            ),
        ],
    )
    # PostgreSQL emits the :: cast syntax.
    assert pg(q) == ('SELECT *, "users"."id"::text AS "id_text" FROM "users"', [])


def test_cast_to_text_sqlite() -> None:
    q = QueryStatement(
        table=SchemaReference(name='users', version=Version.LATEST),
        expressions=[
            SelectExpression(
                expression=Cast(
                    expression=_ref('id', 'users'),
                    to_type=ScalarType.TEXT,
                ),
                alias='id_text',
            ),
        ],
    )
    # SQLite uses the CAST(… AS …) form.
    assert lite(q) == ('SELECT *, CAST("users"."id" AS text) AS "id_text" FROM "users"', [])


def test_cast_double_sqlite() -> None:
    q = QueryStatement(
        table=SchemaReference(name='data', version=Version.LATEST),
        expressions=[
            SelectExpression(
                expression=Cast(
                    expression=_ref('val', 'data'),
                    to_type=ScalarType.DOUBLE,
                ),
                alias='val_real',
            ),
        ],
    )
    assert lite(q) == ('SELECT *, CAST("data"."val" AS double) AS "val_real" FROM "data"', [])


def test_cast_uuid_sqlite() -> None:
    q = QueryStatement(
        table=SchemaReference(name='data', version=Version.LATEST),
        expressions=[
            SelectExpression(
                expression=Cast(
                    expression=_ref('uid', 'data'),
                    to_type=ScalarType.UUID,
                ),
                alias='uid_text',
            ),
        ],
    )
    assert lite(q) == ('SELECT *, CAST("data"."uid" AS uuid) AS "uid_text" FROM "data"', [])


def test_cast_jsonb_sqlite() -> None:
    q = QueryStatement(
        table=SchemaReference(name='data', version=Version.LATEST),
        expressions=[
            SelectExpression(
                expression=Cast(
                    expression=_ref('payload', 'data'),
                    to_type=ScalarType.JSONB,
                ),
                alias='payload_json',
            ),
        ],
    )
    assert lite(q) == (
        'SELECT *, CAST("data"."payload" AS jsonb) AS "payload_json" FROM "data"',
        [],
    )


# ---------------------------------------------------------------------------
# CASE WHEN
# ---------------------------------------------------------------------------


def test_case_simple() -> None:
    q = QueryStatement(
        table=SchemaReference(name='users', version=Version.LATEST),
        expressions=[
            SelectExpression(
                expression=Case(
                    cases=[
                        WhenClause(
                            condition=Conditions(
                                Condition(
                                    left=_ref('status', 'users'),
                                    lookup=FieldLookup.EQ,
                                    right=Value('active'),
                                ),
                            ),
                            result=Value('yes'),
                        ),
                    ],
                    default=Value('no'),
                ),
                alias='is_active',
            ),
        ],
    )
    assert pg(q) == (
        'SELECT *, CASE WHEN "users"."status" = %s THEN %s ELSE %s END AS "is_active" FROM "users"',
        ['active', 'yes', 'no'],
    )


def test_case_multiple_whens() -> None:
    q = QueryStatement(
        table=SchemaReference(name='orders', version=Version.LATEST),
        expressions=[
            SelectExpression(
                expression=Case(
                    cases=[
                        WhenClause(
                            condition=Conditions(
                                Condition(
                                    left=_ref('amount', 'orders'),
                                    lookup=FieldLookup.GT,
                                    right=Value(1000),
                                ),
                            ),
                            result=Value('high'),
                        ),
                        WhenClause(
                            condition=Conditions(
                                Condition(
                                    left=_ref('amount', 'orders'),
                                    lookup=FieldLookup.GT,
                                    right=Value(100),
                                ),
                            ),
                            result=Value('medium'),
                        ),
                    ],
                    default=Value('low'),
                ),
                alias='tier',
            ),
        ],
    )
    assert pg(q) == (
        'SELECT *, CASE WHEN "orders"."amount" > %s THEN %s'
        ' WHEN "orders"."amount" > %s THEN %s ELSE %s END AS "tier" FROM "orders"',
        [1000, 'high', 100, 'medium', 'low'],
    )


def test_case_without_default() -> None:
    q = QueryStatement(
        table=SchemaReference(name='users', version=Version.LATEST),
        expressions=[
            SelectExpression(
                expression=Case(
                    cases=[
                        WhenClause(
                            condition=Conditions(
                                Condition(
                                    left=_ref('status', 'users'),
                                    lookup=FieldLookup.EQ,
                                    right=Value('admin'),
                                ),
                            ),
                            result=Value('Admin User'),
                        ),
                    ],
                ),
                alias='label',
            ),
        ],
    )
    assert pg(q) == (
        'SELECT *, CASE WHEN "users"."status" = %s THEN %s END AS "label" FROM "users"',
        ['admin', 'Admin User'],
    )


def test_case_in_where() -> None:
    q = QueryStatement(
        table=SchemaReference(name='orders', version=Version.LATEST),
        where=Conditions(
            Condition(
                left=Case(
                    cases=[
                        WhenClause(
                            condition=Conditions(
                                Condition(
                                    left=_ref('amount', 'orders'),
                                    lookup=FieldLookup.GT,
                                    right=Value(1000),
                                ),
                            ),
                            result=Value('high'),
                        ),
                    ],
                    default=Value('low'),
                ),
                lookup=FieldLookup.EQ,
                right=Value('high'),
            ),
        ),
    )
    assert pg(q) == (
        'SELECT * FROM "orders" WHERE CASE WHEN "orders"."amount" > %s THEN %s ELSE %s END = %s',
        [1000, 'high', 'low', 'high'],
    )


# ---------------------------------------------------------------------------
# EXISTS / NOT EXISTS
# ---------------------------------------------------------------------------


def test_exists_in_where() -> None:
    subquery = QueryStatement(
        table=SchemaReference(name='orders', version=Version.LATEST),
        only=[FieldReference(field=Field(name='id'), table_name='orders')],
        where=Conditions(
            Condition(
                left=_ref('user_id', 'orders'),
                lookup=FieldLookup.EQ,
                right=_ref('id', 'users'),
            ),
        ),
    )
    q = QueryStatement(
        table=SchemaReference(name='users', version=Version.LATEST),
        where=Conditions(
            Exists(subquery=SubQueryStatement(query=subquery, alias='_exists')),
        ),
    )
    assert pg(q) == (
        'SELECT * FROM "users"'
        ' WHERE EXISTS(SELECT "orders"."id" FROM "orders"'
        ' WHERE "orders"."user_id" = "users"."id")',
        [],
    )


def test_not_exists_in_where() -> None:
    subquery = QueryStatement(
        table=SchemaReference(name='orders', version=Version.LATEST),
        only=[FieldReference(field=Field(name='id'), table_name='orders')],
    )
    q = QueryStatement(
        table=SchemaReference(name='users', version=Version.LATEST),
        where=Conditions(
            Exists(
                subquery=SubQueryStatement(query=subquery, alias='_exists'),
                negated=True,
            ),
        ),
    )
    assert pg(q) == (
        'SELECT * FROM "users" WHERE (NOT EXISTS(SELECT "orders"."id" FROM "orders"))',
        [],
    )


# ---------------------------------------------------------------------------
# Window expressions
# ---------------------------------------------------------------------------


def test_window_partition_by_single_field_pg() -> None:
    q = QueryStatement(
        table=SchemaReference(name='sales', version=Version.LATEST),
        expressions=[
            SelectExpression(
                expression=Window(
                    expression=Count(),
                    partition_by=[_ref('department', 'sales')],
                    order_by=[
                        OrderByQuery(
                            field=FieldReference(field=Field(name='amount'), table_name='sales'),
                            direction=OrderDirection.DESC,
                        ),
                    ],
                ),
                alias='row_num',
            ),
        ],
    )
    assert pg(q) == (
        'SELECT *, COUNT(*) OVER'
        ' (PARTITION BY "sales"."department" ORDER BY "sales"."amount" DESC)'
        ' AS "row_num" FROM "sales"',
        [],
    )


def test_window_partition_by_multiple_fields_pg() -> None:
    q = QueryStatement(
        table=SchemaReference(name='sales', version=Version.LATEST),
        expressions=[
            SelectExpression(
                expression=Window(
                    expression=Sum(expression=_ref('amount', 'sales')),
                    partition_by=[
                        _ref('department', 'sales'),
                        _ref('year', 'sales'),
                    ],
                ),
                alias='dept_year_total',
            ),
        ],
    )
    assert pg(q) == (
        'SELECT *, SUM("sales"."amount") OVER'
        ' (PARTITION BY "sales"."department", "sales"."year")'
        ' AS "dept_year_total" FROM "sales"',
        [],
    )


def test_window_partition_by_single_field_sqlite() -> None:
    q = QueryStatement(
        table=SchemaReference(name='sales', version=Version.LATEST),
        expressions=[
            SelectExpression(
                expression=Window(
                    expression=Count(),
                    partition_by=[_ref('department', 'sales')],
                    order_by=[
                        OrderByQuery(
                            field=FieldReference(field=Field(name='amount'), table_name='sales'),
                            direction=OrderDirection.DESC,
                        ),
                    ],
                ),
                alias='row_num',
            ),
        ],
    )
    assert lite(q) == (
        'SELECT *, COUNT(*) OVER'
        ' (PARTITION BY "sales"."department" ORDER BY "sales"."amount" DESC)'
        ' AS "row_num" FROM "sales"',
        [],
    )


def test_window_rows_frame_pg() -> None:
    q = QueryStatement(
        table=SchemaReference(name='sales', version=Version.LATEST),
        expressions=[
            SelectExpression(
                expression=Window(
                    expression=Sum(expression=_ref('amount', 'sales')),
                    partition_by=[_ref('department', 'sales')],
                    order_by=[
                        OrderByQuery(
                            field=FieldReference(field=Field(name='amount'), table_name='sales'),
                            direction=OrderDirection.ASC,
                        ),
                    ],
                    frame=WindowFrame(
                        frame_type=WindowFrameType.ROWS,
                        start=None,
                        end=0,
                    ),
                ),
                alias='running_total',
            ),
        ],
    )
    assert pg(q) == (
        'SELECT *, SUM("sales"."amount") OVER'
        ' (PARTITION BY "sales"."department" ORDER BY "sales"."amount" ASC'
        ' ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)'
        ' AS "running_total" FROM "sales"',
        [],
    )


def test_window_groups_frame_pg() -> None:
    q = QueryStatement(
        table=SchemaReference(name='sales', version=Version.LATEST),
        expressions=[
            SelectExpression(
                expression=Window(
                    expression=Sum(expression=_ref('amount', 'sales')),
                    partition_by=[_ref('department', 'sales')],
                    frame=WindowFrame(
                        frame_type=WindowFrameType.GROUPS,
                        start=None,
                        end=0,
                    ),
                ),
                alias='group_total',
            ),
        ],
    )
    assert pg(q) == (
        'SELECT *, SUM("sales"."amount") OVER'
        ' (PARTITION BY "sales"."department"'
        ' GROUPS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)'
        ' AS "group_total" FROM "sales"',
        [],
    )


def test_window_range_frame_pg() -> None:
    q = QueryStatement(
        table=SchemaReference(name='sales', version=Version.LATEST),
        expressions=[
            SelectExpression(
                expression=Window(
                    expression=Sum(expression=_ref('amount', 'sales')),
                    order_by=[
                        OrderByQuery(
                            field=FieldReference(field=Field(name='amount'), table_name='sales'),
                            direction=OrderDirection.ASC,
                        ),
                    ],
                    frame=WindowFrame(
                        frame_type=WindowFrameType.RANGE,
                        start=None,
                        end=0,
                    ),
                ),
                alias='range_total',
            ),
        ],
    )
    assert pg(q) == (
        'SELECT *, SUM("sales"."amount") OVER'
        ' (ORDER BY "sales"."amount" ASC'
        ' RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)'
        ' AS "range_total" FROM "sales"',
        [],
    )


def test_window_n_preceding_and_following() -> None:
    q = QueryStatement(
        table=SchemaReference(name='sales', version=Version.LATEST),
        expressions=[
            SelectExpression(
                expression=Window(
                    expression=Sum(expression=_ref('amount', 'sales')),
                    order_by=[
                        OrderByQuery(
                            field=FieldReference(field=Field(name='amount'), table_name='sales'),
                            direction=OrderDirection.ASC,
                        ),
                    ],
                    frame=WindowFrame(
                        frame_type=WindowFrameType.ROWS,
                        start=-3,
                        end=3,
                    ),
                ),
                alias='sliding_sum',
            ),
        ],
    )
    assert pg(q) == (
        'SELECT *, SUM("sales"."amount") OVER'
        ' (ORDER BY "sales"."amount" ASC'
        ' ROWS BETWEEN 3 PRECEDING AND 3 FOLLOWING)'
        ' AS "sliding_sum" FROM "sales"',
        [],
    )


# ---------------------------------------------------------------------------
# Vector expressions (PostgreSQL only)
# ---------------------------------------------------------------------------


def test_vector_l2_distance_pg() -> None:
    q = QueryStatement(
        table=SchemaReference(name='items', version=Version.LATEST),
        expressions=[
            SelectExpression(
                expression=L2Distance(left=_ref('embedding', 'items'), right=Value('[1,2,3]')),
                alias='distance',
            ),
        ],
    )
    assert pg(q) == (
        'SELECT *, "items"."embedding" <-> %s AS "distance" FROM "items"',
        ['[1,2,3]'],
    )


def test_vector_cosine_distance_pg() -> None:
    q = QueryStatement(
        table=SchemaReference(name='items', version=Version.LATEST),
        expressions=[
            SelectExpression(
                expression=CosineDistance(left=_ref('embedding', 'items'), right=Value('[1,2,3]')),
                alias='distance',
            ),
        ],
    )
    assert pg(q) == (
        'SELECT *, "items"."embedding" <=> %s AS "distance" FROM "items"',
        ['[1,2,3]'],
    )


def test_vector_inner_product_pg() -> None:
    q = QueryStatement(
        table=SchemaReference(name='items', version=Version.LATEST),
        expressions=[
            SelectExpression(
                expression=InnerProduct(left=_ref('embedding', 'items'), right=Value('[1,2,3]')),
                alias='product',
            ),
        ],
    )
    assert pg(q) == (
        'SELECT *, "items"."embedding" <#> %s AS "product" FROM "items"',
        ['[1,2,3]'],
    )


def test_vector_l1_distance_pg() -> None:
    q = QueryStatement(
        table=SchemaReference(name='items', version=Version.LATEST),
        expressions=[
            SelectExpression(
                expression=L1Distance(left=_ref('embedding', 'items'), right=Value('[1,2,3]')),
                alias='distance',
            ),
        ],
    )
    assert pg(q) == (
        'SELECT *, "items"."embedding" <+> %s AS "distance" FROM "items"',
        ['[1,2,3]'],
    )


def test_vector_sqlite_unsupported() -> None:
    q = QueryStatement(
        table=SchemaReference(name='items', version=Version.LATEST),
        expressions=[
            SelectExpression(
                expression=L2Distance(left=_ref('embedding', 'items'), right=Value('[1,2,3]')),
                alias='distance',
            ),
        ],
    )
    with pytest.raises(UnsupportedFeatureError):
        lite(q)


# ---------------------------------------------------------------------------
# JSONB array
# ---------------------------------------------------------------------------


def test_jsonb_build_array_pg() -> None:
    q = QueryStatement(
        table=SchemaReference(name='data', version=Version.LATEST),
        expressions=[
            SelectExpression(
                expression=JsonbArray(items=[_ref('a', 'data'), _ref('b', 'data')]),
                alias='arr',
            ),
        ],
    )
    assert pg(q) == (
        'SELECT *, jsonb_build_array("data"."a", "data"."b") AS "arr" FROM "data"',
        [],
    )


def test_jsonb_build_array_sqlite_mapped() -> None:
    # SQLite has no jsonb_build_array; the generator maps it to json_array().
    q = QueryStatement(
        table=SchemaReference(name='data', version=Version.LATEST),
        expressions=[
            SelectExpression(
                expression=JsonbArray(items=[Value(1), Value(2)]),
                alias='arr',
            ),
        ],
    )
    assert lite(q) == ('SELECT *, json_array(?, ?) AS "arr" FROM "data"', [1, 2])


# ---------------------------------------------------------------------------
# FTS helpers in SELECT (PostgreSQL only)
# ---------------------------------------------------------------------------


def _art(name: str) -> FieldReferenceExpression:
    return _ref(name, 'articles')


def test_search_vector_in_select() -> None:
    q = QueryStatement(
        table=SchemaReference(name='articles', version=Version.LATEST),
        expressions=[
            SelectExpression(
                expression=SearchVector(
                    name='to_tsvector',
                    args=[Value(value='english'), _art('body')],
                ),
                alias='vec',
            ),
        ],
    )
    assert pg(q) == (
        'SELECT *, to_tsvector(%s, "articles"."body") AS "vec" FROM "articles"',
        ['english'],
    )


def test_search_rank_in_select() -> None:
    q = QueryStatement(
        table=SchemaReference(name='articles', version=Version.LATEST),
        expressions=[
            SelectExpression(
                expression=SearchRank(
                    name='ts_rank',
                    args=[
                        _art('search_vector'),
                        SearchQuery(
                            args=[Value(value='english'), Value(value='test')],
                            search_type='plain',
                        ),
                    ],
                ),
                alias='rank',
            ),
        ],
    )
    assert pg(q) == (
        'SELECT *, ts_rank("articles"."search_vector", plainto_tsquery(%s, %s)) AS "rank" FROM "articles"',
        ['english', 'test'],
    )


def test_search_headline_in_select() -> None:
    q = QueryStatement(
        table=SchemaReference(name='articles', version=Version.LATEST),
        expressions=[
            SelectExpression(
                expression=SearchHeadline(
                    name='ts_headline',
                    args=[
                        Value(value='english'),
                        _art('body'),
                        SearchQuery(
                            args=[Value(value='english'), Value(value='highlight')],
                            search_type='plain',
                        ),
                    ],
                ),
                alias='headline',
            ),
        ],
    )
    assert pg(q) == (
        'SELECT *, ts_headline(%s, "articles"."body", plainto_tsquery(%s, %s)) AS "headline" FROM "articles"',
        ['english', 'english', 'highlight'],
    )


# ---------------------------------------------------------------------------
# ARRAY (SELECT …) subquery
# ---------------------------------------------------------------------------


def test_array_subquery_pg() -> None:
    subquery = QueryStatement(
        table=SchemaReference(name='users', version=Version.LATEST),
        only=[FieldReference(field=Field(name='id'), table_name='users')],
    )
    q = QueryStatement(
        table=SchemaReference(name='orders', version=Version.LATEST),
        expressions=[
            SelectExpression(
                expression=ArraySubquery(
                    subquery=SubQueryStatement(query=subquery, alias='_sub'),
                ),
                alias='user_ids',
            ),
        ],
    )
    assert pg(q) == (
        'SELECT *, ARRAY (SELECT "users"."id" FROM "users") AS "user_ids" FROM "orders"',
        [],
    )


def test_array_subquery_sqlite_unsupported() -> None:
    subquery = QueryStatement(
        table=SchemaReference(name='users', version=Version.LATEST),
        only=[FieldReference(field=Field(name='id'), table_name='users')],
    )
    q = QueryStatement(
        table=SchemaReference(name='orders', version=Version.LATEST),
        expressions=[
            SelectExpression(
                expression=ArraySubquery(
                    subquery=SubQueryStatement(query=subquery, alias='_sub'),
                ),
                alias='user_ids',
            ),
        ],
    )
    with pytest.raises(UnsupportedFeatureError):
        lite(q)


# ---------------------------------------------------------------------------
# COLLATE expression
# ---------------------------------------------------------------------------


def test_collate_in_select_pg() -> None:
    q = QueryStatement(
        table=SchemaReference(name='users', version=Version.LATEST),
        expressions=[
            SelectExpression(
                expression=Collate(expression=_ref('name', 'users'), collation='C'),
                alias='name_c',
            ),
        ],
    )
    assert pg(q) == (
        'SELECT *, "users"."name" COLLATE "C" AS "name_c" FROM "users"',
        [],
    )


def test_collate_in_where_pg() -> None:
    q = QueryStatement(
        table=SchemaReference(name='users', version=Version.LATEST),
        where=Conditions(
            Condition(
                left=Collate(
                    expression=_ref('name', 'users'),
                    collation='case_insensitive',
                ),
                lookup=FieldLookup.EQ,
                right=Value('test'),
            ),
        ),
    )
    assert pg(q) == (
        'SELECT * FROM "users" WHERE "users"."name" COLLATE "case_insensitive" = %s',
        ['test'],
    )


def test_collate_sqlite() -> None:
    q = QueryStatement(
        table=SchemaReference(name='users', version=Version.LATEST),
        expressions=[
            SelectExpression(
                expression=Collate(expression=_ref('name', 'users'), collation='NOCASE'),
                alias='name_nc',
            ),
        ],
    )
    assert lite(q) == (
        'SELECT *, "users"."name" COLLATE NOCASE AS "name_nc" FROM "users"',
        [],
    )


# ---------------------------------------------------------------------------
# Aggregation with ORDER BY inside the aggregate
# ---------------------------------------------------------------------------


def test_aggregation_with_order_by() -> None:
    q = QueryStatement(
        table=SchemaReference(name='users', version=Version.LATEST),
        expressions=[
            SelectExpression(
                expression=Sum(
                    expression=_ref('score', 'users'),
                    order_by=[
                        OrderByQuery(
                            field=FieldReference(field=Field(name='name'), table_name='users'),
                            direction=OrderDirection.ASC,
                        ),
                    ],
                ),
                alias='ordered_sum',
            ),
        ],
    )
    assert pg(q) == (
        'SELECT *, SUM("users"."score" ORDER BY "users"."name" ASC) AS "ordered_sum" FROM "users"',
        [],
    )


# ---------------------------------------------------------------------------
# Scalar subquery / EXISTS in SELECT and WHERE
# ---------------------------------------------------------------------------


def test_scalar_subquery_in_select() -> None:
    subquery = QueryStatement(
        table=SchemaReference(name='orders', version=Version.LATEST),
        expressions=[SelectExpression(expression=Count(), alias='cnt')],
    )
    q = QueryStatement(
        table=SchemaReference(name='users', version=Version.LATEST),
        expressions=[
            SelectExpression(
                expression=Exists(
                    subquery=SubQueryStatement(query=subquery, alias='_sub'),
                ),
                alias='has_orders',
            ),
        ],
    )
    assert pg(q) == (
        'SELECT *, EXISTS(SELECT *, COUNT(*) AS "cnt" FROM "orders") AS "has_orders" FROM "users"',
        [],
    )


def test_scalar_subquery_in_where() -> None:
    subquery = QueryStatement(
        table=SchemaReference(name='orders', version=Version.LATEST),
        expressions=[SelectExpression(expression=Count(), alias='cnt')],
        where=Conditions(
            Condition(
                left=_ref('user_id', 'orders'),
                lookup=FieldLookup.EQ,
                right=_ref('id', 'users'),
            ),
        ),
    )
    q = QueryStatement(
        table=SchemaReference(name='users', version=Version.LATEST),
        where=Conditions(
            Exists(subquery=SubQueryStatement(query=subquery, alias='_sub')),
        ),
    )
    # dollar-style to match the source intent (any style produces the same SQL
    # here because there are no value params — but we verify exact text).
    sql, params = _pg_dollar.compile_query(q)
    assert sql == (
        'SELECT * FROM "users"'
        ' WHERE EXISTS(SELECT *, COUNT(*) AS "cnt" FROM "orders"'
        ' WHERE "orders"."user_id" = "users"."id")'
    )
    assert params == []


# ---------------------------------------------------------------------------
# Power (**) and BitwiseXor (^) — per-dialect native rendering (qcraft >= 2.5.0)
# ---------------------------------------------------------------------------


def _select(expr) -> QueryStatement:
    return QueryStatement(
        table=SchemaReference(name='t', version=Version.LATEST),
        only=[],
        expressions=[SelectExpression(expression=expr, alias='v')],
    )


def test_power_operator_postgres_uses_caret() -> None:
    # In Postgres, `^` is the exponentiation operator.
    q = _select(Combined(left=Value(value=2), operator='**', right=Value(value=3)))
    assert pg(q) == ('SELECT %s ^ %s AS "v" FROM "t"', [2, 3])


def test_power_operator_sqlite_uses_power_function() -> None:
    # SQLite has no exponentiation operator — the built-in power() function is used.
    q = _select(Combined(left=Value(value=2), operator='**', right=Value(value=3)))
    assert lite(q) == ('SELECT power(?, ?) AS "v" FROM "t"', [2, 3])


def test_power_operator_over_fields_postgres() -> None:
    q = _select(Combined(left=_ref('base', 't'), operator='**', right=_ref('exp', 't')))
    assert pg(q) == ('SELECT "t"."base" ^ "t"."exp" AS "v" FROM "t"', [])


def test_bitwise_xor_postgres_uses_hash() -> None:
    # In Postgres, `#` is the bitwise-XOR operator.
    q = _select(Combined(left=Value(value=5), operator='^', right=Value(value=3)))
    assert pg(q) == ('SELECT %s # %s AS "v" FROM "t"', [5, 3])


def test_bitwise_xor_sqlite_expands_to_or_minus_and() -> None:
    # SQLite has no bitwise-XOR operator; the identity a^b = (a|b) - (a&b) is emitted,
    # fully parenthesised. Each operand appears twice, so its bound value is pushed twice.
    q = _select(Combined(left=Value(value=5), operator='^', right=Value(value=3)))
    assert lite(q) == ('SELECT (((?) | (?)) - ((?) & (?))) AS "v" FROM "t"', [5, 3, 5, 3])
