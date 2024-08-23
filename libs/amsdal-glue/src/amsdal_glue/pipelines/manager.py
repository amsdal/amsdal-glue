from collections.abc import Generator

from amsdal_glue.pipelines.containers import ContainerRegistry
from amsdal_glue_core.containers import ServiceType
from amsdal_glue_core.containers import SubContainer


class PipelineManager:
    def __init__(self) -> None:
        self.registry = ContainerRegistry()
        self._pipelines_per_service: dict[type[ServiceType], list[str]] = {}

    def define(self, service_type: type[ServiceType], container_names: list[str]) -> None:
        self._pipelines_per_service[service_type] = container_names

    def iter_container(self, service_type: type[ServiceType]) -> Generator[SubContainer, None, None]:
        for container_name in self._pipelines_per_service.get(service_type, []):
            yield self.registry.get(container_name)
