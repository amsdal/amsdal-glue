from typing import Any
from typing import Protocol

from amsdal_glue_core.common.expressions.common import Combinable


class MathOperatorTransform(Protocol):
    def __call__(self, left: Any, operator: str, right: Any) -> str: ...


def default_math_operator_transform(
    left: Any,
    operator: str,
    right: Any,
) -> str:
    """Transforms a mathematical operation into a string representation.

    Args:
        left (Any): The left operand.
        operator (str): The operator as a string.
        right (Any): The right operand.

    Returns:
        str: The string representation of the mathematical operation.
    """

    return f'{left} {operator} {right}'


def sqlite_math_operator_transform(
    left: Any,
    operator: str,
    right: Any,
) -> str:
    """Transforms a mathematical operation into a string representation for SQLite.

    Args:
        left (Any): The left operand.
        operator (str): The operator as a string.
        right (Any): The right operand.

    Returns:
        str: The string representation of the mathematical operation for SQLite.
    """

    if operator == Combinable.POW:
        return f'POWER({left}, {right})'
    return f'{left} {operator} {right}'


pg_math_operator_transform = sqlite_math_operator_transform
