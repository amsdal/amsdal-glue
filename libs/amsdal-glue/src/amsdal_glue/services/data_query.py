# mypy: disable-error-code="type-abstract"
from amsdal_glue_core.common.data_models.results.data import DataResult
from amsdal_glue_core.common.executors.manager import AsyncExecutorManager
from amsdal_glue_core.common.executors.manager import ExecutorManager
from amsdal_glue_core.common.operations.queries import DataQueryOperation
from amsdal_glue_core.common.services.queries import AsyncDataQueryService
from amsdal_glue_core.common.services.queries import DataQueryService
from amsdal_glue_core.queries.planner.data_query_planner import AsyncDataQueryPlanner
from amsdal_glue_core.queries.planner.data_query_planner import DataQueryPlanner

from amsdal_glue.pipelines.services.router_mixin import AsyncPipelineServiceMixin
from amsdal_glue.pipelines.services.router_mixin import PipelineServiceMixin


class DefaultDataQueryService(DataQueryService):
    """
    DefaultDataQueryService is responsible for executing data query operations.

    Example:
        Here is an example to run a data query operation:

        ```python
        from amsdal_glue import init_default_containers
        from amsdal_glue import Container
        from amsdal_glue import FieldReference, FieldLookup, Value, Field
        from amsdal_glue import DataQueryOperation
        from amsdal_glue.services import DataQueryService

        # Register default containers
        init_default_containers()

        # Get the registered DefaultDataQueryService
        service = Container.services.get(DataQueryService)

        # Query `users` schema and get only `first_name` and `last_name` fields
        service.execute(
            DataQueryOperation(
                query=QueryStatement(
                    table=SchemaReference(name='users', version=Version.LATEST),
                    only=[
                        FieldReference(field=Field(name='first_name'), table_name='users'),
                        FieldReference(field=Field(name='last_name'), table_name='users'),
                    ],
                ),
            ),
        )
        ```
    """

    def execute(self, query_op: DataQueryOperation) -> DataResult:
        """
        Executes the given data query operation.

        Args:
            query_op (DataQueryOperation): The data query operation to be executed.

        Returns:
            DataResult: The result of the data query operation execution.
        """
        from amsdal_glue_core.containers import Container

        _query_planner = Container.planners.get(DataQueryPlanner)
        plan = _query_planner.plan_data_query(query_op.query)

        executor_manager = Container.managers.get(ExecutorManager)
        plan.executor = executor_manager.resolve_by_service(DataQueryService)

        try:
            plan.execute(transaction_id=query_op.root_transaction_id, lock_id=query_op.lock_id)
        except Exception as exc:  # noqa: BLE001
            return DataResult(success=False, message=str(exc), exception=exc)

        _data = plan.final_task.result if plan.final_task else plan.tasks[-1].result

        return DataResult(success=True, data=_data)


class PipelineDataQueryService(PipelineServiceMixin, DefaultDataQueryService): ...


class DefaultAsyncDataQueryService(AsyncDataQueryService):
    """
    DefaultAsyncDataQueryService is responsible for executing data query operations.

    Example:
        Here is an example to run a data query operation:

        ```python
        from amsdal_glue import init_default_containers
        from amsdal_glue import Container
        from amsdal_glue import FieldReference, FieldLookup, Value, Field
        from amsdal_glue import DataQueryOperation
        from amsdal_glue.services import AsyncDataQueryService

        # Register default containers
        init_default_containers()

        # Get the registered DefaultAsyncDataQueryService
        service = Container.services.get(AsyncDataQueryService)

        # Query `users` schema and get only `first_name` and `last_name` fields
        await service.execute(
            DataQueryOperation(
                query=QueryStatement(
                    table=SchemaReference(name='users', version=Version.LATEST),
                    only=[
                        FieldReference(field=Field(name='first_name'), table_name='users'),
                        FieldReference(field=Field(name='last_name'), table_name='users'),
                    ],
                ),
            ),
        )
        ```
    """

    async def execute(self, query_op: DataQueryOperation) -> DataResult:
        """
        Executes the given data query operation.

        Args:
            query_op (DataQueryOperation): The data query operation to be executed.

        Returns:
            DataResult: The result of the data query operation execution.
        """
        from amsdal_glue_core.containers import Container

        _query_planner = Container.planners.get(AsyncDataQueryPlanner)
        plan = _query_planner.plan_data_query(query_op.query)

        executor_manager = Container.managers.get(AsyncExecutorManager)
        plan.executor = executor_manager.resolve_by_service(AsyncDataQueryService)

        try:
            await plan.execute(transaction_id=query_op.root_transaction_id, lock_id=query_op.lock_id)
        except Exception as exc:  # noqa: BLE001
            return DataResult(success=False, message=str(exc), exception=exc)

        _data = plan.final_task.result if plan.final_task else plan.tasks[-1].result

        return DataResult(success=True, data=_data)


class PipelineAsyncDataQueryService(AsyncPipelineServiceMixin, DefaultAsyncDataQueryService): ...
