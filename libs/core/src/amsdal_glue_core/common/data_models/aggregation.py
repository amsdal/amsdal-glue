from dataclasses import dataclass

from amsdal_glue_core.common.expressions.aggregation import Aggregation


@dataclass(kw_only=True)
class AggregationQuery:
    """Represents an aggregation query.

    Attributes:
        expression (Aggregation): The aggregation expression.
        alias (str): The alias for the aggregation.
    """

    expression: Aggregation
    alias: str
