from amsdal_glue_core.common.enums import FieldLookup
from amsdal_glue_core.common.expressions.expression import Expression


def polars_operator_constructor(  # noqa: C901, PLR0912
    left: Expression,
    lookup: FieldLookup,
    right: Expression,
) -> str:
    """
    Constructs a Polars SQL operator fragment for use with ``pl.SQLContext``.

    The result is a SQL string such as ``table.field = 'value'`` that is embedded
    directly in a Polars in-memory SQL query.  Only the lookups supported by
    Polars SQL are handled; unsupported lookups raise ``NotImplementedError``.

    Args:
        left (Expression): The left-hand expression (usually a field reference).
        lookup (FieldLookup): The comparison operator / lookup type.
        right (Expression): The right-hand expression (usually a value).

    Returns:
        str: The constructed SQL condition fragment.
    """
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
            right_stmt = f"GLOB '*{right_stmt}*'"
        case FieldLookup.ICONTAINS:
            left_stmt = f'LOWER({left_stmt})'
            right_stmt = f"LIKE '%{right_stmt.lower()}%'"
        case FieldLookup.STARTSWITH:
            right_stmt = f"GLOB '{right_stmt}*'"
        case FieldLookup.ISTARTSWITH:
            left_stmt = f'LOWER({left_stmt})'
            right_stmt = f"LIKE '{right_stmt.lower()}%'"
        case FieldLookup.ENDSWITH:
            right_stmt = f"GLOB '*{right_stmt}'"
        case FieldLookup.IENDSWITH:
            left_stmt = f'LOWER({left_stmt})'
            right_stmt = f"LIKE '%{right_stmt.lower()}'"
        case FieldLookup.ISNULL:
            right_stmt = 'IS NULL'
        case FieldLookup.REGEX:
            right_stmt = f'REGEXP {right_stmt}'
        case FieldLookup.IREGEX:
            left_stmt = f'LOWER({left_stmt})'
            right_stmt = f'REGEXP {right_stmt.lower()}'
        case _:
            msg = f'{lookup} is not supported in the cross-database Polars executor'
            raise NotImplementedError(msg)

    return f'{left_stmt} {right_stmt}'
