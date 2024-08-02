from typing import Union

from amsdal_glue_core.common.data_models.conditions import Condition
from amsdal_glue_core.common.data_models.conditions import Conditions as CoreConditions
from amsdal_glue_core.common.enums import FilterConnector
from pydantic import BaseModel


class Conditions(BaseModel):
    children: list[Union[Condition, 'Conditions']]

    connector: FilterConnector = FilterConnector.AND
    negated: bool = False


def conditions_to_core_conditions(conditions: Conditions | None) -> CoreConditions | None:
    if conditions is None:
        return None

    return conditions_to_core_conditions_required(conditions)


def conditions_to_core_conditions_required(conditions: Conditions) -> CoreConditions:
    return CoreConditions(
        *conditions.children,
        connector=conditions.connector,
        negated=conditions.negated,
    )
