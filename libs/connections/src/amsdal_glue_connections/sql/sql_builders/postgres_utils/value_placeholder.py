from typing import Any

from amsdal_glue_core.common.data_models.output_type import OutputType

from amsdal_glue_connections.sql.sql_builders.transform import Transform
from amsdal_glue_connections.sql.sql_builders.transform import TransformTypes


def pg_value_placeholder_transform(
    value: Any,  # noqa: ARG001
    transform: Transform,
    output_type: type | OutputType | None = None,
) -> str:
    placeholder = '%s'

    if output_type is not None:
        placeholder = transform.apply(TransformTypes.CAST, placeholder, output_type)
    return placeholder
