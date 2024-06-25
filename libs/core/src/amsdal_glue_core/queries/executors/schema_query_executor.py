from typing import TYPE_CHECKING

from amsdal_glue_core.common.helpers.singleton import Singleton
from amsdal_glue_core.common.services.managers.connection import ConnectionManager

if TYPE_CHECKING:
    from amsdal_glue_core.queries.schema_query_nodes import SchemaQueryNode


class SchemaQueryNodeExecutor(metaclass=Singleton):
    def execute(self, query_node: 'SchemaQueryNode') -> None:
        from amsdal_glue_core.containers import Container

        connection_manager = Container.managers.get(ConnectionManager)
        connection = connection_manager.get_connection(query_node.schema_name_connection)
        query_node.result = connection.query_schema(query_node.filters)
