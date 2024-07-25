# mypy: disable-error-code="type-abstract"
import pytest
from amsdal_glue_core.common.data_models.data import Data
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.enums import Version
from amsdal_glue_core.common.operations.commands import DataCommand
from amsdal_glue_core.common.operations.mutations.data import InsertData
from amsdal_glue_core.common.services.commands import DataCommandService
from amsdal_glue_core.containers import Container
from fastapi.testclient import TestClient


@pytest.fixture(scope='function', autouse=True)
def _fixture_data() -> None:
    service = Container.services.get(DataCommandService)
    service.execute(
        command=DataCommand(
            mutations=[
                InsertData(
                    schema=SchemaReference(name='customers', version=Version.LATEST),
                    data=[
                        Data(data={'customer_id': 1, 'name': 'John Doe', 'email': 'e1@example.com'}),
                        Data(data={'customer_id': 2, 'name': 'Jane Doe', 'email': 'e2@example.com'}),
                        Data(data={'customer_id': 3, 'name': 'Josh Doe', 'email': 'e3@example.com'}),
                        Data(data={'customer_id': 4, 'name': 'Jane Doe', 'email': 'e4@example.com'}),
                    ],
                ),
                InsertData(
                    schema=SchemaReference(name='logs', version=Version.LATEST),
                    data=[
                        Data(data={'created_at': '2021-01-01 00:00:00', 'message': 'Lorem ipsum dolor sit amet'}),
                        Data(data={'created_at': '2021-01-02 00:00:00', 'message': 'consectetur adipiscing elit'}),
                        Data(data={'created_at': '2021-01-03 00:00:00', 'message': 'sed do eiusmod tempor incididunt'}),
                        Data(data={'created_at': '2021-01-04 00:00:00', 'message': 'ut labore et dolore magna aliqua'}),
                    ],
                ),
                InsertData(
                    schema=SchemaReference(name='orders', version=Version.LATEST),
                    data=[
                        Data(data={'order_id': 1, 'customer_id': 1, 'product_id': 1, 'quantity': 1}),
                        Data(data={'order_id': 2, 'customer_id': 1, 'product_id': 2, 'quantity': 2}),
                        Data(data={'order_id': 3, 'customer_id': 2, 'product_id': 3, 'quantity': 3}),
                        Data(data={'order_id': 4, 'customer_id': 2, 'product_id': 4, 'quantity': 4}),
                    ],
                ),
            ],
        ),
    )


def test_query_customers(test_client: TestClient) -> None:
    response = test_client.post(
        '/api/v1/operations/data-query/',
        json={
            'table': {'name': 'customers', 'version': 'LATEST'},
        },
    )
    assert response.status_code == 200, response.text

    assert response.json() == [
        {'data': {'customer_id': 1, 'name': 'John Doe', 'email': 'e1@example.com'}, 'metadata': None},
        {'data': {'customer_id': 2, 'name': 'Jane Doe', 'email': 'e2@example.com'}, 'metadata': None},
        {'data': {'customer_id': 3, 'name': 'Josh Doe', 'email': 'e3@example.com'}, 'metadata': None},
        {'data': {'customer_id': 4, 'name': 'Jane Doe', 'email': 'e4@example.com'}, 'metadata': None},
    ]


def test_query_customers_with_limit(test_client: TestClient) -> None:
    response = test_client.post(
        '/api/v1/operations/data-query/',
        json={
            'table': {'name': 'customers', 'version': 'LATEST'},
            'limit': {'limit': 2},
        },
    )
    assert response.status_code == 200, response.text

    assert response.json() == [
        {'data': {'customer_id': 1, 'name': 'John Doe', 'email': 'e1@example.com'}, 'metadata': None},
        {'data': {'customer_id': 2, 'name': 'Jane Doe', 'email': 'e2@example.com'}, 'metadata': None},
    ]


def test_query_customers_annotation(test_client: TestClient) -> None:
    response = test_client.post(
        '/api/v1/operations/data-query/',
        json={
            'table': {'name': 'customers', 'alias': 'c', 'version': 'LATEST'},
            'only': [
                {
                    'alias': 'customer_id',
                    'field': {'name': 'customer_id'},
                    'table_name': 'c',
                }
            ],
            'annotations': [
                {
                    'value': {
                        'alias': 'total_quantity',
                        'query': {
                            'aggregations': [
                                {
                                    'expression': {
                                        'name': 'SUM',
                                        'field': {'field': {'name': 'quantity'}, 'table_name': 'o'},
                                    },
                                    'alias': 'tq',
                                }
                            ],
                            'table': {'name': 'orders', 'alias': 'o', 'version': 'LATEST'},
                            'where': {
                                'children': [
                                    {
                                        'field': {'field': {'name': 'customer_id'}, 'table_name': 'o'},
                                        'lookup': 'EQ',
                                        'value': {'field': {'name': 'customer_id'}, 'table_name': 'c'},
                                    },
                                ],
                            },
                        },
                    },
                }
            ],
            'order_by': [
                {
                    'field': {'field': {'name': 'customer_id'}, 'table_name': 'c'},
                    'direction': 'ASC',
                },
            ],
        },
    )
    assert response.status_code == 200, response.text

    assert response.json() == [
        {'data': {'customer_id': 1, 'total_quantity': 3}, 'metadata': None},
        {'data': {'customer_id': 2, 'total_quantity': 7}, 'metadata': None},
        {'data': {'customer_id': 3, 'total_quantity': None}, 'metadata': None},
        {'data': {'customer_id': 4, 'total_quantity': None}, 'metadata': None},
    ]
