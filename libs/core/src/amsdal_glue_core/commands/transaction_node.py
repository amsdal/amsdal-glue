from dataclasses import dataclass
from typing import Any

from amsdal_glue_core.common.operations.commands import TransactionCommand


@dataclass(kw_only=True)
class ExecutionTransactionCommandNode:
    """
    Represents a node in the transaction command tree.

    Attributes:
        command (TransactionCommand): The transaction command to be executed.
        result (Any | None): The result of the transaction command execution.
    """

    command: TransactionCommand
    result: Any = None
