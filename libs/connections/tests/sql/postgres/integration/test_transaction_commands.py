import datetime
from collections.abc import Generator

import pytest
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.enums import TransactionAction
from amsdal_glue_core.common.enums import Version
from amsdal_glue_core.common.operations.commands import TransactionCommand

from amsdal_glue_connections.sql.connections.postgres_connection import PostgresConnection


@pytest.fixture(scope='function')
def fixture_connection(database_connection: PostgresConnection) -> Generator[PostgresConnection, None, None]:
    database_connection.execute('CREATE TABLE customers (id SERIAL PRIMARY KEY, name VARCHAR(255), age INT)')
    database_connection.execute('CREATE TABLE orders (id SERIAL PRIMARY KEY, customer_id INT, amount INT, date DATE)')
    database_connection.connection.commit()

    yield database_connection


def test_successful_transaction(fixture_connection: PostgresConnection) -> None:
    assert fixture_connection.begin_transaction(
        transaction=TransactionCommand(
            transaction_id='test_transaction',
            schema=SchemaReference(name='customers', version=Version.LATEST),
            action=TransactionAction.BEGIN,
        )
    )

    fixture_connection.execute('INSERT INTO customers (name, age) VALUES (%s, %s)', 'customer', 25)
    fixture_connection.execute(
        'INSERT INTO orders (customer_id, amount, date) VALUES (%s, %s, %s)', 1, 100, '2021-01-01'
    )

    assert fixture_connection.commit_transaction(
        transaction=TransactionCommand(
            transaction_id='test_transaction',
            schema=SchemaReference(name='customers', version=Version.LATEST),
            action=TransactionAction.COMMIT,
        )
    )

    assert fixture_connection.execute('SELECT id, name, age FROM customers').fetchall() == [
        (1, 'customer', 25),
    ]
    assert [
        (1, 1, 100, datetime.date(2021, 1, 1)),
    ] == fixture_connection.execute('SELECT id, customer_id, amount, date FROM orders').fetchall()


def test_successful_transaction_rollback(fixture_connection: PostgresConnection) -> None:
    assert fixture_connection.begin_transaction(
        transaction=TransactionCommand(
            transaction_id='test_transaction',
            schema=SchemaReference(name='customers', version=Version.LATEST),
            action=TransactionAction.BEGIN,
        )
    )

    fixture_connection.execute('INSERT INTO customers (name, age) VALUES (%s, %s)', 'customer', 25)
    fixture_connection.execute(
        'INSERT INTO orders (customer_id, amount, date) VALUES (%s, %s, %s)', 1, 100, '2021-01-01'
    )

    assert fixture_connection.rollback_transaction(
        transaction=TransactionCommand(
            transaction_id='test_transaction',
            schema=SchemaReference(name='customers', version=Version.LATEST),
            action=TransactionAction.ROLLBACK,
        )
    )

    assert fixture_connection.execute('SELECT id, name, age FROM customers').fetchall() == []
    assert fixture_connection.execute('SELECT id, customer_id, amount, date FROM orders').fetchall() == []


def test_successful_nested_transaction(fixture_connection: PostgresConnection) -> None:
    assert fixture_connection.begin_transaction(
        transaction=TransactionCommand(
            transaction_id='test_transaction',
            schema=SchemaReference(name='customers', version=Version.LATEST),
            action=TransactionAction.BEGIN,
        )
    )

    fixture_connection.execute('INSERT INTO customers (name, age) VALUES (%s, %s)', 'customer', 25)

    assert fixture_connection.begin_transaction(
        transaction=TransactionCommand(
            transaction_id='test_nested_transaction',
            schema=SchemaReference(name='customers', version=Version.LATEST),
            action=TransactionAction.BEGIN,
            parent_transaction_id='test_transaction',
        )
    )
    fixture_connection.execute(
        'INSERT INTO orders (customer_id, amount, date) VALUES (%s, %s, %s)', 1, 100, '2021-01-01'
    )

    assert fixture_connection.commit_transaction(
        transaction=TransactionCommand(
            transaction_id='test_transaction',
            schema=SchemaReference(name='customers', version=Version.LATEST),
            action=TransactionAction.COMMIT,
        )
    )

    assert fixture_connection.execute('SELECT id, name, age FROM customers').fetchall() == [
        (1, 'customer', 25),
    ]
    assert [
        (1, 1, 100, datetime.date(2021, 1, 1)),
    ] == fixture_connection.execute('SELECT id, customer_id, amount, date FROM orders').fetchall()


def test_successful_nested_transaction_revert(fixture_connection: PostgresConnection) -> None:
    assert fixture_connection.begin_transaction(
        transaction=TransactionCommand(
            transaction_id='test_transaction',
            schema=SchemaReference(name='customers', version=Version.LATEST),
            action=TransactionAction.BEGIN,
        )
    )

    fixture_connection.execute('INSERT INTO customers (name, age) VALUES (%s, %s)', 'customer', 25)

    assert fixture_connection.begin_transaction(
        transaction=TransactionCommand(
            transaction_id='test_nested_transaction',
            schema=SchemaReference(name='customers', version=Version.LATEST),
            action=TransactionAction.BEGIN,
            parent_transaction_id='test_transaction',
        )
    )
    fixture_connection.execute(
        'INSERT INTO orders (customer_id, amount, date) VALUES (%s, %s, %s)', 1, 100, '2021-01-01'
    )

    assert fixture_connection.rollback_transaction(
        transaction=TransactionCommand(
            transaction_id='test_nested_transaction',
            schema=SchemaReference(name='customers', version=Version.LATEST),
            action=TransactionAction.ROLLBACK,
            parent_transaction_id='test_transaction',
        )
    )

    assert fixture_connection.commit_transaction(
        transaction=TransactionCommand(
            transaction_id='test_transaction',
            schema=SchemaReference(name='customers', version=Version.LATEST),
            action=TransactionAction.COMMIT,
        )
    )

    assert fixture_connection.execute('SELECT id, name, age FROM customers').fetchall() == [
        (1, 'customer', 25),
    ]
    assert fixture_connection.execute('SELECT id, customer_id, amount, date FROM orders').fetchall() == []


def test_successful_nested_transaction_revert_outer(fixture_connection: PostgresConnection) -> None:
    assert fixture_connection.begin_transaction(
        transaction=TransactionCommand(
            transaction_id='test_transaction',
            schema=SchemaReference(name='customers', version=Version.LATEST),
            action=TransactionAction.BEGIN,
        )
    )

    fixture_connection.execute('INSERT INTO customers (name, age) VALUES (%s, %s)', 'customer', 25)

    assert fixture_connection.begin_transaction(
        transaction=TransactionCommand(
            transaction_id='test_nested_transaction',
            schema=SchemaReference(name='customers', version=Version.LATEST),
            action=TransactionAction.BEGIN,
            parent_transaction_id='test_transaction',
        )
    )
    fixture_connection.execute(
        'INSERT INTO orders (customer_id, amount, date) VALUES (%s, %s, %s)', 1, 100, '2021-01-01'
    )

    assert fixture_connection.rollback_transaction(
        transaction=TransactionCommand(
            transaction_id='test_transaction',
            schema=SchemaReference(name='customers', version=Version.LATEST),
            action=TransactionAction.ROLLBACK,
        )
    )

    assert fixture_connection.execute('SELECT id, name, age FROM customers').fetchall() == []
    assert fixture_connection.execute('SELECT id, customer_id, amount, date FROM orders').fetchall() == []
