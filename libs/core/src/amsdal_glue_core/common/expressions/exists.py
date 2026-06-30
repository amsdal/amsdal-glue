from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from amsdal_glue_core.common.expressions.expression import Expression

if TYPE_CHECKING:
    from amsdal_glue_core.common.data_models.sub_query import SubQueryStatement


@dataclass(kw_only=True)
class Exists(Expression):
    subquery: SubQueryStatement
    negated: bool = False
