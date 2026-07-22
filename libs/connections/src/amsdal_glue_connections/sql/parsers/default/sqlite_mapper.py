from __future__ import annotations

from typing import TYPE_CHECKING

from amsdal_glue_core.common.enums import ScalarType
from amsdal_glue_core.common.expressions.func import Func
from amsdal_glue_core.common.expressions.now import Now
from amsdal_glue_core.common.expressions.value import Value

from amsdal_glue_connections.sql.parsers.default.ast import FuncCall
from amsdal_glue_connections.sql.parsers.default.ast import Literal
from amsdal_glue_connections.sql.parsers.default.ast import Node
from amsdal_glue_connections.sql.parsers.default.ast import TypeCast
from amsdal_glue_connections.sql.parsers.default.base_mapper import BaseDefaultMapper

if TYPE_CHECKING:
    from amsdal_glue_core.common.data_models.types import FieldType
    from amsdal_glue_core.common.expressions.expression import Expression


class _SqliteDefaultMapper(BaseDefaultMapper):
    def _map_literal(self, node: Literal, ctx: FieldType | None) -> Expression:
        # SQLite stores booleans as 1/0
        if isinstance(ctx, ScalarType) and ctx == ScalarType.BOOLEAN:
            if node.value == 1:
                return Value(value=True)
            if node.value == 0:
                return Value(value=False)

        return Value(value=node.value)

    def _map_typecast(self, node: TypeCast, ctx: FieldType | None) -> Expression:
        return self.map_node(node.expr, ctx)

    def _map_func(self, node: FuncCall, ctx: FieldType | None) -> Expression:  # noqa: ARG002
        lower_name = node.name.lower()

        # datetime('now') → Now()
        if lower_name == 'datetime' and len(node.args) == 1:
            arg = node.args[0]
            if isinstance(arg, Literal) and arg.value == 'now':
                return Now()

        return Func(name=lower_name, args=[self.map_node(arg) for arg in node.args])


_MAPPER = _SqliteDefaultMapper()


def map_node(node: Node, field_type: FieldType | None = None) -> Expression:
    return _MAPPER.map_node(node, field_type)
