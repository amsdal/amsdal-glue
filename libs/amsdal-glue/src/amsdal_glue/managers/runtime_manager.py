from collections.abc import Callable

from amsdal_glue_core.common.interfaces.runtime_manager import RuntimeManager


class DefaultRuntimeManager(RuntimeManager):
    def __init__(self) -> None:
        self._shutdown_hooks: list[Callable[[], None]] = []

    def add_shutdown_hook(self, func: Callable[[], None]):
        self._shutdown_hooks.append(func)

    def shutdown(self) -> None:
        for func in self._shutdown_hooks:
            func()

        self._shutdown_hooks.clear()
