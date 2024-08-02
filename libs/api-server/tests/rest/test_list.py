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
            ],
        ),
    )


def test_list_customers(test_client: TestClient) -> None:
    response = test_client.get('/api/v1/schemas/customers/')
    assert response.status_code == 200
    response_json = response.json()
    assert response_json == [
        {'customer_id': 1, 'name': 'John Doe', 'email': 'e1@example.com'},
        {'customer_id': 2, 'name': 'Jane Doe', 'email': 'e2@example.com'},
        {'customer_id': 3, 'name': 'Josh Doe', 'email': 'e3@example.com'},
        {'customer_id': 4, 'name': 'Jane Doe', 'email': 'e4@example.com'},
    ]


def test_list_not_existing_schema(test_client: TestClient) -> None:
    response = test_client.get('/api/v1/schemas/test/')
    assert response.status_code == 404
    assert response.json() == {'detail': 'Not Found'}


def test_list_ordering(test_client: TestClient) -> None:
    response = test_client.get('/api/v1/schemas/customers/?order=customer_id')
    assert response.status_code == 200
    response_json = response.json()
    assert response_json == [
        {'customer_id': 1, 'name': 'John Doe', 'email': 'e1@example.com'},
        {'customer_id': 2, 'name': 'Jane Doe', 'email': 'e2@example.com'},
        {'customer_id': 3, 'name': 'Josh Doe', 'email': 'e3@example.com'},
        {'customer_id': 4, 'name': 'Jane Doe', 'email': 'e4@example.com'},
    ]

    response = test_client.get('/api/v1/schemas/customers/?order=customer_id.desc')
    assert response.status_code == 200
    response_json = response.json()
    assert response_json == [
        {'customer_id': 4, 'name': 'Jane Doe', 'email': 'e4@example.com'},
        {'customer_id': 3, 'name': 'Josh Doe', 'email': 'e3@example.com'},
        {'customer_id': 2, 'name': 'Jane Doe', 'email': 'e2@example.com'},
        {'customer_id': 1, 'name': 'John Doe', 'email': 'e1@example.com'},
    ]

    response = test_client.get('/api/v1/schemas/customers/?order=name,customer_id.desc')
    assert response.status_code == 200
    response_json = response.json()
    assert response_json == [
        {'customer_id': 4, 'name': 'Jane Doe', 'email': 'e4@example.com'},
        {'customer_id': 2, 'name': 'Jane Doe', 'email': 'e2@example.com'},
        {'customer_id': 1, 'name': 'John Doe', 'email': 'e1@example.com'},
        {'customer_id': 3, 'name': 'Josh Doe', 'email': 'e3@example.com'},
    ]

    response = test_client.get('/api/v1/schemas/customers/?order=name,customer_id.asc')
    assert response.status_code == 200
    response_json = response.json()
    assert response_json == [
        {'customer_id': 2, 'name': 'Jane Doe', 'email': 'e2@example.com'},
        {'customer_id': 4, 'name': 'Jane Doe', 'email': 'e4@example.com'},
        {'customer_id': 1, 'name': 'John Doe', 'email': 'e1@example.com'},
        {'customer_id': 3, 'name': 'Josh Doe', 'email': 'e3@example.com'},
    ]


def test_list_pagination(test_client: TestClient) -> None:
    response = test_client.get('/api/v1/schemas/customers/?limit=2')
    assert response.status_code == 200
    response_json = response.json()
    assert response_json == [
        {'customer_id': 1, 'name': 'John Doe', 'email': 'e1@example.com'},
        {'customer_id': 2, 'name': 'Jane Doe', 'email': 'e2@example.com'},
    ]

    response = test_client.get('/api/v1/schemas/customers/?limit=3')
    assert response.status_code == 200
    response_json = response.json()
    assert response_json == [
        {'customer_id': 1, 'name': 'John Doe', 'email': 'e1@example.com'},
        {'customer_id': 2, 'name': 'Jane Doe', 'email': 'e2@example.com'},
        {'customer_id': 3, 'name': 'Josh Doe', 'email': 'e3@example.com'},
    ]

    response = test_client.get('/api/v1/schemas/customers/?limit=2&offset=1')
    assert response.status_code == 200
    response_json = response.json()
    assert response_json == [
        {'customer_id': 2, 'name': 'Jane Doe', 'email': 'e2@example.com'},
        {'customer_id': 3, 'name': 'Josh Doe', 'email': 'e3@example.com'},
    ]


def test_filtering_eq(test_client: TestClient) -> None:
    response = test_client.get('/api/v1/schemas/customers/?customer_id=1')
    assert response.status_code == 200
    response_json = response.json()
    assert response_json == [
        {'customer_id': 1, 'name': 'John Doe', 'email': 'e1@example.com'},
    ]

    response = test_client.get('/api/v1/schemas/customers/?customer_id=eq.2')
    assert response.status_code == 200
    response_json = response.json()
    assert response_json == [
        {'customer_id': 2, 'name': 'Jane Doe', 'email': 'e2@example.com'},
    ]


