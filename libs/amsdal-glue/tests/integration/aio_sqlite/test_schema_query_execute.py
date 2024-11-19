# mypy: disable-error-code="type-abstract"
from collections.abc import AsyncGenerator
from pathlib import Path

import pytest
from amsdal_glue_connections.sql.connections.sqlite_connection import AsyncSqliteConnection
from amsdal_glue_core.common.interfaces.connection_manager import AsyncConnectionManager
from amsdal_glue_core.containers import Container
from amsdal_glue_core.queries.planner.schema_query_planner import AsyncSchemaQueryPlanner

from amsdal_glue.connections.connection_pool import DefaultAsyncConnectionPool
from amsdal_glue.initialize import init_default_containers

FIXTURES_PATH = Path(__file__).parent / 'fixtures'


@pytest.fixture(autouse=True)
async def register_default_connection() -> AsyncGenerator[None, None]:
    init_default_containers()
    connection_mng = Container.managers.get(AsyncConnectionManager)

    connection_mng.register_connection_pool(
        DefaultAsyncConnectionPool(
            AsyncSqliteConnection, db_path=FIXTURES_PATH / 'customers.sqlite', check_same_thread=False
        )
    )

    try:
        yield
    finally:
        await connection_mng.disconnect_all()


def _add_shipping_connection():
    connection_mng = Container.managers.get(AsyncConnectionManager)

    connection_mng.register_connection_pool(
        DefaultAsyncConnectionPool(
            AsyncSqliteConnection, db_path=FIXTURES_PATH / 'shippings.sqlite', check_same_thread=False
        ),
        schema_name='shippings',
    )


@pytest.mark.asyncio
async def test_query_schemas_for_one_connection(register_default_connection: AsyncGenerator[None, None]) -> None:
    async for _ in register_default_connection:
        query_planner = Container.planners.get(AsyncSchemaQueryPlanner)
        plan = query_planner.plan_schema_query()
        await plan.execute(transaction_id=None, lock_id=None)

        result = plan.result
        assert len(result) == 4
        table_names = {item.name for item in result}
        assert table_names == {
            'customers',
            'orders',
            'items',
            'vendor',
        }


@pytest.mark.asyncio
async def test_query_schemas_for_multiple_connections(register_default_connection: AsyncGenerator[None, None]) -> None:
    async for _ in register_default_connection:
        _add_shipping_connection()
        query_planner = Container.planners.get(AsyncSchemaQueryPlanner)
        plan = query_planner.plan_schema_query()
        await plan.execute(transaction_id=None, lock_id=None)

        result = plan.result
        assert len(result) == 5
        table_names = {item.name for item in result}
        assert table_names == {
            'customers',
            'orders',
            'items',
            'vendor',
            'shippings',
        }
