from dataclasses import dataclass

from amsdal_glue_core.common.expressions.aggregation import AggregationExpression


@dataclass(kw_only=True)
class AggregationQuery:
    """Represents an aggregation query.

    Attributes:
        expression (AggregationExpression): The aggregation expression.
        alias (str): The alias for the aggregation.
    """

    expression: AggregationExpression
    alias: str
