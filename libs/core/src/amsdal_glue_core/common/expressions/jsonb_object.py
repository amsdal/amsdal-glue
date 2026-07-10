from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING

from amsdal_glue_core.common.expressions.expression import Expression

if TYPE_CHECKING:
    from amsdal_glue_core.common.data_models.types import FieldType


class JsonbObject(Expression):
    """Represents a JSON object built from ordered key -> expression pairs.

    Renders as ``jsonb_build_object(...)`` on PostgreSQL and ``json_object(...)`` on SQLite.

    Attributes:
        pairs (list[tuple[str, Expression]]): The ordered key/expression pairs.
    """

    def __init__(
        self,
        pairs: Mapping[str, Expression] | list[tuple[str, Expression]],
        output_type: FieldType | None = None,
    ) -> None:
        super().__init__(output_type=output_type)
        if isinstance(pairs, Mapping):
            self.pairs: list[tuple[str, Expression]] = list(pairs.items())
        else:
            self.pairs = list(pairs)
