from typing import Any

from amsdal_glue_core.common.executors.interfaces import FinalDataQueryExecutor
from amsdal_glue_core.common.workflows.task import Task
from amsdal_glue_core.queries.data_query_nodes import DataQueryNode
from amsdal_glue_core.queries.data_query_nodes import FinalDataQueryNode
from amsdal_glue_core.queries.executors.data_query_executor import DataQueryNodeExecutor


class DataQueryTask(Task):
    """
    Task for query execution.
    """

    def __init__(self, query_node: DataQueryNode):
        self.query_node = query_node
        self.executor = DataQueryNodeExecutor()

    def execute(self, transaction_id: str | None, lock_id: str | None):
        self.executor.execute(self.query_node, transaction_id=transaction_id, lock_id=lock_id)

    @property
    def item(self) -> Any:
        return self.query_node

    @property
    def result(self) -> Any:
        return self.query_node.result


class FinalDataQueryTask(Task):
    def __init__(self, query_node: FinalDataQueryNode):
        from amsdal_glue_core.containers import Container

        self.query_node = query_node
        self.executor = Container.executors.get(FinalDataQueryExecutor)

    def execute(self, transaction_id: str | None, lock_id: str | None) -> None:
        self.executor.execute(self.query_node, transaction_id=transaction_id, lock_id=lock_id)

    @property
    def item(self) -> Any:
        return self.query_node

    @property
    def result(self) -> Any:
        return self.query_node.result
