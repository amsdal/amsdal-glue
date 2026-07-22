"""Coerce raw Python values to the native DB-binding type expected for a given FieldType.

Coercion happens in the Python ORM layer, **before** the value crosses the
Rust (PyO3) boundary, so the binding remains type-blind and a ``Value`` carrying
an ``output_type`` yields a param already of the intended DB type.

Rules:
- ``None`` is always returned unchanged (SQL NULL passthrough).
- ``ScalarType`` families dispatch to the appropriate Python native type.
- ``ArrayType`` recurses over element items.
- ``CustomType / NestedType / DictType / VectorType`` pass through unchanged.
"""

from __future__ import annotations

import contextlib
import uuid
from decimal import Decimal
from decimal import InvalidOperation
from typing import Any

from amsdal_glue_core.common.enums import ScalarType

_INTEGER_FAMILY: frozenset[ScalarType] = frozenset({
    ScalarType.INTEGER,
    ScalarType.SMALLINT,
    ScalarType.BIGINT,
    ScalarType.SERIAL,
    ScalarType.SMALLSERIAL,
    ScalarType.BIGSERIAL,
})

_FLOAT_FAMILY: frozenset[ScalarType] = frozenset({
    ScalarType.FLOAT,
    ScalarType.DOUBLE,
})

_DATETIME_FAMILY: frozenset[ScalarType] = frozenset({
    ScalarType.TIMESTAMP,
    ScalarType.TIMESTAMPTZ,
})


def coerce_to_field_type(value: Any, field_type: Any) -> Any:
    """Coerce *value* to the native Python type that corresponds to *field_type*.

    Args:
        value: The raw Python value from the caller.
        field_type: A ``FieldType`` (``ScalarType``, ``ArrayType``, …).

    Returns:
        The coerced value ready to be handed to the SQL-binding layer.

    Raises:
        ValueError: If *value* cannot be converted to the target type.
    """
    if value is None:
        return None

    # Inline imports to guarantee no circular-import cycle with value.py.
    from amsdal_glue_core.common.data_models.types import ArrayType
    from amsdal_glue_core.common.data_models.types import DecimalType

    if isinstance(field_type, ScalarType):
        return _coerce_scalar(value, field_type)
    if isinstance(field_type, ArrayType):
        if isinstance(value, (list, tuple)):
            return [coerce_to_field_type(item, field_type.item_type) for item in value]
        msg = f'expected a list for an array type but got {value!r}'
        raise ValueError(msg)
    if isinstance(field_type, DecimalType):
        return _coerce_decimal(value)
    # CustomType / NestedType / DictType / VectorType and anything else pass through unchanged.
    return value


def _coerce_scalar(value: Any, scalar_type: ScalarType) -> Any:  # noqa: C901, PLR0911
    # A list/tuple under a NON-JSON scalar type is an ``IN (...)`` collection: each element is a value
    # of that scalar type. Coerce per element, keeping it a list so the generator expands it into
    # ``IN (?, ?, ...)`` -- coercing the whole list would stringify it into one bad parameter. JSON/JSONB
    # are excluded: there a list is a single JSON array value, compared as a whole.
    if isinstance(value, (list, tuple)) and scalar_type not in (ScalarType.JSON, ScalarType.JSONB):
        return [_coerce_scalar(item, scalar_type) for item in value]
    if scalar_type in _INTEGER_FAMILY:
        return _coerce_int(value)
    if scalar_type in _FLOAT_FAMILY:
        return _coerce_float(value)
    if scalar_type == ScalarType.NUMERIC:
        return _coerce_decimal(value)
    if scalar_type == ScalarType.BOOLEAN:
        return _coerce_bool(value)
    if scalar_type == ScalarType.TEXT:
        return str(value)
    if scalar_type == ScalarType.UUID:
        return _coerce_uuid(value)
    if scalar_type == ScalarType.DATE:
        return _coerce_date(value)
    if scalar_type == ScalarType.TIME:
        return _coerce_time(value)
    if scalar_type in _DATETIME_FAMILY:
        return _coerce_datetime(value)
    if scalar_type == ScalarType.BYTEA:
        return _coerce_bytes(value)
    # Passthrough: JSON/JSONB (the connection/binding layer serialises these), INTERVAL,
    # TSVECTOR, TSQUERY, *RANGE types, etc.
    return value


