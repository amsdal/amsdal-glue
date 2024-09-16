from dataclasses import dataclass
from typing import ClassVar

from amsdal_glue_core.common.data_models.field_reference import FieldReference
from amsdal_glue_core.common.expressions.base import BaseExpression


@dataclass(kw_only=True)
class AggregationExpression(BaseExpression):
    """Represents an aggregation expression.

    Attributes:
        name (ClassVar[str]): The name of the aggregation function.
        field (FieldReference): The field to which the aggregation function is applied.
    """

    name: ClassVar[str]
    field: FieldReference


@dataclass(kw_only=True)
class Sum(AggregationExpression):
    """Represents a SUM aggregation expression.

    Attributes:
        name (ClassVar[str]): The name of the aggregation function, which is 'SUM'.
    """

    name: ClassVar[str] = 'SUM'


@dataclass(kw_only=True)
class Count(AggregationExpression):
    """Represents a COUNT aggregation expression.

    Attributes:
        name (ClassVar[str]): The name of the aggregation function, which is 'COUNT'.
    """

    name: ClassVar[str] = 'COUNT'


@dataclass(kw_only=True)
class Avg(AggregationExpression):
    """Represents an AVG aggregation expression.

    Attributes:
        name (ClassVar[str]): The name of the aggregation function, which is 'AVG'.
    """

    name: ClassVar[str] = 'AVG'


@dataclass(kw_only=True)
class Min(AggregationExpression):
    """Represents a MIN aggregation expression.

    Attributes:
        name (ClassVar[str]): The name of the aggregation function, which is 'MIN'.
    """

    name: ClassVar[str] = 'MIN'


@dataclass(kw_only=True)
class Max(AggregationExpression):
    """Represents a MAX aggregation expression.

    Attributes:
        name (ClassVar[str]): The name of the aggregation function, which is 'MAX'.
    """

    name: ClassVar[str] = 'MAX'
