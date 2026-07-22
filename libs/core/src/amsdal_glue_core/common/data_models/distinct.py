from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from amsdal_glue_core.common.data_models.field_reference import FieldReference


@dataclass(kw_only=True)
class DistinctClause:
    on_fields: list[FieldReference] | None = None
