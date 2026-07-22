from __future__ import annotations

from typing import Any
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from amsdal_glue_core.common.expressions.expression import Expression


class Combinable:
    ADD = '+'
    SUB = '-'
    MUL = '*'
    DIV = '/'
    MOD = '%'
    POW = '**'
    XOR = '^'
    AND = '&'
    OR = '|'

    def _combine(self, other: Any, operator: str, *, is_reversed: bool = False) -> Expression:
        from amsdal_glue_core.common.expressions.combined import Combined
        from amsdal_glue_core.common.expressions.expression import Expression
        from amsdal_glue_core.common.expressions.value import Value

        if not isinstance(other, Expression):
            other = other.to_expression() if hasattr(other, 'to_expression') else Value(other)

        if not isinstance(self, Expression):
            _self = self.to_expression() if hasattr(self, 'to_expression') else Value(self)
        else:
            _self = self

        if is_reversed:
            return Combined(other, operator, _self)
        return Combined(_self, operator, other)

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

    def __xor__(self, other: Any) -> Expression:
        return self._combine(other, self.XOR, is_reversed=False)

    def __and__(self, other: Any) -> Expression:
        return self._combine(other, self.AND, is_reversed=False)

    def __or__(self, other: Any) -> Expression:
        return self._combine(other, self.OR, is_reversed=False)

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

    def __rpow__(self, other: Combinable) -> Expression:
        return self._combine(other, self.POW, is_reversed=True)

    def __rxor__(self, other: Combinable) -> Expression:
        return self._combine(other, self.XOR, is_reversed=True)

    def __rand__(self, other: Combinable) -> Expression:
        return self._combine(other, self.AND, is_reversed=True)

    def __ror__(self, other: Combinable) -> Expression:
        return self._combine(other, self.OR, is_reversed=True)
