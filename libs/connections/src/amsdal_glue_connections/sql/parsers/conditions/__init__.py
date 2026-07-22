from __future__ import annotations

from amsdal_glue_core.common.data_models.conditions import Condition
from amsdal_glue_core.common.data_models.conditions import Conditions
from amsdal_glue_core.common.enums import FieldLookup
from amsdal_glue_core.common.enums import FilterConnector
from amsdal_glue_core.common.expressions.value import Value

from amsdal_glue_connections.sql.parsers.default.ast import Between
from amsdal_glue_connections.sql.parsers.default.ast import BinaryOp
from amsdal_glue_connections.sql.parsers.default.ast import InList
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

_CONNECTORS: dict[str, FilterConnector] = {
    'AND': FilterConnector.AND,
    'OR': FilterConnector.OR,
}

# glue has no plain ``LIKE`` lookup, only the high-level ``CONTAINS``/``STARTSWITH``/``ENDSWITH``
# family (the renderer escapes the value and re-wraps it with ``%``). A pattern whose only wildcards
# are the anchoring ``%`` maps losslessly onto one of these; anything with interior wildcards has no
# faithful equivalent and is rejected (the caller degrades it to ``condition=None``).
_LIKE_LOOKUPS: dict[str, FieldLookup] = {
    'LIKE': FieldLookup.CONTAINS,
    'ILIKE': FieldLookup.ICONTAINS,
}
_LIKE_STARTSWITH: dict[str, FieldLookup] = {
    'LIKE': FieldLookup.STARTSWITH,
    'ILIKE': FieldLookup.ISTARTSWITH,
}
_LIKE_ENDSWITH: dict[str, FieldLookup] = {
    'LIKE': FieldLookup.ENDSWITH,
    'ILIKE': FieldLookup.IENDSWITH,
}


def parse_conditions(raw: str) -> Conditions:
    node = parse_ast(raw)
    return _node_to_conditions(node)


def try_parse_conditions(raw: str) -> Conditions | None:
    """Parse a predicate for introspection, degrading to ``None`` when it cannot be represented.

    Introspection reads arbitrary, externally-authored CHECK / partial-index predicates. Anything
    the parser/mapper cannot turn into a glue ``Conditions`` (an exotic operator, a construct with no
    faithful ``FieldLookup``) must not abort the whole ``query_schema`` -- it degrades to ``None``,
    matching the pre-existing "condition not captured" behaviour.
    """
    try:
        return parse_conditions(raw)
    except (ValueError, TypeError, ArithmeticError):
        return None


def _node_to_conditions(node: Node) -> Conditions:
    if isinstance(node, UnaryOp) and node.operator == 'NOT':
        inner = _node_to_conditions(node.operand)
        # Toggle rather than force-set so nested ``NOT NOT`` cancels instead of collapsing to one.
        inner.negated = not inner.negated
        return inner

    if isinstance(node, Between):
        return _between_to_conditions(node)

    if isinstance(node, BinaryOp):
        return _binary_to_conditions(node)

    msg = f'Cannot convert AST node to Conditions: {node}'
    raise ValueError(msg)


def _binary_to_conditions(node: BinaryOp) -> Conditions:
    connector = _CONNECTORS.get(node.operator)
    if connector is not None:
        return Conditions(
            _node_to_conditions(node.left),
            _node_to_conditions(node.right),
            connector=connector,
        )

    lookup = _COMPARISON_OPS.get(node.operator)
    if lookup is not None:
        return Conditions(Condition(left=map_expression(node.left), lookup=lookup, right=map_expression(node.right)))

    if node.operator in ('IS', 'IS NOT'):
        # ``x IS NULL`` -> ISNULL/Value(True); ``x IS NOT NULL`` -> ISNULL/Value(False).
        return Conditions(
            Condition(
                left=map_expression(node.left),
                lookup=FieldLookup.ISNULL,
                right=Value(value=node.operator == 'IS'),
            )
        )

    if node.operator in ('IN', 'NOT IN'):
        return _in_to_conditions(node, negate=node.operator == 'NOT IN')

    if node.operator in ('LIKE', 'ILIKE', 'NOT LIKE', 'NOT ILIKE'):
        return _like_to_conditions(node)

    msg = f'Cannot convert AST node to Conditions: {node}'
    raise ValueError(msg)


def _in_to_conditions(node: BinaryOp, *, negate: bool) -> Conditions:
    if not isinstance(node.right, InList):
        msg = f'Expected a value list on the right side of IN: {node}'
        raise TypeError(msg)

    values = [_literal_value(item) for item in node.right.items]
    return Conditions(
        Condition(
            left=map_expression(node.left),
            lookup=FieldLookup.IN,
            right=Value(value=values),
            negate=negate,
        )
    )


def _between_to_conditions(node: Between) -> Conditions:
    low = _literal_value(node.low)
    high = _literal_value(node.high)
    return Conditions(
        Condition(
            left=map_expression(node.expr),
            lookup=FieldLookup.BETWEEN,
            right=Value(value=[low, high]),
            negate=node.negated,
        )
    )


def _like_to_conditions(node: BinaryOp) -> Conditions:
    negate = node.operator.startswith('NOT ')
    keyword = node.operator[len('NOT ') :] if negate else node.operator

    pattern = _literal_value(node.right)
    if not isinstance(pattern, str):
        msg = f'Expected a string pattern on the right side of LIKE: {node}'
        raise TypeError(msg)

    lookup, value = _like_pattern_to_lookup(keyword, pattern)
    return Conditions(Condition(left=map_expression(node.left), lookup=lookup, right=Value(value=value), negate=negate))


def _like_pattern_to_lookup(keyword: str, pattern: str) -> tuple[FieldLookup, str]:
    starts, ends = pattern.startswith('%'), pattern.endswith('%')
    core = pattern[1:] if starts else pattern
    core = core[:-1] if ends else core

    # The core (the non-anchor part) must itself be free of LIKE wildcards, otherwise the
    # CONTAINS/STARTSWITH/ENDSWITH mapping (which escapes its value) would change the semantics.
    if not core or '%' in core or '_' in core:
        msg = f'Unsupported LIKE pattern (no faithful glue lookup): {pattern!r}'
        raise ValueError(msg)

    if starts and ends:
        return _LIKE_LOOKUPS[keyword], core
    if ends:
        return _LIKE_STARTSWITH[keyword], core
    if starts:
        return _LIKE_ENDSWITH[keyword], core

    msg = f'Unsupported LIKE pattern (no wildcards to anchor): {pattern!r}'
    raise ValueError(msg)


def _literal_value(node: Node) -> object:
    """Return the Python value of a literal AST node, rejecting anything non-constant."""
    expr = map_expression(node)
    if isinstance(expr, Value):
        return expr.value

    msg = f'Expected a literal value, got: {node}'
    raise ValueError(msg)
