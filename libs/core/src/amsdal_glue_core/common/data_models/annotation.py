from dataclasses import dataclass

from amsdal_glue_core.common.data_models.sub_query import SubQueryStatement
from amsdal_glue_core.common.expressions.value import Value


@dataclass(kw_only=True)
class ValueAnnotation:
    value: Value
    alias: str


@dataclass(kw_only=True)
class AnnotationQuery:
    value: SubQueryStatement | ValueAnnotation
