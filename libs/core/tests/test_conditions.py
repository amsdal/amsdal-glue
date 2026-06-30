from amsdal_glue_core.common.data_models.conditions import Condition
from amsdal_glue_core.common.data_models.conditions import Conditions
from amsdal_glue_core.common.data_models.field_reference import Field
from amsdal_glue_core.common.data_models.field_reference import FieldReference
from amsdal_glue_core.common.data_models.query import QueryStatement
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.enums import FieldLookup
from amsdal_glue_core.common.enums import FilterConnector
from amsdal_glue_core.common.expressions.exists import Exists
from amsdal_glue_core.common.expressions.field_reference import FieldReferenceExpression
from amsdal_glue_core.common.expressions.func import Func
from amsdal_glue_core.common.expressions.value import Value


def test_condition_compare() -> None:
    f1 = Field(name='field1')
    f2 = Field(name='field2')

    assert Condition(
        left=FieldReferenceExpression(field_reference=FieldReference(field=f1, table_name='table1')),
        lookup=FieldLookup.EQ,
        right=Value(value='value1'),
    ) == Condition(
        left=FieldReferenceExpression(field_reference=FieldReference(field=f1, table_name='table1')),
        lookup=FieldLookup.EQ,
        right=Value(value='value1'),
    )

    assert Condition(
        left=FieldReferenceExpression(field_reference=FieldReference(field=f1, table_name='table1')),
        lookup=FieldLookup.EQ,
        right=Value(value='value1'),
    ) != Condition(
        left=FieldReferenceExpression(field_reference=FieldReference(field=f2, table_name='table1')),
        lookup=FieldLookup.EQ,
        right=Value(value='value1'),
    )
    assert Condition(
        left=FieldReferenceExpression(field_reference=FieldReference(field=f1, table_name='table1')),
        lookup=FieldLookup.EQ,
        right=Value(value='value1'),
    ) != Condition(
        left=FieldReferenceExpression(field_reference=FieldReference(field=f1, table_name='table1')),
        lookup=FieldLookup.EQ,
        right=Value(value='value1'),
        negate=True,
    )

    assert Condition(
        left=FieldReferenceExpression(field_reference=FieldReference(field=f1, table_name='table1')),
        lookup=FieldLookup.EQ,
        right=Value(value='value1'),
    ) != Condition(
        left=FieldReferenceExpression(field_reference=FieldReference(field=f1, table_name='table2')),
        lookup=FieldLookup.EQ,
        right=Value(value='value1'),
    )

    assert Condition(
        left=FieldReferenceExpression(field_reference=FieldReference(field=f1, table_name='table1')),
        lookup=FieldLookup.EQ,
        right=Value(value='value1'),
    ) != Condition(
        left=FieldReferenceExpression(field_reference=FieldReference(field=f1, table_name='table1')),
        lookup=FieldLookup.NEQ,
        right=Value(value='value1'),
    )


