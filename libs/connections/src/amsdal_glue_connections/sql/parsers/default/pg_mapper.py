from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING

from amsdal_glue_core.common.expressions.func import Func
from amsdal_glue_core.common.expressions.now import Now
from amsdal_glue_core.common.expressions.value import Value

from amsdal_glue_connections.sql.parsers.default.base_mapper import BaseDefaultMapper

if TYPE_CHECKING:
    from amsdal_glue_core.common.data_models.types import FieldType
    from amsdal_glue_core.common.expressions.expression import Expression

    from amsdal_glue_connections.sql.parsers.default.ast import FuncCall
    from amsdal_glue_connections.sql.parsers.default.ast import Node
    from amsdal_glue_connections.sql.parsers.default.ast import TypeCast


class _PostgresDefaultMapper(BaseDefaultMapper):
    def _map_typecast(self, node: TypeCast, ctx: FieldType | None) -> Expression:
        # Strip typecasts, but coerce string literals to the target type when possible
        inner = self.map_node(node.expr, ctx)
        if isinstance(inner, Value) and isinstance(inner.value, str):
            type_lower = node.type_name.lower()
            if type_lower in ('integer', 'int', 'bigint', 'smallint'):
                return Value(value=int(inner.value))
            if type_lower in ('real', 'float', 'double precision'):
                return Value(value=float(inner.value))
            # NUMERIC/DECIMAL are arbitrary-precision: keep them as ``Decimal`` (from the literal
            # text) so a NUMERIC DEFAULT does not lose precision / its type to a binary ``float``.
            if type_lower in ('numeric', 'decimal'):
                return Value(value=Decimal(inner.value))
            if type_lower == 'boolean':
                if inner.value.lower() == 'true':
                    return Value(value=True)
                if inner.value.lower() == 'false':
                    return Value(value=False)
        return inner

    def _map_func(self, node: FuncCall, ctx: FieldType | None) -> Expression:  # noqa: ARG002
        lower_name = node.name.lower()

        if lower_name == 'now' and not node.args:
            return Now()

        return Func(name=lower_name, args=[self.map_node(arg) for arg in node.args])


_MAPPER = _PostgresDefaultMapper()


def map_node(node: Node) -> Expression:
    return _MAPPER.map_node(node)
