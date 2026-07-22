"""Shared AST -> glue ``Expression`` mapping for the dialect DEFAULT / GENERATED mappers.

The ``BoolKeyword`` / ``SqlKeyword`` / ``ColumnRef`` / ``BinaryOp`` / ``UnaryOp`` branches and the
final fallback are identical for Postgres and SQLite. Only the ``Literal``, ``TypeCast`` and
``FuncCall`` branches diverge, so those are overridable hooks (`_map_literal`, `_map_typecast`,
`_map_func`). A ``ctx`` value (the column ``field_type``, or ``None``) threads through the recursion;
the Postgres mapper ignores it, the SQLite mapper uses it (e.g. to render 1/0 as booleans).
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from amsdal_glue_core.common.expressions.combined import Combined
from amsdal_glue_core.common.expressions.current_timestamp import CurrentDate
from amsdal_glue_core.common.expressions.current_timestamp import CurrentTime
from amsdal_glue_core.common.expressions.current_timestamp import CurrentTimestamp
from amsdal_glue_core.common.expressions.field_reference import FieldReferenceExpression
from amsdal_glue_core.common.expressions.func import Func
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


class BaseDefaultMapper:
    """Dialect-neutral AST walker; dialects override the `_map_literal` / `_map_typecast` / `_map_func` hooks."""

    def map_node(self, node: Node, ctx: FieldType | None = None) -> Expression:  # noqa: C901, PLR0911
        if isinstance(node, Literal):
            return self._map_literal(node, ctx)

        if isinstance(node, BoolKeyword):
            return Value(value=node.value)

        if isinstance(node, SqlKeyword):
            expr_cls = _KEYWORD_MAP.get(node.name.upper())
            if expr_cls is not None:
                return expr_cls()
            return RawExpression(node.name)

        if isinstance(node, TypeCast):
            return self._map_typecast(node, ctx)

        if isinstance(node, FuncCall):
            return self._map_func(node, ctx)

        if isinstance(node, ColumnRef):
            from amsdal_glue_core.common.data_models.field_reference import Field
            from amsdal_glue_core.common.data_models.field_reference import FieldReference

            return FieldReferenceExpression(
                field_reference=FieldReference(field=Field(name=node.name), table_name=node.table or '')
            )

        if isinstance(node, BinaryOp):
            return Combined(self.map_node(node.left, ctx), node.operator, self.map_node(node.right, ctx))

        if isinstance(node, UnaryOp):
            if (
                node.operator == '-'
                and isinstance(node.operand, Literal)
                and isinstance(node.operand.value, int | float)
            ):
                return Value(value=-node.operand.value)
            # A non-arithmetic unary op (e.g. ``NOT active``, ``~flags``). Render the operand
            # through the normal expression path -- as a ``Func`` whose "name" is the operator, so
            # it emits ``NOT(<operand SQL>)`` -- instead of embedding the operand's ``repr()`` (which
            # would produce invalid SQL like ``NOT(<FieldReferenceExpression ...>)``).
            inner = self.map_node(node.operand, ctx)
            return Func(name=node.operator, args=[inner])

        return RawExpression(str(node))  # pragma: no cover

    def _map_literal(self, node: Literal, ctx: FieldType | None) -> Expression:  # noqa: ARG002
        return Value(value=node.value)

    def _map_typecast(self, node: TypeCast, ctx: FieldType | None) -> Expression:
        raise NotImplementedError

    def _map_func(self, node: FuncCall, ctx: FieldType | None) -> Expression:
        raise NotImplementedError
