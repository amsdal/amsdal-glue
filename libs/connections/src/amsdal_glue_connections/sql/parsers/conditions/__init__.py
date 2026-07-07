from __future__ import annotations

from amsdal_glue_core.common.data_models.conditions import Condition
from amsdal_glue_core.common.data_models.conditions import Conditions
from amsdal_glue_core.common.enums import FieldLookup
from amsdal_glue_core.common.enums import FilterConnector

from amsdal_glue_connections.sql.parsers.default.ast import BinaryOp
from amsdal_glue_connections.sql.parsers.default.ast import Node
from amsdal_glue_connections.sql.parsers.default.ast import UnaryOp
from amsdal_glue_connections.sql.parsers.default.parser import parse as parse_ast
from amsdal_glue_connections.sql.parsers.default.pg_mapper import map_node as map_expression

_COMPARISON_OPS: dict[str, FieldLookup] = {
    '=': FieldLookup.EQ,
    '<>': FieldLookup.NEQ,
    '!=': FieldLookup.NEQ,
    '>': FieldLookup.GT,
    '>=': FieldLookup.GTE,
    '<': FieldLookup.LT,
    '<=': FieldLookup.LTE,
}


def parse_conditions(raw: str) -> Conditions:
    node = parse_ast(raw)
    return _node_to_conditions(node)


def _node_to_conditions(node: Node) -> Conditions:
    if isinstance(node, UnaryOp) and node.operator == 'NOT':
        inner = _node_to_conditions(node.operand)
        inner.negated = True
        return inner

    if isinstance(node, BinaryOp):
        if node.operator == 'AND':
            left = _node_to_conditions(node.left)
            right = _node_to_conditions(node.right)
            return Conditions(left, right, connector=FilterConnector.AND)

        if node.operator == 'OR':
            left = _node_to_conditions(node.left)
            right = _node_to_conditions(node.right)
            return Conditions(left, right, connector=FilterConnector.OR)

        lookup = _COMPARISON_OPS.get(node.operator)
        if lookup is not None:
            left_expr = map_expression(node.left)
            right_expr = map_expression(node.right)
            condition = Condition(left=left_expr, lookup=lookup, right=right_expr)
            return Conditions(condition)

    msg = f'Cannot convert AST node to Conditions: {node}'
    raise ValueError(msg)
