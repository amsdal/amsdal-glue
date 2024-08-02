# mypy: disable-error-code="type-abstract"
import pytest
from amsdal_glue_core.common.data_models.data import Data
from amsdal_glue_core.common.data_models.query import QueryStatement
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.enums import Version
from amsdal_glue_core.common.operations.commands import DataCommand
from amsdal_glue_core.common.operations.mutations.data import InsertData
from amsdal_glue_core.common.operations.queries import DataQueryOperation
from amsdal_glue_core.common.services.commands import DataCommandService
from amsdal_glue_core.common.services.queries import DataQueryService
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
                    ],
                ),
            ],
        ),
    )


def test_update_customer(test_client: TestClient) -> None:
    response = test_client.put(
        '/api/v1/schemas/customers/1/',
        json={'customer_id': 1, 'name': 'John Doe', 'email': 'e123@example.com'},
    )
    assert response.status_code == 200
    response_json = response.json()
    assert response_json == {'customer_id': 1, 'name': 'John Doe', 'email': 'e123@example.com'}

    query = QueryStatement(table=SchemaReference(name='customers', version=Version.LATEST))
    query_service = Container.services.get(DataQueryService)
    result = query_service.execute(DataQueryOperation(query=query))

    assert [data.data for data in result.data] == [  # type: ignore[union-attr]
        {'customer_id': 1, 'name': 'John Doe', 'email': 'e123@example.com'},
        {'customer_id': 2, 'name': 'Jane Doe', 'email': 'e2@example.com'},
        {'customer_id': 3, 'name': 'Josh Doe', 'email': 'e3@example.com'},
    ]


def test_update_customer_change_id(test_client: TestClient) -> None:
    response = test_client.put(
        '/api/v1/schemas/customers/1/',
        json={'customer_id': 5, 'name': 'John Doe', 'email': 'e123@example.com'},
    )
    assert response.status_code == 200
    response_json = response.json()
    assert response_json == {'customer_id': 5, 'name': 'John Doe', 'email': 'e123@example.com'}

    query = QueryStatement(table=SchemaReference(name='customers', version=Version.LATEST))
    query_service = Container.services.get(DataQueryService)
    result = query_service.execute(DataQueryOperation(query=query))

    assert [data.data for data in result.data] == [  # type: ignore[union-attr]
        {'customer_id': 2, 'name': 'Jane Doe', 'email': 'e2@example.com'},
        {'customer_id': 3, 'name': 'Josh Doe', 'email': 'e3@example.com'},
        {'customer_id': 5, 'name': 'John Doe', 'email': 'e123@example.com'},
    ]


def test_update_customer_change_id_to_existing(test_client: TestClient) -> None:
    response = test_client.put(
        '/api/v1/schemas/customers/1/',
        json={'customer_id': 2, 'name': 'John Doe', 'email': 'e123@example.com'},
    )
    assert response.status_code == 400
    response_json = response.json()
    assert response_json == {
        'detail': (
            "Error executing mutation: UPDATE 'customers' SET 'customer_id' = ?, 'email' = ?, 'name' = ? "
            "WHERE 'customers'.'customer_id' = ? with params: [2, 'e123@example.com', 'John Doe', '1']"
        )
    }

    query = QueryStatement(table=SchemaReference(name='customers', version=Version.LATEST))
    query_service = Container.services.get(DataQueryService)
    result = query_service.execute(DataQueryOperation(query=query))

    assert [data.data for data in result.data] == [  # type: ignore[union-attr]
        {'customer_id': 1, 'name': 'John Doe', 'email': 'e1@example.com'},
        {'customer_id': 2, 'name': 'Jane Doe', 'email': 'e2@example.com'},
        {'customer_id': 3, 'name': 'Josh Doe', 'email': 'e3@example.com'},
    ]
