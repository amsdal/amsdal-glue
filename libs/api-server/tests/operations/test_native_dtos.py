# mypy: disable-error-code="type-abstract"
"""Native-pydantic DTO regression and behaviour tests.

These lock in the redesign that removed the ``_ensure_type_hints_resolvable``
monkey-patch: the request DTOs must build their JSON schema natively (without
mutating any ``amsdal_glue_core`` module) and the recursive ``ExpressionBody``
discriminated union must route each wire shape to the right arm.
"""

from typing import Any

import amsdal_glue_core.common.data_models.distinct as _distinct_mod
import amsdal_glue_core.common.data_models.order_by as _order_by_mod
import amsdal_glue_core.common.expressions.base as _base_mod
import amsdal_glue_core.common.expressions.value as _value_mod
import pytest
from amsdal_glue_core.common.data_models.conditions import Condition as CoreCondition
from amsdal_glue_core.common.data_models.query import QueryStatement
from amsdal_glue_core.common.expressions.aggregation import Sum
from amsdal_glue_core.common.expressions.field_reference import FieldReferenceExpression
from amsdal_glue_core.common.expressions.value import Value
from pydantic import TypeAdapter
from pydantic import ValidationError

from amsdal_glue_api_server.controllers.operations.models import Condition
from amsdal_glue_api_server.controllers.operations.models import condition_to_core_condition
from amsdal_glue_api_server.controllers.operations.models import Conditions
from amsdal_glue_api_server.controllers.operations.models import expression_body_to_core
from amsdal_glue_api_server.controllers.operations.models import ExpressionBody
from amsdal_glue_api_server.controllers.operations.models import FieldRefBody
from amsdal_glue_api_server.controllers.operations.models import query_statement_to_core_query_statement
from amsdal_glue_api_server.controllers.operations.models import QueryStatementBody
from amsdal_glue_api_server.controllers.operations.models import SumBody
from amsdal_glue_api_server.controllers.operations.models import ValueBody

_EXPRESSION_ADAPTER: TypeAdapter[Any] = TypeAdapter(ExpressionBody)


# --- Regression: schema builds natively, core modules stay untouched ---------


def test_condition_json_schema_builds_without_patch() -> None:
    schema = Condition.model_json_schema()
    assert isinstance(schema, dict)
    # Condition is referenced recursively (via Conditions) so it lands under $defs.
    assert 'lookup' in schema['$defs']['Condition']['properties']


def test_conditions_json_schema_builds_without_patch() -> None:
    schema = Conditions.model_json_schema()
    assert isinstance(schema, dict)
    assert 'children' in schema['$defs']['Conditions']['properties']


def test_query_statement_json_schema_builds_without_patch() -> None:
    schema = QueryStatementBody.model_json_schema()
    assert isinstance(schema, dict)


def test_core_modules_are_not_monkey_patched() -> None:
    # The removed crutch used to inject these TYPE_CHECKING-only names into the
    # core modules' __dict__; a native design must not mutate core at all.
    assert 'FieldType' not in vars(_base_mod)
    assert 'FieldType' not in vars(_value_mod)
    assert 'FieldReference' not in vars(_distinct_mod)
    assert 'FieldReference' not in vars(_order_by_mod)
    assert 'Expression' not in vars(_order_by_mod)


# --- Discriminator: structure -> arm, tag-free wire --------------------------


def test_value_shape_routes_to_value_arm() -> None:
    parsed = _EXPRESSION_ADAPTER.validate_python({'value': 1})
    assert isinstance(parsed, ValueBody)
    core = expression_body_to_core(parsed)
    assert isinstance(core, Value)
    assert core.value == 1


def test_value_shape_with_output_type_coerces() -> None:
    parsed = _EXPRESSION_ADAPTER.validate_python({'value': '5', 'output_type': 'integer'})
    assert isinstance(parsed, ValueBody)
    core = expression_body_to_core(parsed)
    assert isinstance(core, Value)
    # Value(...) real constructor runs coerce_to_field_type -> int
    assert core.value == 5
    assert isinstance(core.value, int)


def test_field_reference_shape_routes_to_field_arm() -> None:
    parsed = _EXPRESSION_ADAPTER.validate_python(
        {'field_reference': {'field': {'name': 'customer_id'}, 'table_name': 'c'}}
    )
    assert isinstance(parsed, FieldRefBody)
    core = expression_body_to_core(parsed)
    assert isinstance(core, FieldReferenceExpression)
    assert core.field_reference.table_name == 'c'


def test_aggregation_shape_routes_to_aggregation_arm() -> None:
    parsed = _EXPRESSION_ADAPTER.validate_python(
        {'name': 'SUM', 'field': {'field': {'name': 'quantity'}, 'table_name': 'o'}}
    )
    assert isinstance(parsed, SumBody)
    core = expression_body_to_core(parsed)
    assert isinstance(core, Sum)


def test_unmatched_shape_raises_single_clear_error() -> None:
    with pytest.raises(ValidationError) as exc_info:
        _EXPRESSION_ADAPTER.validate_python({'not_a_known_key': 'x'})
    # Custom discriminator -> one tag error, not the old N-arm union spray.
    assert len(exc_info.value.errors()) == 1


# --- Round-trip: representative data-query body -> core QueryStatement --------


def test_data_query_body_round_trips_to_core() -> None:
    body = QueryStatementBody.model_validate(
        {
            'table': {'name': 'customers', 'version': 'LATEST'},
            'only': [{'field': {'name': 'customer_id'}, 'table_name': 'customers'}],
            'expressions': [
                {'expression': {'value': 'active'}, 'alias': 'status'},
                {
                    'expression': {
                        'name': 'SUM',
                        'field': {'field': {'name': 'quantity'}, 'table_name': 'customers'},
                    },
                    'alias': 'total',
                },
            ],
            'where': {
                'children': [
                    {
                        'left': {'field_reference': {'field': {'name': 'customer_id'}, 'table_name': 'customers'}},
                        'lookup': 'EQ',
                        'right': {'value': 1},
                    }
                ],
            },
            'order_by': [
                {'field': {'field': {'name': 'customer_id'}, 'table_name': 'customers'}, 'direction': 'ASC'},
            ],
        }
    )

    core = query_statement_to_core_query_statement(body)
    assert isinstance(core, QueryStatement)

    assert core.where is not None
    condition = core.where.children[0]
    assert isinstance(condition, CoreCondition)
    assert isinstance(condition.left, FieldReferenceExpression)
    assert isinstance(condition.right, Value)
    assert condition.right.value == 1

    assert core.order_by is not None
    assert core.order_by[0].field.table_name == 'customers'

    assert core.expressions is not None
    assert isinstance(core.expressions[0].expression, Value)
    assert isinstance(core.expressions[1].expression, Sum)


def test_condition_to_core_condition_converts_both_sides() -> None:
    condition = Condition.model_validate(
        {
            'left': {'field_reference': {'field': {'name': 'a'}, 'table_name': 't'}},
            'lookup': 'EQ',
            'right': {'value': 42},
        }
    )
    core = condition_to_core_condition(condition)
    assert isinstance(core.left, FieldReferenceExpression)
    assert isinstance(core.right, Value)
    assert core.right.value == 42
