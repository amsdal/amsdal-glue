from __future__ import annotations

from typing import Literal
from typing import TYPE_CHECKING

from amsdal_glue_core.common.expressions.expression import Expression

if TYPE_CHECKING:
    from amsdal_glue_core.common.data_models.types import FieldType


class VectorExpression(Expression):
    operator: Literal['<->', '<#>', '<=>', '<+>', '<~>', '<%>']

    def __init__(self, left: Expression, right: Expression, output_type: FieldType | None = None) -> None:
        super().__init__(output_type=output_type)
        self.left = left
        self.right = right

    def __repr__(self):
        return f'<{self.__class__.__name__}: {self}>'

    def __str__(self) -> str:
        return f'{self.left} {self.operator} {self.right}'

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, VectorExpression):
            return False

        return self.left == other.left and self.right == other.right and self.operator == other.operator

    def __hash__(self) -> int:
        return hash((self.left, self.right, self.operator))


class L2Distance(VectorExpression):
    operator = '<->'


class InnerProduct(VectorExpression):
    operator = '<#>'


class CosineDistance(VectorExpression):
    operator = '<=>'


class L1Distance(VectorExpression):
    operator = '<+>'


# Backward-compat aliases — old code used the *Expression suffix names.
L2DistanceExpression = L2Distance
InnerProductExpression = InnerProduct
CosineDistanceExpression = CosineDistance
L1DistanceExpression = L1Distance
