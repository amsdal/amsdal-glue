from collections.abc import AsyncGenerator

import pytest

from amsdal_glue_connections.sql.connections.postgres_connection import AsyncPostgresConnection
from tests.sql.aio_postgres.testcases.data_query import query_big_orders
from tests.sql.aio_postgres.testcases.data_query import query_customers
from tests.sql.aio_postgres.testcases.data_query import query_customers_age
from tests.sql.aio_postgres.testcases.data_query import query_customers_expenses
from tests.sql.aio_postgres.testcases.data_query import query_expenses_by_customer
from tests.sql.aio_postgres.testcases.data_query import query_expenses_by_customer_with_name
from tests.sql.aio_postgres.testcases.data_query import query_orders_for_customer
from tests.sql.aio_postgres.testcases.data_query import query_orders_with_customers


@pytest.fixture(scope='function')
async def fixture_connection(
    database_connection: AsyncGenerator[AsyncPostgresConnection, None],
) -> AsyncGenerator[AsyncPostgresConnection, None]:
    async for dc in database_connection:
        await dc.execute('CREATE TABLE customers (id SERIAL PRIMARY KEY, name VARCHAR(255), age INT)')
        await dc.execute('CREATE TABLE orders (id SERIAL PRIMARY KEY, customer_id INT, amount INT, date DATE)')
        await dc.execute('INSERT INTO customers (id, name, age) VALUES (%s, %s, %s)', 1, 'Alice', 25)
        await dc.execute('INSERT INTO customers (id, name, age) VALUES (%s, %s, %s)', 2, 'Bob', 25)
        await dc.execute('INSERT INTO customers (id, name, age) VALUES (%s, %s, %s)', 3, 'Charlie', 35)
        await dc.execute('INSERT INTO orders (id, customer_id, amount) VALUES (%s, %s, %s)', 1, 1, 100)
        await dc.execute('INSERT INTO orders (id, customer_id, amount) VALUES (%s, %s, %s)', 2, 1, 200)
        await dc.execute('INSERT INTO orders (id, customer_id, amount) VALUES (%s, %s, %s)', 3, 2, 400)

        yield dc


@pytest.mark.asyncio
async def test_simple_query(fixture_connection: AsyncGenerator[AsyncPostgresConnection, None]) -> None:
    async for fc in fixture_connection:
        result_data = await query_customers(fc)

    assert [d.data for d in result_data] == [
        {'id': 1, 'name': 'Alice', 'age': 25},
        {'id': 2, 'name': 'Bob', 'age': 25},
        {'id': 3, 'name': 'Charlie', 'age': 35},
    ]


@pytest.mark.asyncio
async def test_join_query(fixture_connection: AsyncGenerator[AsyncPostgresConnection, None]) -> None:
    async for fc in fixture_connection:
        result_data = await query_orders_with_customers(fc)

    assert [d.data for d in result_data] == [
        {'id': 1, 'amount': 100, 'customer_id': 1, 'name': 'Alice', 'age': 25},
        {'id': 2, 'amount': 200, 'customer_id': 1, 'name': 'Alice', 'age': 25},
        {'id': 3, 'amount': 400, 'customer_id': 2, 'name': 'Bob', 'age': 25},
    ]


@pytest.mark.asyncio
async def test_query_distinct(fixture_connection: AsyncGenerator[AsyncPostgresConnection, None]) -> None:
    async for fc in fixture_connection:
        result_data = await query_customers_age(fc)

        assert [d.data for d in result_data] == [
            {'age': 25},
            {'age': 25},
            {'age': 35},
        ]

        result_data = await query_customers_age(fc, distinct=True)

        assert [d.data for d in result_data] == [
            {'age': 25},
            {'age': 35},
        ]


@pytest.mark.asyncio
async def test_filter_conditions(fixture_connection: AsyncGenerator[AsyncPostgresConnection, None]) -> None:
    async for fc in fixture_connection:
        result_data = await query_big_orders(fc)

    assert [d.data for d in result_data] == [
        {'id': 2, 'amount': 200, 'customer_id': 1},
        {'id': 3, 'amount': 400, 'customer_id': 2},
    ]


@pytest.mark.asyncio
async def test_filter_conditions_join(fixture_connection: AsyncGenerator[AsyncPostgresConnection, None]) -> None:
    async for fc in fixture_connection:
        result_data = await query_orders_for_customer(fc)

    assert [d.data for d in result_data] == [
        {'id': 1, 'amount': 100, 'customer_id': 1, 'age': 25},
        {'id': 2, 'amount': 200, 'customer_id': 1, 'age': 25},
    ]


@pytest.mark.asyncio
async def test_annotation(fixture_connection: AsyncGenerator[AsyncPostgresConnection, None]) -> None:
    async for fc in fixture_connection:
        result_data = await query_customers_expenses(fc)

    assert [d.data for d in result_data] == [
        {'id': 1, 'total_amount': 300},
        {'id': 2, 'total_amount': 400},
        {'id': 3, 'total_amount': None},
    ]


@pytest.mark.asyncio
async def test_aggregation(fixture_connection: AsyncGenerator[AsyncPostgresConnection, None]) -> None:
    async for fc in fixture_connection:
        result_data = await query_expenses_by_customer(fc)

    assert [d.data for d in result_data] == [
        {'customer_id': 1, 'total_amount': 300},
        {'customer_id': 2, 'total_amount': 400},
    ]


@pytest.mark.asyncio
async def test_aggregation_join(fixture_connection: AsyncGenerator[AsyncPostgresConnection, None]) -> None:
    async for fc in fixture_connection:
        result_data = await query_expenses_by_customer_with_name(fc)

    assert [d.data for d in result_data] == [
        {'id': 1, 'name': 'Alice', 'sum_amount': 300},
        {'id': 2, 'name': 'Bob', 'sum_amount': 400},
    ]
