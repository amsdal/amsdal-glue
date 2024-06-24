from abc import ABC
from abc import abstractmethod

from amsdal_glue_core.common.operations.commands import TransactionCommand
from amsdal_glue_core.common.workflows.chain import ChainTask


class TransactionCommandPlanner(ABC):
    """
    Base class for command planner.
    """

    @abstractmethod
    def plan_transaction(self, command: TransactionCommand) -> ChainTask:
        """
        Split command into chain of execution (plan).
        """
        ...
