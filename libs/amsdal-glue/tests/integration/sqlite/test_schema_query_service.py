# mypy: disable-error-code="type-abstract"
from collections.abc import Generator
from pathlib import Path

import pytest
from amsdal_glue_connections.sql.connections.sqlite_connection import SqliteConnection
from amsdal_glue_core.common.interfaces.connection_manager import ConnectionManager
from amsdal_glue_core.common.operations.queries import SchemaQueryOperation
from amsdal_glue_core.common.services.queries import SchemaQueryService
from amsdal_glue_core.containers import Container

from amsdal_glue.connections.connection_pool import DefaultConnectionPool
from amsdal_glue.initialize import init_default_containers

FIXTURES_PATH = Path(__file__).parent / 'fixtures'


@pytest.fixture(autouse=True)
def _register_default_connection() -> Generator[None, None, None]:
    init_default_containers()
    connection_mng = Container.managers.get(ConnectionManager)

    connection_mng.register_connection_pool(
        DefaultConnectionPool(SqliteConnection, db_path=FIXTURES_PATH / 'customers.sqlite', check_same_thread=False)
    )

    try:
        yield
    finally:
        connection_mng.disconnect_all()


def _add_shipping_connection():
    connection_mng = Container.managers.get(ConnectionManager)

    connection_mng.register_connection_pool(
        DefaultConnectionPool(SqliteConnection, db_path=FIXTURES_PATH / 'shippings.sqlite', check_same_thread=False),
        schema_name='shippings',
    )


def test_schema_query_service_single_connection() -> None:
    query_service = Container.services.get(SchemaQueryService)
    result = query_service.execute(
        SchemaQueryOperation(filters=None),
    )
    assert result.success is True
    assert result.schemas
    assert len(result.schemas) == 4


def test_schema_query_service_multiple_connection() -> None:
    _add_shipping_connection()
    query_service = Container.services.get(SchemaQueryService)
    result = query_service.execute(
        SchemaQueryOperation(filters=None),
    )
    assert result.success is True
    assert result.schemas
    assert len(result.schemas) == 5
    table_names = {item.name if item else None for item in result.schemas}
    assert table_names == {
        'customers',
        'orders',
        'items',
        'vendor',
        'shippings',
    }
