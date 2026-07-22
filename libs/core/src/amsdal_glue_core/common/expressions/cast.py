from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from amsdal_glue_core.common.expressions.expression import Expression

if TYPE_CHECKING:
    from amsdal_glue_core.common.data_models.types import FieldType


@dataclass(kw_only=True)
class Cast(Expression):
    expression: Expression
    to_type: FieldType
