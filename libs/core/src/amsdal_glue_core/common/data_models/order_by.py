from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from amsdal_glue_core.common.enums import OrderDirection

if TYPE_CHECKING:
    from amsdal_glue_core.common.expressions.expression import Expression


@dataclass(kw_only=True)
class OrderByQuery:
    """Represents an ORDER BY query.

    Expression-only, symmetric with :class:`GroupByQuery`. To order by a plain
    field, wrap it in a ``FieldReferenceExpression``.

    Attributes:
        expression (Expression): The expression to order by.
        direction (OrderDirection): The direction of the order (ASC/DESC). Defaults to OrderDirection.ASC.
    """

    expression: Expression
    direction: OrderDirection = OrderDirection.ASC
