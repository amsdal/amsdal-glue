from unittest import mock

from tests.sql.postgres.testcases.data_mutations import delete_customer
from tests.sql.postgres.testcases.data_mutations import insert_customers_and_orders
from tests.sql.postgres.testcases.data_mutations import simple_customer_insert
from tests.sql.postgres.testcases.data_mutations import update_two_customers
from tests.sql.postgres.unit.conftest import MockPostgresConnection


def test_insert(database_connection: MockPostgresConnection) -> None:
    simple_customer_insert(database_connection)

    database_connection.execute_mock.assert_called_once_with(
        'INSERT INTO customers (id, name) VALUES (%s, %s)',
        ('1', 'customer'),
    )


def test_insert_benchmark(database_connection: MockPostgresConnection, benchmark) -> None:
    def run_mutations():
        simple_customer_insert(database_connection)

    benchmark(run_mutations)


def test_insert_multiple(database_connection: MockPostgresConnection) -> None:
    insert_customers_and_orders(database_connection)

    database_connection.execute_mock.assert_has_calls([
        mock.call('INSERT INTO customers (id, name) VALUES (%s, %s)', ('1', 'customer')),
        mock.call('INSERT INTO customers (age, id, name) VALUES (%s, %s, %s)', (25, '2', 'customer')),
        mock.call('INSERT INTO orders (amount, customer_id, id) VALUES (%s, %s, %s)', (100, '1', '1')),
    ])


def test_insert_multiple_benchmark(database_connection: MockPostgresConnection, benchmark) -> None:
    def run_mutations():
        insert_customers_and_orders(database_connection)

    benchmark(run_mutations)


def test_update(database_connection: MockPostgresConnection) -> None:
    update_two_customers(database_connection)

    database_connection.execute_mock.assert_has_calls([
        mock.call('UPDATE customers SET id = %s, name = %s', ('1', 'new_customer')),
    ])


def test_update_benchmark(database_connection: MockPostgresConnection, benchmark) -> None:
    def run_mutations():
        update_two_customers(database_connection)

    benchmark(run_mutations)


def test_delete(database_connection: MockPostgresConnection) -> None:
    delete_customer(database_connection)

    database_connection.execute_mock.assert_called_once_with(
        'DELETE FROM customers WHERE age < %s',
        (27,),
    )


def test_delete_benchmark(database_connection: MockPostgresConnection, benchmark) -> None:
    def run_mutations():
        delete_customer(database_connection)

    benchmark(run_mutations)