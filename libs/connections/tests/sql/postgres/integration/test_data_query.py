from collections.abc import Generator

import pytest

from amsdal_glue_connections.sql.connections.postgres_connection import PostgresConnection
from tests.sql.postgres.testcases.data_query import query_big_orders
from tests.sql.postgres.testcases.data_query import query_customers
from tests.sql.postgres.testcases.data_query import query_customers_age
from tests.sql.postgres.testcases.data_query import query_customers_expenses
from tests.sql.postgres.testcases.data_query import query_expenses_by_customer
from tests.sql.postgres.testcases.data_query import query_expenses_by_customer_with_name
from tests.sql.postgres.testcases.data_query import query_orders_for_customer
from tests.sql.postgres.testcases.data_query import query_orders_with_customers


@pytest.fixture(scope='function')
def fixture_connection(database_connection: PostgresConnection) -> Generator[PostgresConnection, None, None]:
    database_connection.execute('CREATE TABLE customers (id SERIAL PRIMARY KEY, name VARCHAR(255), age INT)')
    database_connection.execute('CREATE TABLE orders (id SERIAL PRIMARY KEY, customer_id INT, amount INT, date DATE)')
    database_connection.execute('INSERT INTO customers (id, name, age) VALUES (%s, %s, %s)', 1, 'Alice', 25)
    database_connection.execute('INSERT INTO customers (id, name, age) VALUES (%s, %s, %s)', 2, 'Bob', 25)
    database_connection.execute('INSERT INTO customers (id, name, age) VALUES (%s, %s, %s)', 3, 'Charlie', 35)
    database_connection.execute('INSERT INTO orders (id, customer_id, amount) VALUES (%s, %s, %s)', 1, 1, 100)
    database_connection.execute('INSERT INTO orders (id, customer_id, amount) VALUES (%s, %s, %s)', 2, 1, 200)
    database_connection.execute('INSERT INTO orders (id, customer_id, amount) VALUES (%s, %s, %s)', 3, 2, 400)

    yield database_connection


def test_simple_query(fixture_connection: PostgresConnection) -> None:
    result_data = query_customers(fixture_connection)

    assert [d.data for d in result_data] == [
        {'id': 1, 'name': 'Alice', 'age': 25},
        {'id': 2, 'name': 'Bob', 'age': 25},
        {'id': 3, 'name': 'Charlie', 'age': 35},
    ]


def test_join_query(fixture_connection: PostgresConnection) -> None:
    result_data = query_orders_with_customers(fixture_connection)

    assert [d.data for d in result_data] == [
        {'id': 1, 'amount': 100, 'customer_id': 1, 'name': 'Alice', 'age': 25},
        {'id': 2, 'amount': 200, 'customer_id': 1, 'name': 'Alice', 'age': 25},
        {'id': 3, 'amount': 400, 'customer_id': 2, 'name': 'Bob', 'age': 25},
    ]


def test_query_distinct(fixture_connection: PostgresConnection) -> None:
    result_data = query_customers_age(fixture_connection)

    assert [d.data for d in result_data] == [
        {'age': 25},
        {'age': 25},
        {'age': 35},
    ]

    result_data = query_customers_age(fixture_connection, distinct=True)

    assert [d.data for d in result_data] == [
        {'age': 25},
        {'age': 35},
    ]


def test_filter_conditions(fixture_connection: PostgresConnection) -> None:
    result_data = query_big_orders(fixture_connection)

    assert [d.data for d in result_data] == [
        {'id': 2, 'amount': 200, 'customer_id': 1},
        {'id': 3, 'amount': 400, 'customer_id': 2},
    ]


def test_filter_conditions_join(fixture_connection: PostgresConnection) -> None:
    result_data = query_orders_for_customer(fixture_connection)

    assert [d.data for d in result_data] == [
        {'id': 1, 'amount': 100, 'customer_id': 1, 'age': 25},
        {'id': 2, 'amount': 200, 'customer_id': 1, 'age': 25},
    ]


def test_annotation(fixture_connection: PostgresConnection) -> None:
    result_data = query_customers_expenses(fixture_connection)

    assert [d.data for d in result_data] == [
        {'id': 1, 'total_amount': 300},
        {'id': 2, 'total_amount': 400},
        {'id': 3, 'total_amount': None},
    ]


def test_aggregation(fixture_connection: PostgresConnection) -> None:
    result_data = query_expenses_by_customer(fixture_connection)

    assert [d.data for d in result_data] == [
        {'customer_id': 1, 'total_amount': 300},
        {'customer_id': 2, 'total_amount': 400},
    ]


def test_aggregation_join(fixture_connection: PostgresConnection) -> None:
    result_data = query_expenses_by_customer_with_name(fixture_connection)

    assert [d.data for d in result_data] == [
        {'id': 1, 'name': 'Alice', 'sum_amount': 300},
        {'id': 2, 'name': 'Bob', 'sum_amount': 400},
    ]
