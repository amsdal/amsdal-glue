# mypy: disable-error-code="type-abstract"
from collections.abc import Generator
from pathlib import Path

import pytest
from amsdal_glue_connections.sql.connections.sqlite_connection import SqliteConnection
from amsdal_glue_core.common.data_models.conditions import Condition
from amsdal_glue_core.common.data_models.conditions import Conditions
from amsdal_glue_core.common.data_models.field_reference import Field
from amsdal_glue_core.common.data_models.field_reference import FieldReference
from amsdal_glue_core.common.data_models.order_by import OrderByQuery
from amsdal_glue_core.common.data_models.query import QueryStatement
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.data_models.sub_query import SubQueryStatement
from amsdal_glue_core.common.enums import FieldLookup
from amsdal_glue_core.common.enums import OrderDirection
from amsdal_glue_core.common.enums import Version
from amsdal_glue_core.common.expressions.exists import Exists
from amsdal_glue_core.common.expressions.field_reference import FieldReferenceExpression
from amsdal_glue_core.common.expressions.value import Value
from amsdal_glue_core.common.interfaces.connection_manager import ConnectionManager
from amsdal_glue_core.containers import Container
from amsdal_glue_core.queries.planner.data_query_planner import DataQueryPlanner

from amsdal_glue.connections.connection_pool import DefaultConnectionPool
from amsdal_glue.initialize import init_default_containers

FIXTURES_PATH = Path(__file__).parent / 'fixtures'


@pytest.fixture(autouse=True)
def _register_default_connection() -> Generator[None, None, None]:
    init_default_containers()
    connection_mng = Container.managers.get(ConnectionManager)

    connection_mng.register_connection_pool(
        DefaultConnectionPool(SqliteConnection, db_path=FIXTURES_PATH / 'customers.sqlite', check_same_thread=False)
    )

    try:
        yield
    finally:
        connection_mng.disconnect_all()


def _correlated_orders_subquery(min_amount: int) -> QueryStatement:
    leaves: list[Condition] = [
        Condition(
            left=FieldReferenceExpression(
                field_reference=FieldReference(
                    field=Field(name='customer_id'),
                    table_name='o',
                )
            ),
            lookup=FieldLookup.EQ,
            right=FieldReferenceExpression(
                field_reference=FieldReference(
                    field=Field(name='id'),
                    table_name='c',
                )
            ),
        ),
    ]
    if min_amount > 0:
        leaves.append(
            Condition(
                left=FieldReferenceExpression(
                    field_reference=FieldReference(
                        field=Field(name='amount'),
                        table_name='o',
                    )
                ),
                lookup=FieldLookup.GT,
                right=Value(value=min_amount),
            )
        )

    return QueryStatement(
        only=[FieldReference(field=Field(name='1'), table_name='')],
        table=SchemaReference(name='orders', alias='o', version=Version.LATEST),
        where=Conditions(*leaves),
    )


def test_not_exists_returns_customers_without_any_orders() -> None:
    query = QueryStatement(
        only=[FieldReference(field=Field(name='id'), table_name='c')],
        table=SchemaReference(name='customers', alias='c', version=Version.LATEST),
        where=Conditions(
            Exists(
                subquery=SubQueryStatement(query=_correlated_orders_subquery(min_amount=0), alias='_exists'),
                negated=True,
            )
        ),
        order_by=[
            OrderByQuery(
                expression=FieldReferenceExpression(
                    field_reference=FieldReference(field=Field(name='id'), table_name='c')
                ),
                direction=OrderDirection.ASC,
            )
        ],
    )
    planner = Container.planners.get(DataQueryPlanner)
    plan = planner.plan_data_query(query)
    plan.execute(transaction_id=None, lock_id=None)

    result = plan.tasks[-1].result

    assert [item.data for item in result] == [{'id': 5}]


def test_exists_returns_customers_with_any_order() -> None:
    query = QueryStatement(
        only=[FieldReference(field=Field(name='id'), table_name='c')],
        table=SchemaReference(name='customers', alias='c', version=Version.LATEST),
        where=Conditions(
            Exists(subquery=SubQueryStatement(query=_correlated_orders_subquery(min_amount=0), alias='_exists'))
        ),
        order_by=[
            OrderByQuery(
                expression=FieldReferenceExpression(
                    field_reference=FieldReference(field=Field(name='id'), table_name='c')
                ),
                direction=OrderDirection.ASC,
            )
        ],
    )
    planner = Container.planners.get(DataQueryPlanner)
    plan = planner.plan_data_query(query)
    plan.execute(transaction_id=None, lock_id=None)

    result = plan.tasks[-1].result

    assert [item.data for item in result] == [{'id': 1}, {'id': 2}, {'id': 3}, {'id': 4}]


def test_exists_with_correlation_and_amount_threshold_returns_customer_three() -> None:
    """Only customer 3 has an order with amount > 5000 (order id=3, amount=12000)."""
    query = QueryStatement(
        only=[FieldReference(field=Field(name='id'), table_name='c')],
        table=SchemaReference(name='customers', alias='c', version=Version.LATEST),
        where=Conditions(
            Exists(subquery=SubQueryStatement(query=_correlated_orders_subquery(min_amount=5000), alias='_exists'))
        ),
        order_by=[
            OrderByQuery(
                expression=FieldReferenceExpression(
                    field_reference=FieldReference(field=Field(name='id'), table_name='c')
                ),
                direction=OrderDirection.ASC,
            )
        ],
    )
    planner = Container.planners.get(DataQueryPlanner)
    plan = planner.plan_data_query(query)
    plan.execute(transaction_id=None, lock_id=None)

    result = plan.tasks[-1].result

    assert [item.data for item in result] == [{'id': 3}]
