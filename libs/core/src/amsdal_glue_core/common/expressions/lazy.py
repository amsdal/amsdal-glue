from __future__ import annotations

from typing import Any

from amsdal_glue_core.common.expressions.value import Value


class ParamStore:
    """Shared mutable container for resolved parameter values.

    Created once per BoundOperation, shared by all LazyValue instances.
    Executor calls .set() before compilation — all LazyValue see their values.
    """

    def __init__(self) -> None:
        self._values: dict[str, Any] = {}

    def set(self, values: dict[str, Any]) -> None:
        self._values = values

    def __getitem__(self, name: str) -> Any:
        return self._values[name]

    def clear(self) -> None:
        self._values.clear()


class LazyValue(Value):
    """Value resolved lazily from a shared ParamStore at compile time."""

    def __init__(self, name: str, store: ParamStore) -> None:
        super().__init__(value=None)
        self._name = name
        self._store = store

    @property  # type: ignore[override]
    def value(self) -> Any:
        return self._store[self._name]

    @value.setter
    def value(self, _val: Any) -> None:
        pass  # ignore — Value.__init__ sets self.value = None
