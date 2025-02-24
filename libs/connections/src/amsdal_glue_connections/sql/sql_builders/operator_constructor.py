from typing import Any
from typing import Protocol

from amsdal_glue_core.common.enums import FieldLookup
from amsdal_glue_core.common.expressions.expression import Expression
from amsdal_glue_core.common.expressions.value import Value

from amsdal_glue_connections.sql.sql_builders.build_expression import build_expression
from amsdal_glue_connections.sql.sql_builders.transform import Transform
from amsdal_glue_connections.sql.sql_builders.transform import TransformTypes


class OperatorConstructor(Protocol):
    def __call__(
        self,
        left: Expression,
        lookup: FieldLookup,
        right: Expression,
        transform: Transform,
        *,
        embed_values: bool = False,
    ) -> tuple[str, list[Any]]: ...


def default_operator_constructor(  # noqa: C901, PLR0915, PLR0912
    left: Expression,
    lookup: FieldLookup,
    right: Expression,
    transform: Transform,
    *,
    embed_values: bool = False,
) -> tuple[str, list[Any]]:
    """
    Constructs an SQL operator for the given field and lookup.

    Args:
        left (Expression): The left expression.
        lookup (FieldLookup): The lookup type.
        right (Expression): The right expression.
        transform (Transform): The transform SQL to database specific.

    Returns:
        tuple[str, list[Any]]: The SQL operator and the list of values.
    """
    value_transform = transform.resolve(TransformTypes.VALUE)
    left_stmt, left_values = build_expression(left, transform, embed_values=embed_values)

    if isinstance(right, Value) and lookup == FieldLookup.IN:
        if not isinstance(right.value, list | tuple | set):
            msg = f'Unsupported value type "{type(right.value)}" for lookup "{lookup}". Must be list, tuple or set.'
            raise ValueError(msg)

        _stmts, _values = [], []
        for value in right.value:
            _right_stmt, _right_values = build_expression(
                Value(value=value, output_type=right.output_type),  # type: ignore[arg-type]
                transform,
                embed_values=embed_values,
            )
            _stmts.append(_right_stmt)
            _values.extend(_right_values)

        right_stmt = ', '.join(_stmts)
        right_values = _values
    else:
        right_stmt, right_values = build_expression(right, transform, embed_values=embed_values)

    raw_values = left_values + right_values
    values = [value_transform(_value) for _value in raw_values]

    match lookup:
        case FieldLookup.EXACT:
            right_stmt = f'IS {right_stmt}'  # type: ignore[union-attr]
        case FieldLookup.EQ:
            right_stmt = f'= {right_stmt}'
        case FieldLookup.NEQ:
            right_stmt = f'!= {right_stmt}'
        case FieldLookup.GT:
            right_stmt = f'> {right_stmt}'
        case FieldLookup.GTE:
            right_stmt = f'>= {right_stmt}'
        case FieldLookup.LT:
            right_stmt = f'< {right_stmt}'
        case FieldLookup.LTE:
            right_stmt = f'<= {right_stmt}'
        case FieldLookup.IN:
            right_stmt = f'IN ({right_stmt})'
        case FieldLookup.CONTAINS:
            right_stmt = f'GLOB {right_stmt}'
            values = [f'*{_value}*' for _value in values]
        case FieldLookup.ICONTAINS:
            left_stmt = f'LOWER({left_stmt})'
            right_stmt = f'LIKE LOWER({right_stmt})'
            values = [f'%{_value}%' for _value in values]
        case FieldLookup.STARTSWITH:
            right_stmt = f'GLOB {right_stmt}'
            values = [f'{_value}*' for _value in values]
        case FieldLookup.ISTARTSWITH:
            left_stmt = f'LOWER({left_stmt})'
            right_stmt = f'LIKE LOWER({right_stmt})'
            values = [f'{_value}%' for _value in values]
        case FieldLookup.ENDSWITH:
            right_stmt = f'GLOB {right_stmt}'
            values = [f'*{_value}' for _value in values]
        case FieldLookup.IENDSWITH:
            left_stmt = f'LOWER({left_stmt})'
            right_stmt = f'LIKE LOWER({right_stmt})'
            values = [f'%{_value}' for _value in values]
        case FieldLookup.ISNULL:
            if not isinstance(right, Value):
                msg = f'Unsupported value type "{type(right)}" for lookup "{lookup}". Must be Value.'
                raise TypeError(msg)

            values = []
            _null_value = transform.apply(TransformTypes.NULL_VALUE)
            right_stmt = f'IS {_null_value}' if right.value else f'IS NOT {_null_value}'  # type: ignore[union-attr]
        case FieldLookup.REGEX:
            right_stmt = f'REGEXP {right_stmt}'
        case FieldLookup.IREGEX:
            left_stmt = f'LOWER({left_stmt})'
            right_stmt = f'REGEXP {right_stmt}'
        case _:
            msg = f'{lookup} not supported'
            raise ValueError(msg)

    return f'{left_stmt} {right_stmt}', values


def repr_operator_constructor(  # noqa: PLR0912, C901
    left: Expression,
    lookup: FieldLookup,
    right: Expression,
    transform: Transform,
    *,
    embed_values: bool = False,  # noqa: ARG001
) -> tuple[str, list[Any]]:
    left_stmt = repr(left)
    right_stmt = repr(right)

    match lookup:
        case FieldLookup.EXACT:
            right_stmt = f'IS {right_stmt}'
        case FieldLookup.EQ:
            right_stmt = f'= {right_stmt}'
        case FieldLookup.NEQ:
            right_stmt = f'!= {right_stmt}'
        case FieldLookup.GT:
            right_stmt = f'> {right_stmt}'
        case FieldLookup.GTE:
            right_stmt = f'>= {right_stmt}'
        case FieldLookup.LT:
            right_stmt = f'< {right_stmt}'
        case FieldLookup.LTE:
            right_stmt = f'<= {right_stmt}'
        case FieldLookup.IN:
            right_stmt = f'IN ({right_stmt})'
        case FieldLookup.CONTAINS:
            right_stmt = f"GLOB '*{right_stmt}*'"  # type: ignore[union-attr]
        case FieldLookup.ICONTAINS:
            left_stmt = f'LOWER({left_stmt})'
            right_stmt = f"LIKE '%{right_stmt.lower()}%'"  # type: ignore[union-attr]
        case FieldLookup.STARTSWITH:
            right_stmt = f"GLOB '{right_stmt}*'"  # type: ignore[union-attr]
        case FieldLookup.ISTARTSWITH:
            left_stmt = f'LOWER({left_stmt})'
            right_stmt = f"LIKE '{right_stmt.lower()}%'"  # type: ignore[union-attr]
        case FieldLookup.ENDSWITH:
            right_stmt = f"GLOB '*{right_stmt}'"  # type: ignore[union-attr]
        case FieldLookup.IENDSWITH:
            left_stmt = f'LOWER({left_stmt})'
            right_stmt = f"LIKE '%{right_stmt.lower()}'"  # type: ignore[union-attr]
        case FieldLookup.ISNULL:
            _null_value = transform.apply(TransformTypes.NULL_VALUE)
            right_stmt = f'IS {_null_value}' if _null_value else f'IS NOT {_null_value}'  # type: ignore[union-attr]
        case FieldLookup.REGEX:
            right_stmt = f'REGEXP {right_stmt}'
        case FieldLookup.IREGEX:
            left_stmt = f'LOWER({left_stmt})'
            right_stmt = f'REGEXP {right_stmt.lower()}'
        case _:
            msg = f'{lookup} not supported'
            raise ValueError(msg)

    return f'{left_stmt} {right_stmt}', []
