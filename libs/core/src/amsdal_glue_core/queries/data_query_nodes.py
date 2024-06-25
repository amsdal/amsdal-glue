from dataclasses import dataclass
from typing import TYPE_CHECKING

from amsdal_glue_core.common.data_models.data import Data
from amsdal_glue_core.common.data_models.query import QueryStatement

if TYPE_CHECKING:
    from amsdal_glue_core.queries.final_query_statement import FinalQueryStatement


@dataclass(kw_only=True)
class DataQueryNode:
    query: QueryStatement
    result: list[Data] | None = None

    def __repr__(self) -> str:
        return f'DataQueryNode<{self.query}>'

    def __hash__(self) -> int:
        return hash(id(self))


@dataclass(kw_only=True)
class FinalDataQueryNode:
    query: 'FinalQueryStatement'
    result: list[Data] | None = None
