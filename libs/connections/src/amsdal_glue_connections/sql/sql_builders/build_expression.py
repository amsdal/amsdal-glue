from typing import Any

from amsdal_glue_core.common.data_models.output_type import OutputType
from amsdal_glue_core.common.expressions.common import CombinedExpression
from amsdal_glue_core.common.expressions.expression import Expression
from amsdal_glue_core.common.expressions.field_reference import FieldReferenceExpression
from amsdal_glue_core.common.expressions.func import Func
from amsdal_glue_core.common.expressions.raw import RawExpression
from amsdal_glue_core.common.expressions.value import Value

from amsdal_glue_connections.sql.sql_builders.build_field import build_field
from amsdal_glue_connections.sql.sql_builders.transform import Transform
from amsdal_glue_connections.sql.sql_builders.transform import TransformTypes


def build_expression(
    expression: Expression,
    transform: Transform,
    *,
    embed_values: bool = False,
) -> tuple[str, list[Any]]:
    if isinstance(expression, FieldReferenceExpression):
        return build_field(expression.field_reference, transform, output_type=expression.output_type), []

    if isinstance(expression, RawExpression):
        stmt = expression.value
        stmt = transform.apply(TransformTypes.CAST, stmt, expression.output_type)

        return stmt, []

    if isinstance(expression, Value):
        if embed_values:
            stmt = transform.apply(
                TransformTypes.VALUE,
                value=expression.value,
            )
            return stmt, []

        stmt = transform.apply(
            TransformTypes.VALUE_PLACEHOLDER,
            expression.value,
            transform=transform,
            output_type=expression.output_type,
        )
        return stmt, [expression.value]

    if isinstance(expression, Func):
        return transform.apply(
            TransformTypes.FUNC,
            expression,
            transform=transform,
        )

    if isinstance(expression, CombinedExpression):
        left_stmt, left_params = build_expression(expression.left, transform, embed_values=embed_values)
        right_stmt, right_params = build_expression(expression.right, transform, embed_values=embed_values)

        stmt = transform.apply(TransformTypes.MATH_OPERATOR, left_stmt, expression.operator, right_stmt)
        stmt = transform.apply(TransformTypes.CAST, stmt, expression.output_type)

        return stmt, left_params + right_params

    msg = f'Unsupported expression type: {type(expression)}'
    raise ValueError(msg)


def build_function(
    name: str,
    template: str,
    arg_template: str,
    args: list[Expression],
    transform: Transform,
    output_type: type | OutputType | None = None,
) -> tuple[str, list[Any]]:
    stmt = template.replace('{name}', name)
    _arg_stmts, values = [], []

    for arg in args:
        _stmt, _values = build_expression(arg, transform)
        _arg_stmts.append(arg_template.replace('{arg}', _stmt))
        values.extend(_values)

    stmt = stmt.replace('{args}', ', '.join(_arg_stmts))
    stmt = transform.apply(TransformTypes.CAST, stmt, output_type)

    return stmt, values
