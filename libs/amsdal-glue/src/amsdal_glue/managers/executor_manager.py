from typing import Any

from amsdal_glue_core.common.executors.manager import ExecutorManager

from amsdal_glue.interfaces import SequentialExecutor


class DefaultExecutorManager(ExecutorManager):
    def __init__(self) -> None:
        self._executors: dict[Any, type[SequentialExecutor]] = {}

    def resolve_by_service(self, service: Any) -> SequentialExecutor | None:
        executor_cls = self._executors.get(service)

        if executor_cls:
            return executor_cls()

        return None

    def register_for_service(self, service: Any, executor: type[SequentialExecutor]) -> None:
        self._executors[service] = executor
