# mypy: disable-error-code="type-abstract"
from amsdal_glue_core.common.data_models.query import QueryStatement
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.enums import Version
from amsdal_glue_core.common.operations.queries import DataQueryOperation
from amsdal_glue_core.common.services.queries import DataQueryService
from amsdal_glue_core.containers import Container
from fastapi.testclient import TestClient


def test_create_customer(test_client: TestClient) -> None:
    response = test_client.post(
        '/api/v1/operations/insert-command/',
        json={
            'schema': {'name': 'customers', 'version': 'LATEST'},
            'data': [
                {'data': {'customer_id': 1, 'name': 'John Doe', 'email': 'e1@example.com'}},
                {'data': {'customer_id': 2, 'name': 'Jane Doe', 'email': 'e2@example.com'}},
                {'data': {'customer_id': 3, 'name': 'John Smith', 'email': 'e3@example.com'}},
            ],
        },
    )
    assert response.status_code == 200, response.text

    query = QueryStatement(table=SchemaReference(name='customers', version=Version.LATEST))
    query_service = Container.services.get(DataQueryService)
    result = query_service.execute(DataQueryOperation(query=query))

    assert [data.data for data in result.data] == [  # type: ignore[union-attr]
        {'customer_id': 1, 'name': 'John Doe', 'email': 'e1@example.com'},
        {'customer_id': 2, 'name': 'Jane Doe', 'email': 'e2@example.com'},
        {'customer_id': 3, 'name': 'John Smith', 'email': 'e3@example.com'},
    ]


def test_update_customer(test_client: TestClient) -> None:
    response = test_client.post(
        '/api/v1/operations/insert-command/',
        json={
            'schema': {'name': 'customers', 'version': 'LATEST'},
            'data': [
                {'data': {'customer_id': 1, 'name': 'John Doe', 'email': 'e1@example.com'}},
                {'data': {'customer_id': 2, 'name': 'Jane Doe', 'email': 'e2@example.com'}},
                {'data': {'customer_id': 3, 'name': 'John Smith', 'email': 'e3@example.com'}},
            ],
        },
    )
    assert response.status_code == 200, response.text

    response = test_client.post(
        '/api/v1/operations/update-command/',
        json={
            'schema': {'name': 'customers', 'version': 'LATEST'},
            'data': {'data': {'customer_id': 1, 'name': 'Jake Doe', 'email': 'e123@example.com'}},
            'query': {
                'children': [
                    {
                        'field': {'field': {'name': 'customer_id'}, 'table_name': 'customers'},
                        'lookup': 'EQ',
                        'value': {'value': 1},
                    }
                ]
            },
        },
    )
    assert response.status_code == 200, response.text

    query = QueryStatement(table=SchemaReference(name='customers', version=Version.LATEST))
    query_service = Container.services.get(DataQueryService)
    result = query_service.execute(DataQueryOperation(query=query))

    assert [data.data for data in result.data] == [  # type: ignore[union-attr]
        {'customer_id': 1, 'name': 'Jake Doe', 'email': 'e123@example.com'},
        {'customer_id': 2, 'name': 'Jane Doe', 'email': 'e2@example.com'},
        {'customer_id': 3, 'name': 'John Smith', 'email': 'e3@example.com'},
    ]


def test_delete_customer(test_client: TestClient) -> None:
    response = test_client.post(
        '/api/v1/operations/insert-command/',
        json={
            'schema': {'name': 'customers', 'version': 'LATEST'},
            'data': [
                {'data': {'customer_id': 1, 'name': 'John Doe', 'email': 'e1@example.com'}},
                {'data': {'customer_id': 2, 'name': 'Jane Doe', 'email': 'e2@example.com'}},
                {'data': {'customer_id': 3, 'name': 'John Smith', 'email': 'e3@example.com'}},
            ],
        },
    )
    assert response.status_code == 200, response.text

    response = test_client.post(
        '/api/v1/operations/delete-command/',
        json={
            'schema': {'name': 'customers', 'version': 'LATEST'},
            'query': {
                'children': [
                    {
                        'field': {'field': {'name': 'customer_id'}, 'table_name': 'customers'},
                        'lookup': 'EQ',
                        'value': {'value': 1},
                    }
                ]
            },
        },
    )
    assert response.status_code == 200, response.text

    query = QueryStatement(table=SchemaReference(name='customers', version=Version.LATEST))
    query_service = Container.services.get(DataQueryService)
    result = query_service.execute(DataQueryOperation(query=query))

    assert [data.data for data in result.data] == [  # type: ignore[union-attr]
        {'customer_id': 2, 'name': 'Jane Doe', 'email': 'e2@example.com'},
        {'customer_id': 3, 'name': 'John Smith', 'email': 'e3@example.com'},
    ]
