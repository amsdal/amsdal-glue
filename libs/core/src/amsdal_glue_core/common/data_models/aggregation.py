from dataclasses import dataclass

from amsdal_glue_core.common.expressions.aggregation import AggregationExpression


@dataclass(kw_only=True)
class AggregationQuery:
    expression: AggregationExpression
    alias: str
