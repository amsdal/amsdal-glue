from amsdal_glue_connections.sql.sql_builders.operator_constructor import repr_operator_constructor
from amsdal_glue_core.common.data_models.field_reference import FieldReference
from amsdal_glue_core.common.enums import FieldLookup
from amsdal_glue_core.common.expressions.value import Value


def polars_operator_constructor(
    field: str,
    lookup: FieldLookup,
    value: Value | FieldReference,
) -> str:
    """
    Constructs a Polars operator statement based on the given field, lookup, and value.

    Args:
        field (str): The field to be used in the operator.
        lookup (FieldLookup): The lookup type for the field.
        value (Value | FieldReference): The value or field reference to be used in the operator.

    Returns:
        str: The constructed Polars operator statement.
    """
    _stmt, _ = repr_operator_constructor(
        field=field,
        lookup=lookup,
        value=value,
        value_placeholder='',
        table_separator='.',
    )

    return _stmt
