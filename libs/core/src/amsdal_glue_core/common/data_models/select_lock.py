from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from amsdal_glue_core.common.enums import LockStrength

if TYPE_CHECKING:
    from amsdal_glue_core.common.data_models.schema import SchemaReference


@dataclass(kw_only=True)
class SelectLock:
    strength: LockStrength = LockStrength.UPDATE
    of: list[SchemaReference] | None = None
    nowait: bool = False
    skip_locked: bool = False
