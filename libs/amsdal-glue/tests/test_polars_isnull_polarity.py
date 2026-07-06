"""Polars operator constructor: IS NULL / IS NOT NULL polarity is value-driven.

A `right` value of ``True`` means ``IS NULL``; ``False`` means ``IS NOT NULL``.
"""

from amsdal_glue_core.common.data_models.field_reference import Field
from amsdal_glue_core.common.data_models.field_reference import FieldReference
from amsdal_glue_core.common.enums import FieldLookup
from amsdal_glue_core.common.expressions.field_reference import FieldReferenceExpression
from amsdal_glue_core.common.expressions.value import Value

from amsdal_glue.queries.polars_operator_constructor import polars_operator_constructor


def _field(name: str) -> FieldReferenceExpression:
    return FieldReferenceExpression(field_reference=FieldReference(field=Field(name=name), table_name='t'))


def test_isnull_true_emits_is_null() -> None:
    sql = polars_operator_constructor(left=_field('deleted_at'), lookup=FieldLookup.ISNULL, right=Value(value=True))

    assert sql.endswith('IS NULL')
    assert 'IS NOT NULL' not in sql


def test_isnull_false_emits_is_not_null() -> None:
    sql = polars_operator_constructor(left=_field('deleted_at'), lookup=FieldLookup.ISNULL, right=Value(value=False))

    assert sql.endswith('IS NOT NULL')
