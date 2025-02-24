from amsdal_glue_connections.sql.sql_builders.operator_constructor import repr_operator_constructor
from amsdal_glue_connections.sql.sql_builders.transform import Transform
from amsdal_glue_core.common.enums import FieldLookup
from amsdal_glue_core.common.expressions.expression import Expression


def polars_operator_constructor(
    left: Expression,
    lookup: FieldLookup,
    right: Expression,
    transform: Transform,
) -> str:
    """
    Constructs a Polars operator statement based on the given field, lookup, and value.

    Args:
        field (Expression): The field to be used in the operator.
        lookup (FieldLookup): The lookup type for the field.
        value (Expression): The value or field reference to be used in the operator.

    Returns:
        str: The constructed Polars operator statement.
    """
    _stmt, _ = repr_operator_constructor(
        left=left,
        lookup=lookup,
        right=right,
        transform=transform,
    )

    return _stmt
