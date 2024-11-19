# mypy: disable-error-code="type-abstract"
import tempfile
from collections.abc import AsyncGenerator

import pytest
from pytest_mock import MockerFixture

from amsdal_glue import AsyncSqliteConnection
from amsdal_glue import Container
from amsdal_glue import Data
from amsdal_glue import DataCommand
from amsdal_glue import DataQueryOperation
from amsdal_glue import DefaultAsyncConnectionPool
from amsdal_glue import Field
from amsdal_glue import FieldReference
from amsdal_glue import InsertData
from amsdal_glue import OrderByQuery
from amsdal_glue import OrderDirection
from amsdal_glue import QueryStatement
from amsdal_glue import RegisterSchema
from amsdal_glue import SchemaCommand
from amsdal_glue import SchemaReference
from amsdal_glue import Version
from amsdal_glue.applications.cqrs import AsyncCQRSApplication
from amsdal_glue.interfaces import AsyncDataCommandService
from amsdal_glue.interfaces import AsyncDataQueryService
from amsdal_glue.interfaces import AsyncSchemaCommandService
from amsdal_glue.interfaces import RuntimeManager


@pytest.fixture()
async def cqrs_app() -> AsyncGenerator[AsyncCQRSApplication, None]:
    app = AsyncCQRSApplication()

    with tempfile.TemporaryDirectory() as temp_dir:
        query_db_path = f'{temp_dir}/query_data.sqlite'
        command_db_path = f'{temp_dir}/command_data.sqlite'

        app.query_connection_manager.register_connection_pool(
            DefaultAsyncConnectionPool(
                AsyncSqliteConnection,
                db_path=query_db_path,
            ),
        )
        app.command_connection_manager.register_connection_pool(
            DefaultAsyncConnectionPool(
                AsyncSqliteConnection,
                db_path=command_db_path,
            ),
        )

        for connection_manager in [app.query_connection_manager, app.command_connection_manager]:
            await (await connection_manager.get_connection_pool('customers').get_connection()).execute(  # type: ignore[attr-defined]
                'CREATE TABLE IF NOT EXISTS customers (id TEXT, name TEXT)',
            )

        try:
            yield app
        finally:
            await app.shutdown()


@pytest.mark.asyncio
async def test_schema_command(cqrs_app: AsyncGenerator[AsyncCQRSApplication, None]) -> None:
    async for app in cqrs_app:
        from .fixtures.user_schema import user_schema

        service = Container.services.get(AsyncSchemaCommandService)
        result = await service.execute(
            SchemaCommand(
                mutations=[
                    RegisterSchema(schema=user_schema),
                ],
            ),
        )

        # wait for the runtime to finish
        runtime = Container.managers.get(RuntimeManager)
        runtime.shutdown()

        assert result.success is True
        assert result.schemas == [None]

        connections = [
            await app.query_connection_manager.get_connection_pool(user_schema.name).get_connection(),
            await app.command_connection_manager.get_connection_pool(user_schema.name).get_connection(),
        ]

        # check table was created in both connections
        for connection in connections:
            cursor = await connection.execute(f'PRAGMA table_info({user_schema.name})')  # type: ignore[attr-defined]
            columns = await cursor.fetchall()
            await cursor.close()

            assert len(columns) == 5


@pytest.mark.asyncio
async def test_data_command(cqrs_app: AsyncGenerator[AsyncCQRSApplication, None]):
    async for app in cqrs_app:
        service = Container.services.get(AsyncDataCommandService)
        result = await service.execute(
            DataCommand(
                mutations=[
                    InsertData(
                        schema=SchemaReference(name='customers', version=Version.LATEST),
                        data=[
                            Data(data={'id': '1', 'name': 'Alice'}),
                            Data(data={'id': '2', 'name': 'Bob'}),
                        ],
                    ),
                ],
            ),
        )

        assert result.success is True

        connections = [
            await app.query_connection_manager.get_connection_pool('customers').get_connection(),
            await app.command_connection_manager.get_connection_pool('customers').get_connection(),
        ]

        # wait for the runtime to finish
        runtime = Container.managers.get(RuntimeManager)
        runtime.shutdown()

        # check records were created in both connections
        for connection in connections:
            cursor = await connection.execute('SELECT * FROM customers ORDER BY id')  # type: ignore[attr-defined]
            records = await cursor.fetchall()
            await cursor.close()

            assert records == [('1', 'Alice'), ('2', 'Bob')]


@pytest.mark.asyncio
async def test_data_query(cqrs_app: AsyncGenerator[AsyncCQRSApplication, None], mocker: MockerFixture):
    async for app in cqrs_app:
        service = Container.services.get(AsyncDataCommandService)
        result = await service.execute(
            DataCommand(
                mutations=[
                    InsertData(
                        schema=SchemaReference(name='customers', version=Version.LATEST),
                        data=[
                            Data(data={'id': '1', 'name': 'Alice'}),
                            Data(data={'id': '2', 'name': 'Bob'}),
                        ],
                    ),
                ],
            ),
        )

        assert result.success is True

        # wait for the runtime to finish
        runtime = Container.managers.get(RuntimeManager)
        runtime.shutdown()

        mocked_command_connection_pool = mocker.Mock(spec=DefaultAsyncConnectionPool)
        await app.command_connection_manager.disconnect_all()
        app.command_connection_manager.register_connection_pool(mocked_command_connection_pool)

        query_service = Container.services.get(AsyncDataQueryService)
        query = QueryStatement(
            table=SchemaReference(name='customers', version=Version.LATEST),
            order_by=[
                OrderByQuery(
                    field=FieldReference(field=Field(name='id'), table_name='customers'),
                    direction=OrderDirection.ASC,
                ),
            ],
        )
        data_result = await query_service.execute(
            query_op=DataQueryOperation(
                query=query,
            ),
        )
        assert data_result.success is True
        assert data_result.data
        assert [item.data if item else None for item in data_result.data] == [
            {'id': '1', 'name': 'Alice'},
            {'id': '2', 'name': 'Bob'},
        ]
        assert mocked_command_connection_pool.get_connection.called is False
