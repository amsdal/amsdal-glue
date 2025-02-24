from typing import Any

from amsdal_glue_core.common.expressions.expression import Expression


class RawExpression(Expression):
    def __init__(self, value: str, output_type: type[Any] | None = None) -> None:
        super().__init__(output_type=output_type)
        self.value = value
