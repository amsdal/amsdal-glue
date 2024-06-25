from dataclasses import dataclass
from typing import Any

from amsdal_glue_core.common.data_models.schema import Schema
from amsdal_glue_core.common.workflows.task import Task
from amsdal_glue_core.queries.executors.schema_query_executor import SchemaQueryNodeExecutor
from amsdal_glue_core.queries.schema_query_nodes import SchemaQueryNode


@dataclass(kw_only=True)
class SchemaQueryTask(Task):
    schema_query_node: SchemaQueryNode

    def execute(self, transaction_id: str | None, lock_id: str | None) -> None:
        _query_executor = SchemaQueryNodeExecutor()
        _query_executor.execute(self.schema_query_node, transaction_id=transaction_id, lock_id=lock_id)

    @property
    def item(self) -> Any:
        return self.schema_query_node

    @property
    def result(self) -> list[Schema] | None:
        return self.schema_query_node.result


class FinalSchemaQueryTask(Task):
    def __init__(
        self,
        tasks: list[SchemaQueryTask],
    ):
        self._tasks = tasks
        self._results: list[Schema] = []

    @property
    def item(self) -> Any:
        return [task.item for task in self._tasks]

    @property
    def result(self) -> list[Schema]:
        return self._results

    def execute(self, transaction_id: str | None, lock_id: str | None) -> None:  # noqa: ARG002
        self._results = []

        for task in self._tasks:
            self._results.extend(task.result or [])
