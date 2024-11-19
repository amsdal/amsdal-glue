from typing import TYPE_CHECKING

from amsdal_glue_core.common.helpers.resolve_connection import resolve_async_connection
from amsdal_glue_core.common.helpers.resolve_connection import resolve_connection

if TYPE_CHECKING:
    from amsdal_glue_core.commands.mutation_nodes import DataMutationNode


class DataCommandNodeExecutor:
    """Executes a node in the data command tree.

    This class implements the business logic for executing a single node of a data command tree.

    Methods:
        execute(mutation: DataMutationNode, transaction_id: str | None, lock_id: str | None) -> None:
            Executes the given data mutation node.
    """

    def execute(self, mutation: 'DataMutationNode', transaction_id: str | None, lock_id: str | None) -> None:  # noqa: ARG002
        """Executes the given data mutation node.

        Args:
            mutation (DataMutationNode): The data mutation node to be executed.
            transaction_id (str | None): The transaction ID to be used during execution.
            lock_id (str | None): The lock ID to be used during execution.
        """
        _query = mutation.mutations[0]
        _connection = resolve_connection(_query.schema, transaction_id=transaction_id)

        mutation.result = _connection.run_mutations(mutation.mutations)


class AsyncDataCommandNodeExecutor:
    """Executes a node in the data command tree.

    This class implements the business logic for executing a single node of a data command tree.

    Methods:
        execute(mutation: DataMutationNode, transaction_id: str | None, lock_id: str | None) -> None:
            Executes the given data mutation node.
    """

    async def execute(self, mutation: 'DataMutationNode', transaction_id: str | None, lock_id: str | None) -> None:  # noqa: ARG002
        """Executes the given data mutation node.

        Args:
            mutation (DataMutationNode): The data mutation node to be executed.
            transaction_id (str | None): The transaction ID to be used during execution.
            lock_id (str | None): The lock ID to be used during execution.
        """
        _query = mutation.mutations[0]
        _connection = await resolve_async_connection(_query.schema, transaction_id=transaction_id)

        mutation.result = await _connection.run_mutations(mutation.mutations)
