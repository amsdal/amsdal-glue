from typing import Any

from amsdal_glue_core.common.data_models.vector import Vector


def pg_value_transform(value: Any, value_type: type | None = None) -> Any:
    from psycopg.types.json import Json
    from psycopg.types.json import Jsonb

    if value_type is None:
        value_type = type(value)

    if value_type in (dict, list):
        return Jsonb(value)

    if value_type is str and value.startswith('"') and value.endswith('"'):
        return Json(value[1:-1])

    if isinstance(value, Vector) or value_type in (Vector,):
        return str(value)

    return value
