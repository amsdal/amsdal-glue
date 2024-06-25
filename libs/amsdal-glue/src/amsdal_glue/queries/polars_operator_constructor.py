from amsdal_glue_connections.sql.sql_builders.operator_constructor import repr_operator_constructor
from amsdal_glue_core.common.data_models.field_reference import FieldReference
from amsdal_glue_core.common.enums import FieldLookup
from amsdal_glue_core.common.expressions.value import Value


def polars_operator_constructor(
    field: str,
    lookup: FieldLookup,
    value: Value | FieldReference,
) -> str:
    _stmt, _ = repr_operator_constructor(
        field=field,
        lookup=lookup,
        value=value,
        value_placeholder='',
        field_separator='__',
        table_separator='.',
    )

    return _stmt
