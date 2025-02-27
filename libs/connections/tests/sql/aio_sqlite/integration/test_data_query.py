import pytest

from amsdal_glue_connections.sql.connections.sqlite_connection import AsyncSqliteConnection
from tests.sql.aio_sqlite.testcases.data_query import query_big_orders
from tests.sql.aio_sqlite.testcases.data_query import query_customers
from tests.sql.aio_sqlite.testcases.data_query import query_customers_age
from tests.sql.aio_sqlite.testcases.data_query import query_customers_expenses
from tests.sql.aio_sqlite.testcases.data_query import query_expenses_by_customer
from tests.sql.aio_sqlite.testcases.data_query import query_expenses_by_customer_with_name
from tests.sql.aio_sqlite.testcases.data_query import query_orders_for_customer
from tests.sql.aio_sqlite.testcases.data_query import query_orders_with_customers


@pytest.fixture(scope='function')
async def fixture_connection(database_connection: AsyncSqliteConnection) -> AsyncSqliteConnection:
    await database_connection.execute('CREATE TABLE customers (id SERIAL PRIMARY KEY, name VARCHAR(255), age INT)')
    await database_connection.execute(
        'CREATE TABLE orders (id SERIAL PRIMARY KEY, customer_id INT, amount INT, date DATE)'
    )
    await database_connection.execute('INSERT INTO customers (id, name, age) VALUES (?, ?, ?)', 1, 'Alice', 25)
    await database_connection.execute('INSERT INTO customers (id, name, age) VALUES (?, ?, ?)', 2, 'Bob', 25)
    await database_connection.execute('INSERT INTO customers (id, name, age) VALUES (?, ?, ?)', 3, 'Charlie', 35)
    await database_connection.execute('INSERT INTO orders (id, customer_id, amount) VALUES (?, ?, ?)', 1, 1, 100)
    await database_connection.execute('INSERT INTO orders (id, customer_id, amount) VALUES (?, ?, ?)', 2, 1, 200)
    await database_connection.execute('INSERT INTO orders (id, customer_id, amount) VALUES (?, ?, ?)', 3, 2, 400)

    return database_connection


@pytest.mark.asyncio
async def test_simple_query(fixture_connection: AsyncSqliteConnection) -> None:
    result_data = await query_customers(fixture_connection)

    assert [d.data for d in result_data] == [
        {'id': 1, 'name': 'Alice', 'age': 25},
        {'id': 2, 'name': 'Bob', 'age': 25},
        {'id': 3, 'name': 'Charlie', 'age': 35},
    ]


@pytest.mark.asyncio
async def test_join_query(fixture_connection: AsyncSqliteConnection) -> None:
    result_data = await query_orders_with_customers(fixture_connection)

    assert [d.data for d in result_data] == [
        {'id': 1, 'amount': 100, 'customer_id': 1, 'name': 'Alice', 'age': 25},
        {'id': 2, 'amount': 200, 'customer_id': 1, 'name': 'Alice', 'age': 25},
        {'id': 3, 'amount': 400, 'customer_id': 2, 'name': 'Bob', 'age': 25},
    ]


@pytest.mark.asyncio
async def test_query_distinct(fixture_connection: AsyncSqliteConnection) -> None:
    result_data = await query_customers_age(fixture_connection)

    assert [d.data for d in result_data] == [
        {'age': 25},
        {'age': 25},
        {'age': 35},
    ]

    result_data = await query_customers_age(fixture_connection, distinct=True)

    assert [d.data for d in result_data] == [
        {'age': 25},
        {'age': 35},
    ]


@pytest.mark.asyncio
async def test_filter_conditions(fixture_connection: AsyncSqliteConnection) -> None:
    result_data = await query_big_orders(fixture_connection)

    assert [d.data for d in result_data] == [
        {'id': 2, 'amount': 200, 'customer_id': 1},
        {'id': 3, 'amount': 400, 'customer_id': 2},
    ]


@pytest.mark.asyncio
async def test_filter_conditions_join(fixture_connection: AsyncSqliteConnection) -> None:
    result_data = await query_orders_for_customer(fixture_connection)

    assert [d.data for d in result_data] == [
        {'id': 1, 'amount': 100, 'customer_id': 1, 'age': 25},
        {'id': 2, 'amount': 200, 'customer_id': 1, 'age': 25},
    ]


@pytest.mark.asyncio
async def test_annotation(fixture_connection: AsyncSqliteConnection) -> None:
    result_data = await query_customers_expenses(fixture_connection)

    assert [d.data for d in result_data] == [
        {'id': 1, 'total_amount': 300},
        {'id': 2, 'total_amount': 400},
        {'id': 3, 'total_amount': None},
    ]


@pytest.mark.asyncio
async def test_aggregation(fixture_connection: AsyncSqliteConnection) -> None:
    result_data = await query_expenses_by_customer(fixture_connection)

    assert [d.data for d in result_data] == [
        {'customer_id': 1, 'total_amount': 300},
        {'customer_id': 2, 'total_amount': 400},
    ]


@pytest.mark.asyncio
async def test_aggregation_join(fixture_connection: AsyncSqliteConnection) -> None:
    result_data = await query_expenses_by_customer_with_name(fixture_connection)

    assert [d.data for d in result_data] == [
        {'id': 1, 'name': 'Alice', 'sum_amount': 300},
        {'id': 2, 'name': 'Bob', 'sum_amount': 400},
    ]
