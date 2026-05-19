"""EXISTS / NOT EXISTS subquery — a boolean Expression."""

from dataclasses import dataclass

from amsdal_glue_core.common.data_models.query import QueryStatement
from amsdal_glue_core.common.expressions.expression import Expression


@dataclass(kw_only=True)
class Exists(Expression):
    """EXISTS / NOT EXISTS subquery — a boolean Expression.

    Usable anywhere `Expression` is accepted:
    - WHERE / JOIN ON: pass directly inside `Conditions.children`.
    - SELECT projection: wrap in `ExpressionAnnotation(expression=Exists(...))`.
    - As `Condition.left` or `Condition.right` (rare: `WHERE EXISTS(...) = TRUE`).

    The subquery may reference outer-query columns via qualified `table_name`
    in its WHERE conditions (correlated subquery).

    Attributes:
        query: The subquery whose existence is tested.
        negated: When True, emits `NOT EXISTS (...)`; otherwise `EXISTS (...)`.
    """

    query: QueryStatement
    negated: bool = False
