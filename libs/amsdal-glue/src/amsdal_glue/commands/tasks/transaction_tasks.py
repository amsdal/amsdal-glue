from dataclasses import dataclass
from typing import Any

from amsdal_glue_core.commands.transaction_node import ExecutionTransactionCommandNode
from amsdal_glue_core.common.operations.commands import TransactionCommand
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


@dataclass(kw_only=True)
class TransactionCommandFinalTask(Task):
    tasks: list[TransactionCommandTask]

    def __post_init__(self) -> None:
        self._result: ExecutionTransactionCommandNode | None = None

    def execute(self, transaction_id: str | None, lock_id: str | None) -> None:  # noqa: ARG002
        if not self.tasks:
            return

        _command = TransactionCommand(
            lock_id=self.tasks[0].item.command.lock_id,
            transaction_id=self.tasks[0].item.command.transaction_id,
            action=self.tasks[0].item.command.action,
            parent_transaction_id=self.tasks[0].item.command.parent_transaction_id,
        )
        _result = None

        for task in self.tasks:
            _result = _result and task.result if _result else task.result

        self._result = ExecutionTransactionCommandNode(
            command=_command,
            result=_result,
        )

    @property
    def item(self) -> Any:
        return [task.item for task in self.tasks]

    @property
    def result(self) -> list[Any] | None:
        return self._result.result if self._result else None
