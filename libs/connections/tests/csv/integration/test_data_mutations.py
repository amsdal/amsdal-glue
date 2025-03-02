import datetime

import numpy as np
import pandas as pd
import pytest
from amsdal_glue_core.common.data_models.data import Data
from amsdal_glue_core.common.data_models.schema import PropertySchema
from amsdal_glue_core.common.data_models.schema import Schema
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.enums import Version
from amsdal_glue_core.common.operations.commands import SchemaCommand
from amsdal_glue_core.common.operations.mutations.data import InsertData
from amsdal_glue_core.common.operations.mutations.schema import RegisterSchema

from amsdal_glue_connections.sql.connections.csv_connection import CsvConnection
from tests.csv.testcases.data_mutations import delete_customer
from tests.csv.testcases.data_mutations import insert_customers_and_orders
from tests.csv.testcases.data_mutations import simple_customer_insert
from tests.csv.testcases.data_mutations import update_two_customers


@pytest.fixture(scope='function')
def fixture_connection(database_connection: CsvConnection) -> CsvConnection:
    database_connection.run_schema_command(
        SchemaCommand(
            mutations=[
                RegisterSchema(
                    schema=Schema(
                        name='customers',
                        version=Version.LATEST,
                        properties=[
                            PropertySchema(name='id', type=int, required=True),
                            PropertySchema(name='name', type=str, required=True),
                            PropertySchema(name='age', type=int, required=True),
                        ],
                    )
                )
            ]
        )
    )
    database_connection.run_schema_command(
        SchemaCommand(
            mutations=[
                RegisterSchema(
                    schema=Schema(
                        name='orders',
                        version=Version.LATEST,
                        properties=[
                            PropertySchema(name='id', type=int, required=True),
                            PropertySchema(name='customer_id', type=int, required=True),
                            PropertySchema(name='amount', type=int, required=True),
                            PropertySchema(name='date', type=datetime.date, required=True),
                        ],
                    )
                )
            ]
        )
    )

    return database_connection


def test_insert(fixture_connection: CsvConnection) -> None:
    simple_customer_insert(fixture_connection)

    assert pd.read_csv(fixture_connection.db_path / 'customers.csv').replace(np.nan, None).to_dict(
        orient='records'
    ) == [
        {'id': 1, 'name': 'customer', 'age': None},
    ]

    assert pd.read_csv(fixture_connection.db_path / 'orders.csv').to_dict(orient='records') == []


def test_insert_multiple(fixture_connection: CsvConnection) -> None:
    insert_customers_and_orders(fixture_connection)
    assert pd.read_csv(fixture_connection.db_path / 'customers.csv').replace(np.nan, None).to_dict(
        orient='records'
    ) == [
        {'id': 1, 'name': 'customer', 'age': None},
        {'id': 2, 'name': 'customer', 'age': 25},
    ]
    assert pd.read_csv(fixture_connection.db_path / 'orders.csv').replace(np.nan, None).to_dict(orient='records') == [
        {'id': 1, 'customer_id': 1, 'amount': 100, 'date': None},
    ]


def test_update(fixture_connection: CsvConnection) -> None:
    update_two_customers(fixture_connection)

    assert pd.read_csv(fixture_connection.db_path / 'customers.csv').replace(np.nan, None).to_dict(
        orient='records'
    ) == [
        {'id': 1, 'name': 'new_customer', 'age': None},
    ]


def test_delete(fixture_connection: CsvConnection) -> None:
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
    assert pd.read_csv(fixture_connection.db_path / 'customers.csv').replace(np.nan, None).to_dict(
        orient='records'
    ) == [
        {'id': 1, 'name': 'customer', 'age': None},
        {'id': 2, 'name': 'customer', 'age': 25},
        {'id': 3, 'name': 'customer', 'age': 30},
    ]

    delete_customer(fixture_connection)
    assert pd.read_csv(fixture_connection.db_path / 'customers.csv').replace(np.nan, None).to_dict(
        orient='records'
    ) == [
        {'id': 1, 'name': 'customer', 'age': None},
        {'id': 3, 'name': 'customer', 'age': 30},
    ]
