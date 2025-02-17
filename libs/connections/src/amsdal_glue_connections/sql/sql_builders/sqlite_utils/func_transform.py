from typing import Any

from amsdal_glue_core.common.expressions.func import Func
from amsdal_glue_core.common.expressions.jsonb_array import JSONB_ARRAY_FUNC_NAME

from amsdal_glue_connections.sql.sql_builders.build_expression import build_function
from amsdal_glue_connections.sql.sql_builders.transform import Transform

SQLITE_FUNC_NAMES: dict[str, str] = {}
SQLITE_FUNC_TEMPLATE: dict[str, str] = {JSONB_ARRAY_FUNC_NAME: 'jsonb_array({args})'}
SQLITE_FUNC_ARG_TEMPLATE: dict[str, str] = {
    JSONB_ARRAY_FUNC_NAME: 'CASE WHEN json_valid({arg}) THEN jsonb({arg}) ELSE {arg} END'
}


def func_transform(expression: Func, transform: Transform) -> tuple[str, list[Any]]:
    _name = SQLITE_FUNC_NAMES.get(expression.name, expression.name)
    _template = SQLITE_FUNC_TEMPLATE.get(expression.name, expression.TEMPLATE)
    _arg_template = SQLITE_FUNC_ARG_TEMPLATE.get(expression.name, expression.ARG_TEMPLATE)

    return build_function(
        name=_name,
        template=_template,
        arg_template=_arg_template,
        args=expression.args,
        transform=transform,
    )