def test_filtering_gt(test_client: TestClient) -> None:
    response = test_client.get('/api/v1/schemas/customers/?customer_id=gt.1')
    assert response.status_code == 200
    response_json = response.json()
    assert response_json == [
        {'customer_id': 2, 'name': 'Jane Doe', 'email': 'e2@example.com'},
        {'customer_id': 3, 'name': 'Josh Doe', 'email': 'e3@example.com'},
        {'customer_id': 4, 'name': 'Jane Doe', 'email': 'e4@example.com'},
    ]

    response = test_client.get('/api/v1/schemas/customers/?customer_id=gte.3')
    assert response.status_code == 200
    response_json = response.json()
    assert response_json == [
        {'customer_id': 3, 'name': 'Josh Doe', 'email': 'e3@example.com'},
        {'customer_id': 4, 'name': 'Jane Doe', 'email': 'e4@example.com'},
    ]


def test_filtering_lt(test_client: TestClient) -> None:
    response = test_client.get('/api/v1/schemas/customers/?customer_id=lt.4')
    assert response.status_code == 200
    response_json = response.json()
    assert response_json == [
        {'customer_id': 1, 'name': 'John Doe', 'email': 'e1@example.com'},
        {'customer_id': 2, 'name': 'Jane Doe', 'email': 'e2@example.com'},
        {'customer_id': 3, 'name': 'Josh Doe', 'email': 'e3@example.com'},
    ]

    response = test_client.get('/api/v1/schemas/customers/?customer_id=lte.2')
    assert response.status_code == 200
    response_json = response.json()
    assert response_json == [
        {'customer_id': 1, 'name': 'John Doe', 'email': 'e1@example.com'},
        {'customer_id': 2, 'name': 'Jane Doe', 'email': 'e2@example.com'},
    ]


def test_filtering_contains(test_client: TestClient) -> None:
    response = test_client.get('/api/v1/schemas/logs/?message=contains.Lo')
    assert response.status_code == 200
    response_json = response.json()
    assert response_json == [
        {'created_at': '2021-01-01T00:00:00', 'message': 'Lorem ipsum dolor sit amet'},
    ]

    response = test_client.get('/api/v1/schemas/logs/?message=icontains.Lo')
    assert response.status_code == 200
    response_json = response.json()
    assert response_json == [
        {'created_at': '2021-01-01T00:00:00', 'message': 'Lorem ipsum dolor sit amet'},
        {'created_at': '2021-01-04T00:00:00', 'message': 'ut labore et dolore magna aliqua'},
    ]


def test_filtering_startswith(test_client: TestClient) -> None:
    response = test_client.get('/api/v1/schemas/logs/?message=startswith.Lorem')
    assert response.status_code == 200
    response_json = response.json()
    assert response_json == [
        {'created_at': '2021-01-01T00:00:00', 'message': 'Lorem ipsum dolor sit amet'},
    ]

    response = test_client.get('/api/v1/schemas/logs/?message=istartswith.lorem')
    assert response.status_code == 200
    response_json = response.json()
    assert response_json == [
        {'created_at': '2021-01-01T00:00:00', 'message': 'Lorem ipsum dolor sit amet'},
    ]


def test_filtering_endswith(test_client: TestClient) -> None:
    response = test_client.get('/api/v1/schemas/logs/?message=endswith.amet')
    assert response.status_code == 200
    response_json = response.json()
    assert response_json == [
        {'created_at': '2021-01-01T00:00:00', 'message': 'Lorem ipsum dolor sit amet'},
    ]

    response = test_client.get('/api/v1/schemas/logs/?message=iendswith.AMET')
    assert response.status_code == 200
    response_json = response.json()
    assert response_json == [
        {'created_at': '2021-01-01T00:00:00', 'message': 'Lorem ipsum dolor sit amet'},
    ]


def test_filtering_not_eq(test_client: TestClient) -> None:
    response = test_client.get('/api/v1/schemas/customers/?customer_id=neq.1')
    assert response.status_code == 200
    response_json = response.json()
    assert response_json == [
        {'customer_id': 2, 'name': 'Jane Doe', 'email': 'e2@example.com'},
        {'customer_id': 3, 'name': 'Josh Doe', 'email': 'e3@example.com'},
        {'customer_id': 4, 'name': 'Jane Doe', 'email': 'e4@example.com'},
    ]

    response = test_client.get('/api/v1/schemas/customers/?customer_id=not.eq.1')
    assert response.status_code == 200
    response_json = response.json()
    assert response_json == [
        {'customer_id': 2, 'name': 'Jane Doe', 'email': 'e2@example.com'},
        {'customer_id': 3, 'name': 'Josh Doe', 'email': 'e3@example.com'},
        {'customer_id': 4, 'name': 'Jane Doe', 'email': 'e4@example.com'},
    ]
