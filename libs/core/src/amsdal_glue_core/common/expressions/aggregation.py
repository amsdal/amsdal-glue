from dataclasses import dataclass
from typing import ClassVar

from amsdal_glue_core.common.data_models.field_reference import FieldReference
from amsdal_glue_core.common.expressions.base import Expression


@dataclass(kw_only=True)
class AggregationExpression(Expression):
    name: ClassVar[str]
    field: FieldReference


@dataclass(kw_only=True)
class Sum(AggregationExpression):
    name: ClassVar[str] = 'SUM'


@dataclass(kw_only=True)
class Count(AggregationExpression):
    name: ClassVar[str] = 'COUNT'


@dataclass(kw_only=True)
class Avg(AggregationExpression):
    name: ClassVar[str] = 'AVG'


@dataclass(kw_only=True)
class Min(AggregationExpression):
    name: ClassVar[str] = 'MIN'


@dataclass(kw_only=True)
class Max(AggregationExpression):
    name: ClassVar[str] = 'MAX'
