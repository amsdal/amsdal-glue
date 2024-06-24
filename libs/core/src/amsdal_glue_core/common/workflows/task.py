from abc import ABC
from abc import abstractmethod
from typing import Any


class Task(ABC):
    @abstractmethod
    def execute(self) -> None:
        """
        Execute task.
        """
        ...

    @property
    @abstractmethod
    def item(self) -> Any:
        """
        Get item of task execution.
        """
        ...

    @property
    @abstractmethod
    def result(self) -> Any:
        """
        Get result of task execution.
        """
        ...
