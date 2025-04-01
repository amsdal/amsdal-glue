from collections.abc import Iterator

import pytest

from amsdal_glue_core.common.data_models.conditions import Conditions
from amsdal_glue_core.common.data_models.query import QueryStatement
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.interfaces.connection_manager import AsyncConnectionManager
from amsdal_glue_core.common.interfaces.connection_manager import ConnectionManager
from amsdal_glue_core.containers import Container
from amsdal_glue_core.queries.data_query_nodes import DataQueryNode
from amsdal_glue_core.queries.executors.data_query_executor import AsyncDataQueryNodeExecutor
from amsdal_glue_core.queries.executors.data_query_executor import DataQueryNodeExecutor
from amsdal_glue_core.queries.executors.schema_query_executor import AsyncSchemaQueryNodeExecutor
from amsdal_glue_core.queries.executors.schema_query_executor import SchemaQueryNodeExecutor
from amsdal_glue_core.queries.schema_query_nodes import SchemaQueryNode
from tests.conftest import DEFAULT_SCHEMA_NAME
from tests.conftest import MockAsyncConnectionManager
from tests.conftest import MockConnectionManager


@pytest.fixture(autouse=True)
def _register_mocks(
    mock_connection_manager: MockConnectionManager,
    mock_async_connection_manager: MockAsyncConnectionManager,
) -> Iterator[None]:
    try:
        Container.managers.register(ConnectionManager, mock_connection_manager)  # type: ignore[type-abstract]
        Container.managers.register(AsyncConnectionManager, mock_async_connection_manager)  # type: ignore[type-abstract]
        yield
    finally:
        Container.__sub_containers__.clear()


def test_data_query(mock_connection_manager: MockConnectionManager) -> None:
    data_query_node = DataQueryNode(
        query=QueryStatement(
            table=SchemaReference(name=DEFAULT_SCHEMA_NAME),
        )
    )
    DataQueryNodeExecutor().execute(data_query_node, None, None)

    mock_connection_manager.connection_pool.connection.query.assert_called_once_with(data_query_node.query)


async def test_async_data_query(mock_async_connection_manager: MockAsyncConnectionManager) -> None:
    data_query_node = DataQueryNode(
        query=QueryStatement(
            table=SchemaReference(name=DEFAULT_SCHEMA_NAME),
        )
    )
    await AsyncDataQueryNodeExecutor().execute(data_query_node, None, None)

    mock_async_connection_manager.connection_pool.connection.query.assert_called_once_with(data_query_node.query)


def test_schema_query(mock_connection_manager: MockConnectionManager) -> None:
    schema_query_node = SchemaQueryNode(
        schema_name_connection=DEFAULT_SCHEMA_NAME,
        filters=Conditions(),
    )
    SchemaQueryNodeExecutor().execute(schema_query_node, None, None)

    mock_connection_manager.connection_pool.connection.query_schema.assert_called_once_with(schema_query_node.filters)


async def test_async_schema_query(mock_async_connection_manager: MockAsyncConnectionManager) -> None:
    schema_query_node = SchemaQueryNode(
        schema_name_connection=DEFAULT_SCHEMA_NAME,
        filters=Conditions(),
    )
    await AsyncSchemaQueryNodeExecutor().execute(schema_query_node, None, None)

    mock_async_connection_manager.connection_pool.connection.query_schema.assert_called_once_with(
        schema_query_node.filters
    )
