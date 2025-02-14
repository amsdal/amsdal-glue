from dataclasses import dataclass

from amsdal_glue_core.common.data_models.field_reference import FieldReference
from amsdal_glue_core.common.expressions.expression import Expression


@dataclass(kw_only=True)
class FieldReferenceExpression(Expression):
    field_reference: FieldReference
