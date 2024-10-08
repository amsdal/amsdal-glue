from amsdal_glue_core.common.data_models.conditions import Condition
from amsdal_glue_core.common.data_models.conditions import Conditions
from amsdal_glue_core.common.data_models.field_reference import Field
from amsdal_glue_core.common.data_models.field_reference import FieldReference
from amsdal_glue_core.common.enums import FieldLookup
from amsdal_glue_core.common.enums import FilterConnector
from amsdal_glue_core.common.expressions.value import Value


def test_condition_compare() -> None:
    f1 = Field(name='field1')
    f2 = Field(name='field2')

    assert Condition(
        field=FieldReference(field=f1, table_name='table1'),
        lookup=FieldLookup.EQ,
        value=Value(value='value1'),
    ) == Condition(
        field=FieldReference(field=f1, table_name='table1'),
        lookup=FieldLookup.EQ,
        value=Value(value='value1'),
    )

    assert Condition(
        field=FieldReference(field=f1, table_name='table1'),
        lookup=FieldLookup.EQ,
        value=Value(value='value1'),
    ) != Condition(
        field=FieldReference(field=f2, table_name='table1'),
        lookup=FieldLookup.EQ,
        value=Value(value='value1'),
    )
    assert Condition(
        field=FieldReference(field=f1, table_name='table1'),
        lookup=FieldLookup.EQ,
        value=Value(value='value1'),
    ) != Condition(
        field=FieldReference(field=f1, table_name='table1'),
        lookup=FieldLookup.EQ,
        value=Value(value='value1'),
        negate=True,
    )

    assert Condition(
        field=FieldReference(field=f1, table_name='table1'),
        lookup=FieldLookup.EQ,
        value=Value(value='value1'),
    ) != Condition(
        field=FieldReference(field=f1, table_name='table2'),
        lookup=FieldLookup.EQ,
        value=Value(value='value1'),
    )

    assert Condition(
        field=FieldReference(field=f1, table_name='table1'),
        lookup=FieldLookup.EQ,
        value=Value(value='value1'),
    ) != Condition(
        field=FieldReference(field=f1, table_name='table1'),
        lookup=FieldLookup.NEQ,
        value=Value(value='value1'),
    )


def test_conditions_compare() -> None:
    f1 = Field(name='field1')
    f2 = Field(name='field2')

    c1 = Condition(
        field=FieldReference(field=f1, table_name='table1'),
        lookup=FieldLookup.EQ,
        value=Value(value='value1'),
    )
    c2 = Condition(
        field=FieldReference(field=f2, table_name='table2'),
        lookup=FieldLookup.EQ,
        value=Value(value='value2'),
    )
    assert Conditions(c1, c2) == Conditions(c1, c2)
    assert Conditions(c1, c2, negated=True) == Conditions(c1, c2, negated=True)
    assert Conditions(c1, c2) != Conditions(c1, c2, c1)
    assert Conditions(c1, c2) != Conditions(c2, c1)
    assert Conditions(c1, c2, negated=True) != Conditions(c1, c2, negated=False)


def test_and_conditions_flatten() -> None:
    f1 = Field(name='field1')
    f2 = Field(name='field2')

    c1 = Condition(
        field=FieldReference(field=f1, table_name='table1'),
        lookup=FieldLookup.EQ,
        value=Value(value='value1'),
    )
    c2 = Condition(
        field=FieldReference(field=f2, table_name='table2'),
        lookup=FieldLookup.EQ,
        value=Value(value='value2'),
    )
    c1_n = Condition(
        field=FieldReference(field=f1, table_name='table1'),
        lookup=FieldLookup.EQ,
        value=Value(value='value1'),
        negate=True,
    )
    c2_n = Condition(
        field=FieldReference(field=f2, table_name='table2'),
        lookup=FieldLookup.EQ,
        value=Value(value='value2'),
        negate=True,
    )
    assert Conditions(Conditions(c1, c2)) == Conditions(c1, c2)

    assert Conditions(Conditions(c1, c2, negated=True)) == Conditions(c1, c2, negated=True)
    assert Conditions(Conditions(c1, c2), negated=True) == Conditions(c1, c2, negated=True)

    assert Conditions(Conditions(c1, c2, negated=True), negated=True) == Conditions(c1, c2)

    assert Conditions(
        Conditions(c1, c2, connector=FilterConnector.OR),
        Conditions(c1_n, c2_n, connector=FilterConnector.OR),
        connector=FilterConnector.AND,
    ) == Conditions(
        Conditions(c1, c1_n, connector=FilterConnector.AND),
        Conditions(c1, c2_n, connector=FilterConnector.AND),
        Conditions(c2, c1_n, connector=FilterConnector.AND),
        Conditions(c2, c2_n, connector=FilterConnector.AND),
        connector=FilterConnector.OR,
    )