def _coerce_int(value: Any) -> int:
    if isinstance(value, bool):
        return int(value)
    if isinstance(value, int):
        return value
    if isinstance(value, float):
        # int(inf) raises OverflowError; int(nan) raises ValueError — surface the clean message.
        try:
            int_val = int(value)
        except (ValueError, OverflowError) as exc:
            msg = f'expected an integer but got {value!r}'
            raise ValueError(msg) from exc
        if int_val == value:
            return int_val
        msg = f'expected an integer but got {value!r}'
        raise ValueError(msg)
    if isinstance(value, Decimal):
        dec_int: int | None = None
        # int(Decimal('NaN')) raises ValueError; int(Decimal('Infinity')) raises OverflowError —
        # suppress all three so a non-finite Decimal falls through to the clean message below.
        with contextlib.suppress(ValueError, OverflowError, InvalidOperation):
            dec_int = int(value)
        if dec_int is not None and Decimal(dec_int) == value:
            return dec_int
        msg = f'expected a number but got {value!r}'
        raise ValueError(msg)
    if isinstance(value, str):
        try:
            return int(value)
        except ValueError as exc:
            msg = f'expected a number but got {value!r}'
            raise ValueError(msg) from exc
    msg = f'expected a number but got {value!r}'
    raise ValueError(msg)


def _coerce_float(value: Any) -> float:
    if isinstance(value, bool):
        return float(value)
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, (str, Decimal)):
        try:
            return float(value)
        except (ValueError, InvalidOperation) as exc:
            msg = f'expected a number but got {value!r}'
            raise ValueError(msg) from exc
    msg = f'expected a number but got {value!r}'
    raise ValueError(msg)


def _coerce_decimal(value: Any) -> Decimal:
    if isinstance(value, Decimal):
        return value
    if isinstance(value, bool):
        # bool is an int subclass; int/float families already accept it (True->1), so NUMERIC does too.
        return Decimal(int(value))
    try:
        return Decimal(str(value))
    except InvalidOperation as exc:
        msg = f'expected a decimal number but got {value!r}'
        raise ValueError(msg) from exc


def _coerce_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, int):
        if value == 1:
            return True
        if value == 0:
            return False
        msg = f'expected a boolean but got {value!r}'
        raise ValueError(msg)
    if isinstance(value, str):
        low = value.lower()
        if low in ('true', '1'):
            return True
        if low in ('false', '0'):
            return False
        msg = f'expected a boolean but got {value!r}'
        raise ValueError(msg)
    msg = f'expected a boolean but got {value!r}'
    raise ValueError(msg)


def _coerce_uuid(value: Any) -> uuid.UUID:
    if isinstance(value, uuid.UUID):
        return value
    try:
        return uuid.UUID(str(value))
    except (ValueError, AttributeError) as exc:
        msg = f'expected a UUID but got {value!r}'
        raise ValueError(msg) from exc


def _coerce_date(value: Any) -> Any:
    import datetime

    if isinstance(value, datetime.datetime):
        return value.date()
    if isinstance(value, datetime.date):
        return value
    if isinstance(value, str):
        try:
            return datetime.date.fromisoformat(value)
        except ValueError as exc:
            msg = f'expected a date but got {value!r}'
            raise ValueError(msg) from exc
    msg = f'expected a date but got {value!r}'
    raise ValueError(msg)


def _coerce_time(value: Any) -> Any:
    import datetime

    if isinstance(value, datetime.time):
        return value
    if isinstance(value, str):
        try:
            return datetime.time.fromisoformat(value)
        except ValueError as exc:
            msg = f'expected a time but got {value!r}'
            raise ValueError(msg) from exc
    msg = f'expected a time but got {value!r}'
    raise ValueError(msg)


def _coerce_datetime(value: Any) -> Any:
    import datetime

    if isinstance(value, datetime.datetime):
        return value
    if isinstance(value, datetime.date):
        return datetime.datetime(value.year, value.month, value.day)  # noqa: DTZ001
    if isinstance(value, str):
        try:
            return datetime.datetime.fromisoformat(value)
        except ValueError as exc:
            msg = f'expected a datetime but got {value!r}'
            raise ValueError(msg) from exc
    msg = f'expected a datetime but got {value!r}'
    raise ValueError(msg)


def _coerce_bytes(value: Any) -> bytes:
    if isinstance(value, (bytes, bytearray, memoryview)):
        return bytes(value)
    if isinstance(value, str):
        return value.encode()
    msg = f'expected bytes but got {value!r}'
    raise ValueError(msg)
