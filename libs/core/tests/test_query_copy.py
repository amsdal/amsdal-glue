from copy import copy

from amsdal_glue_core.common.data_models.field_reference import Field
from amsdal_glue_core.common.data_models.field_reference import FieldReference
from amsdal_glue_core.common.data_models.query import QueryStatement
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.enums import Version


def _table() -> SchemaReference:
    return SchemaReference(name='orders', version=Version.LATEST)


def test_copy_preserves_explicit_empty_only() -> None:
    # `only=[]` is a deliberate, load-bearing contract: "project no default
    # columns; rely on `expressions`". copy() must NOT collapse it to None.
    original = QueryStatement(table=_table(), only=[])

    duplicate = copy(original)

    assert duplicate.only == []
    assert duplicate.only is not None


def test_copy_preserves_none_only() -> None:
    original = QueryStatement(table=_table(), only=None)

    duplicate = copy(original)

    assert duplicate.only is None


def test_copy_duplicates_populated_only_by_value() -> None:
    ref = FieldReference(field=Field(name='id'), table_name='orders')
    original = QueryStatement(table=_table(), only=[ref])

    duplicate = copy(original)

    assert duplicate.only == [ref]
    # copied by value: mutating the copy must not touch the original list
    assert duplicate.only is not original.only
