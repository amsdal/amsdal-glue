# mypy: disable-error-code="type-abstract"
from amsdal_glue_core.commands.planner.lock_command_planner import AsyncLockCommandPlanner
from amsdal_glue_core.commands.planner.lock_command_planner import LockCommandPlanner
from amsdal_glue_core.common.data_models.results.data import LockResult
from amsdal_glue_core.common.executors.manager import AsyncExecutorManager
from amsdal_glue_core.common.executors.manager import ExecutorManager
from amsdal_glue_core.common.operations.commands import LockCommand
from amsdal_glue_core.common.services.commands import AsyncLockCommandService
from amsdal_glue_core.common.services.commands import LockCommandService

from amsdal_glue.pipelines.services.router_mixin import AsyncPipelineServiceMixin
from amsdal_glue.pipelines.services.router_mixin import PipelineServiceMixin


class DefaultLockCommandService(LockCommandService):
    """
    DefaultLockCommandService is responsible for executing lock commands.

    Example:
        Here is an example to run a lock command:

        ```python
        from amsdal_glue import init_default_containers
        from amsdal_glue import Container
        from amsdal_glue import LockCommand, LockAction, LockMode, LockParameter, LockSchemaReference
        from amsdal_glue import SchemaReference, Version
        from amsdal_glue.services import LockCommandService

        # Register default containers
        init_default_containers()

        # Get the registered DefaultLockCommandService
        service = Container.services.get(LockCommandService)

        # Lock a resource
        service.execute(
            LockCommand(
                lock_id=None,
                transaction_id=None,
                action=LockAction.ACQUIRE,
                mode=LockMode.EXCLUSIVE,
                parameter=LockParameter.SKIP_LOCKED,
                locked_objects=[LockSchemaReference(schema=SchemaReference(name='customers', version=Version.LATEST))],
            ),
        )
        ```
    """

    def execute(self, command: LockCommand) -> LockResult:
        """
        Executes the given lock command.

        Args:
            command (LockCommand): The lock command to be executed.

        Returns:
            LockResult: The result of the lock command execution.
        """
        from amsdal_glue_core.containers import Container

        query_planner = Container.planners.get(LockCommandPlanner)
        plan = query_planner.plan_lock(command)

        executor_manager = Container.managers.get(ExecutorManager)
        plan.executor = executor_manager.resolve_by_service(LockCommandService)

        try:
            plan.execute(transaction_id=command.root_transaction_id, lock_id=command.lock_id)
        except Exception as exc:  # noqa: BLE001
            return LockResult(success=False, message=str(exc), exception=exc)

        return LockResult(success=True, result=plan.result)


class PipelineLockCommandService(PipelineServiceMixin, DefaultLockCommandService): ...


class DefaultAsyncLockCommandService(AsyncLockCommandService):
    """
    DefaultAsyncLockCommandService is responsible for executing lock commands.

    Example:
        Here is an example to run a lock command:

        ```python
        from amsdal_glue import init_default_containers
        from amsdal_glue import Container
        from amsdal_glue import LockCommand, LockAction, LockMode, LockParameter, LockSchemaReference
        from amsdal_glue import SchemaReference, Version
        from amsdal_glue.services import AsyncLockCommandService

        # Register default containers
        init_default_containers()

        # Get the registered DefaultAsyncLockCommandService
        service = Container.services.get(AsyncLockCommandService)

        # Lock a resource
        await service.execute(
            LockCommand(
                lock_id=None,
                transaction_id=None,
                action=LockAction.ACQUIRE,
                mode=LockMode.EXCLUSIVE,
                parameter=LockParameter.SKIP_LOCKED,
                locked_objects=[LockSchemaReference(schema=SchemaReference(name='customers', version=Version.LATEST))],
            ),
        )
        ```
    """

    async def execute(self, command: LockCommand) -> LockResult:
        """
        Executes the given lock command.

        Args:
            command (LockCommand): The lock command to be executed.

        Returns:
            LockResult: The result of the lock command execution.
        """
        from amsdal_glue_core.containers import Container

        query_planner = Container.planners.get(AsyncLockCommandPlanner)
        plan = query_planner.plan_lock(command)

        executor_manager = Container.managers.get(AsyncExecutorManager)
        plan.executor = executor_manager.resolve_by_service(AsyncLockCommandService)

        try:
            await plan.execute(transaction_id=command.root_transaction_id, lock_id=command.lock_id)
        except Exception as exc:  # noqa: BLE001
            return LockResult(success=False, message=str(exc), exception=exc)

        return LockResult(success=True, result=plan.result)


class PipelineAsyncLockCommandService(AsyncPipelineServiceMixin, DefaultAsyncLockCommandService): ...
