# mypy: disable-error-code="type-abstract"
from collections.abc import AsyncGenerator
from pathlib import Path

import pytest
from amsdal_glue_connections.sql.connections.sqlite_connection import AsyncSqliteConnection
from amsdal_glue_core.common.interfaces.connection_manager import AsyncConnectionManager
from amsdal_glue_core.common.operations.queries import SchemaQueryOperation
from amsdal_glue_core.common.services.queries import AsyncSchemaQueryService
from amsdal_glue_core.containers import Container

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
async def test_schema_query_service_single_connection(register_default_connection: AsyncGenerator[None, None]) -> None:
    async for _ in register_default_connection:
        query_service = Container.services.get(AsyncSchemaQueryService)
        result = await query_service.execute(
            SchemaQueryOperation(filters=None),
        )
        assert result.success is True
        assert result.schemas
        assert len(result.schemas) == 4


@pytest.mark.asyncio
async def test_schema_query_service_multiple_connection(
    register_default_connection: AsyncGenerator[None, None],
) -> None:
    async for _ in register_default_connection:
        _add_shipping_connection()
        query_service = Container.services.get(AsyncSchemaQueryService)
        result = await query_service.execute(
            SchemaQueryOperation(filters=None),
        )
        assert result.success is True
        assert result.schemas
        assert len(result.schemas) == 5
        table_names = {item.name if item else None for item in result.schemas}
        assert table_names == {
            'customers',
            'orders',
            'items',
            'vendor',
            'shippings',
        }
