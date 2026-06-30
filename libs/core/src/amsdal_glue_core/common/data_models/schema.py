from __future__ import annotations

from copy import copy
from dataclasses import dataclass
from typing import Any
from typing import TYPE_CHECKING

from amsdal_glue_core.common.enums import Version

if TYPE_CHECKING:
    from amsdal_glue_core.common.data_models.constraints import BaseConstraint
    from amsdal_glue_core.common.data_models.indexes import IndexSchema
    from amsdal_glue_core.common.data_models.types import FieldType
    from amsdal_glue_core.common.expressions.expression import Expression


_IDENTITY_DEFAULTS: dict[str, set[int]] = {
    'start': {1},
    'increment': {1},
    'min_value': {1},
    'max_value': {2147483647, 9223372036854775807},  # int4, int8
    'cache': {1},
}


@dataclass(kw_only=True)
class IdentityConfig:
    """SQL standard GENERATED { ALWAYS | BY DEFAULT } AS IDENTITY configuration."""

    always: bool = False
    start: int | None = None
    increment: int | None = None
    min_value: int | None = None
    max_value: int | None = None
    cycle: bool = False
    cache: int | None = None

    def __eq__(self, other: object) -> bool:  # noqa: PLR0911, C901
        if other is True:
            return self == IdentityConfig(always=False)
        if not isinstance(other, IdentityConfig):
            return NotImplemented
        if self.always != other.always:
            return False
        if self.cycle != other.cycle:
            return False
        for field in ('start', 'increment', 'min_value', 'max_value', 'cache'):
            left = getattr(self, field)
            right = getattr(other, field)
            if left is None and right is None:
                continue
            if left is None:
                if right not in _IDENTITY_DEFAULTS.get(field, set()):
                    return False
            elif right is None:
                if left not in _IDENTITY_DEFAULTS.get(field, set()):
                    return False
            elif left != right:
                return False
        return True

    def __hash__(self) -> int:
        return hash((self.always, self.start, self.increment, self.min_value, self.max_value, self.cycle, self.cache))


@dataclass(kw_only=True)
class Schema:
    name: str
    version: str | Version = Version.LATEST
    namespace: str | None = None
    properties: list[PropertySchema]
    constraints: list[BaseConstraint] | None = None
    indexes: list[IndexSchema] | None = None
    metadata: dict[str, Any] | None = None

    def __hash__(self):
        return hash(repr(self))

    def __repr__(self):
        return (
            f'Schema<{self.namespace}.{self.name}_v_{self.version}:{self.properties}:{self.constraints}:{self.indexes}>'
        )

    def __copy__(self):
        return Schema(
            name=self.name,
            version=self.version,
            namespace=self.namespace,
            properties=[copy(prop) for prop in self.properties],
            constraints=[copy(constraint) for constraint in self.constraints] if self.constraints is not None else None,
            indexes=[copy(index) for index in self.indexes] if self.indexes is not None else None,
            metadata=self.metadata.copy() if self.metadata is not None else None,
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Schema):
            return False

        return (
            self.name == other.name
            and self.version == other.version
            and self.namespace == other.namespace
            and sorted(self.properties, key=lambda p: p.name) == sorted(other.properties, key=lambda p: p.name)
            and (
                sorted(self.constraints or [], key=lambda c: c.name)
                == sorted(other.constraints or [], key=lambda c: c.name)
            )
            and sorted(self.indexes or [], key=lambda i: i.name) == sorted(other.indexes or [], key=lambda i: i.name)
        )


def _normalize_identity(value: bool | IdentityConfig | None) -> IdentityConfig | None:  # noqa: FBT001
    """Normalize identity to IdentityConfig or None for comparison."""
    if value is True:
        return IdentityConfig(always=False)
    if value is False or value is None:
        return None
    return value


@dataclass(kw_only=True)
class PropertySchema:
    name: str
    type: FieldType
    required: bool
    description: str | None = None
    default: Expression | None = None
    generated: Expression | None = None
    db_collation: str | None = None
    identity: bool | IdentityConfig | None = None

    def __ne__(self, other):
        return not self.__eq__(other)

    def __eq__(self, other):
        if not isinstance(other, PropertySchema):
            return False

        return (
            self.name == other.name
            and self.type == other.type
            and self.required == other.required
            and _normalize_identity(self.identity) == _normalize_identity(other.identity)
            and self.default == other.default
            and self.generated == other.generated
            and self.db_collation == other.db_collation
        )

    def __repr__(self):
        return f'PropertySchema<{self.name}:{self.type}:{self.required}:{self.description}:{self.default}>'

    def __copy__(self):
        return PropertySchema(
            name=self.name,
            type=copy(self.type),
            required=self.required,
            description=self.description,
            default=self.default,
            generated=self.generated,
            db_collation=self.db_collation,
            identity=self.identity,
        )

    def __hash__(self) -> int:
        return hash((self.name, self.required))


@dataclass(kw_only=True)
class SchemaReference:
    name: str
    version: str | Version = Version.LATEST
    alias: str | None = None
    namespace: str | None = None
    metadata: dict[str, Any] | None = None

    def __copy__(self):
        return SchemaReference(
            name=self.name,
            version=self.version,
            alias=self.alias,
            namespace=self.namespace,
            metadata=self.metadata,
        )

    def __repr__(self):
        return f'SchemaReference<{self.namespace}.{self.name}__v__{self.version}:{self.alias}>'
