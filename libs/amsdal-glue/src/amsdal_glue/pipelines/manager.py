from collections.abc import Generator
from typing import Any

from amsdal_glue_core.containers import SubContainer

from amsdal_glue.pipelines.containers import ContainerRegistry


class PipelineManager:
    def __init__(self) -> None:
        self.registry = ContainerRegistry()
        self._pipelines_per_service: dict[type[Any], list[str]] = {}

    def define(self, service_type: type[Any], container_names: list[str]) -> None:
        self._pipelines_per_service[service_type] = container_names

    def iter_container(self, service_type: type[Any]) -> Generator[SubContainer, None, None]:
        for container_name in self._pipelines_per_service.get(service_type, []):
            yield self.registry.get(container_name)
