from __future__ import annotations

import copy
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from amsdal_glue_core.common.data_models.types import FieldType


@dataclass(kw_only=True)
class BaseExpression:
    output_type: FieldType | None = None

    def copy(self) -> BaseExpression:
        return copy.copy(self)
