from dataclasses import dataclass
from typing import Any

from amsdal_glue_core.commands.executors.schema_command_executor import SchemaCommandNodeExecutor
from amsdal_glue_core.commands.mutation_nodes import SchemaCommandNode
from amsdal_glue_core.common.operations.commands import SchemaCommand
from amsdal_glue_core.common.workflows.task import Task


@dataclass(kw_only=True)
class SchemaCommandTask(Task):
    command_node: SchemaCommandNode

    def __post_init__(self) -> None:
        self._executor = SchemaCommandNodeExecutor()

    def execute(self, transaction_id: str | None, lock_id: str | None) -> None:
        self._executor.execute(self.command_node, transaction_id=transaction_id, lock_id=lock_id)

    @property
    def item(self) -> Any:
        return self.command_node.command

    @property
    def result(self) -> list[Any] | None:
        return self.command_node.result


@dataclass(kw_only=True)
class FinalSchemaCommandTask(Task):
    tasks: list[SchemaCommandTask]

    def __post_init__(self) -> None:
        self._result: SchemaCommandNode | None = None

    def execute(self, transaction_id: str | None, lock_id: str | None) -> None:  # noqa: ARG002
        if not self.tasks:
            return

        _command = SchemaCommand(
            lock_id=self.tasks[0].item.lock_id,
            transaction_id=self.tasks[0].item.transaction_id,
            mutations=[],
        )
        _result = []

        for task in self.tasks:
            _command.mutations.extend(task.item.mutations)
            _results = [task.result[i] if task.result else None for i in range(len(task.item.mutations))]
            _result.extend(_results)

        self._result = SchemaCommandNode(
            command=_command,
            result=_result,
        )

    @property
    def item(self) -> Any:
        return [task.item for task in self.tasks]

    @property
    def result(self) -> list[Any] | None:
        return self._result.result if self._result else None
