from dataclasses import dataclass

from amsdal_glue_core.common.data_models.data import Data
from amsdal_glue_core.common.data_models.schema import Schema
from amsdal_glue_core.common.operations.commands import SchemaCommand
from amsdal_glue_core.common.operations.mutations.data import DataMutation


@dataclass(kw_only=True)
class DataMutationNode:
    mutations: list[DataMutation]
    result: list[list[Data] | None] | None = None

    def __repr__(self) -> str:
        return f'DataMutationNode<{self.mutations}>'

    def __hash__(self) -> int:
        return hash(id(self))


@dataclass(kw_only=True)
class SchemaCommandNode:
    command: SchemaCommand
    result: list[Schema | None] | None = None

    def __repr__(self) -> str:
        return f'SchemaCommandNode<{self.command}>'

    def __hash__(self) -> int:
        return hash(id(self))
