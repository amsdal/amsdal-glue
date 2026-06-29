from dataclasses import dataclass

from amsdal_glue_core.common.expressions.expression import Expression


@dataclass(kw_only=True)
class SelectExpression:
    expression: Expression
    alias: str
