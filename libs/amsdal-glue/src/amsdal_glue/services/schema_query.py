# mypy: disable-error-code="type-abstract"
from amsdal_glue_core.common.data_models.results.schema import SchemaResult
from amsdal_glue_core.common.executors.manager import AsyncExecutorManager
from amsdal_glue_core.common.executors.manager import ExecutorManager
from amsdal_glue_core.common.operations.queries import SchemaQueryOperation
from amsdal_glue_core.common.services.queries import AsyncSchemaQueryService
from amsdal_glue_core.common.services.queries import SchemaQueryService
from amsdal_glue_core.queries.planner.schema_query_planner import AsyncSchemaQueryPlanner
from amsdal_glue_core.queries.planner.schema_query_planner import SchemaQueryPlanner

from amsdal_glue.pipelines.services.router_mixin import AsyncPipelineServiceMixin
from amsdal_glue.pipelines.services.router_mixin import PipelineServiceMixin


class DefaultSchemaQueryService(SchemaQueryService):
    """
    DefaultSchemaQueryService is responsible for executing schema query operations.

    Example:
        Here is an example to run a schema query operation:

        ```python
        from amsdal_glue import init_default_containers
        from amsdal_glue import Container
        from amsdal_glue import Conditions, Condition, FieldReference, FieldLookup, Value, Field
        from amsdal_glue import SchemaQueryOperation
        from amsdal_glue.services import SchemaQueryService

        # Register default containers
        init_default_containers()

        # Get the registered DefaultSchemaQueryService
        service = Container.services.get(SchemaQueryService)

        # Query `users` schema
        service.execute(
            SchemaQueryOperation(
                filters=Conditions(
                    Condition(
                        field=FieldReference(field=Field(name='name'), table_name='amsdal_schema_registry'),
                        lookup=FieldLookup.EQ,
                        value=Value('users'),
                    )
                ),
            ),
        )
        ```

        Note, the `amsdal_schema_registry` is reserved AMSDAL Glue name of the schema registry table.
        Use it to filter the schemas by name.
    """

    def execute(self, query_op: SchemaQueryOperation) -> SchemaResult:
        """
        Executes the given schema query operation.

        Args:
            query_op (SchemaQueryOperation): The schema query operation to be executed.

        Returns:
            SchemaResult: The result of the schema query operation execution.
        """
        from amsdal_glue_core.containers import Container

        _schema_query_planner = Container.planners.get(SchemaQueryPlanner)
        plan = _schema_query_planner.plan_schema_query(query_op.filters)

        executor_manager = Container.managers.get(ExecutorManager)
        plan.executor = executor_manager.resolve_by_service(SchemaQueryService)

        try:
            plan.execute(transaction_id=query_op.root_transaction_id, lock_id=query_op.lock_id)
        except Exception as exc:  # noqa: BLE001
            return SchemaResult(success=False, message=str(exc), exception=exc)

        _schemas = plan.final_task.result if plan.final_task else plan.tasks[-1].result

        return SchemaResult(success=True, schemas=_schemas)


class PipelineSchemaQueryService(PipelineServiceMixin, DefaultSchemaQueryService): ...


class DefaultAsyncSchemaQueryService(AsyncSchemaQueryService):
    """
    DefaultAsyncSchemaQueryService is responsible for executing schema query operations.

    Example:
        Here is an example to run a schema query operation:

        ```python
        from amsdal_glue import init_default_containers
        from amsdal_glue import Container
        from amsdal_glue import Conditions, Condition, FieldReference, FieldLookup, Value, Field
        from amsdal_glue import SchemaQueryOperation
        from amsdal_glue.services import AsyncSchemaQueryService

        # Register default containers
        init_default_containers()

        # Get the registered DefaultAsyncSchemaQueryService
        service = Container.services.get(AsyncSchemaQueryService)

        # Query `users` schema
        await service.execute(
            SchemaQueryOperation(
                filters=Conditions(
                    Condition(
                        field=FieldReference(field=Field(name='name'), table_name='amsdal_schema_registry'),
                        lookup=FieldLookup.EQ,
                        value=Value('users'),
                    )
                ),
            ),
        )
        ```

        Note, the `amsdal_schema_registry` is reserved AMSDAL Glue name of the schema registry table.
        Use it to filter the schemas by name.
    """

    async def execute(self, query_op: SchemaQueryOperation) -> SchemaResult:
        """
        Executes the given schema query operation.

        Args:
            query_op (SchemaQueryOperation): The schema query operation to be executed.

        Returns:
            SchemaResult: The result of the schema query operation execution.
        """
        from amsdal_glue_core.containers import Container

        _schema_query_planner = Container.planners.get(AsyncSchemaQueryPlanner)
        plan = _schema_query_planner.plan_schema_query(query_op.filters)

        executor_manager = Container.managers.get(AsyncExecutorManager)
        plan.executor = executor_manager.resolve_by_service(AsyncSchemaQueryService)

        try:
            await plan.execute(transaction_id=query_op.root_transaction_id, lock_id=query_op.lock_id)
        except Exception as exc:  # noqa: BLE001
            return SchemaResult(success=False, message=str(exc), exception=exc)

        _schemas = plan.final_task.result if plan.final_task else plan.tasks[-1].result

        return SchemaResult(success=True, schemas=_schemas)


class PipelineAsyncSchemaQueryService(AsyncPipelineServiceMixin, DefaultAsyncSchemaQueryService): ...
