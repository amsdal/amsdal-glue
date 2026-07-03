# mypy: disable-error-code="type-abstract"
import pytest
from amsdal_glue_connections.sql.schema_registry import TABLE_REGISTRY
from amsdal_glue_core.common.data_models.query import QueryStatement
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.enums import Version
from amsdal_glue_core.common.operations.queries import SchemaQueryOperation
from amsdal_glue_core.common.services.queries import SchemaQueryService
from amsdal_glue_core.containers import Container
from fastapi.testclient import TestClient

_SCHEMA_QUERY = SchemaQueryOperation(
    query=QueryStatement(table=SchemaReference(name=TABLE_REGISTRY, version=Version.LATEST)),
)


def test_register_schema(test_client: TestClient) -> None:
    response = test_client.post(
        '/api/v1/sql/command/',
        json={
            'sql': 'CREATE TABLE test_schema (customer_id INTEGER, name VARCHAR, email VARCHAR)',
        },
    )
    assert response.status_code == 200, response.text

    query_service = Container.services.get(SchemaQueryService)
    result = query_service.execute(
        _SCHEMA_QUERY,
    )
    assert {'test_schema', 'products', 'orders', 'cart', 'logs', 'profile', 'customers'} == {
        schema.name  # type: ignore[union-attr]
        for schema in result.schemas  # type: ignore[union-attr]
    }


def test_delete_schema(test_client: TestClient) -> None:
    response = test_client.post(
        '/api/v1/sql/command/',
        json={
            'sql': 'DROP TABLE products',
        },
    )
    assert response.status_code == 200, response.text

    query_service = Container.services.get(SchemaQueryService)
    result = query_service.execute(
        _SCHEMA_QUERY,
    )
    assert {'orders', 'cart', 'logs', 'profile', 'customers'} == {schema.name for schema in result.schemas}  # type: ignore[union-attr]


def test_rename_schema(test_client: TestClient) -> None:
    response = test_client.post(
        '/api/v1/sql/command/',
        json={
            'sql': 'ALTER TABLE orders RENAME TO orders_v2',
        },
    )
    assert response.status_code == 200, response.text

    query_service = Container.services.get(SchemaQueryService)
    result = query_service.execute(
        _SCHEMA_QUERY,
    )
    assert {'products', 'orders_v2', 'cart', 'logs', 'profile', 'customers'} == {
        schema.name  # type: ignore[union-attr]
        for schema in result.schemas  # type: ignore[union-attr]
    }


def test_add_property(test_client: TestClient) -> None:
    response = test_client.post(
        '/api/v1/sql/command/',
        json={
            'sql': 'ALTER TABLE customers ADD COLUMN phone VARCHAR',
        },
    )
    assert response.status_code == 200, response.text

    query_service = Container.services.get(SchemaQueryService)
    result = query_service.execute(
        _SCHEMA_QUERY,
    )
    assert {
        'customer_id',
        'name',
        'email',
        'phone',
    } == {prop.name for schema in result.schemas for prop in schema.properties if schema.name == 'customers'}  # type: ignore[union-attr]


def test_delete_property(test_client: TestClient) -> None:
    response = test_client.post(
        '/api/v1/sql/command/',
        json={
            'sql': 'ALTER TABLE customers DROP COLUMN email',
        },
    )
    assert response.status_code == 200, response.text

    query_service = Container.services.get(SchemaQueryService)
    result = query_service.execute(
        _SCHEMA_QUERY,
    )
    assert {
        'customer_id',
        'name',
    } == {prop.name for schema in result.schemas for prop in schema.properties if schema.name == 'customers'}  # type: ignore[union-attr]


def test_rename_property(test_client: TestClient) -> None:
    response = test_client.post(
        '/api/v1/sql/command/',
        json={
            'sql': 'ALTER TABLE customers RENAME COLUMN email TO email_address',
        },
    )
    assert response.status_code == 200, response.text

    query_service = Container.services.get(SchemaQueryService)
    result = query_service.execute(
        _SCHEMA_QUERY,
    )
    assert {
        'customer_id',
        'name',
        'email_address',
    } == {prop.name for schema in result.schemas for prop in schema.properties if schema.name == 'customers'}  # type: ignore[union-attr]


@pytest.mark.skip
def test_update_property(test_client: TestClient) -> None:
    response = test_client.post(
        '/api/v1/sql/command/',
        json={
            'sql': 'ALTER TABLE customers ALTER COLUMN email_address SET DATA TYPE VARCHAR(255)',
        },
    )
    assert response.status_code == 200, response.text

    query_service = Container.services.get(SchemaQueryService)
    result = query_service.execute(
        _SCHEMA_QUERY,
    )
    assert {
        'customer_id',
        'name',
        'email',
    } == {prop.name for schema in result.schemas for prop in schema.properties if schema.name == 'customers'}  # type: ignore[union-attr]


@pytest.mark.skip
def test_add_constraint(test_client: TestClient) -> None:
    response = test_client.post(
        '/api/v1/sql/command/',
        json={
            'sql': 'ALTER TABLE customers ADD CONSTRAINT email_unique UNIQUE (email_address)',
        },
    )
    assert response.status_code == 200, response.text

    query_service = Container.services.get(SchemaQueryService)
    result = query_service.execute(
        _SCHEMA_QUERY,
    )
    assert {
        'email_unique',
    } == {
        constraint.name
        for schema in result.schemas  # type: ignore[union-attr]
        for constraint in schema.constraints  # type: ignore[union-attr]
        if schema.name == 'customers'  # type: ignore[union-attr]
    }
