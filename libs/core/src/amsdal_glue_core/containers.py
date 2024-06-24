# mypy: disable-error-code="type-abstract"
from typing import TypeVar

ServiceType = TypeVar('ServiceType')


class DependencyContainer:
    def __init__(self) -> None:
        self._providers: dict[type[ServiceType], type[ServiceType]] = {}  # type: ignore[valid-type]

    def register(self, dependency: type[ServiceType], provider: type[ServiceType]) -> None:
        self._providers[dependency] = provider

    def get(self, dependency: type[ServiceType]) -> ServiceType:
        if dependency in self._providers:
            cls = self._providers[dependency]
            return cls()  # type: ignore[misc]

        msg = f'No provider for {dependency}'
        raise ValueError(msg)


class Container:
    managers = DependencyContainer()
    services = DependencyContainer()
    executors = DependencyContainer()
    planners = DependencyContainer()
