from amsdal_glue_core.commands.mutation_nodes import SchemaCommandNode
from amsdal_glue_core.common.helpers.singleton import Singleton
from amsdal_glue_core.common.interfaces.connection import ConnectionBase
from amsdal_glue_core.common.operations.mutations.schema import SchemaMutation
from amsdal_glue_core.common.services.managers.connection import ConnectionManager


class SchemaCommandNodeExecutor(metaclass=Singleton):
    def __init__(self) -> None:
        from amsdal_glue_core.containers import Container

        self.connection_manager = Container.managers.get(ConnectionManager)

    def execute(self, command_node: SchemaCommandNode, transaction_id: str | None, lock_id: str | None) -> None:  # noqa: ARG002
        _command = command_node.command
        _connection = self.resolve_connection(_command.mutations, transaction_id)

        _connection.run_schema_command(_command)

    def resolve_connection(self, mutations: list[SchemaMutation], transaction_id: str | None) -> ConnectionBase:
        if not mutations:
            msg = 'No mutations to resolve connection for'
            raise ValueError(msg)

        return self.connection_manager.get_connection_pool(mutations[0].get_schema_name()).get_connection(
            transaction_id
        )
