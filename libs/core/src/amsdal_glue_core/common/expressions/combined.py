from __future__ import annotations

from typing import TYPE_CHECKING

from amsdal_glue_core.common.expressions.expression import Expression

if TYPE_CHECKING:
    from amsdal_glue_core.common.data_models.types import FieldType


class Combined(Expression):
    def __init__(
        self,
        left: Expression,
        operator: str,
        right: Expression,
        output_type: FieldType | None = None,
    ) -> None:
        super().__init__(output_type=output_type)
        self.left = left
        self.operator = operator
        self.right = right

    def __repr__(self):
        return f'<{self.__class__.__name__}: {self}>'

    def __str__(self):
        return f'{self.left} {self.operator} {self.right}'

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Combined):
            return False

        return self.left == other.left and self.operator == other.operator and self.right == other.right

    def __hash__(self) -> int:
        return hash((self.left, self.operator, self.right))
