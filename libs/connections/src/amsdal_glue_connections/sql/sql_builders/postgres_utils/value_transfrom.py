from typing import Any


def pg_value_transform(value: Any, value_type: type | None = None) -> Any:
    from psycopg.types.json import Json
    from psycopg.types.json import Jsonb

    if value_type is None:
        value_type = type(value)

    if value_type in (dict, list):
        return Jsonb(value)

    if value_type is str and value.startswith('"') and value.endswith('"'):
        return Json(value[1:-1])

    return value
