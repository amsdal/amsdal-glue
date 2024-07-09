from amsdal_glue.connections.connection_pool import DefaultConnectionPool
from amsdal_glue_core.common.data_models.data import Data
from amsdal_glue_core.common.data_models.query import QueryStatement
from amsdal_glue_core.common.data_models.schema import Schema
from amsdal_glue_core.common.operations.queries import DataQueryOperation
from amsdal_glue_core.common.operations.queries import SchemaQueryOperation
from amsdal_glue_core.common.services.managers.connection import ConnectionManager
from amsdal_glue_core.common.services.queries import DataQueryService
from amsdal_glue_core.common.services.queries import SchemaQueryService
from amsdal_glue_core.containers import Container
from connection import DailyTreasureWebConnection


def register_connections() -> None:
    web_treasure_pool = DefaultConnectionPool(DailyTreasureWebConnection)

    connection_mng = Container.managers.get(ConnectionManager)
    connection_mng.register_connection_pool(web_treasure_pool)


def fetch_schemas() -> list[Schema]:
    query_service = Container.services.get(SchemaQueryService)
    result = query_service.execute(
        SchemaQueryOperation(filters=None),
    )
    assert result.success is True, result.message
    assert result.schemas is not None

    return result.schemas


def query_data(query: QueryStatement) -> list[Data]:
    query_service = Container.services.get(DataQueryService)
    result = query_service.execute(
        DataQueryOperation(query=query),
    )
    assert result.success is True, result.message
    assert result.data is not None

    return result.data
