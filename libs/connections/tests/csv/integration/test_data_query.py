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
from tests.csv.testcases.data_query import query_big_orders
from tests.csv.testcases.data_query import query_customers
from tests.csv.testcases.data_query import query_customers_age
from tests.csv.testcases.data_query import query_customers_expenses
from tests.csv.testcases.data_query import query_expenses_by_customer
from tests.csv.testcases.data_query import query_expenses_by_customer_with_name
from tests.csv.testcases.data_query import query_orders_for_customer
from tests.csv.testcases.data_query import query_orders_with_customers


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
                        ],
                    )
                )
            ]
        )
    )
    database_connection.run_mutations([
        InsertData(
            schema=SchemaReference(name='customers', version=Version.LATEST),
            data=[Data(data={'id': 1, 'name': 'Alice', 'age': 25})],
        ),
        InsertData(
            schema=SchemaReference(name='customers', version=Version.LATEST),
            data=[Data(data={'id': 2, 'name': 'Bob', 'age': 25})],
        ),
        InsertData(
            schema=SchemaReference(name='customers', version=Version.LATEST),
            data=[Data(data={'id': 3, 'name': 'Charlie', 'age': 35})],
        ),
        InsertData(
            schema=SchemaReference(name='orders', version=Version.LATEST),
            data=[Data(data={'id': 1, 'customer_id': 1, 'amount': 100})],
        ),
        InsertData(
            schema=SchemaReference(name='orders', version=Version.LATEST),
            data=[Data(data={'id': 2, 'customer_id': 1, 'amount': 200})],
        ),
        InsertData(
            schema=SchemaReference(name='orders', version=Version.LATEST),
            data=[Data(data={'id': 3, 'customer_id': 2, 'amount': 400})],
        ),
    ])
    return database_connection


def test_simple_query(fixture_connection: CsvConnection) -> None:
    result_data = query_customers(fixture_connection)

    assert [d.data for d in result_data] == [
        {'id': 1, 'name': 'Alice', 'age': 25},
        {'id': 2, 'name': 'Bob', 'age': 25},
        {'id': 3, 'name': 'Charlie', 'age': 35},
    ]


def test_join_query(fixture_connection: CsvConnection) -> None:
    result_data = query_orders_with_customers(fixture_connection)

    assert [d.data for d in result_data] == [
        {'id': 1, 'amount': 100, 'customer_id': 1, 'name': 'Alice', 'age': 25},
        {'id': 2, 'amount': 200, 'customer_id': 1, 'name': 'Alice', 'age': 25},
        {'id': 3, 'amount': 400, 'customer_id': 2, 'name': 'Bob', 'age': 25},
    ]


def test_query_distinct(fixture_connection: CsvConnection) -> None:
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


def test_filter_conditions(fixture_connection: CsvConnection) -> None:
    result_data = query_big_orders(fixture_connection)

    assert [d.data for d in result_data] == [
        {'id': 2, 'amount': 200, 'customer_id': 1},
        {'id': 3, 'amount': 400, 'customer_id': 2},
    ]


def test_filter_conditions_join(fixture_connection: CsvConnection) -> None:
    result_data = query_orders_for_customer(fixture_connection)

    assert [d.data for d in result_data] == [
        {'id': 1, 'amount': 100, 'customer_id': 1, 'age': 25},
        {'id': 2, 'amount': 200, 'customer_id': 1, 'age': 25},
    ]


def test_annotation(fixture_connection: CsvConnection) -> None:
    result_data = query_customers_expenses(fixture_connection)

    assert [d.data for d in result_data] == [
        {'id': 1, 'total_amount': 300},
        {'id': 2, 'total_amount': 400},
        {'id': 3, 'total_amount': 0},
    ]


def test_aggregation(fixture_connection: CsvConnection) -> None:
    result_data = query_expenses_by_customer(fixture_connection)

    assert [d.data for d in result_data] == [
        {'customer_id': 1, 'total_amount': 300},
        {'customer_id': 2, 'total_amount': 400},
    ]


def test_aggregation_join(fixture_connection: CsvConnection) -> None:
    result_data = query_expenses_by_customer_with_name(fixture_connection)

    assert [d.data for d in result_data] == [
        {'id': 1, 'name': 'Alice', 'sum_amount': 300},
        {'id': 2, 'name': 'Bob', 'sum_amount': 400},
    ]
