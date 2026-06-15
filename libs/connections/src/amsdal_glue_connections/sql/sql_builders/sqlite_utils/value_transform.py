import json
from decimal import Decimal
from typing import Any


def sqlite_value_transform(value: Any) -> Any:
    if isinstance(value, dict | list):
        return json.dumps(value)

    if isinstance(value, Decimal):
        return str(value)

    return value
