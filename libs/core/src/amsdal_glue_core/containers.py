# mypy: disable-error-code="type-abstract"
from typing import TypeVar

ServiceType = TypeVar('ServiceType')


class Singleton:
    """
    The `Singleton` class is a decorator that ensures that only one instance of a class is created.

    Example:
        Here is an example of how to use the `Singleton` decorator:

        ```python
        import amsdal_glue
        from amsdal_glue import Container, Singleton

        Container.managers.register(Singleton(ConnectionManager), ConnectionManager)
        ```
    """
    def __init__(self, cls: ServiceType) -> None:
        print('INIT SINGLETON')
        self._cls = cls
        self._instance = None

    def __call__(self) -> ServiceType:
        print('CALL SINGLETON', self._instance)
        if self._instance is None:
            self._instance = self._cls()
        return self._instance


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
        self._resolved: dict[ServiceType, type[ServiceType]] = {}  # type: ignore[valid-type]

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
            instance = cls()
            self._resolved[instance] = dependency
            return instance  # type: ignore[misc]

        msg = f'No provider for {dependency}'
        raise ValueError(msg)

    def get_dependency_type(self, instance: ServiceType) -> type[ServiceType]:
        """
        Retrieves the type of the dependency for the given instance.

        Args:
            instance (ServiceType): An instance of the provider.

        Returns:
            type[ServiceType]: The type of the dependency for the given instance.

        Raises:
            ValueError: If no dependency type is registered for the given instance.
        """
        if instance in self._resolved:
            return self._resolved[instance]

        msg = f'No dependency type for {instance}'
        raise ValueError(msg)


class Container:
    """
    The `Container` class is a central registry for managing dependencies in the application. It provides
    separate containers for different types of dependencies, such as managers, services, executors, and planners.

    Instead of directly instantiating dependencies, use the `Container` class to retrieve instances of the required
    dependencies. This promotes a more modular design, allows for easier management of dependencies and
    simplifies testing.

    Example:
        These examples demonstrate how to work with the Container class.
        Note that the examples assume usage via the `amsdal_glue` package. If you are using the Container
        class directly via the `amsdal_glue_core` package, you should adjust the imports accordingly.

        1. Get an instance of the [ConnectionManager][amsdal_glue.ConnectionManager] and register connection pool
        ```python
        import amsdal_glue
        from amsdal_glue import Container

        connection_manager = Container.managers.get(ConnectionManager)
        connection_manager.register_connection_pool(
            amsdal_glue.DefaultConnectionPool(
                amsdal_glue.PostgresConnection,
                dsn='postgres://db_user:db_password@localhost:5433/db_name',
            ),
        )
        ```

        2. Register the own [SequentialExecutor][amsdal_glue.interfaces.SequentialExecutor] implementation
        ```python
        import amsdal_glue
        from amsdal_glue import Container
        from amsdal_glue.executors import SequentialExecutor


        class MySequentialExecutor(SequentialExecutor):
            pass


        Container.managers.register(SequentialExecutor, MySequentialExecutor)
        ```

    Note, when you get an instance of the dependency, you should use the base class type, not the implementation type.

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
