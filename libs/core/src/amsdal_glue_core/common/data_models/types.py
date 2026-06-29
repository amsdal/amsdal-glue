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


FieldType = ScalarType | CustomType | ArrayType | NestedType | DictType | VectorType
