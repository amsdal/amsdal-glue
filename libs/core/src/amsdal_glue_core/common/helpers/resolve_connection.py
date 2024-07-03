from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.data_models.sub_query import SubQueryStatement
from amsdal_glue_core.common.interfaces.connection import ConnectionBase
from amsdal_glue_core.common.services.managers.connection import ConnectionManager
from amsdal_glue_core.containers import Container


def resolve_connection(
    table: SchemaReference | SubQueryStatement,
    transaction_id: str | None,
) -> ConnectionBase:
    if isinstance(table, SchemaReference):
        _table_name = table.name
    elif isinstance(table, SubQueryStatement):
        _table_name = resolve_connection(table.query.table, transaction_id=transaction_id)  # type: ignore[assignment]
    else:
        msg = 'Table must be either a SchemaReference or a SubQueryStatement.'
        raise RuntimeError(msg)  # noqa: TRY004

    connection_manager = Container.managers.get(ConnectionManager)

    return connection_manager.get_connection_pool(_table_name).get_connection(transaction_id)
