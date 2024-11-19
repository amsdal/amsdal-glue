# mypy: disable-error-code="type-abstract"
from amsdal_glue_core.commands.planner.schema_command_planner import AsyncSchemaCommandPlanner
from amsdal_glue_core.commands.planner.schema_command_planner import SchemaCommandPlanner
from amsdal_glue_core.common.data_models.results.schema import SchemaResult
from amsdal_glue_core.common.executors.manager import AsyncExecutorManager
from amsdal_glue_core.common.executors.manager import ExecutorManager
from amsdal_glue_core.common.operations.commands import SchemaCommand
from amsdal_glue_core.common.services.commands import AsyncSchemaCommandService
from amsdal_glue_core.common.services.commands import SchemaCommandService

from amsdal_glue.pipelines.services.router_mixin import AsyncPipelineServiceMixin
from amsdal_glue.pipelines.services.router_mixin import PipelineServiceMixin


class DefaultSchemaCommandService(SchemaCommandService):
    """
    DefaultSchemaCommandService is responsible for executing schema commands.

    Example:
        Here is an example to run a delete schema command:

        ```python
        from amsdal_glue import init_default_containers
        from amsdal_glue import Container
        from amsdal_glue import SchemaCommand, SchemaReference, Version
        from amsdal_glue.services import SchemaCommandService

        # Register default containers
        init_default_containers()

        # Get the registered DefaultSchemaCommandService
        service = Container.services.get(SchemaCommandService)

        # Delete `user` schema
        service.execute(
            SchemaCommand(
                mutations=[
                    DeleteSchema(
                        schema_reference=SchemaReference(
                            name='user',
                            version=Version.LATEST,
                        ),
                    ),
                ],
            ),
        )
        ```
    """

    def execute(self, command: SchemaCommand) -> SchemaResult:
        """
        Executes the given schema command.

        Args:
            command (SchemaCommand): The schema command to be executed.

        Returns:
            SchemaResult: The result of the schema command execution.
        """
        from amsdal_glue_core.containers import Container

        query_planner = Container.planners.get(SchemaCommandPlanner)
        plan = query_planner.plan_schema_command(command)

        executor_manager = Container.managers.get(ExecutorManager)
        plan.executor = executor_manager.resolve_by_service(SchemaCommandService)

        try:
            plan.execute(transaction_id=command.root_transaction_id, lock_id=command.lock_id)
        except Exception as exc:  # noqa: BLE001
            return SchemaResult(success=False, message=str(exc), exception=exc)
        else:
            _schemas = plan.final_task.result if plan.final_task else plan.tasks[-1].result

        return SchemaResult(success=True, schemas=_schemas)


class PipelineSchemaCommandService(PipelineServiceMixin, DefaultSchemaCommandService): ...


class DefaultAsyncSchemaCommandService(AsyncSchemaCommandService):
    """
    DefaultAsyncSchemaCommandService is responsible for executing schema commands.

    Example:
        Here is an example to run a delete schema command:

        ```python
        from amsdal_glue import init_default_containers
        from amsdal_glue import Container
        from amsdal_glue import SchemaCommand, SchemaReference, Version
        from amsdal_glue.services import AsyncSchemaCommandService

        # Register default containers
        init_default_containers()

        # Get the registered DefaultAsyncSchemaCommandService
        service = Container.services.get(AsyncSchemaCommandService)

        # Delete `user` schema
        await service.execute(
            SchemaCommand(
                mutations=[
                    DeleteSchema(
                        schema_reference=SchemaReference(
                            name='user',
                            version=Version.LATEST,
                        ),
                    ),
                ],
            ),
        )
        ```
    """

    async def execute(self, command: SchemaCommand) -> SchemaResult:
        """
        Executes the given schema command.

        Args:
            command (SchemaCommand): The schema command to be executed.

        Returns:
            SchemaResult: The result of the schema command execution.
        """
        from amsdal_glue_core.containers import Container

        query_planner = Container.planners.get(AsyncSchemaCommandPlanner)
        plan = query_planner.plan_schema_command(command)

        executor_manager = Container.managers.get(AsyncExecutorManager)
        plan.executor = executor_manager.resolve_by_service(AsyncSchemaCommandService)

        try:
            await plan.execute(transaction_id=command.root_transaction_id, lock_id=command.lock_id)
        except Exception as exc:  # noqa: BLE001
            return SchemaResult(success=False, message=str(exc), exception=exc)
        else:
            _schemas = plan.final_task.result if plan.final_task else plan.tasks[-1].result

        return SchemaResult(success=True, schemas=_schemas)


class PipelineAsyncSchemaCommandService(AsyncPipelineServiceMixin, DefaultAsyncSchemaCommandService): ...
