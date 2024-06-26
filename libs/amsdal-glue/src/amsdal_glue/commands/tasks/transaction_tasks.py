from dataclasses import dataclass
from typing import Any

from amsdal_glue_core.commands.transaction_node import ExecutionTransactionCommandNode
from amsdal_glue_core.common.workflows.task import Task


@dataclass(kw_only=True)
class TransactionCommandTask(Task):
    transaction_command: ExecutionTransactionCommandNode

    def execute(self, transaction_id: str | None, lock_id: str | None) -> None:
        from amsdal_glue_core.commands.executors.transaction_command_executor import TransactionNodeExecutor

        _command_executor = TransactionNodeExecutor()
        _command_executor.execute(self.transaction_command, transaction_id=transaction_id, lock_id=lock_id)

    @property
    def item(self) -> Any:
        return self.transaction_command

    @property
    def result(self) -> Any:
        return self.transaction_command.result

    def __repr__(self) -> str:
        return f'TransactionCommandTask<{self.transaction_command}>'

    def __hash__(self) -> int:
        return hash(id(self))
