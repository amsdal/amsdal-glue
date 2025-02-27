from collections.abc import Generator

import pytest
from amsdal_glue_core.common.data_models.data import Data
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.enums import Version
from amsdal_glue_core.common.operations.mutations.data import InsertData

from amsdal_glue_connections.sql.connections.postgres_connection import PostgresConnection
from tests.sql.postgres.testcases.data_mutations import delete_customer
from tests.sql.postgres.testcases.data_mutations import insert_customers_and_orders
from tests.sql.postgres.testcases.data_mutations import simple_customer_insert
from tests.sql.postgres.testcases.data_mutations import update_two_customers


@pytest.fixture(scope='function')
def fixture_connection(database_connection: PostgresConnection) -> Generator[PostgresConnection, None, None]:
    database_connection.execute('CREATE TABLE customers (id SERIAL PRIMARY KEY, name VARCHAR(255), age INT)')
    database_connection.execute('CREATE TABLE orders (id SERIAL PRIMARY KEY, customer_id INT, amount INT, date DATE)')

    yield database_connection


def test_insert(fixture_connection: PostgresConnection) -> None:
    simple_customer_insert(fixture_connection)

    assert fixture_connection.execute('SELECT id, name, age FROM customers').fetchall() == [(1, 'customer', None)]


def test_insert_multiple(fixture_connection: PostgresConnection) -> None:
    insert_customers_and_orders(fixture_connection)
    assert fixture_connection.execute('SELECT id, name, age FROM customers').fetchall() == [
        (1, 'customer', None),
        (2, 'customer', 25),
    ]
    assert fixture_connection.execute('SELECT id, customer_id, amount FROM orders').fetchall() == [(1, 1, 100)]


def test_update(fixture_connection: PostgresConnection) -> None:
    update_two_customers(fixture_connection)

    assert fixture_connection.execute('SELECT id, name, age FROM customers').fetchall() == [(1, 'new_customer', None)]


def test_delete(fixture_connection: PostgresConnection) -> None:
    fixture_connection.run_mutations([
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
    assert fixture_connection.execute('SELECT id, name, age FROM customers').fetchall() == [
        (1, 'customer', None),
        (2, 'customer', 25),
        (3, 'customer', 30),
    ]

    delete_customer(fixture_connection)
    assert fixture_connection.execute('SELECT id, name, age FROM customers').fetchall() == [
        (1, 'customer', None),
        (3, 'customer', 30),
    ]
