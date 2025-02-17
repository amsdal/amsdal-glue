from typing import Any

from amsdal_glue_core.common.expressions.func import Func

from amsdal_glue_connections.sql.sql_builders.build_expression import build_function
from amsdal_glue_connections.sql.sql_builders.transform import Transform

PG_FUNC_NAMES: dict[str, str] = {}
PG_FUNC_TEMPLATE: dict[str, str] = {}
PG_FUNC_ARG_TEMPLATE: dict[str, str] = {}


def func_transform(expression: Func, transform: Transform) -> tuple[str, list[Any]]:
    _name = PG_FUNC_NAMES.get(expression.name, expression.name)
    _template = PG_FUNC_TEMPLATE.get(expression.name, expression.TEMPLATE)
    _arg_template = PG_FUNC_ARG_TEMPLATE.get(expression.name, expression.ARG_TEMPLATE)

    return build_function(
        name=_name,
        template=_template,
        arg_template=_arg_template,
        args=expression.args,
        transform=transform,
    )
