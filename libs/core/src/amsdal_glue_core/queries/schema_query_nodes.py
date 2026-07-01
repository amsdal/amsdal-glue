from dataclasses import dataclass

from amsdal_glue_core.common.data_models.query import QueryStatement
from amsdal_glue_core.common.data_models.schema import Schema


@dataclass(kw_only=True)
class SchemaQueryNode:
    """
    Represents a node in the schema query tree.

    Attributes:
        schema_name_connection (str): The name of the schema connection.
        query (QueryStatement): The query statement for the schema query.
        result (list[Schema] | None): The result of the schema query execution.
    """

    schema_name_connection: str
    query: QueryStatement
    result: list[Schema] | None = None

    def __repr__(self) -> str:
        """
        Returns a string representation of the SchemaQueryNode.

        Returns:
            str: A string representation of the SchemaQueryNode.
        """
        return f'SchemaQueryNode<{self.query}>'

    def __hash__(self) -> int:
        """
        Returns the hash of the SchemaQueryNode.

        Returns:
            int: The hash of the SchemaQueryNode.
        """
        return hash(id(self))
