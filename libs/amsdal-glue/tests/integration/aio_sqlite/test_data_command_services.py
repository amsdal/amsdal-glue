# mypy: disable-error-code="type-abstract"
import tempfile
from collections.abc import AsyncGenerator
from pathlib import Path

import pytest
from amsdal_glue_connections.sql.connections.sqlite_connection import AsyncSqliteConnection
from amsdal_glue_core.common.data_models.data import Data
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.enums import Version
from amsdal_glue_core.common.interfaces.connection_manager import AsyncConnectionManager
from amsdal_glue_core.common.operations.commands import DataCommand
from amsdal_glue_core.common.operations.mutations.data import InsertData
from amsdal_glue_core.common.services.commands import AsyncDataCommandService
from amsdal_glue_core.containers import Container

from amsdal_glue.connections.connection_pool import DefaultAsyncConnectionPool
from amsdal_glue.initialize import init_default_containers


@pytest.fixture(autouse=True)
async def register_default_connection() -> AsyncGenerator[None, None]:
    init_default_containers()
    connection_mng = Container.managers.get(AsyncConnectionManager)

    with tempfile.TemporaryDirectory() as temp_dir:
        connection_mng.register_connection_pool(
            DefaultAsyncConnectionPool(
                AsyncSqliteConnection, db_path=Path(f'{temp_dir}/data.sqlite'), check_same_thread=False
            ),
        )
        connection_mng.register_connection_pool(
            DefaultAsyncConnectionPool(
                AsyncSqliteConnection, db_path=Path(f'{temp_dir}/data.sqlite'), check_same_thread=False
            ),
            schema_name='Customer',
        )

        await (await connection_mng.get_connection_pool('Shipping').get_connection()).execute(  # type: ignore[attr-defined]
            'CREATE TABLE IF NOT EXISTS Shipping (id TEXT, customer_id TEXT, status TEXT)',
        )

        await (await connection_mng.get_connection_pool('Customer').get_connection()).execute(  # type: ignore[attr-defined]
            'CREATE TABLE IF NOT EXISTS Customer (id TEXT, name TEXT)',
        )

        try:
            yield
        finally:
            await connection_mng.disconnect_all()


@pytest.mark.asyncio
async def test_data_command_service(register_default_connection: AsyncGenerator[None, None]) -> None:
    async for _ in register_default_connection:
        service = Container.services.get(AsyncDataCommandService)
        await service.execute(
            command=DataCommand(
                mutations=[
                    InsertData(
                        schema=SchemaReference(name='Shipping', version=Version.LATEST),
                        data=[
                            Data(
                                data={'id': 'id-1', 'customer_id': 'customer-1', 'status': 'shipped'},
                            ),
                        ],
                    ),
                ],
            ),
        )
        connection_mng = Container.managers.get(AsyncConnectionManager)
        connection = await connection_mng.get_connection_pool('Shipping').get_connection()
        cursor = await connection.execute('SELECT * FROM Shipping')  # type: ignore[attr-defined]
        assert await cursor.fetchall() == [('id-1', 'customer-1', 'shipped')]


@pytest.mark.asyncio
async def test_data_command_service_multiple_databases(register_default_connection: AsyncGenerator[None, None]) -> None:
    async for _ in register_default_connection:
        service = Container.services.get(AsyncDataCommandService)
        await service.execute(
            command=DataCommand(
                mutations=[
                    InsertData(
                        schema=SchemaReference(name='Shipping', version=Version.LATEST),
                        data=[
                            Data(
                                data={'id': 'id-1', 'customer_id': 'customer-1', 'status': 'shipped'},
                            ),
                        ],
                    ),
                    InsertData(
                        schema=SchemaReference(name='Customer', version=Version.LATEST),
                        data=[
                            Data(
                                data={'id': 'customer-1', 'name': 'John Doe'},
                            ),
                        ],
                    ),
                ],
            ),
        )
        connection_mng = Container.managers.get(AsyncConnectionManager)
        connection = await connection_mng.get_connection_pool('Shipping').get_connection()
        cursor = await connection.execute('SELECT * FROM Shipping')  # type: ignore[attr-defined]
        assert await cursor.fetchall() == [('id-1', 'customer-1', 'shipped')]

        connection = await connection_mng.get_connection_pool('Customer').get_connection()
        cursor = await connection.execute('SELECT * FROM Customer')  # type: ignore[attr-defined]
        assert await cursor.fetchall() == [('customer-1', 'John Doe')]
