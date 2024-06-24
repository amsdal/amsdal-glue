from dataclasses import dataclass
from typing import Any

from amsdal_glue_core.common.operations.commands import TransactionCommand


@dataclass(kw_only=True)
class ExecutionTransactionCommandNode:
    command: TransactionCommand
    result: Any = None
