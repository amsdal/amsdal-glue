from dataclasses import dataclass
from typing import TYPE_CHECKING

from amsdal_glue_core.common.expressions.expression import Expression

if TYPE_CHECKING:
    from amsdal_glue_core.common.data_models.query import QueryStatement


@dataclass(kw_only=True)
class SubQueryStatement(Expression):
    """A subquery placed directly inside an expression slot.

    Subclasses :class:`Expression` so it can be assigned to
    ``Condition.right`` (e.g. ``WHERE col IN (SELECT ...)``) or
    ``SelectExpression.expression`` (scalar subquery in the projection
    list) without a separate wrapper.  The Rust SQL generator dispatches
    on the concrete class name; the Python query analyzer treats it as a
    cross-DB subquery candidate when its inner ``query`` resolves to a
    different pool.

    Attributes:
        query: The query being used as a subquery.
        alias: The alias for the subquery.
    """

    query: 'QueryStatement'
    alias: str
