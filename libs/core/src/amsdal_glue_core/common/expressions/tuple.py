from __future__ import annotations

from typing import TYPE_CHECKING

from amsdal_glue_core.common.expressions.expression import Expression

if TYPE_CHECKING:
    from amsdal_glue_core.common.data_models.types import FieldType


class TupleExpression(Expression):
    """Row/tuple constructor: ``(expr1, expr2, ...)``.

    Used for composite key operations like::

        WHERE (user_id, product_id) IN ((1, 10), (2, 20))
    """

    def __init__(self, *items: Expression, output_type: FieldType | None = None) -> None:
        super().__init__(output_type=output_type)
        self.items = list(items)
