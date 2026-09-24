from __future__ import annotations

from copy import copy
from dataclasses import dataclass
from typing import Any
from typing import TYPE_CHECKING
from typing import TypeAlias

from amsdal_glue_core.common.enums import BuiltinIndexType
from amsdal_glue_core.common.enums import OrderDirection

if TYPE_CHECKING:
    from amsdal_glue_core.common.data_models.conditions import Conditions


@dataclass(kw_only=True)
class CustomIndexType:
    """An access method not covered by :class:`BuiltinIndexType`, e.g. pgvector's ``hnsw`` / ``ivfflat``."""

    name: str
    params: dict[str, Any] | None = None


IndexType: TypeAlias = BuiltinIndexType | CustomIndexType


@dataclass(kw_only=True)
class IndexField:
    name: str
    direction: OrderDirection = OrderDirection.ASC
    op_class: str | None = None


def _index_type_supports_ordering(index_type: IndexType) -> bool:
    """Only ``btree`` honours per-column ``ASC``/``DESC``; every other access method always reports ascending."""
    return index_type == BuiltinIndexType.BTREE


@dataclass(kw_only=True)
class IndexSchema:
    name: str
    fields: list[IndexField]
    unique: bool = False
    index_type: IndexType = BuiltinIndexType.BTREE
    include: list[str] | None = None
    condition: Conditions | None = None
    # Per-access-method tuning options, rendered as `WITH (...)`, e.g. pgvector's `m` /
    # `ef_construction` (hnsw) or `lists` (ivfflat). Not enforced by glue; see pgvector's docs for
    # limits (e.g. hnsw's 2000-dimension cap, ivfflat's `lists` needing to scale with row count).
    parameters: dict[str, str] | None = None

    def __ne__(self, other):
        return not self.__eq__(other)

    def __eq__(self, other):
        if not isinstance(other, IndexSchema):
            return False

        return (
            self.name == other.name
            and self.unique == other.unique
            and self.index_type == other.index_type
            and self.include == other.include
            and self.condition == other.condition
            and self.parameters == other.parameters
            and self._fields_equal(other.fields)
        )

    def _fields_equal(self, other_fields: list[IndexField]) -> bool:
        """Compare fields, ignoring `direction` when this index's access method doesn't support ordering."""
        if len(self.fields) != len(other_fields):
            return False

        ordering_matters = _index_type_supports_ordering(self.index_type)

        return all(
            own.name == other.name
            and own.op_class == other.op_class
            and (not ordering_matters or own.direction == other.direction)
            for own, other in zip(self.fields, other_fields, strict=True)
        )

    def __repr__(self):
        return f'IndexSchema<{self.name}:{self.fields}:{self.condition}>'

    def __copy__(self):
        return IndexSchema(
            name=self.name,
            fields=copy(self.fields),
            unique=self.unique,
            index_type=self.index_type,
            include=copy(self.include) if self.include is not None else None,
            condition=copy(self.condition) if self.condition is not None else None,
            parameters=copy(self.parameters) if self.parameters is not None else None,
        )

    def __hash__(self) -> int:
        # Must hash the same fields `_fields_equal` treats as significant, so equal schemas hash equal.
        ordering_matters = _index_type_supports_ordering(self.index_type)
        fields_key = tuple(
            (field.name, field.direction, field.op_class) if ordering_matters else (field.name, field.op_class)
            for field in self.fields
        )
        include_key = tuple(self.include) if self.include else None
        return hash((self.name, fields_key, include_key, self.condition))
