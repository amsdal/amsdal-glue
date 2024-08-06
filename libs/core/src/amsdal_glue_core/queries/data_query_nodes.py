from dataclasses import dataclass
from typing import TYPE_CHECKING

from amsdal_glue_core.common.data_models.data import Data
from amsdal_glue_core.common.data_models.query import QueryStatement

if TYPE_CHECKING:
    from amsdal_glue_core.queries.final_query_statement import FinalQueryStatement


@dataclass(kw_only=True)
class DataQueryNode:
    """
    Represents a node in the data query tree.

    Attributes:
        query (QueryStatement): The query statement to be executed.
        result (list[Data] | None): The result of the data query execution.
    """

    query: QueryStatement
    result: list[Data] | None = None

    def __repr__(self) -> str:
        """
        Returns a string representation of the DataQueryNode.

        Returns:
            str: A string representation of the DataQueryNode.
        """
        return f'DataQueryNode<{self.query}>'

    def __hash__(self) -> int:
        """
        Returns the hash of the DataQueryNode.

        Returns:
            int: The hash of the DataQueryNode.
        """
        return hash(id(self))


@dataclass(kw_only=True)
class FinalDataQueryNode:
    """
    Represents a node in the final data query tree.

    Attributes:
        query (FinalQueryStatement): The final query statement to be executed.
        result (list[Data] | None): The result of the final data query execution.
    """

    query: 'FinalQueryStatement'
    result: list[Data] | None = None
