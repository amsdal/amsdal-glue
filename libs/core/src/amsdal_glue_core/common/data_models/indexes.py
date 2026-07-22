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
    name: str
    params: dict[str, Any] | None = None


IndexType: TypeAlias = BuiltinIndexType | CustomIndexType


@dataclass(kw_only=True)
class IndexField:
    name: str
    direction: OrderDirection = OrderDirection.ASC
    op_class: str | None = None


@dataclass(kw_only=True)
class IndexSchema:
    name: str
    fields: list[IndexField]
    unique: bool = False
    index_type: IndexType = BuiltinIndexType.BTREE
    include: list[str] | None = None
    condition: Conditions | None = None
    parameters: dict[str, str] | None = None

    def __ne__(self, other):
        return not self.__eq__(other)

    def __eq__(self, other):
        if not isinstance(other, IndexSchema):
            return False

        return (
            self.name == other.name
            and self.fields == other.fields
            and self.unique == other.unique
            and self.index_type == other.index_type
            and self.condition == other.condition
            and self.parameters == other.parameters
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
        return hash((self.name, tuple(self.fields) if self.fields else None, self.condition))