def test_conditions_compare() -> None:
    f1 = Field(name='field1')
    f2 = Field(name='field2')

    c1 = Condition(
        left=FieldReferenceExpression(field_reference=FieldReference(field=f1, table_name='table1')),
        lookup=FieldLookup.EQ,
        right=Value(value='value1'),
    )
    c2 = Condition(
        left=FieldReferenceExpression(field_reference=FieldReference(field=f2, table_name='table2')),
        lookup=FieldLookup.EQ,
        right=Value(value='value2'),
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
        left=FieldReferenceExpression(field_reference=FieldReference(field=f1, table_name='table1')),
        lookup=FieldLookup.EQ,
        right=Value(value='value1'),
    )
    c2 = Condition(
        left=FieldReferenceExpression(field_reference=FieldReference(field=f2, table_name='table2')),
        lookup=FieldLookup.EQ,
        right=Value(value='value2'),
    )
    c1_n = Condition(
        left=FieldReferenceExpression(field_reference=FieldReference(field=f1, table_name='table1')),
        lookup=FieldLookup.EQ,
        right=Value(value='value1'),
        negate=True,
    )
    c2_n = Condition(
        left=FieldReferenceExpression(field_reference=FieldReference(field=f2, table_name='table2')),
        lookup=FieldLookup.EQ,
        right=Value(value='value2'),
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


def _exists_expr(*, negated: bool = False) -> Exists:
    sub = QueryStatement(
        only=[FieldReference(field=Field(name='1'), table_name='')],
        table=SchemaReference(name='Employee'),
    )
    return Exists(subquery=sub, negated=negated)


def test_invert_flips_exists_child_negation() -> None:
    """`~Conditions(Exists(...))` must flip `Exists.negated` (De Morgan).

    `_negate()` previously only recursed into Conditions/Condition children,
    silently dropping the NOT for any boolean Expression child.
    """
    inner = _exists_expr(negated=False)
    tree = Conditions(inner)

    inverted = ~tree

    assert len(inverted.children) == 1
    flipped = inverted.children[0]
    assert isinstance(flipped, Exists)
    assert flipped.negated is True


def test_invert_flips_exists_inside_mixed_children() -> None:
    """`_negate()` must flip Exists alongside Condition siblings."""
    f1 = FieldReferenceExpression(field_reference=FieldReference(field=Field(name='a'), table_name='t'))
    condition = Condition(left=f1, lookup=FieldLookup.EQ, right=Value(value=1))
    inner_exists = _exists_expr(negated=False)
    tree = Conditions(condition, inner_exists, connector=FilterConnector.AND)

    inverted = ~tree

    assert inverted.connector == FilterConnector.OR
    found_exists = [c for c in inverted.children if isinstance(c, Exists)]
    assert len(found_exists) == 1
    assert found_exists[0].negated is True


def test_double_invert_restores_exists_negation() -> None:
    """Double negation restores the original `Exists.negated` value."""
    inner = _exists_expr(negated=True)
    tree = Conditions(inner)

    double = ~(~tree)

    assert isinstance(double.children[0], Exists)
    assert double.children[0].negated is True


def test_invert_preserves_negation_for_unknown_expression_child() -> None:
    """`~Conditions(Func(...))` must preserve the NOT.

    Any Expression child that is not Conditions/Condition/Exists has no
    flippable `negated`/`negate` attribute. `_negate` must NOT silently lose
    the outer negation — it should fall back to wrapping the parent.
    """
    func = Func(name='IsActive', args=[])
    tree = Conditions(func)

    inverted = ~tree

    # The outer-negation flag must be set so that the SQL builder emits
    # `NOT (...)` around the Func. Either via `inverted.negated=True` or via
    # any other mechanism that yields `NOT (...)` in the rendered SQL.
    assert inverted.negated is True, (
        f'Outer NOT lost. inverted.negated={inverted.negated}, '
        f'connector={inverted.connector}, children={inverted.children!r}'
    )


def test_and_over_negated_or_does_not_distribute() -> None:
    """`Conditions(C, neg_or, AND)` must NOT CNF-distribute through a negated OR.

    Before the fix, `c AND NOT(a OR b)` was silently rewritten to
    `(c AND a) OR (c AND b)` — dropping the inner negation entirely.
    """
    field_a = FieldReferenceExpression(field_reference=FieldReference(field=Field(name='a'), table_name='t'))
    field_b = FieldReferenceExpression(field_reference=FieldReference(field=Field(name='b'), table_name='t'))
    field_c = FieldReferenceExpression(field_reference=FieldReference(field=Field(name='c'), table_name='t'))
    a = Condition(left=field_a, lookup=FieldLookup.EQ, right=Value(value=1))
    b = Condition(left=field_b, lookup=FieldLookup.EQ, right=Value(value=2))
    c = Condition(left=field_c, lookup=FieldLookup.EQ, right=Value(value=3))

    inner_neg_or = Conditions(a, b, connector=FilterConnector.OR, negated=True)
    outer = Conditions(c, inner_neg_or, connector=FilterConnector.AND)

    # Outer must stay AND. Either the negated OR child is preserved as-is,
    # or De Morgan has been pushed in (AND of negated leaves) — both are
    # semantically equivalent. What is NOT acceptable is plain OR distribution.
    assert outer.connector == FilterConnector.AND, (
        f'Expected AND preserved; got {outer.connector}. Children: {outer.children!r}'
    )


def test_conditions_hash_uses_tuple_children() -> None:
    """`Conditions.__hash__` must hash `tuple(self.children)`, not the raw list.

    Hashing a `list` raises `TypeError: unhashable type: 'list'`. Empty
    `Conditions` has no children to hash, so this isolates the list-vs-tuple
    conversion bug from any deeper child-hashability concerns.
    """
    c = Conditions()

    # Must not raise TypeError on hashing a list.
    hash(c)


def test_root_negated_survives_construction() -> None:
    """`negated=True` on construction is preserved when no nested Conditions to absorb into."""
    field_a = FieldReferenceExpression(field_reference=FieldReference(field=Field(name='a'), table_name='t'))
    field_b = FieldReferenceExpression(field_reference=FieldReference(field=Field(name='b'), table_name='t'))
    c = Conditions(
        Condition(left=field_a, lookup=FieldLookup.EQ, right=Value(value=1)),
        Condition(left=field_b, lookup=FieldLookup.EQ, right=Value(value=2)),
        negated=True,
    )

    assert c.negated is True
    assert len(c.children) == 2
