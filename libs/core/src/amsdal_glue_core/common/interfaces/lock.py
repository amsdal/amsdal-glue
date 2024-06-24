from abc import ABC
from abc import abstractmethod
from typing import Any

from amsdal_glue_core.common.interfaces.connectable import Connectable


class LockBase(Connectable, ABC):
    @abstractmethod
    def acquire(
        self,
        lock_id: str,
        *,
        timeout_ms: int = -1,
        blocking: bool = True,
        metadata: dict[str, Any] | None = None,
    ) -> str | None: ...

    @abstractmethod
    def release(self, lock_id: str) -> None: ...
