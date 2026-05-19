"""Polars final-query executor: outer/nested Conditions.negated must be honored."""

from amsdal_glue_core.common.data_models.conditions import Condition
from amsdal_glue_core.common.data_models.conditions import Conditions
from amsdal_glue_core.common.data_models.field_reference import Field
from amsdal_glue_core.common.data_models.field_reference import FieldReference
from amsdal_glue_core.common.enums import FieldLookup
from amsdal_glue_core.common.enums import FilterConnector
from amsdal_glue_core.common.expressions.field_reference import FieldReferenceExpression
from amsdal_glue_core.common.expressions.value import Value

from amsdal_glue.queries.executors.palars_final_query_executor import PolarsFinalQueryDataExecutorMixin


def _eq(field: str, value: int) -> Condition:
    return Condition(
        left=FieldReferenceExpression(field_reference=FieldReference(field=Field(name=field), table_name='t')),
        lookup=FieldLookup.EQ,
        right=Value(value=value),
    )


def test_outer_negated_conditions_wraps_with_not() -> None:
    """`Conditions(negated=True)` at the root must produce `NOT (...)` SQL."""
    mixin = PolarsFinalQueryDataExecutorMixin()
    conditions = Conditions(_eq('a', 1), _eq('b', 2), negated=True)

    sql = mixin._sql_build_conditions(conditions)  # noqa: SLF001

    upper = sql.upper()
    assert 'NOT' in upper, f'Expected NOT wrapper, got: {sql!r}'


def test_nested_negated_conditions_wraps_with_not() -> None:
    """Nested `Conditions(negated=True)` must produce `NOT (...)` in the emitted SQL.

    Outer connector OR avoids the AND-over-OR CNF distribution path.
    """
    mixin = PolarsFinalQueryDataExecutorMixin()
    nested = Conditions(_eq('a', 1), _eq('b', 2), connector=FilterConnector.AND, negated=True)
    conditions = Conditions(_eq('c', 3), nested, connector=FilterConnector.OR)

    sql = mixin._sql_build_conditions(conditions)  # noqa: SLF001

    upper = sql.upper()
    assert 'NOT' in upper, f'Expected NOT in nested clause, got: {sql!r}'


def test_non_negated_conditions_emits_no_not() -> None:
    """Sanity check: a non-negated tree must not introduce stray NOT."""
    mixin = PolarsFinalQueryDataExecutorMixin()
    conditions = Conditions(_eq('a', 1), _eq('b', 2))

    sql = mixin._sql_build_conditions(conditions)  # noqa: SLF001

    assert 'NOT' not in sql.upper(), f'Unexpected NOT in: {sql!r}'
