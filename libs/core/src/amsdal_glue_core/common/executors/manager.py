from abc import ABC
from abc import abstractmethod
from typing import Any

from amsdal_glue_core.common.executors.interfaces import AsyncSequentialExecutor
from amsdal_glue_core.common.executors.interfaces import SequentialExecutor


class ExecutorManager(ABC):
    @abstractmethod
    def resolve_by_service(self, service: type[Any]) -> SequentialExecutor | None:
        """Resolves the sequential executor.

        Returns:
            SequentialExecutor | None: An instance of the sequential executor if found, otherwise None.
        """
        ...

    @abstractmethod
    def register_for_service(self, service: type[Any], executor: type[SequentialExecutor]) -> None:
        """Registers the sequential executor for the given service.

        Args:
            service (ServiceType): The service to be registered.
            executor (SequentialExecutor): The sequential executor to be registered.
        """
        ...


class AsyncExecutorManager(ABC):
    @abstractmethod
    def resolve_by_service(self, service: type[Any]) -> AsyncSequentialExecutor | None:
        """Resolves the sequential executor.

        Returns:
            AsyncSequentialExecutor | None: An instance of the sequential executor if found, otherwise None.
        """
        ...

    @abstractmethod
    def register_for_service(self, service: type[Any], executor: type[AsyncSequentialExecutor]) -> None:
        """Registers the sequential executor for the given service.

        Args:
            service (ServiceType): The service to be registered.
            executor (AsyncSequentialExecutor): The sequential executor to be registered.
        """
        ...
