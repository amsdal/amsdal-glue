"""Smoke tests for the `Exists` Expression primitive."""

from amsdal_glue_core.common.data_models.field_reference import Field
from amsdal_glue_core.common.data_models.field_reference import FieldReference
from amsdal_glue_core.common.data_models.query import QueryStatement
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.expressions.exists import Exists


def test_exists_constructs_with_default_negated_false() -> None:
    sub = QueryStatement(
        only=[FieldReference(field=Field(name='1'), table_name='')],
        table=SchemaReference(name='Employee'),
    )

    expr = Exists(subquery=sub)

    assert expr.subquery is sub
    assert expr.negated is False


def test_exists_constructs_with_explicit_negated_true() -> None:
    sub = QueryStatement(
        only=[FieldReference(field=Field(name='1'), table_name='')],
        table=SchemaReference(name='Employee'),
    )

    expr = Exists(subquery=sub, negated=True)

    assert expr.negated is True
