# mypy: disable-error-code="type-abstract"
from collections.abc import Generator
from pathlib import Path

import pytest
from amsdal_glue.initialize import init_default_containers
from amsdal_glue_connections.sql.connections.sqlite_connection import SqliteConnection
from amsdal_glue_core.common.helpers.singleton import Singleton
from amsdal_glue_core.common.services.managers.connection import ConnectionManager
from amsdal_glue_core.containers import Container
from amsdal_glue_core.queries.planner.schema_query_planner import SchemaQueryPlanner

FIXTURES_PATH = Path(__file__).parent / 'fixtures'


@pytest.fixture(autouse=True)
def _register_default_connection() -> Generator[None, None, None]:
    init_default_containers()
    connection_mng = Container.managers.get(ConnectionManager)

    connection = SqliteConnection()
    connection_mng.register_connection(connection)

    connection.connect(db_path=FIXTURES_PATH / 'customers.sqlite', check_same_thread=False)

    try:
        yield
    finally:
        connection_mng.disconnect_all()
        Singleton.invalidate_all_instances()


def _add_shipping_connection():
    connection_mng = Container.managers.get(ConnectionManager)

    shipping_connection = SqliteConnection()
    connection_mng.register_connection(shipping_connection, schema_name='shippings')

    shipping_connection.connect(db_path=FIXTURES_PATH / 'shippings.sqlite', check_same_thread=False)


def test_query_schemas_for_one_connection() -> None:
    query_planner = Container.planners.get(SchemaQueryPlanner)
    plan = query_planner.plan_schema_query()
    plan.execute()

    result = plan.result
    assert len(result) == 4
    table_names = {item.name for item in result}
    assert table_names == {
        'customers',
        'orders',
        'items',
        'vendor',
    }


def test_query_schemas_for_multiple_connections() -> None:
    _add_shipping_connection()
    query_planner = Container.planners.get(SchemaQueryPlanner)
    plan = query_planner.plan_schema_query()
    plan.execute()

    result = plan.result
    assert len(result) == 5
    table_names = {item.name for item in result}
    assert table_names == {
        'customers',
        'orders',
        'items',
        'vendor',
        'shippings',
    }
