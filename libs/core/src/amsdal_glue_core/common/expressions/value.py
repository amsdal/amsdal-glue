from dataclasses import dataclass
from typing import Any

from amsdal_glue_core.common.expressions.base import Expression


@dataclass
class Value(Expression):
    value: Any

    def __repr__(self) -> str:
        return repr(self.value)
