from dataclasses import dataclass
from typing import Any

from amsdal_glue_core.common.expressions.base import BaseExpression


@dataclass
class Value(BaseExpression):
    """Represents a value expression.

    Attributes:
        value (Any): The value of the expression.
    """

    value: Any

    def __repr__(self) -> str:
        return repr(self.value)

    def __hash__(self):
        return hash(self.value)
