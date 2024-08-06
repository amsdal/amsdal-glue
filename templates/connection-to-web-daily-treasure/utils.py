from amsdal_glue import Data
from amsdal_glue import QueryStatement
from amsdal_glue import Schema


def register_connections() -> None:
    from amsdal_glue import Container, ConnectionManager, DefaultConnectionPool
    from connection import DailyTreasureWebConnection

    web_treasure_pool = DefaultConnectionPool(DailyTreasureWebConnection)

    connection_mng = Container.managers.get(ConnectionManager)
    connection_mng.register_connection_pool(web_treasure_pool)


def fetch_schemas() -> list[Schema]:
    from amsdal_glue import Container, SchemaQueryOperation
    from amsdal_glue.interfaces import SchemaQueryService

    query_service = Container.services.get(SchemaQueryService)
    result = query_service.execute(
        SchemaQueryOperation(filters=None),
    )
    assert result.success is True, result.message
    assert result.schemas is not None

    return result.schemas


def query_data(query: QueryStatement) -> list[Data]:
    from amsdal_glue import Container, DataQueryOperation
    from amsdal_glue.interfaces import DataQueryService

    query_service = Container.services.get(DataQueryService)
    result = query_service.execute(
        DataQueryOperation(query=query),
    )
    assert result.success is True, result.message
    assert result.data is not None

    return result.data
