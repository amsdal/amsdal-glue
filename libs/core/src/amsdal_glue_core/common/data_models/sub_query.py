from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from amsdal_glue_core.common.data_models.query import QueryStatement


@dataclass(kw_only=True)
class SubQueryStatement:
    query: 'QueryStatement'
    alias: str
