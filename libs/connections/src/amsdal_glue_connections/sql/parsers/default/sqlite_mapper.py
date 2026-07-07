from __future__ import annotations

from typing import TYPE_CHECKING

from amsdal_glue_core.common.enums import ScalarType
from amsdal_glue_core.common.expressions.combined import Combined
from amsdal_glue_core.common.expressions.current_timestamp import CurrentDate
from amsdal_glue_core.common.expressions.current_timestamp import CurrentTime
from amsdal_glue_core.common.expressions.current_timestamp import CurrentTimestamp
from amsdal_glue_core.common.expressions.field_reference import FieldReferenceExpression
from amsdal_glue_core.common.expressions.func import Func
from amsdal_glue_core.common.expressions.now import Now
from amsdal_glue_core.common.expressions.raw import RawExpression
from amsdal_glue_core.common.expressions.value import Value

from amsdal_glue_connections.sql.parsers.default.ast import BinaryOp
from amsdal_glue_connections.sql.parsers.default.ast import BoolKeyword
from amsdal_glue_connections.sql.parsers.default.ast import ColumnRef
from amsdal_glue_connections.sql.parsers.default.ast import FuncCall
from amsdal_glue_connections.sql.parsers.default.ast import Literal
from amsdal_glue_connections.sql.parsers.default.ast import Node
from amsdal_glue_connections.sql.parsers.default.ast import SqlKeyword
from amsdal_glue_connections.sql.parsers.default.ast import TypeCast
from amsdal_glue_connections.sql.parsers.default.ast import UnaryOp

if TYPE_CHECKING:
    from amsdal_glue_core.common.data_models.types import FieldType
    from amsdal_glue_core.common.expressions.expression import Expression

_KEYWORD_MAP: dict[str, type[Expression]] = {
    'CURRENT_TIMESTAMP': CurrentTimestamp,
    'CURRENT_DATE': CurrentDate,
    'CURRENT_TIME': CurrentTime,
}


def map_node(node: Node, field_type: FieldType | None = None) -> Expression:  # noqa: C901, PLR0911, PLR0912
    if isinstance(node, Literal):
        # SQLite stores booleans as 1/0
        if isinstance(field_type, ScalarType) and field_type == ScalarType.BOOLEAN:
            if node.value == 1:
                return Value(value=True)
            if node.value == 0:
                return Value(value=False)

        return Value(value=node.value)

    if isinstance(node, BoolKeyword):
        return Value(value=node.value)

    if isinstance(node, SqlKeyword):
        expr_cls = _KEYWORD_MAP.get(node.name.upper())
        if expr_cls is not None:
            return expr_cls()
        return RawExpression(node.name)

    if isinstance(node, TypeCast):
        return map_node(node.expr, field_type)

    if isinstance(node, FuncCall):
        lower_name = node.name.lower()

        # datetime('now') → Now()
        if lower_name == 'datetime' and len(node.args) == 1:
            arg = node.args[0]
            if isinstance(arg, Literal) and arg.value == 'now':
                return Now()

        return Func(name=lower_name, args=[map_node(arg) for arg in node.args])

    if isinstance(node, ColumnRef):
        from amsdal_glue_core.common.data_models.field_reference import Field
        from amsdal_glue_core.common.data_models.field_reference import FieldReference

        return FieldReferenceExpression(
            field_reference=FieldReference(field=Field(name=node.name), table_name=node.table or '')
        )

    if isinstance(node, BinaryOp):
        return Combined(map_node(node.left, field_type), node.operator, map_node(node.right, field_type))

    if isinstance(node, UnaryOp):
        if node.operator == '-' and isinstance(node.operand, Literal) and isinstance(node.operand.value, int | float):
            return Value(value=-node.operand.value)
        inner = map_node(node.operand, field_type)
        return RawExpression(f'{node.operator}({inner!r})')

    return RawExpression(str(node))  # pragma: no cover
