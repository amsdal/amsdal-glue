from amsdal_glue_core.common.expressions.expression import Expression
from amsdal_glue_core.common.expressions.func import Func

JSONB_ARRAY_FUNC_NAME: str = 'jsonb_build_array'


class JsonbArrayExpression(Func):
    def __init__(self, items: list[Expression]) -> None:
        super().__init__(name=JSONB_ARRAY_FUNC_NAME, args=items)
