# mypy: disable-error-code="type-abstract"
from amsdal_glue_core.common.data_models.query import QueryStatement
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.enums import Version
from amsdal_glue_core.common.operations.queries import DataQueryOperation
from amsdal_glue_core.common.services.queries import DataQueryService
from amsdal_glue_core.containers import Container
from fastapi.testclient import TestClient


def test_create_customer(test_client: TestClient) -> None:
    response = test_client.post('/api/v1/schemas/customers/', json={'name': 'John Doe', 'email': 'e1@example.com'})
    assert response.status_code == 201
    response_json = response.json()
    assert response_json == {'customer_id': None, 'name': 'John Doe', 'email': 'e1@example.com'}

    query = QueryStatement(table=SchemaReference(name='customers', version=Version.LATEST))
    query_service = Container.services.get(DataQueryService)
    result = query_service.execute(DataQueryOperation(query=query))

    assert [data.data for data in result.data] == [{'customer_id': 1, 'name': 'John Doe', 'email': 'e1@example.com'}]  # type: ignore[union-attr]


def test_create_customer_validation_error(test_client: TestClient) -> None:
    response = test_client.post('/api/v1/schemas/customers/', json={'name': 'John Doe', 'email': 1})
    assert response.status_code == 422
    response_json = response.json()
    assert response_json == {
        'detail': [
            {'input': 1, 'loc': ['body', 'email'], 'msg': 'Input should be a valid string', 'type': 'string_type'}
        ]
    }

    query = QueryStatement(table=SchemaReference(name='customers', version=Version.LATEST))
    query_service = Container.services.get(DataQueryService)
    result = query_service.execute(DataQueryOperation(query=query))

    assert [data.data for data in result.data] == []  # type: ignore[union-attr]


def test_create_customer_duplicate_error(test_client: TestClient) -> None:
    response = test_client.post(
        '/api/v1/schemas/customers/',
        json={'customer_id': 1, 'name': 'John Doe', 'email': 'e1@example.com'},
    )
    assert response.status_code == 201
    response_json = response.json()
    assert response_json == {'customer_id': 1, 'name': 'John Doe', 'email': 'e1@example.com'}

    response = test_client.post(
        '/api/v1/schemas/customers/',
        json={'customer_id': 1, 'name': 'John Doe', 'email': 'e1@example.com'},
    )
    assert response.status_code == 400
    response_json = response.json()
    assert response_json == {
        'detail': (
            "Error executing mutation: INSERT INTO 'customers' ('customer_id', "
            "'email', 'name') VALUES (?, ?, ?) with params: [1, 'e1@example.com', 'John Doe']"
        )
    }

    query = QueryStatement(table=SchemaReference(name='customers', version=Version.LATEST))
    query_service = Container.services.get(DataQueryService)
    result = query_service.execute(DataQueryOperation(query=query))

    assert [data.data for data in result.data] == [{'customer_id': 1, 'name': 'John Doe', 'email': 'e1@example.com'}]  # type: ignore[union-attr]
