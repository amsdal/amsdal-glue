"""Polars operator constructor: `regex` / `iregex` are not supported by the cross-database executor.

The right side of a Polars condition is rendered with Python `repr()`, which is not an SQL literal: a
backslash comes out doubled and a pattern with `'` becomes a double-quoted identifier, and `iregex` used to
lower-case the pattern. Rather than return wrong rows, the lookups are rejected like any other unsupported one.
"""

import pytest
from amsdal_glue_core.common.data_models.field_reference import Field
from amsdal_glue_core.common.data_models.field_reference import FieldReference
from amsdal_glue_core.common.enums import FieldLookup
from amsdal_glue_core.common.expressions.field_reference import FieldReferenceExpression
from amsdal_glue_core.common.expressions.value import Value

from amsdal_glue.queries.polars_operator_constructor import polars_operator_constructor


@pytest.mark.parametrize('lookup', [FieldLookup.REGEX, FieldLookup.IREGEX])
def test_regex_lookups_are_not_supported(lookup: FieldLookup) -> None:
    name = FieldReferenceExpression(field_reference=FieldReference(field=Field(name='name'), table_name='t'))

    with pytest.raises(NotImplementedError, match='not supported in the cross-database Polars executor'):
        polars_operator_constructor(left=name, lookup=lookup, right=Value(value=r'^\d+$'))
