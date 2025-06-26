from typing import Any
from typing import Literal

from amsdal_glue_core.common.expressions.expression import Expression


class VectorExpression(Expression):
    operator: Literal['<->', '<#>', '<=>', '<+>', '<~>', '<%>']

    def __init__(self, left: Expression, right: Expression, output_type: type[Any] | None = None) -> None:
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


class L2DistanceExpression(VectorExpression):
    operator = '<->'


class InnerProductExpression(VectorExpression):
    operator = '<#>'


class CosineDistanceExpression(VectorExpression):
    operator = '<=>'


class L1DistanceExpression(VectorExpression):
    operator = '<+>'
