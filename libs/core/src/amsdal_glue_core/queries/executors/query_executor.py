from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.data_models.sub_query import SubQueryStatement
from amsdal_glue_core.common.helpers.singleton import Singleton
from amsdal_glue_core.common.interfaces.connection import ConnectionBase
from amsdal_glue_core.common.services.managers.connection import ConnectionManager
from amsdal_glue_core.queries.planner.query_nodes import DataQueryNode


class QueryNodeExecutor(metaclass=Singleton):
    def __init__(self) -> None:
        from amsdal_glue_core.containers import Container

        self.connection_manager = Container.managers.get(ConnectionManager)

    def execute(self, query: DataQueryNode) -> None:
        _query = query.query
        _connection = self.resolve_connection(_query.table)

        query.result = _connection.query(_query)

    def resolve_connection(self, table: SchemaReference | SubQueryStatement) -> ConnectionBase:
        if isinstance(table, SchemaReference):
            return self.connection_manager.get_connection(table.name)

        if isinstance(table, SubQueryStatement):
            return self.resolve_connection(table.query.table)

        msg = f'QueryNodeExecutor does not support queries with {type(table)} as table.'
        raise RuntimeError(msg)
