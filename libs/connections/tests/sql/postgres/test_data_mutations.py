from collections.abc import Generator

import pytest
from amsdal_glue_connections.sql.connections.postgres_connection import PostgresConnection
from amsdal_glue_core.common.data_models.conditions import Condition
from amsdal_glue_core.common.data_models.conditions import Conditions
from amsdal_glue_core.common.data_models.data import Data
from amsdal_glue_core.common.data_models.field_reference import Field
from amsdal_glue_core.common.data_models.field_reference import FieldReference
from amsdal_glue_core.common.data_models.metadata import Metadata
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.enums import FieldLookup
from amsdal_glue_core.common.enums import Version
from amsdal_glue_core.common.expressions.value import Value
from amsdal_glue_core.common.operations.mutations.data import DeleteData
from amsdal_glue_core.common.operations.mutations.data import InsertData
from amsdal_glue_core.common.operations.mutations.data import UpdateData


@pytest.fixture(scope='function')
def fixture_connection(database_connection: PostgresConnection) -> Generator[PostgresConnection, None, None]:
    database_connection.execute('CREATE TABLE customers (id SERIAL PRIMARY KEY, name VARCHAR(255), age INT)')
    database_connection.execute('CREATE TABLE orders (id SERIAL PRIMARY KEY, customer_id INT, amount INT, date DATE)')

    yield database_connection


def test_insert_mutation(fixture_connection: PostgresConnection) -> None:
    fixture_connection.run_mutations([
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
                )
            ],
        ),
    ])

    assert fixture_connection.execute('SELECT id, name, age FROM customers').fetchall() == [(1, 'customer', None)]


def test_insert_multiple(fixture_connection: PostgresConnection) -> None:
    fixture_connection.run_mutations([
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
                )
            ],
        ),
        InsertData(
            schema=SchemaReference(name='customers', version=Version.LATEST),
            data=[
                Data(
                    data={'id': '2', 'name': 'customer', 'age': 25},
                    metadata=Metadata(
                        object_id='2',
                        object_version='2',
                        created_at='2021-01-01T00:00:00Z',
                        updated_at='2021-01-01T00:00:00Z',
                    ),
                )
            ],
        ),
        InsertData(
            schema=SchemaReference(name='orders', version=Version.LATEST),
            data=[
                Data(
                    data={'id': '1', 'customer_id': '1', 'amount': 100},
                    metadata=Metadata(
                        object_id='1',
                        object_version='1',
                        created_at='2021-01-01T00:00:00Z',
                        updated_at='2021-01-01T00:00:00Z',
                    ),
                )
            ],
        ),
    ])

    assert fixture_connection.execute('SELECT id, name, age FROM customers').fetchall() == [
        (1, 'customer', None),
        (2, 'customer', 25),
    ]
    assert fixture_connection.execute('SELECT id, customer_id, amount FROM orders').fetchall() == [(1, 1, 100)]


def test_update_mutation(fixture_connection: PostgresConnection) -> None:
    fixture_connection.run_mutations([
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
                )
            ],
        ),
        UpdateData(
            schema=SchemaReference(name='customers', version=Version.LATEST),
            data=Data(
                data={'id': '1', 'name': 'new_customer'},
                metadata=Metadata(
                    object_id='1',
                    object_version='2',
                    created_at='2021-01-01T00:00:00Z',
                    updated_at='2021-01-01T00:00:00Z',
                ),
            ),
        ),
    ])

    assert fixture_connection.execute('SELECT id, name, age FROM customers').fetchall() == [(1, 'new_customer', None)]


def test_delete_mutation(fixture_connection: PostgresConnection) -> None:
    fixture_connection.run_mutations([
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
    assert fixture_connection.execute('SELECT id, name, age FROM customers').fetchall() == [
        (1, 'customer', None),
        (2, 'customer', 25),
        (3, 'customer', 30),
    ]

    fixture_connection.run_mutations([
        DeleteData(
            schema=SchemaReference(name='customers', version=Version.LATEST),
            query=Conditions(
                Condition(
                    field=FieldReference(field=Field(name='age'), table_name=''),
                    lookup=FieldLookup.LT,
                    value=Value(27),
                ),
            ),
        ),
    ])
    assert fixture_connection.execute('SELECT id, name, age FROM customers').fetchall() == [
        (1, 'customer', None),
        (3, 'customer', 30),
    ]