from dataclasses import dataclass

from amsdal_glue_core.common.data_models.conditions import Conditions
from amsdal_glue_core.common.data_models.data import Data
from amsdal_glue_core.common.data_models.query import QueryStatement


@dataclass(kw_only=True)
class DataQueryNode:
    query: QueryStatement
    result: list[Data] | None = None

    def __repr__(self) -> str:
        return f'DataQueryNode<{self.query}>'

    def __hash__(self) -> int:
        return hash(id(self))


@dataclass(kw_only=True)
class SchemaQueryNode:
    filters: Conditions
    result: list[Data] | None = None

    def __repr__(self) -> str:
        return f'SchemaQueryNode<{self.filters}>'

    def __hash__(self) -> int:
        return hash(id(self))
