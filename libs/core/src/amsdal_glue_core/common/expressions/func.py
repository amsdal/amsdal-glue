from dataclasses import dataclass
from typing import ClassVar

from amsdal_glue_core.common.expressions.expression import Expression


@dataclass(kw_only=True)
class Func(Expression):
    """Represents a function expression.

    Attributes:
        TEMPLATE (ClassVar[str]): The template for the function.
        name (str): The name of the function.
        args (list[Expression]): The arguments of the function.
    """

    TEMPLATE: ClassVar[str] = '{name}({args})'
    ARG_TEMPLATE: ClassVar[str] = '{arg}'

    name: str
    args: list[Expression]
