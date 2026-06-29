# libs/connections/tests/golden/test_conditions.py
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

from ._harness import pg


def _cond(field: str, lookup: FieldLookup, value: object, *, negate: bool = False) -> Condition:
    return Condition(
        left=FieldReferenceExpression(
            field_reference=FieldReference(field=Field(name=field), table_name='users'),
        ),
        lookup=lookup,
        right=Value(value=value),
        negate=negate,
    )


def _q(where: Conditions) -> QueryStatement:
    return QueryStatement(table=SchemaReference(name='users', version=Version.LATEST), where=where)


def test_and_pg() -> None:
    where = Conditions(_cond('age', FieldLookup.GT, 18), _cond('active', FieldLookup.EXACT, True))
    assert pg(_q(where)) == (
        'SELECT * FROM "users" WHERE "users"."age" > %s AND "users"."active" IS %s',
        [18, True],
    )


def test_or_pg() -> None:
    where = Conditions(
        _cond('age', FieldLookup.GT, 18),
        _cond('age', FieldLookup.LT, 5),
        connector=FilterConnector.OR,
    )
    assert pg(_q(where)) == (
        'SELECT * FROM "users" WHERE "users"."age" > %s OR "users"."age" < %s',
        [18, 5],
    )


def test_nested_and_or_pg() -> None:
    inner = Conditions(
        _cond('age', FieldLookup.GT, 18),
        _cond('active', FieldLookup.EXACT, True),
    )
    where = Conditions(inner, _cond('name', FieldLookup.EQ, 'foo'), connector=FilterConnector.OR)
    assert pg(_q(where)) == (
        'SELECT * FROM "users" WHERE ("users"."age" > %s AND "users"."active" IS %s) OR "users"."name" = %s',
        [18, True, 'foo'],
    )


def test_negated_condition_pg() -> None:
    where = Conditions(_cond('age', FieldLookup.GT, 18, negate=True))
    assert pg(_q(where)) == (
        'SELECT * FROM "users" WHERE NOT ("users"."age" > %s)',
        [18],
    )


def test_negated_conditions_group_pg() -> None:
    where = Conditions(
        _cond('age', FieldLookup.GT, 18),
        _cond('active', FieldLookup.EXACT, True),
        negated=True,
    )
    assert pg(_q(where)) == (
        'SELECT * FROM "users" WHERE NOT ("users"."age" > %s AND "users"."active" IS %s)',
        [18, True],
    )
