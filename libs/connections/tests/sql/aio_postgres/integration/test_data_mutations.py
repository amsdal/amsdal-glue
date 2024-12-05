from collections.abc import AsyncGenerator

import pytest
from amsdal_glue_core.common.data_models.data import Data
from amsdal_glue_core.common.data_models.metadata import Metadata
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.enums import Version
from amsdal_glue_core.common.operations.mutations.data import InsertData

from amsdal_glue_connections.sql.connections.postgres_connection import AsyncPostgresConnection
from tests.sql.aio_postgres.testcases.data_mutations import delete_customer
from tests.sql.aio_postgres.testcases.data_mutations import insert_customers_and_orders
from tests.sql.aio_postgres.testcases.data_mutations import simple_customer_insert
from tests.sql.aio_postgres.testcases.data_mutations import update_two_customers


@pytest.fixture(scope='function')
async def fixture_connection(
    database_connection: AsyncGenerator[AsyncPostgresConnection, None],
) -> AsyncGenerator[AsyncPostgresConnection, None]:
    async for dc in database_connection:
        await dc.execute('CREATE TABLE customers (id SERIAL PRIMARY KEY, name VARCHAR(255), age INT)')
        await dc.execute('CREATE TABLE orders (id SERIAL PRIMARY KEY, customer_id INT, amount INT, date DATE)')

        yield dc


@pytest.mark.asyncio
async def test_insert(fixture_connection: AsyncGenerator[AsyncPostgresConnection, None]) -> None:
    async for fc in fixture_connection:
        await simple_customer_insert(fc)

        assert await (await fc.execute('SELECT id, name, age FROM customers')).fetchall() == [(1, 'customer', None)]


@pytest.mark.asyncio
async def test_insert_multiple(
    fixture_connection: AsyncGenerator[AsyncPostgresConnection, None],
) -> None:
    async for fc in fixture_connection:
        await insert_customers_and_orders(fc)
        assert await (await fc.execute('SELECT id, name, age FROM customers')).fetchall() == [
            (1, 'customer', None),
            (2, 'customer', 25),
        ]
        assert await (await fc.execute('SELECT id, customer_id, amount FROM orders')).fetchall() == [(1, 1, 100)]


@pytest.mark.asyncio
async def test_update(
    fixture_connection: AsyncGenerator[AsyncPostgresConnection, None],
) -> None:
    async for fc in fixture_connection:
        await update_two_customers(fc)

        assert await (await fc.execute('SELECT id, name, age FROM customers')).fetchall() == [(1, 'new_customer', None)]


@pytest.mark.asyncio
async def test_delete(
    fixture_connection: AsyncGenerator[AsyncPostgresConnection, None],
) -> None:
    async for fc in fixture_connection:
        await fc.run_mutations([
            InsertData(
                schema=SchemaReference(name='customers', version=Version.LATEST),
                data=[
                    Data(
                        data={'id': '1', 'name': 'customer'},
                        metadata=Metadata(
                            object_id='1',
                            object_version='1',
                            created_at='2021-01-01T00:00:00Z',
                            updated_at='2021-01-01T00:00:00Z',
                        ),
                    ),
                    Data(
                        data={'id': '2', 'name': 'customer', 'age': 25},
                        metadata=Metadata(
                            object_id='2',
                            object_version='2',
                            created_at='2021-01-01T00:00:00Z',
                            updated_at='2021-01-01T00:00:00Z',
                        ),
                    ),
                    Data(
                        data={'id': '3', 'name': 'customer', 'age': 30},
                        metadata=Metadata(
                            object_id='3',
                            object_version='3',
                            created_at='2021-01-01T00:00:00Z',
                            updated_at='2021-01-01T00:00:00Z',
                        ),
                    ),
                ],
            ),
        ])
        assert await (await fc.execute('SELECT id, name, age FROM customers')).fetchall() == [
            (1, 'customer', None),
            (2, 'customer', 25),
            (3, 'customer', 30),
        ]

        await delete_customer(fc)
        assert await (await fc.execute('SELECT id, name, age FROM customers')).fetchall() == [
            (1, 'customer', None),
            (3, 'customer', 30),
        ]
