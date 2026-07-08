from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from amsdal_glue_core.common.enums import ScalarType


@dataclass(kw_only=True)
class CustomType:
    name: str
    params: dict[str, Any] | None = None


@dataclass(kw_only=True)
class ArrayType:
    item_type: FieldType


@dataclass(kw_only=True)
class NestedType:
    properties: dict[str, FieldType]


@dataclass(kw_only=True)
class DictType:
    key_type: ScalarType
    value_type: FieldType


@dataclass(kw_only=True)
class VectorType:
    dimensions: int


@dataclass(kw_only=True)
class DecimalType:
    """Dialect-agnostic fixed-point decimal.

    Renders ``NUMERIC(precision, scale)`` on PostgreSQL and a TEXT-affinity
    ``DECIMAL_TEXT(precision, scale)`` on SQLite (so decimal strings are stored
    without the float coercion that ``NUMERIC`` affinity would cause). ``scale``
    without ``precision`` is invalid and rejected at render time.
    """

    precision: int | None = None
    scale: int | None = None


FieldType = ScalarType | CustomType | ArrayType | NestedType | DictType | VectorType | DecimalType
