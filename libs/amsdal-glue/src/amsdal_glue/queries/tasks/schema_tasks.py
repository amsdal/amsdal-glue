from typing import Any

from amsdal_glue_core.common.data_models.conditions import Conditions
from amsdal_glue_core.common.data_models.schema import Schema
from amsdal_glue_core.common.interfaces.connection import ConnectionBase
from amsdal_glue_core.common.workflows.task import Task


class SchemaQueryTask(Task):
    def __init__(
        self,
        connection: ConnectionBase,
        filters: Conditions | None,
    ):
        self._connection = connection
        self._filters = filters
        self._result: list[Schema] = []

    @property
    def item(self) -> Any:
        return self._connection, self._filters

    @property
    def result(self) -> list[Schema]:
        return self._result

    def execute(self):
        self._result = self._connection.query_schema(self._filters)  # type: ignore[arg-type]


class FinalSchemaQueryTask(Task):
    def __init__(
        self,
        tasks: list[SchemaQueryTask],
    ):
        self._tasks = tasks
        self._results: list[Any] = []

    @property
    def item(self) -> Any:
        return [task.item for task in self._tasks]

    @property
    def result(self) -> Any:
        return self._results

    def execute(self):
        self._results = []

        for task in self._tasks:
            self._results.extend(task.result)
