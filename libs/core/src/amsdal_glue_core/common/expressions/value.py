from dataclasses import dataclass
from typing import Any

from amsdal_glue_core.common.expressions.expression import Expression


@dataclass(kw_only=True)
class Value(Expression):
    """Represents a value expression.

    Attributes:
        value (Any): The value of the expression.
    """

    value: Any

    def __init__(self, value: Any, output_type: type[Any] | None = None) -> None:
        super().__init__(output_type=output_type)
        self.value = value

    def __repr__(self) -> str:
        return repr(self.value)

    def __hash__(self):
        return hash(self.value)
