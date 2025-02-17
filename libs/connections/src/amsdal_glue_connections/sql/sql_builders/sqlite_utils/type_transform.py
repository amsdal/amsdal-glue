from datetime import date
from datetime import datetime


def sqlite_value_type_transform(value_type: type) -> str:  # noqa: PLR0911
    if value_type is str:
        return 'TEXT'
    if value_type is int:
        return 'INTEGER'
    if value_type is float:
        return 'REAL'
    if value_type is bool:
        return 'BOOLEAN'
    if value_type in (dict, list):
        return 'JSONB'
    if value_type in (bytes, bytearray):
        return 'BLOB'
    if value_type == datetime:
        return 'TIMESTAMP'
    if value_type == date:
        return 'DATE'

    msg = f'Unsupported type: {value_type}'
    raise ValueError(msg)
