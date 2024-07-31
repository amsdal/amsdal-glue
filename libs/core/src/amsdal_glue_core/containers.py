# mypy: disable-error-code="type-abstract"
from typing import TypeVar

ServiceType = TypeVar('ServiceType')


class DependencyContainer:
    """
    The `DependencyContainer` class is responsible for managing the registration and retrieval of dependencies.
    It maintains a mapping of dependency types to their respective provider types.

    Attributes:
        _providers (dict[type[ServiceType], type[ServiceType]]): A dictionary mapping dependency types to
                                                                 provider types.

    Methods:
        register(dependency: type[ServiceType], provider: type[ServiceType]) -> None:
            Registers a provider for a given dependency type.

        get(dependency: type[ServiceType]) -> ServiceType:
            Retrieves an instance of the provider for the given dependency type.
    """

    def __init__(self) -> None:
        """
        Initializes a new instance of the `DependencyContainer` class.
        """
        self._providers: dict[type[ServiceType], type[ServiceType]] = {}  # type: ignore[valid-type]

    def register(self, dependency: type[ServiceType], provider: type[ServiceType]) -> None:
        """
        Registers a provider for a given dependency type.

        Args:
            dependency (type[ServiceType]): The type of the dependency.
            provider (type[ServiceType]): The type of the provider.
        """
        self._providers[dependency] = provider

    def get(self, dependency: type[ServiceType]) -> ServiceType:
        """
        Retrieves an instance of the provider for the given dependency type.

        Args:
            dependency (type[ServiceType]): The type of the dependency.

        Returns:
            ServiceType: An instance of the provider for the given dependency type.

        Raises:
            ValueError: If no provider is registered for the given dependency type.
        """
        if dependency in self._providers:
            cls = self._providers[dependency]
            return cls()  # type: ignore[misc]

        msg = f'No provider for {dependency}'
        raise ValueError(msg)


class Container:
    """
    The `Container` class is a central registry for managing dependencies in the application. It provides
    separate containers for different types of dependencies, such as managers, services, executors, and planners.

    Attributes:
        managers (DependencyContainer): A container for manager dependencies.
        services (DependencyContainer): A container for service dependencies.
        executors (DependencyContainer): A container for executor dependencies.
        planners (DependencyContainer): A container for planner dependencies.
    """

    managers = DependencyContainer()
    services = DependencyContainer()
    executors = DependencyContainer()
    planners = DependencyContainer()
