from abc import ABC
from abc import abstractmethod

from amsdal_glue_core.common.operations.commands import DataCommand
from amsdal_glue_core.common.workflows.chain import ChainTask


class DataCommandPlanner(ABC):
    """
    Base class for command planner.
    """

    @abstractmethod
    def plan_data_command(self, command: DataCommand) -> ChainTask:
        """
        Split command into chain of execution (plan).
        """
        ...
