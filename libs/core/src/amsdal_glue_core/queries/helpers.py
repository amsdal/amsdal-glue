from amsdal_glue_core.common.data_models.query import QueryStatement
from amsdal_glue_core.common.services.managers.connection import ConnectionManager


def has_multiple_connections(query: QueryStatement) -> bool:
    from amsdal_glue_core.containers import Container

    _connection_manager = Container.managers.get(ConnectionManager)
    _connections = set()
    _tables = query.get_related_tables()

    for table_name in _tables:
        connection_name = _connection_manager.get_connection_pool(table_name)
        _connections.add(connection_name)

    return len(_connections) > 1
