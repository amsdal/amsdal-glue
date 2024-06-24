from abc import ABC
from abc import abstractmethod

from amsdal_glue_core.common.data_models.conditions import Conditions
from amsdal_glue_core.common.data_models.query import QueryStatement
from amsdal_glue_core.common.workflows.chain import ChainTask


class DataQueryPlanner(ABC):
    """
    Base class for query planner.
    """

    @abstractmethod
    def plan_data_query(self, query: QueryStatement) -> ChainTask:
        """
        Split query into chain of execution (plan).
        """
        ...


class SchemaQueryPlanner(ABC):
    @abstractmethod
    def plan_schema_query(self, filters: Conditions | None = None) -> ChainTask:
        """
        Split schema query into chain of execution (plan).
        """
        ...
