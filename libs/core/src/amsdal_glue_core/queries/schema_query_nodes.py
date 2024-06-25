from dataclasses import dataclass

from amsdal_glue_core.common.data_models.conditions import Conditions
from amsdal_glue_core.common.data_models.schema import Schema


@dataclass(kw_only=True)
class SchemaQueryNode:
    schema_name_connection: str
    filters: Conditions
    result: list[Schema] | None = None

    def __repr__(self) -> str:
        return f'SchemaQueryNode<{self.filters}>'

    def __hash__(self) -> int:
        return hash(id(self))
