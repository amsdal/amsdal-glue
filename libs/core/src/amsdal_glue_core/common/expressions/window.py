from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from amsdal_glue_core.common.enums import WindowFrameType
from amsdal_glue_core.common.expressions.expression import Expression

if TYPE_CHECKING:
    from amsdal_glue_core.common.data_models.order_by import OrderByQuery


@dataclass(kw_only=True)
class WindowFrame:
    frame_type: WindowFrameType = WindowFrameType.RANGE
    start: int | None = None
    end: int | None = None


@dataclass(kw_only=True)
class Window(Expression):
    expression: Expression
    partition_by: list[Expression] | None = None
    order_by: list[OrderByQuery] | None = None
    frame: WindowFrame | None = None
