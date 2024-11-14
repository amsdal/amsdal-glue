# mypy: disable-error-code="type-abstract"
from amsdal_glue_core.commands.planner.transaction_command_planner import AsyncTransactionCommandPlanner
from amsdal_glue_core.commands.planner.transaction_command_planner import TransactionCommandPlanner
from amsdal_glue_core.common.data_models.results.data import TransactionResult
from amsdal_glue_core.common.executors.manager import AsyncExecutorManager
from amsdal_glue_core.common.executors.manager import ExecutorManager
from amsdal_glue_core.common.operations.commands import TransactionCommand
from amsdal_glue_core.common.services.commands import AsyncTransactionCommandService
from amsdal_glue_core.common.services.commands import TransactionCommandService

from amsdal_glue.pipelines.services.router_mixin import AsyncPipelineServiceMixin
from amsdal_glue.pipelines.services.router_mixin import PipelineServiceMixin


class DefaultTransactionCommandService(TransactionCommandService):
    """
    DefaultTransactionCommandService is responsible for executing transaction commands.

    Example:
        Here is an example to run a transaction command:

        ```python
        from amsdal_glue import init_default_containers
        from amsdal_glue import Container
        from amsdal_glue import TransactionCommand, Transaction, TransactionAction
        from amsdal_glue import SchemaReference, Version
        from amsdal_glue.services import TransactionCommandService

        # Register default containers
        init_default_containers()

        # Get the registered DefaultTransactionCommandService
        service = Container.services.get(TransactionCommandService)

        # Begin a transaction command
        service.execute(
            TransactionCommand(
                transaction_id='test_transaction',
                schema=SchemaReference(name='customers', version=Version.LATEST),
                action=TransactionAction.BEGIN,
            ),
        )
        ```
    """

    def execute(self, command: TransactionCommand) -> TransactionResult:
        """
        Executes the given transaction command.

        Args:
            command (TransactionCommand): The transaction command to be executed.

        Returns:
            TransactionResult: The result of the transaction command execution.
        """
        from amsdal_glue_core.containers import Container

        query_planner = Container.planners.get(TransactionCommandPlanner)
        plan = query_planner.plan_transaction(command)

        executor_manager = Container.managers.get(ExecutorManager)
        plan.executor = executor_manager.resolve_by_service(TransactionCommandService)

        try:
            plan.execute(transaction_id=command.root_transaction_id, lock_id=command.lock_id)
        except Exception as exc:  # noqa: BLE001
            return TransactionResult(success=False, message=str(exc), exception=exc)

        return TransactionResult(success=True, result=plan.result)


class PipelineTransactionCommandService(PipelineServiceMixin, DefaultTransactionCommandService): ...


class DefaultAsyncTransactionCommandService(AsyncTransactionCommandService):
    """
    DefaultAsyncTransactionCommandService is responsible for executing transaction commands.

    Example:
        Here is an example to run a transaction command:

        ```python
        from amsdal_glue import init_default_containers
        from amsdal_glue import Container
        from amsdal_glue import TransactionCommand, Transaction, TransactionAction
        from amsdal_glue import SchemaReference, Version
        from amsdal_glue.services import AsyncTransactionCommandService

        # Register default containers
        init_default_containers()

        # Get the registered DefaultAsyncTransactionCommandService
        service = Container.services.get(AsyncTransactionCommandService)

        # Begin a transaction command
        await service.execute(
            TransactionCommand(
                transaction_id='test_transaction',
                schema=SchemaReference(name='customers', version=Version.LATEST),
                action=TransactionAction.BEGIN,
            ),
        )
        ```
    """

    async def execute(self, command: TransactionCommand) -> TransactionResult:
        """
        Executes the given transaction command.

        Args:
            command (TransactionCommand): The transaction command to be executed.

        Returns:
            TransactionResult: The result of the transaction command execution.
        """
        from amsdal_glue_core.containers import Container

        query_planner = Container.planners.get(AsyncTransactionCommandPlanner)
        plan = query_planner.plan_transaction(command)

        executor_manager = Container.managers.get(AsyncExecutorManager)
        plan.executor = executor_manager.resolve_by_service(AsyncTransactionCommandService)

        try:
            await plan.execute(transaction_id=command.root_transaction_id, lock_id=command.lock_id)
        except Exception as exc:  # noqa: BLE001
            return TransactionResult(success=False, message=str(exc), exception=exc)

        return TransactionResult(success=True, result=plan.result)


class PipelineAsyncTransactionCommandService(AsyncPipelineServiceMixin, DefaultAsyncTransactionCommandService): ...
