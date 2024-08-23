from abc import ABC
from abc import abstractmethod

from amsdal_glue_core.common.executors.interfaces import SequentialExecutor
from amsdal_glue_core.containers import ServiceType


class ExecutorManager(ABC):
    @abstractmethod
    def resolve_by_service(self, service: ServiceType) -> SequentialExecutor:
        """Resolves the sequential executor.

        Returns:
            SequentialExecutor: The sequential executor.
        """
        ...

    @abstractmethod
    def register_for_service(self, service: ServiceType, executor: type[SequentialExecutor]) -> None:
        """Registers the sequential executor for the given service.

        Args:
            service (ServiceType): The service to be registered.
            executor (SequentialExecutor): The sequential executor to be registered.
        """
        ...
