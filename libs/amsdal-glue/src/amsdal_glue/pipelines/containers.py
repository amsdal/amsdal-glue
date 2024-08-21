from collections.abc import Generator

from amsdal_glue_core.containers import Container
from amsdal_glue_core.containers import DependencyContainer
from amsdal_glue_core.containers import ServiceType


class SubDependencyContainer(DependencyContainer):
    def __init__(self, attribute: str) -> None:
        self._attribute = attribute
        super().__init__()

    def get(self, dependency: type[ServiceType]) -> ServiceType:
        try:
            return super().get(dependency)
        except ValueError:
            return getattr(Container, self._attribute).get(dependency)


class SubContainer:
    def __init__(self) -> None:
        self.managers = SubDependencyContainer('managers')
        self.services = SubDependencyContainer('services')
        self.executors = SubDependencyContainer('executors')
        self.planners = SubDependencyContainer('planners')


class ContainerRegistry:
    def __init__(self) -> None:
        self._containers: dict[str, SubContainer] = {}

    def register(self, name: str, container: SubContainer) -> None:
        self._containers[name] = container

    def get(self, name: str) -> SubContainer:
        return self._containers[name]


class Pipeline:
    def __init__(self) -> None:
        self.registry = ContainerRegistry()
        self._pipelines_per_service: dict[type[ServiceType], list[str]] = {}

    def register(self, service_type: type[ServiceType], container_names: list[str]) -> None:
        self._pipelines_per_service[service_type] = container_names

    def iter_container(self, service_type: type[ServiceType]) -> Generator[SubContainer, None, None]:
        for container_name in self._pipelines_per_service.get(service_type, []):
            yield self.registry.get(container_name)
