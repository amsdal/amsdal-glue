# mypy: disable-error-code="type-abstract"
from amsdal_glue_core.common.data_models.query import QueryStatement
from amsdal_glue_core.common.interfaces.connection_manager import AsyncConnectionManager
from amsdal_glue_core.common.interfaces.connection_manager import ConnectionManager


def has_multiple_connections(query: QueryStatement, *, is_async: bool = False) -> bool:
    from amsdal_glue_core.containers import Container

    _connection_manager = Container.managers.get(AsyncConnectionManager if is_async else ConnectionManager)

    _connections = set()
    _tables = query.get_related_tables()

    for table_name in _tables:
        connection_name = _connection_manager.get_connection_pool(table_name)  # type: ignore[attr-defined]
        _connections.add(connection_name)

    return len(_connections) > 1
