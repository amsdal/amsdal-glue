from typing import Union

from amsdal_glue_core.common.data_models.conditions import Condition as CoreCondition
from amsdal_glue_core.common.data_models.conditions import Conditions as CoreConditions
from amsdal_glue_core.common.enums import FieldLookup
from amsdal_glue_core.common.enums import FilterConnector
from amsdal_glue_core.common.expressions.field_reference import FieldReferenceExpression
from amsdal_glue_core.common.expressions.value import Value
from pydantic import BaseModel


class Condition(BaseModel):
    left: FieldReferenceExpression | Value
    lookup: FieldLookup
    right: FieldReferenceExpression | Value
    negate: bool = False


class Conditions(BaseModel):
    children: list[Union[Condition, 'Conditions']]

    connector: FilterConnector = FilterConnector.AND
    negated: bool = False


def condition_to_core_condition(condition: Condition) -> CoreCondition:
    return CoreCondition(
        left=condition.left,
        lookup=condition.lookup,
        right=condition.right,
        negate=condition.negate,
    )


def conditions_to_core_conditions(conditions: Conditions | None) -> CoreConditions | None:
    if conditions is None:
        return None

    return conditions_to_core_conditions_required(conditions)


def conditions_to_core_conditions_required(conditions: Conditions) -> CoreConditions:
    return CoreConditions(
        *[_process_condition(c) for c in conditions.children],
        connector=conditions.connector,
        negated=conditions.negated,
    )


def _process_condition(condition: Condition | Conditions) -> CoreCondition | CoreConditions:
    if isinstance(condition, Condition):
        return condition_to_core_condition(condition)
    return conditions_to_core_conditions_required(condition)
