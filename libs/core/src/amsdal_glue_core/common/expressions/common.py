import copy
from typing import Any

from amsdal_glue_core.common.expressions.base import BaseExpression
from amsdal_glue_core.common.expressions.value import Value


class Expression(BaseExpression):
    def __init__(self, output_type: type[Any] | None = None) -> None:
        self.output_type = output_type

    def to_expression(self) -> 'Expression':
        return self.copy()

    def copy(self) -> 'Expression':
        return copy.copy(self)


class Combinable:
    """Mixin class to provide combinable operations for expressions.

    This class defines methods for combining expressions using various
    mathematical operators such as addition, subtraction, multiplication,
    division, modulus, and exponentiation.
    """

    ADD = '+'
    SUB = '-'
    MUL = '*'
    DIV = '/'
    POW = '^'
    MOD = '%'

    def _combine(self, other: Any, operator: str, *, is_reversed: bool = False) -> Expression:
        if not hasattr(other, 'to_expression'):
            other = Value(other)
        if is_reversed:
            return CombinedExpression(other, operator, self)
        return CombinedExpression(self, operator, other)

    def __neg__(self: Any) -> Expression:
        return self._combine(-1, self.MUL, is_reversed=False)

    def __add__(self, other: Any) -> Expression:
        return self._combine(other, self.ADD, is_reversed=False)

    def __sub__(self, other: Any) -> Expression:
        return self._combine(other, self.SUB, is_reversed=False)

    def __mul__(self, other: Any) -> Expression:
        return self._combine(other, self.MUL, is_reversed=False)

    def __truediv__(self, other: Any) -> Expression:
        return self._combine(other, self.DIV, is_reversed=False)

    def __mod__(self, other: Any) -> Expression:
        return self._combine(other, self.MOD, is_reversed=False)

    def __pow__(self, other: Any) -> Expression:
        return self._combine(other, self.POW, is_reversed=False)

    def __radd__(self, other: Any) -> Expression:
        return self._combine(other, self.ADD, is_reversed=True)

    def __rsub__(self, other: Any) -> Expression:
        return self._combine(other, self.SUB, is_reversed=True)

    def __rmul__(self, other: Any) -> Expression:
        return self._combine(other, self.MUL, is_reversed=True)

    def __rtruediv__(self, other: Any) -> Expression:
        return self._combine(other, self.DIV, is_reversed=True)

    def __rmod__(self, other: Any) -> Expression:
        return self._combine(other, self.MOD, is_reversed=True)

    def __rpow__(self, other: 'Combinable') -> Expression:
        return self._combine(other, self.POW, is_reversed=True)


class CombinedExpression(Expression):
    """Represents a combined expression using a mathematical operator.

    This class combines two expressions or values using a specified
    mathematical operator and provides a string representation of the
    combined expression.

    Attributes:
        left (Any): The left operand of the combined expression.
        operator (str): The operator used to combine the operands.
        right (Any): The right operand of the combined expression.
        output_type (type[Any] | None): The output type of the expression.
    """

    def __init__(
        self,
        left: Any,
        operator: str,
        right: Any,
        output_type: type[Any] | None = None,
    ) -> None:
        super().__init__(output_type=output_type)
        self.left = left
        self.operator = operator
        self.right = right

    def __repr__(self):
        return f'<{self.__class__.__name__}: {self}>'

    def __str__(self):
        return f'{self.left} {self.operator} {self.right}'
