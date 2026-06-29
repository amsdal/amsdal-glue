from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar
from typing import TYPE_CHECKING

from amsdal_glue_core.common.expressions.expression import Expression

if TYPE_CHECKING:
    from amsdal_glue_core.common.data_models.conditions import Conditions
    from amsdal_glue_core.common.data_models.order_by import OrderByQuery


@dataclass(kw_only=True)
class Aggregation(Expression):
    name: ClassVar[str]
    expression: Expression | None = None
    distinct: bool = False
    filter: Conditions | None = None
    args: list[Expression] | None = None
    order_by: list[OrderByQuery] | None = None


@dataclass(kw_only=True)
class Sum(Aggregation):
    name: ClassVar[str] = 'SUM'


@dataclass(kw_only=True)
class Count(Aggregation):
    name: ClassVar[str] = 'COUNT'


@dataclass(kw_only=True)
class Avg(Aggregation):
    name: ClassVar[str] = 'AVG'


@dataclass(kw_only=True)
class Min(Aggregation):
    name: ClassVar[str] = 'MIN'


@dataclass(kw_only=True)
class Max(Aggregation):
    name: ClassVar[str] = 'MAX'


# Backward-compat alias — old code imported AggregationExpression from this module.
AggregationExpression = Aggregation
