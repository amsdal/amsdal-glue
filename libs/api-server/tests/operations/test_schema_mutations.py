# mypy: disable-error-code="type-abstract"
import pytest
from amsdal_glue_core.common.operations.queries import SchemaQueryOperation
from amsdal_glue_core.common.services.queries import SchemaQueryService
from amsdal_glue_core.containers import Container
from fastapi.testclient import TestClient


def test_register_schema(test_client: TestClient) -> None:
    response = test_client.post(
        '/api/v1/operations/register-schema/',
        json={
            'schema': {
                'name': 'test_schema',
                'version': 'LATEST',
                'properties': [
                    {'name': 'customer_id', 'type': 'int', 'required': True},
                    {'name': 'name', 'type': 'str', 'required': True},
                    {'name': 'email', 'type': 'str', 'required': True},
                ],
            },
        },
    )
    assert response.status_code == 200, response.text

    query_service = Container.services.get(SchemaQueryService)
    result = query_service.execute(
        SchemaQueryOperation(filters=None),
    )
    assert {'test_schema', 'products', 'orders', 'cart', 'logs', 'profile', 'customers'} == {
        schema.name  # type: ignore[union-attr]
        for schema in result.schemas  # type: ignore[union-attr]
    }


def test_delete_schema(test_client: TestClient) -> None:
    response = test_client.post(
        '/api/v1/operations/delete-schema/',
        json={'schema_reference': {'name': 'products', 'version': 'LATEST'}},
    )
    assert response.status_code == 200, response.text

    query_service = Container.services.get(SchemaQueryService)
    result = query_service.execute(
        SchemaQueryOperation(filters=None),
    )
    assert {'orders', 'cart', 'logs', 'profile', 'customers'} == {schema.name for schema in result.schemas}  # type: ignore[union-attr]


def test_rename_schema(test_client: TestClient) -> None:
    response = test_client.post(
        '/api/v1/operations/rename-schema/',
        json={'schema_reference': {'name': 'orders', 'version': 'LATEST'}, 'new_schema_name': 'orders_v2'},
    )
    assert response.status_code == 200, response.text

    query_service = Container.services.get(SchemaQueryService)
    result = query_service.execute(
        SchemaQueryOperation(filters=None),
    )
    assert {'products', 'orders_v2', 'cart', 'logs', 'profile', 'customers'} == {
        schema.name  # type: ignore[union-attr]
        for schema in result.schemas  # type: ignore[union-attr]
    }


def test_add_property(test_client: TestClient) -> None:
    response = test_client.post(
        '/api/v1/operations/add-property/',
        json={
            'schema_reference': {'name': 'customers', 'version': 'LATEST'},
            'property': {'name': 'phone', 'type': 'str', 'required': True},
        },
    )
    assert response.status_code == 200, response.text

    query_service = Container.services.get(SchemaQueryService)
    result = query_service.execute(
        SchemaQueryOperation(filters=None),
    )
    assert {
        'customer_id',
        'name',
        'email',
        'phone',
    } == {prop.name for schema in result.schemas for prop in schema.properties if schema.name == 'customers'}  # type: ignore[union-attr]


def test_delete_property(test_client: TestClient) -> None:
    response = test_client.post(
        '/api/v1/operations/delete-property/',
        json={'schema_reference': {'name': 'customers', 'version': 'LATEST'}, 'property_name': 'email'},
    )
    assert response.status_code == 200, response.text

    query_service = Container.services.get(SchemaQueryService)
    result = query_service.execute(
        SchemaQueryOperation(filters=None),
    )
    assert {
        'customer_id',
        'name',
    } == {prop.name for schema in result.schemas for prop in schema.properties if schema.name == 'customers'}  # type: ignore[union-attr]


def test_rename_property(test_client: TestClient) -> None:
    response = test_client.post(
        '/api/v1/operations/rename-property/',
        json={
            'schema_reference': {'name': 'customers', 'version': 'LATEST'},
            'old_name': 'email',
            'new_name': 'email_address',
        },
    )
    assert response.status_code == 200, response.text

    query_service = Container.services.get(SchemaQueryService)
    result = query_service.execute(
        SchemaQueryOperation(filters=None),
    )
    assert {
        'customer_id',
        'name',
        'email_address',
    } == {prop.name for schema in result.schemas for prop in schema.properties if schema.name == 'customers'}  # type: ignore[union-attr]


@pytest.mark.skip
def test_update_property(test_client: TestClient) -> None:
    response = test_client.post(
        '/api/v1/operations/update-property/',
        json={
            'schema_reference': {'name': 'customers', 'version': 'LATEST'},
            'property': {'name': 'email', 'type': 'int', 'required': True},
        },
    )
    assert response.status_code == 200, response.text

    query_service = Container.services.get(SchemaQueryService)
    result = query_service.execute(
        SchemaQueryOperation(filters=None),
    )
    assert {
        'customer_id',
        'name',
        'email',
    } == {prop.name for schema in result.schemas for prop in schema.properties if schema.name == 'customers'}  # type: ignore[union-attr]


@pytest.mark.skip
def test_add_constraint(test_client: TestClient) -> None:
    response = test_client.post(
        '/api/v1/operations/add-constraint/',
        json={
            'schema_reference': {'name': 'customers', 'version': 'LATEST'},
            'constraint': {'name': 'email_unique', 'type': 'unique', 'fields': ['email']},
        },
    )
    assert response.status_code == 200, response.text

    query_service = Container.services.get(SchemaQueryService)
    result = query_service.execute(
        SchemaQueryOperation(filters=None),
    )
    assert {
        'email_unique',
    } == {
        constraint.name
        for schema in result.schemas  # type: ignore[union-attr]
        for constraint in schema.constraints  # type: ignore[union-attr]
        if schema.name == 'customers'  # type: ignore[union-attr]
    }
