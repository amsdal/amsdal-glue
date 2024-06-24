from dataclasses import dataclass
from typing import Any

from amsdal_glue_core.commands.executors.data_command_executor import DataCommandNodeExecutor
from amsdal_glue_core.commands.mutation_nodes import DataMutationNode
from amsdal_glue_core.common.workflows.task import Task


@dataclass(kw_only=True)
class DataMutationTask(Task):
    data_mutation_node: DataMutationNode

    def execute(self) -> None:
        _query_executor = DataCommandNodeExecutor()
        _query_executor.execute(self.data_mutation_node)

    @property
    def item(self) -> Any:
        return self.data_mutation_node

    @property
    def result(self) -> Any:
        return self.data_mutation_node.result
