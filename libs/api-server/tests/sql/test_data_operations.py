# mypy: disable-error-code="type-abstract"
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


def test_create_customer(test_client: TestClient) -> None:
    response = test_client.post(
        '/api/v1/sql/command/',
        json={
            'sql': (
                'INSERT INTO customers (customer_id, name, email) VALUES '
                "(1, 'John Doe', 'e1@example.com'), "
                "(2, 'Jake Doe', 'e2@example.com'), "
                "(3, 'Jane Doe', 'e3@example.com')"
            )
        },
    )
    assert response.status_code == 200
    assert response.json() == [{'success': True, 'message': None, 'exception': None, 'data': [None]}]

    query = QueryStatement(table=SchemaReference(name='customers', version=Version.LATEST))
    query_service = Container.services.get(DataQueryService)
    result = query_service.execute(DataQueryOperation(query=query))

    assert [data.data for data in result.data] == [  # type: ignore[union-attr]
        {'customer_id': 1, 'name': 'John Doe', 'email': 'e1@example.com'},
        {'customer_id': 2, 'name': 'Jake Doe', 'email': 'e2@example.com'},
        {'customer_id': 3, 'name': 'Jane Doe', 'email': 'e3@example.com'},
    ]


def test_update_customer(test_client: TestClient) -> None:
    service = Container.services.get(DataCommandService)
    service.execute(
        command=DataCommand(
            mutations=[
                InsertData(
                    schema=SchemaReference(name='customers', version=Version.LATEST),
                    data=[
                        Data(data={'customer_id': 1, 'name': 'John Doe', 'email': 'e1@example.com'}),
                        Data(data={'customer_id': 2, 'name': 'Jake Doe', 'email': 'e2@example.com'}),
                        Data(data={'customer_id': 3, 'name': 'Jane Doe', 'email': 'e3@example.com'}),
                    ],
                ),
            ],
        ),
    )

    response = test_client.post(
        '/api/v1/sql/command/',
        json={'sql': ("UPDATE customers SET email = 'e123@example.com', name = 'Josh Black' WHERE customer_id == 1")},
    )
    assert response.status_code == 200
    assert response.json() == [{'success': True, 'message': None, 'exception': None, 'data': [None]}]

    query = QueryStatement(table=SchemaReference(name='customers', version=Version.LATEST))
    query_service = Container.services.get(DataQueryService)
    result = query_service.execute(DataQueryOperation(query=query))

    assert [data.data for data in result.data] == [  # type: ignore[union-attr]
        {'customer_id': 1, 'name': 'Josh Black', 'email': 'e123@example.com'},
        {'customer_id': 2, 'name': 'Jake Doe', 'email': 'e2@example.com'},
        {'customer_id': 3, 'name': 'Jane Doe', 'email': 'e3@example.com'},
    ]


def test_delete_customer(test_client: TestClient) -> None:
    service = Container.services.get(DataCommandService)
    service.execute(
        command=DataCommand(
            mutations=[
                InsertData(
                    schema=SchemaReference(name='customers', version=Version.LATEST),
                    data=[
                        Data(data={'customer_id': 1, 'name': 'John Doe', 'email': 'e1@example.com'}),
                        Data(data={'customer_id': 2, 'name': 'Jake Doe', 'email': 'e2@example.com'}),
                        Data(data={'customer_id': 3, 'name': 'Jane Doe', 'email': 'e3@example.com'}),
                    ],
                ),
            ],
        ),
    )

    response = test_client.post(
        '/api/v1/sql/command/',
        json={'sql': ('DELETE FROM customers WHERE customer_id == 1 OR customer_id == 3')},
    )
    assert response.status_code == 200
    assert response.json() == [{'success': True, 'message': None, 'exception': None, 'data': [None]}]

    query = QueryStatement(table=SchemaReference(name='customers', version=Version.LATEST))
    query_service = Container.services.get(DataQueryService)
    result = query_service.execute(DataQueryOperation(query=query))

    assert [data.data for data in result.data] == [  # type: ignore[union-attr]
        {'customer_id': 2, 'name': 'Jake Doe', 'email': 'e2@example.com'},
    ]
