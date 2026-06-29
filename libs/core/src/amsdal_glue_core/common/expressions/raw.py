from __future__ import annotations

from typing import Any
from typing import TYPE_CHECKING

from amsdal_glue_core.common.expressions.expression import Expression

if TYPE_CHECKING:
    from amsdal_glue_core.common.data_models.types import FieldType


class RawExpression(Expression):
    def __init__(self, value: str, params: tuple[Any, ...] = (), output_type: FieldType | None = None) -> None:
        super().__init__(output_type=output_type)
        self.value = value
        self.params = params
