from abc import ABC
from abc import abstractmethod
from collections.abc import Callable


class RuntimeManager(ABC):
    @abstractmethod
    def add_shutdown_hook(self, func: Callable[[], None]): ...

    @abstractmethod
    def shutdown(self) -> None: ...
