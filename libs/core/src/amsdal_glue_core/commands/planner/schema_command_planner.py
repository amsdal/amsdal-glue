from abc import ABC
from abc import abstractmethod

from amsdal_glue_core.common.operations.commands import SchemaCommand
from amsdal_glue_core.common.workflows.chain import ChainTask


class SchemaCommandPlanner(ABC):
    @abstractmethod
    def plan_schema_command(self, command: SchemaCommand) -> ChainTask:
        """
        Split schema command into chain of execution (plan).
        """
        ...
