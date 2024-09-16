from amsdal_glue_core.containers import SubContainer


class ContainerRegistry:
    def __init__(self) -> None:
        self._containers: dict[str, SubContainer] = {}

    def register(self, name: str, container: SubContainer) -> None:
        self._containers[name] = container

    def get(self, name: str) -> SubContainer:
        return self._containers[name]
