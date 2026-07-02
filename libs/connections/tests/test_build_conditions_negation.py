"""SQL emission for `Conditions.negated` at every level.

Re-pointed to Rust SqlGenerator: conditions are wrapped in a minimal QueryStatement
and compile_query is called; the WHERE portion is extracted from the result.
"""

from amsdal_glue_connections._sql_core import SqlGenerator
from amsdal_glue_core.common.data_models.conditions import Condition
from amsdal_glue_core.common.data_models.conditions import Conditions
from amsdal_glue_core.common.data_models.field_reference import Field
from amsdal_glue_core.common.data_models.field_reference import FieldReference
from amsdal_glue_core.common.data_models.query import QueryStatement
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.enums import FieldLookup
from amsdal_glue_core.common.enums import FilterConnector
from amsdal_glue_core.common.enums import Version
from amsdal_glue_core.common.expressions.field_reference import FieldReferenceExpression
from amsdal_glue_core.common.expressions.value import Value

_gen = SqlGenerator('sqlite', param_style='qmark')
_TABLE = SchemaReference(name='t', version=Version.LATEST)
_PREFIX = 'SELECT * FROM "t" WHERE '


def _build_conditions(conditions: Conditions) -> tuple[str, list]:
    """Compile conditions via QueryStatement and return only the WHERE clause."""
    sql, params = _gen.compile_query(QueryStatement(table=_TABLE, where=conditions))
    assert sql.startswith(_PREFIX), f'Unexpected SQL: {sql!r}'
    return sql[len(_PREFIX) :], params


def _leaf(name: str, value: object) -> Condition:
    return Condition(
        left=FieldReferenceExpression(field_reference=FieldReference(field=Field(name=name), table_name='')),
        lookup=FieldLookup.EQ,
        right=Value(value=value),
    )


def test_build_conditions_root_negated_emits_not_wrap() -> None:
    c = Conditions(_leaf('a', 1), _leaf('b', 2), negated=True)

    sql, values = _build_conditions(c)

    # Re-baselined: identifiers are double-quoted (was unquoted in old builder).
    assert sql == 'NOT ("a" = ? AND "b" = ?)'
    assert values == [1, 2]


def test_build_conditions_root_not_negated_no_wrap_regression() -> None:
    c = Conditions(_leaf('a', 1), _leaf('b', 2), negated=False)

    sql, _ = _build_conditions(c)

    assert not sql.startswith('NOT')


def test_build_conditions_root_negated_with_or() -> None:
    c = Conditions(_leaf('a', 1), _leaf('b', 2), connector=FilterConnector.OR, negated=True)

    sql, _ = _build_conditions(c)

    assert sql == 'NOT ("a" = ? OR "b" = ?)'


def test_build_conditions_nested_and_root_negation_both_emit() -> None:
    inner = Conditions(_leaf('x', 9), negated=True)
    outer = Conditions(_leaf('a', 1), inner, negated=True)

    sql, _ = _build_conditions(outer)

    assert sql.startswith('NOT (')
    # Re-baselined: identifiers are double-quoted.
    assert 'NOT ("x" = ?)' in sql


def test_build_conditions_empty_negated_returns_empty() -> None:
    """An empty `Conditions` group must be FILTERED OUT by `compile_query` — with or without NOT —
    so no WHERE is emitted (never the invalid `WHERE NOT ()`). Matches the old builder's ('', [])."""
    c = Conditions(negated=True)

    sql, params = _gen.compile_query(QueryStatement(table=_TABLE, where=c))

    assert sql == 'SELECT * FROM "t"'
    assert params == []


def test_build_conditions_empty_not_negated_returns_empty() -> None:
    """An empty `Conditions` group (no NOT) is likewise filtered out — no WHERE."""
    c = Conditions()

    sql, params = _gen.compile_query(QueryStatement(table=_TABLE, where=c))

    assert sql == 'SELECT * FROM "t"'
    assert params == []
