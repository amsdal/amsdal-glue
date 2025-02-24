import json
from typing import Any


def sqlite_value_transform(value: Any) -> Any:
    if isinstance(value, dict | list):
        return json.dumps(value)

    return value
