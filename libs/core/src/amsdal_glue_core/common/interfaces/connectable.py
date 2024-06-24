from abc import ABC
from abc import abstractmethod
from typing import Any


class Connectable(ABC):
    @abstractmethod
    def connect(self, *args: Any, **kwargs: Any) -> None:
        """
        Connects to the database.
        :param kwargs: the connection parameters
        :type kwargs: Any

        :return: None
        """
        ...

    @abstractmethod
    def disconnect(self) -> None:
        """
        Disconnects from the database.

        :return: None
        """
        ...

    @property
    @abstractmethod
    def is_connected(self) -> bool:
        """
        Checks if the connection is established.

        :return: True if connected, False otherwise
        :rtype: bool
        """
        ...
