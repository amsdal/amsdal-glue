"""Regression: copy() of the outer COUNT shape must keep `only=[]`.

The historical/lakehouse path runs the query through ``copy()`` (via
table_name_transform). If ``copy()`` collapses the deliberate ``only=[]``
to ``None``, the generator renders a default ``SELECT *`` and — since
``expressions`` ADD to the projection — emits the invalid ``SELECT *, COUNT(*)``,
which PostgreSQL rejects. Both dialects must compile the copied query to a
clean ``SELECT COUNT(*) AS "total_count" FROM (...)`` with no leading star.
"""

from copy import copy

from amsdal_glue_core.common.data_models.query import QueryStatement
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.data_models.select_expression import SelectExpression
from amsdal_glue_core.common.data_models.sub_query import SubQueryStatement
from amsdal_glue_core.common.enums import Version
from amsdal_glue_core.common.expressions.aggregation import Count

from ._harness import lite
from ._harness import pg


def _outer_count() -> QueryStatement:
    inner = QueryStatement(table=SchemaReference(name='orders', version=Version.LATEST))
    return QueryStatement(
        table=SubQueryStatement(query=inner, alias='sub'),
        only=[],
        expressions=[SelectExpression(expression=Count(), alias='total_count')],
    )


def test_copy_outer_count_pg() -> None:
    q = copy(_outer_count())
    sql, params = pg(q)
    assert sql == 'SELECT COUNT(*) AS "total_count" FROM (SELECT * FROM "orders") AS "sub"'
    assert params == []


def test_copy_outer_count_lite() -> None:
    q = copy(_outer_count())
    sql, params = lite(q)
    assert sql == 'SELECT COUNT(*) AS "total_count" FROM (SELECT * FROM "orders") AS "sub"'
    assert params == []
