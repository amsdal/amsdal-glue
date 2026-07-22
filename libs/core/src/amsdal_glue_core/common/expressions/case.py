from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from amsdal_glue_core.common.expressions.expression import Expression

if TYPE_CHECKING:
    from amsdal_glue_core.common.data_models.conditions import Conditions


@dataclass(kw_only=True)
class WhenClause:
    condition: Conditions
    result: Expression


@dataclass(kw_only=True)
class Case(Expression):
    cases: list[WhenClause]
    default: Expression | None = None
