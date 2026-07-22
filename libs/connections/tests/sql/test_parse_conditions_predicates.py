"""Unit tests for the introspection predicate parser (`parse_conditions`).

These cover the keyword comparison predicates that appear in CHECK constraints and partial-index
``WHERE`` clauses -- ``IS [NOT] NULL``, ``IN`` / ``NOT IN``, ``LIKE`` / ``ILIKE``, ``BETWEEN`` --
plus the ``NOT NOT`` double-negation case. Before the parser was extended these raised ``ValueError``
(aborting the whole ``query_schema``); now they parse into proper glue ``Conditions``.
"""

import pytest
from amsdal_glue_core.common.data_models.conditions import Condition
from amsdal_glue_core.common.data_models.conditions import Conditions
from amsdal_glue_core.common.enums import FieldLookup
from amsdal_glue_core.common.expressions.value import Value

from amsdal_glue_connections.sql.parsers.conditions import parse_conditions
from amsdal_glue_connections.sql.parsers.conditions import try_parse_conditions


def _only_condition(conds: Conditions) -> Condition:
    assert isinstance(conds, Conditions)
    assert len(conds.children) == 1
    child = conds.children[0]
    assert isinstance(child, Condition)
    return child


def test_is_not_null_parses_to_isnull_false():
    cond = _only_condition(parse_conditions('"email" IS NOT NULL'))
    assert cond.lookup is FieldLookup.ISNULL
    assert cond.right == Value(value=False)
    assert cond.negate is False


def test_is_null_parses_to_isnull_true():
    cond = _only_condition(parse_conditions('"email" IS NULL'))
    assert cond.lookup is FieldLookup.ISNULL
    assert cond.right == Value(value=True)


def test_in_list_parses_to_in_lookup():
    cond = _only_condition(parse_conditions("\"status\" IN ('a', 'b', 'c')"))
    assert cond.lookup is FieldLookup.IN
    assert cond.right == Value(value=['a', 'b', 'c'])
    assert cond.negate is False


def test_not_in_list_parses_negated():
    cond = _only_condition(parse_conditions('"n" NOT IN (1, 2, 3)'))
    assert cond.lookup is FieldLookup.IN
    assert cond.right == Value(value=[1, 2, 3])
    assert cond.negate is True


def test_between_parses_to_between_lookup():
    cond = _only_condition(parse_conditions('"age" BETWEEN 1 AND 9'))
    assert cond.lookup is FieldLookup.BETWEEN
    assert cond.right == Value(value=[1, 9])
    assert cond.negate is False


def test_not_between_parses_negated():
    cond = _only_condition(parse_conditions('"age" NOT BETWEEN 1 AND 9'))
    assert cond.lookup is FieldLookup.BETWEEN
    assert cond.right == Value(value=[1, 9])
    assert cond.negate is True


@pytest.mark.parametrize(
    ('predicate', 'lookup', 'value'),
    [
        ('"e" LIKE \'%@%\'', FieldLookup.CONTAINS, '@'),
        ('"e" LIKE \'abc%\'', FieldLookup.STARTSWITH, 'abc'),
        ('"e" LIKE \'%abc\'', FieldLookup.ENDSWITH, 'abc'),
        ('"e" ILIKE \'%@%\'', FieldLookup.ICONTAINS, '@'),
        ('"e" ILIKE \'abc%\'', FieldLookup.ISTARTSWITH, 'abc'),
        ('"e" ILIKE \'%abc\'', FieldLookup.IENDSWITH, 'abc'),
    ],
)
def test_like_patterns_map_to_high_level_lookups(predicate, lookup, value):
    cond = _only_condition(parse_conditions(predicate))
    assert cond.lookup is lookup
    assert cond.right == Value(value=value)
    assert cond.negate is False


def test_not_like_parses_negated():
    cond = _only_condition(parse_conditions('"e" NOT LIKE \'%@%\''))
    assert cond.lookup is FieldLookup.CONTAINS
    assert cond.right == Value(value='@')
    assert cond.negate is True


def test_like_with_interior_wildcard_is_unrepresentable():
    # A pattern with an interior wildcard has no faithful CONTAINS/STARTSWITH/ENDSWITH mapping
    # (those escape their value), so it must raise -- and degrade to None through the safe wrapper.
    with pytest.raises(ValueError):
        parse_conditions('"e" LIKE \'a%b\'')
    assert try_parse_conditions('"e" LIKE \'a%b\'') is None


def test_double_negation_cancels():
    # `NOT NOT a = 1` must be the plain (non-negated) predicate, not a single negation.
    conds = parse_conditions('NOT NOT "a" = 1')
    assert isinstance(conds, Conditions)
    assert conds.negated is False
    cond = _only_condition(conds)
    assert cond.lookup is FieldLookup.EQ
    assert cond.negate is False


def test_single_negation_still_negates():
    conds = parse_conditions('NOT "a" = 1')
    assert conds.negated is True


def test_triple_negation_is_negated():
    conds = parse_conditions('NOT NOT NOT "a" = 1')
    assert conds.negated is True


def test_predicate_combined_with_and():
    conds = parse_conditions('"a" > 5 AND "b" IS NULL')
    assert isinstance(conds, Conditions)
    assert len(conds.children) == 2
    lookups = {c.lookup for c in conds.children if isinstance(c, Condition)}
    assert lookups == {FieldLookup.GT, FieldLookup.ISNULL}
