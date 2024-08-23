from amsdal_glue.interfaces import SequentialExecutor
from amsdal_glue_core.common.executors.manager import ExecutorManager
from amsdal_glue_core.containers import ServiceType


class DefaultExecutorManager(ExecutorManager):
    def __init__(self) -> None:
        self._executors: dict[ServiceType, type[SequentialExecutor]] = {}

    def resolve_by_service(self, service: ServiceType) -> SequentialExecutor | None:
        executor_cls = self._executors.get(service)

        if executor_cls:
            return executor_cls()

    def register_for_service(self, service: ServiceType, executor: type[SequentialExecutor]) -> None:
        self._executors[service] = executor
