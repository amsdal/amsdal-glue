from abc import ABC
from abc import abstractmethod

from amsdal_glue_core.common.operations.commands import LockCommand
from amsdal_glue_core.common.workflows.chain import ChainTask


class LockCommandPlanner(ABC):
    """
    Base class for command planner.
    """

    @abstractmethod
    def plan_lock(self, command: LockCommand) -> ChainTask:
        """
        Split command into chain of execution (plan).
        """
        ...
