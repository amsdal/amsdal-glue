from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from amsdal_glue_core.common.data_models.query import QueryStatement
    from amsdal_glue_core.common.enums import SetOperationType


@dataclass(kw_only=True)
class SetOperation:
    left: QueryStatement
    right: QueryStatement
    operation: SetOperationType
