from typing import Any

from amsdal_glue_core.common.data_models.output_type import OutputType

from amsdal_glue_connections.sql.sql_builders.transform import Transform
from amsdal_glue_connections.sql.sql_builders.transform import TransformTypes


def sqlite_value_placeholder_transform(
    value: Any,
    transform: Transform,
    output_type: type | OutputType | None = None,
) -> str:
    placeholder = '?'

    if isinstance(value, dict | list):
        return f'json({placeholder})'

    if output_type is not None:
        placeholder = transform.apply(TransformTypes.CAST, placeholder, output_type)
    return placeholder
