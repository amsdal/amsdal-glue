from abc import ABC
from abc import abstractmethod
from typing import Any


class Connectable(ABC):
    @abstractmethod
    def connect(self, *args: Any, **kwargs: Any) -> None:
        """
        Connects to the database.
        param kwargs: the connection parameters
        type kwargs: Any

        return: None
        """
        ...

    @abstractmethod
    def disconnect(self) -> None:
        """
        Disconnects from the database.

        return: None
        """
        ...

    @property
    @abstractmethod
    def is_connected(self) -> bool:
        """
        Checks if the connection is established.

        return: True if connected, False otherwise
        rtype: bool
        """
        ...

    @property
    @abstractmethod
    def is_alive(self) -> bool:
        """
        Checks if the connection is alive.

        return: True if alive, False otherwise
        rtype: bool
        """
        ...


class AsyncConnectable(ABC):
    @abstractmethod
    async def connect(self, *args: Any, **kwargs: Any) -> None:
        """
        Connects to the database.
        param kwargs: the connection parameters
        type kwargs: Any

        return: None
        """
        ...

    @abstractmethod
    async def disconnect(self) -> None:
        """
        Disconnects from the database.

        return: None
        """
        ...

    @property
    @abstractmethod
    async def is_connected(self) -> bool:
        """
        Checks if the connection is established.

        return: True if connected, False otherwise
        rtype: bool
        """
        ...

    @property
    @abstractmethod
    async def is_alive(self) -> bool:
        """
        Checks if the connection is alive.

        return: True if alive, False otherwise
        rtype: bool
        """
        ...
