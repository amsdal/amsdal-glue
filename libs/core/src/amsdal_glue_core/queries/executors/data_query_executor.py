from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.data_models.sub_query import SubQueryStatement
from amsdal_glue_core.common.helpers.singleton import Singleton
from amsdal_glue_core.common.interfaces.connection import ConnectionBase
from amsdal_glue_core.common.services.managers.connection import ConnectionManager
from amsdal_glue_core.queries.data_query_nodes import DataQueryNode


class DataQueryNodeExecutor(metaclass=Singleton):
    def __init__(self) -> None:
        from amsdal_glue_core.containers import Container

        self.connection_manager = Container.managers.get(ConnectionManager)

    def execute(self, query: DataQueryNode, transaction_id: str | None, lock_id: str | None) -> None:  # noqa: ARG002
        _query = query.query
        _connection = self.resolve_connection(_query.table, transaction_id)

        query.result = _connection.query(_query)

    def resolve_connection(
        self,
        table: SchemaReference | SubQueryStatement,
        transaction_id: str | None,
    ) -> ConnectionBase:
        if isinstance(table, SchemaReference):
            return self.connection_manager.get_connection_pool(table.name).get_connection(transaction_id)

        if isinstance(table, SubQueryStatement):
            return self.resolve_connection(table.query.table, transaction_id)

        msg = f'QueryNodeExecutor does not support queries with {type(table)} as table.'
        raise RuntimeError(msg)
