from dataclasses import dataclass

from amsdal_glue_core.common.data_models.data import Data
from amsdal_glue_core.common.data_models.schema import Schema
from amsdal_glue_core.common.operations.commands import SchemaCommand
from amsdal_glue_core.common.operations.mutations.data import DataMutation


@dataclass(kw_only=True)
class DataMutationNode:
    """
    Represents a node in the data mutation tree.

    Attributes:
        mutations (list[DataMutation]): The list of data mutations to be applied.
        result (list[list[Data] | None] | None): The result of the data mutations.
    """

    mutations: list[DataMutation]
    result: list[list[Data] | None] | None = None

    def __repr__(self) -> str:
        """
        Returns a string representation of the DataMutationNode.

        Returns:
            str: A string representation of the DataMutationNode.
        """
        return f'DataMutationNode<{self.mutations}>'

    def __hash__(self) -> int:
        """
        Returns the hash of the DataMutationNode.

        Returns:
            int: The hash of the DataMutationNode.
        """
        return hash(id(self))


@dataclass(kw_only=True)
class SchemaCommandNode:
    """
    Represents a node in the schema command tree.

    Attributes:
        command (SchemaCommand): The schema command to be executed.
        result (list[Schema | None] | None): The result of the schema command execution.
    """

    command: SchemaCommand
    result: list[Schema | None] | None = None

    def __repr__(self) -> str:
        """
        Returns a string representation of the SchemaCommandNode.

        Returns:
            str: A string representation of the SchemaCommandNode.
        """
        return f'SchemaCommandNode<{self.command}>'

    def __hash__(self) -> int:
        """
        Returns the hash of the SchemaCommandNode.

        Returns:
            int: The hash of the SchemaCommandNode.
        """
        return hash(id(self))
