from dataclasses import dataclass

from amsdal_glue_core.common.data_models.field_reference import FieldReference
from amsdal_glue_core.common.enums import OrderDirection


@dataclass(kw_only=True)
class OrderByQuery:
    """Represents an ORDER BY query.

    Attributes:
        field (FieldReference): The field to order by.
        direction (OrderDirection): The direction of the order (ASC/DESC). Defaults to OrderDirection.ASC.
    """

    field: FieldReference
    direction: OrderDirection = OrderDirection.ASC
