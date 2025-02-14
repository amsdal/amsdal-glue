from typing import Any

from amsdal_glue_core.common.expressions.expression import Expression


class Value(Expression):
    """Represents a value expression.

    Attributes:
        value (Any): The value of the expression.
    """

    def __init__(self, value: Any, output_type: type[Any] | None = None) -> None:
        super().__init__(output_type=output_type)
        self.value = value

    def __repr__(self) -> str:
        return repr(self.value)

    def __hash__(self):
        return hash(self.value)
