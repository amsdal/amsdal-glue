from dataclasses import dataclass

from amsdal_glue_core.common.data_models.sub_query import SubQueryStatement
from amsdal_glue_core.common.expressions.expression import Expression
from amsdal_glue_core.common.expressions.value import Value


@dataclass(kw_only=True)
class ValueAnnotation:
    """Represents a value annotation.

    Attributes:
        value (Value): The value being annotated.
        alias (str): The alias for the annotation.
    """

    value: Value
    alias: str


@dataclass(kw_only=True)
class ExpressionAnnotation:
    """Represents an expression annotation.

    Attributes:
        expression (Expression): The expression being annotated.
        alias (str): The alias for the annotation.
    """

    expression: Expression
    alias: str


@dataclass(kw_only=True)
class AnnotationQuery:
    """Represents an annotation query.

    Attributes:
        value (SubQueryStatement | ValueAnnotation): The value or subquery being annotated.
    """

    value: SubQueryStatement | ValueAnnotation | ExpressionAnnotation
