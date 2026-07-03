from typing import Union

import amsdal_glue_core.common.data_models.distinct as _distinct_mod
import amsdal_glue_core.common.data_models.order_by as _order_by_mod
import amsdal_glue_core.common.expressions.aggregation as _aggregation_mod
import amsdal_glue_core.common.expressions.base as _base_mod
import amsdal_glue_core.common.expressions.value as _value_mod
from amsdal_glue_core.common.data_models.conditions import Condition as CoreCondition
from amsdal_glue_core.common.data_models.conditions import Conditions as CoreConditions
from amsdal_glue_core.common.data_models.field_reference import FieldReference as _FieldReference
from amsdal_glue_core.common.data_models.order_by import OrderByQuery as _OrderByQuery
from amsdal_glue_core.common.data_models.types import FieldType as _FieldType
from amsdal_glue_core.common.enums import FieldLookup
from amsdal_glue_core.common.enums import FilterConnector
from amsdal_glue_core.common.expressions.expression import Expression as _Expression
from amsdal_glue_core.common.expressions.field_reference import FieldReferenceExpression
from amsdal_glue_core.common.expressions.value import Value
from pydantic import BaseModel
from pydantic import ConfigDict


class Condition(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    left: FieldReferenceExpression | Value
    lookup: FieldLookup
    right: FieldReferenceExpression | Value
    negate: bool = False


class Conditions(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

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


def _ensure_type_hints_resolvable() -> None:
    """Patch TYPE_CHECKING-only symbols into core modules so pydantic can evaluate annotations via get_type_hints."""
    _base_mod.__dict__.setdefault('FieldType', _FieldType)
    _value_mod.__dict__.setdefault('FieldType', _FieldType)
    _distinct_mod.__dict__.setdefault('FieldReference', _FieldReference)
    _order_by_mod.__dict__.setdefault('FieldReference', _FieldReference)
    _order_by_mod.__dict__.setdefault('Expression', _Expression)
    _aggregation_mod.__dict__.setdefault('Conditions', CoreConditions)
    _aggregation_mod.__dict__.setdefault('OrderByQuery', _OrderByQuery)


_ensure_type_hints_resolvable()
Conditions.model_rebuild()
