from typing import TYPE_CHECKING

from amsdal_glue_core.common.helpers.resolve_connection import resolve_connection
from amsdal_glue_core.common.helpers.singleton import Singleton

if TYPE_CHECKING:
    from amsdal_glue_core.commands.mutation_nodes import DataMutationNode


class DataCommandNodeExecutor(metaclass=Singleton):
    def execute(self, mutation: 'DataMutationNode') -> None:
        _query = mutation.mutations[0]
        _connection = resolve_connection(_query.schema)

        mutation.result = _connection.run_mutations(mutation.mutations)
