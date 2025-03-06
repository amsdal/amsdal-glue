# mypy: disable-error-code="type-abstract"
import logging
import pickle
from collections.abc import Iterator
from contextlib import contextmanager
from contextvars import ContextVar
from typing import Any
from typing import ClassVar
from typing import Generic
from typing import TypeVar
from uuid import uuid4

logger = logging.getLogger(__name__)

T = TypeVar('T')


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

    def __init__(self, cls: type[Any]) -> None:
        self._cls = cls
        self._instance = None

    def __call__(self) -> type[Any]:
        if self._instance is None:
            _instance = self._cls()
            self._instance = _instance
        else:
            _instance = self._instance

        return _instance


class DependencyContainer:
    """
    The `DependencyContainer` class is responsible for managing the registration and retrieval of dependencies.
    It maintains a mapping of dependency types to their respective provider types.

    Attributes:
        _providers (dict[type[Any], type[Any]]): A dictionary mapping dependency types to
                                                                 provider types.

    Methods:
        register(dependency: type[Any], provider: type[Any]) -> None:
            Registers a provider for a given dependency type.

        get(dependency: type[Any]) -> Any:
            Retrieves an instance of the provider for the given dependency type.
    """

    def __init__(self) -> None:
        """
        Initializes a new instance of the `DependencyContainer` class.
        """
        self._providers: dict[type[Any], type[Any]] = {}  # type: ignore[valid-type]
        self._resolved: dict[type[Any], type[Any]] = {}  # type: ignore[valid-type]

    def register(self, dependency: type[T], provider: T | Singleton) -> None:
        """
        Registers a provider for a given dependency type.

        Args:
            dependency (type[Any]): The type of the dependency.
            provider (type[Any]): The type of the provider.
        """
        self._providers[dependency] = provider  # type: ignore[assignment]

    def get(self, dependency: type[T]) -> T:
        """
        Retrieves an instance of the provider for the given dependency type.

        Args:
            dependency (type[Any]): The type of the dependency.

        Returns:
            Any: An instance of the provider for the given dependency type.

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

    def get_dependency_type(self, instance: Any) -> type[Any]:
        """
        Retrieves the type of the dependency for the given instance.

        Args:
            instance (Any): An instance of the provider.

        Returns:
            type[Any]: The type of the dependency for the given instance.

        Raises:
            ValueError: If no dependency type is registered for the given instance.
        """
        if instance in self._resolved:
            return self._resolved[instance]

        msg = f'No dependency type for {instance}'
        raise ValueError(msg)


class SubContainer:
    def __init__(self, name: str = '') -> None:
        self.name = name
        self.managers = DependencyContainer()
        self.services = DependencyContainer()
        self.executors = DependencyContainer()
        self.planners = DependencyContainer()


class ContainerPropertyDescriptor:
    def __init__(self, name: str) -> None:
        self.name = name

    def __get__(self, _, cls: type['Container']) -> DependencyContainer:
        if cls.__current_container__ is None:
            return getattr(cls, f'_root_{self.name}')

        return getattr(cls.__sub_containers__[cls.__current_container__], self.name)


class ContextVarDescriptor(Generic[T]):
    def __init__(self, context_var: ContextVar[T]) -> None:
        self.context_var = context_var

    def __get__(self, instance, owner) -> T:
        return self.context_var.get()

    def __set__(self, instance, value) -> None:
        self.context_var.set(value)


class MetaContainer(type):
    def __getattr__(cls, name):
        if name == '__current_container__':
            descriptor = cls.__dict__['__current_container__']
            return descriptor.__get__(None, cls)
        return super().__getattribute__(name)

    def __setattr__(cls, name, value):
        if name == '__current_container__':
            descriptor = cls.__dict__.get('__current_container__')

            if isinstance(descriptor, ContextVarDescriptor):
                descriptor.__set__(None, value)
        else:
            super().__setattr__(name, value)


CURRENT_CONTAINER_CONTEXT: ContextVar[str | None] = ContextVar('__current_container__', default=None)


class Container(metaclass=MetaContainer):
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

    _root_managers = DependencyContainer()
    _root_services = DependencyContainer()
    _root_executors = DependencyContainer()
    _root_planners = DependencyContainer()

    __current_container__ = ContextVarDescriptor[str | None](CURRENT_CONTAINER_CONTEXT)
    __sub_containers__: ClassVar[dict[str, SubContainer]] = {}

    managers = ContainerPropertyDescriptor('managers')
    services = ContainerPropertyDescriptor('services')
    executors = ContainerPropertyDescriptor('executors')
    planners = ContainerPropertyDescriptor('planners')

    @classmethod
    def define_sub_container(cls, name: str = '') -> SubContainer:
        name = name or uuid4().hex
        cls.__sub_containers__[name] = SubContainer(name)
        return cls.__sub_containers__[name]

    @classmethod
    @contextmanager
    def switch(cls, name: str) -> Iterator[Any]:
        previous = Container.__current_container__
        Container.__current_container__ = name  # type: ignore[assignment]

        try:
            yield cls.__sub_containers__[name]
        finally:
            Container.__current_container__ = previous  # type: ignore[assignment]

    @classmethod
    @contextmanager
    def root(cls) -> Iterator[Any]:
        previous = Container.__current_container__
        Container.__current_container__ = None  # type: ignore[assignment]

        try:
            yield Container
        finally:
            Container.__current_container__ = previous  # type: ignore[assignment]

    @classmethod
    def serialize_state(cls) -> bytes:
        return pickle.dumps({
            '_root_managers': cls._root_managers._providers,  # noqa: SLF001
            '_root_services': cls._root_services._providers,  # noqa: SLF001
            '_root_executors': cls._root_executors._providers,  # noqa: SLF001
            '_root_planners': cls._root_planners._providers,  # noqa: SLF001
            '__current_container__': cls.__current_container__,
            '__sub_containers__': {
                name: (
                    sub_container.managers._providers,  # noqa: SLF001
                    sub_container.services._providers,  # noqa: SLF001
                    sub_container.executors._providers,  # noqa: SLF001
                    sub_container.planners._providers,  # noqa: SLF001
                )
                for name, sub_container in cls.__sub_containers__.items()
            },
        })

    @classmethod
    def deserialize_state(cls, state: bytes) -> None:
        data = pickle.loads(state)  # noqa: S301
        cls._root_managers._providers = data['_root_managers']  # noqa: SLF001
        cls._root_services._providers = data['_root_services']  # noqa: SLF001
        cls._root_executors._providers = data['_root_executors']  # noqa: SLF001
        cls._root_planners._providers = data['_root_planners']  # noqa: SLF001
        cls.__current_container__ = data['__current_container__']

        for name, (_managers, _service, _executors, _planners) in data['__sub_containers__'].items():
            sub_container = SubContainer(name)
            sub_container.managers._providers = _managers  # noqa: SLF001
            sub_container.services._providers = _service  # noqa: SLF001
            sub_container.executors._providers = _executors  # noqa: SLF001
            sub_container.planners._providers = _planners  # noqa: SLF001

            cls.__sub_containers__[name] = sub_container
