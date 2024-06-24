from typing import Any
from typing import TypeVar

T = TypeVar('T', bound='Singleton')


class Singleton(type):
    _instances: dict[type[T], T] = {}  # type: ignore[valid-type] # noqa: RUF012

    def __call__(cls: type[T], *args: Any, **kwargs: Any) -> T:  # type: ignore[misc]
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)  # noqa: UP008
        return cls._instances[cls]

    @classmethod
    def invalidate_all_instances(cls: type[T]) -> None:
        cls._instances = {}

    @classmethod
    def invalidate_instance(cls: type[T], target_cls: type[T]) -> None:
        if target_cls in cls._instances:
            del cls._instances[target_cls]
