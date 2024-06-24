from dataclasses import dataclass

from amsdal_glue_core.common.data_models.field_reference import FieldReference
from amsdal_glue_core.common.enums import OrderDirection


@dataclass(kw_only=True)
class OrderByQuery:
    field: FieldReference
    direction: OrderDirection = OrderDirection.ASC
