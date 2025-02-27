import pytest
from amsdal_glue_core.common.data_models.data import Data
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
    database_connection: AsyncPostgresConnection,
) -> AsyncPostgresConnection:
    await database_connection.execute('CREATE TABLE customers (id SERIAL PRIMARY KEY, name VARCHAR(255), age INT)')
    await database_connection.execute(
        'CREATE TABLE orders (id SERIAL PRIMARY KEY, customer_id INT, amount INT, date DATE)'
    )

    return database_connection


@pytest.mark.asyncio
async def test_insert(fixture_connection: AsyncPostgresConnection) -> None:
    await simple_customer_insert(fixture_connection)

    assert await (await fixture_connection.execute('SELECT id, name, age FROM customers')).fetchall() == [
        (1, 'customer', None)
    ]


@pytest.mark.asyncio
async def test_insert_multiple(fixture_connection: AsyncPostgresConnection) -> None:
    await insert_customers_and_orders(fixture_connection)
    assert await (await fixture_connection.execute('SELECT id, name, age FROM customers')).fetchall() == [
        (1, 'customer', None),
        (2, 'customer', 25),
    ]
    assert await (await fixture_connection.execute('SELECT id, customer_id, amount FROM orders')).fetchall() == [
        (1, 1, 100)
    ]


@pytest.mark.asyncio
async def test_update(fixture_connection: AsyncPostgresConnection) -> None:
    await update_two_customers(fixture_connection)

    assert await (await fixture_connection.execute('SELECT id, name, age FROM customers')).fetchall() == [
        (1, 'new_customer', None)
    ]


@pytest.mark.asyncio
async def test_delete(fixture_connection: AsyncPostgresConnection) -> None:
    await fixture_connection.run_mutations([
        InsertData(
            schema=SchemaReference(name='customers', version=Version.LATEST),
            data=[
                Data(
                    data={'id': '1', 'name': 'customer'},
                ),
                Data(
                    data={'id': '2', 'name': 'customer', 'age': 25},
                ),
                Data(
                    data={'id': '3', 'name': 'customer', 'age': 30},
                ),
            ],
        ),
    ])
    assert await (await fixture_connection.execute('SELECT id, name, age FROM customers')).fetchall() == [
        (1, 'customer', None),
        (2, 'customer', 25),
        (3, 'customer', 30),
    ]

    await delete_customer(fixture_connection)
    assert await (await fixture_connection.execute('SELECT id, name, age FROM customers')).fetchall() == [
        (1, 'customer', None),
        (3, 'customer', 30),
    ]
