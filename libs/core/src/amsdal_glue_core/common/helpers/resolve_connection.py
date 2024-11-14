# mypy: disable-error-code="type-abstract"
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.data_models.sub_query import SubQueryStatement
from amsdal_glue_core.common.interfaces.connection import AsyncConnectionBase
from amsdal_glue_core.common.interfaces.connection import ConnectionBase
from amsdal_glue_core.common.interfaces.connection_manager import AsyncConnectionManager
from amsdal_glue_core.common.interfaces.connection_manager import ConnectionManager
from amsdal_glue_core.common.interfaces.connection_pool import AsyncConnectionPoolBase
from amsdal_glue_core.common.interfaces.connection_pool import ConnectionPoolBase
from amsdal_glue_core.containers import Container


def resolve_connection_pool(
    table: SchemaReference | SubQueryStatement,
    *,
    is_async: bool = False,
) -> ConnectionPoolBase | AsyncConnectionPoolBase:
    if isinstance(table, SchemaReference):
        _table_name = table.name
    elif isinstance(table, SubQueryStatement):
        return resolve_connection_pool(table.query.table, is_async=is_async)
    else:
        msg = 'Table must be either a SchemaReference or a SubQueryStatement.'
        raise RuntimeError(msg)  # noqa: TRY004

    if is_async:
        return Container.managers.get(AsyncConnectionManager).get_connection_pool(_table_name)

    return Container.managers.get(ConnectionManager).get_connection_pool(_table_name)


def resolve_connection(
    table: SchemaReference | SubQueryStatement,
    transaction_id: str | None,
) -> ConnectionBase:
    connection_pool = resolve_connection_pool(table=table)

    if not isinstance(connection_pool, ConnectionPoolBase):
        msg = 'Connection pool must be an instance of ConnectionPoolBase'
        raise TypeError(msg)
    return connection_pool.get_connection(transaction_id=transaction_id)


async def resolve_async_connection(
    table: SchemaReference | SubQueryStatement,
    transaction_id: str | None,
) -> AsyncConnectionBase:
    connection_pool = resolve_connection_pool(table=table, is_async=True)

    if not isinstance(connection_pool, AsyncConnectionPoolBase):
        msg = 'Connection pool must be an instance of AsyncConnectionPoolBase'
        raise TypeError(msg)

    return await connection_pool.get_connection(transaction_id=transaction_id)
