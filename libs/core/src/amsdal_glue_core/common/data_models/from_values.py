from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from amsdal_glue_core.common.expressions.expression import Expression


@dataclass(kw_only=True)
class FromValues:
    """VALUES as table source: (VALUES (1,'a'), (2,'b')) AS t(id, name)."""

    rows: list[list[Expression]]
    alias: str
    columns: list[str]
