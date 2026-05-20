"""SQL emission for `Conditions.negated` at every level."""

from amsdal_glue_core.common.data_models.conditions import Condition
from amsdal_glue_core.common.data_models.conditions import Conditions
from amsdal_glue_core.common.data_models.field_reference import Field
from amsdal_glue_core.common.data_models.field_reference import FieldReference
from amsdal_glue_core.common.enums import FieldLookup
from amsdal_glue_core.common.enums import FilterConnector
from amsdal_glue_core.common.expressions.field_reference import FieldReferenceExpression
from amsdal_glue_core.common.expressions.value import Value

from amsdal_glue_connections.sql.connections.sqlite_connection import get_sqlite_transform
from amsdal_glue_connections.sql.sql_builders.query_builder import build_conditions


def _leaf(name: str, value: object) -> Condition:
    return Condition(
        left=FieldReferenceExpression(field_reference=FieldReference(field=Field(name=name), table_name='')),
        lookup=FieldLookup.EQ,
        right=Value(value=value),
    )


def test_build_conditions_root_negated_emits_not_wrap() -> None:
    c = Conditions(_leaf('a', 1), _leaf('b', 2), negated=True)

    sql, values = build_conditions(c, transform=get_sqlite_transform())

    assert sql == 'NOT (a = ? AND b = ?)'
    assert values == [1, 2]


def test_build_conditions_root_not_negated_no_wrap_regression() -> None:
    c = Conditions(_leaf('a', 1), _leaf('b', 2), negated=False)

    sql, _ = build_conditions(c, transform=get_sqlite_transform())

    assert not sql.startswith('NOT')


def test_build_conditions_root_negated_with_or() -> None:
    c = Conditions(_leaf('a', 1), _leaf('b', 2), connector=FilterConnector.OR, negated=True)

    sql, _ = build_conditions(c, transform=get_sqlite_transform())

    assert sql == 'NOT (a = ? OR b = ?)'


def test_build_conditions_nested_and_root_negation_both_emit() -> None:
    inner = Conditions(_leaf('x', 9), negated=True)
    outer = Conditions(_leaf('a', 1), inner, negated=True)

    sql, _ = build_conditions(outer, transform=get_sqlite_transform())

    assert sql.startswith('NOT (')
    assert 'NOT (x = ?)' in sql


def test_build_conditions_empty_negated_returns_empty() -> None:
    """`Conditions(negated=True)` with no children — root negation has nothing to wrap."""
    c = Conditions(negated=True)

    sql, values = build_conditions(c, transform=get_sqlite_transform())

    assert sql == ''
    assert values == []
