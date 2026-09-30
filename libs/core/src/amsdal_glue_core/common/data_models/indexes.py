from __future__ import annotations

from copy import copy
from dataclasses import dataclass
from dataclasses import field
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
    # Tuning options (e.g. pgvector's `m` / `ef_construction`, `lists`) belong on
    # `IndexSchema.parameters`, which is what the extractor actually reads and renders as `WITH
    # (...)`. This field is dead weight kept only for backwards compatibility; it is excluded from
    # equality/hash/repr so a declaration that happens to set it still equals its introspection
    # (which never populates it).
    params: dict[str, Any] | None = field(default=None, compare=False, repr=False)

    def __post_init__(self) -> None:
        # Catalog access-method names (`pg_am.amname`) always come back lowercase, so casefold here
        # too: a declaration of `CustomIndexType(name='HNSW')` must still equal its introspection.
        self.name = self.name.lower()


IndexType: TypeAlias = BuiltinIndexType | CustomIndexType


@dataclass(kw_only=True)
class IndexField:
    name: str
    direction: OrderDirection = OrderDirection.ASC
    op_class: str | None = None
    # Introspection-only: the operator class Postgres would pick by default for this column's type
    # and access method. A declared `op_class` is nulled on read-back when it matches the default
    # (see `TABLE_INDEX_REGISTRY`), so this is what lets `IndexSchema._fields_equal` resolve that
    # flap. Excluded from equality/hash/repr so it never affects raw `IndexField` comparisons.
    default_op_class: str | None = field(default=None, compare=False, repr=False)


def _index_type_supports_ordering(index_type: IndexType) -> bool:
    """Only ``btree`` honours per-column ``ASC``/``DESC``; every other access method always reports ascending."""
    return index_type == BuiltinIndexType.BTREE


def _op_class_equal(own: IndexField, other: IndexField) -> bool:
    """Compare two fields' `op_class`, resolving the default-opclass introspection flap.

    A declared `op_class` that happens to name the access method's default operator class reads
    back as `None` (see `TABLE_INDEX_REGISTRY`'s `opc.opcdefault` check), so a direct `==` would
    never match. `default_op_class` -- populated only by introspection -- carries what the nulled
    side's default actually is, so it is cross-checked against the other side's explicit value.
    """
    if own.op_class == other.op_class:
        return True
    if own.op_class is None and other.op_class is not None:
        return own.default_op_class == other.op_class
    if other.op_class is None and own.op_class is not None:
        return other.default_op_class == own.op_class
    return False


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

    def _fields_equal(self, other_fields: list[IndexField] | None) -> bool:
        """Compare fields, ignoring `direction` when this index's access method doesn't support ordering.

        `fields=None` is tolerated (treated as empty) on either side, matching `IndexSchema`'s
        general None-safe equality semantics -- nothing in-repo constructs it this way, but callers
        outside the repo may.
        """
        own_fields = self.fields or []
        other_fields = other_fields or []

        if len(own_fields) != len(other_fields):
            return False

        ordering_matters = _index_type_supports_ordering(self.index_type)

        # `strict=False`: the length check above already guarantees equal length, so `zip`'s own
        # strictness would be unreachable dead code here.
        return all(
            own.name == other.name
            and _op_class_equal(own, other)
            and (not ordering_matters or own.direction == other.direction)
            for own, other in zip(own_fields, other_fields, strict=False)
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
        # `fields=None`/empty both collapse to `None`, mirroring `_fields_equal`'s None-safe handling.
        ordering_matters = _index_type_supports_ordering(self.index_type)
        fields_key = (
            tuple(
                (own.name, own.direction, own.op_class) if ordering_matters else (own.name, own.op_class)
                for own in self.fields
            )
            if self.fields
            else None
        )
        include_key = tuple(self.include) if self.include else None
        return hash((self.name, fields_key, include_key, self.condition))
