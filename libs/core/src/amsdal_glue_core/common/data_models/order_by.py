from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from amsdal_glue_core.common.enums import OrderDirection

if TYPE_CHECKING:
    from amsdal_glue_core.common.data_models.field_reference import FieldReference
    from amsdal_glue_core.common.expressions.expression import Expression


@dataclass(kw_only=True)
class OrderByQuery:
    """Represents an ORDER BY query.

    Attributes:
        field (FieldReference): The field to order by.
        direction (OrderDirection): The direction of the order (ASC/DESC). Defaults to OrderDirection.ASC.
        expression (Expression | None): Optional expression to order by instead of field.
    """

    field: FieldReference
    direction: OrderDirection = OrderDirection.ASC
    expression: Expression | None = None
