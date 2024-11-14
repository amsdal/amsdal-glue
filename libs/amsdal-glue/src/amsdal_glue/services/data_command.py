# mypy: disable-error-code="type-abstract"
from amsdal_glue_core.commands.planner.data_command_planner import AsyncDataCommandPlanner
from amsdal_glue_core.commands.planner.data_command_planner import DataCommandPlanner
from amsdal_glue_core.common.data_models.results.data import DataResult
from amsdal_glue_core.common.executors.manager import AsyncExecutorManager
from amsdal_glue_core.common.executors.manager import ExecutorManager
from amsdal_glue_core.common.operations.commands import DataCommand
from amsdal_glue_core.common.services.commands import AsyncDataCommandService
from amsdal_glue_core.common.services.commands import DataCommandService

from amsdal_glue.pipelines.services.router_mixin import AsyncPipelineServiceMixin
from amsdal_glue.pipelines.services.router_mixin import PipelineServiceMixin


class DefaultDataCommandService(DataCommandService):
    """
    DefaultDataCommandService is responsible for executing data commands.

    Example:
        Here is an example to run a create data command:

        ```python
        from amsdal_glue import init_default_containers
        from amsdal_glue import Container
        from amsdal_glue import DataCommand, Data, SchemaReference
        from amsdal_glue.services import DataCommandService

        # Register default containers
        init_default_containers()

        # Get the registered DefaultDataCommandService
        service = Container.services.get(DataCommandService)

        # Insert data into `customers` and `logs` schemas
        service.execute(
            command=DataCommand(
                mutations=[
                    InsertData(
                        schema=SchemaReference(name='customers', version=Version.LATEST),
                        data=[
                            Data(data={'customer_id': 1, 'name': 'John Doe', 'email': 'e1@example.com'}),
                            Data(data={'customer_id': 2, 'name': 'Jane Doe', 'email': 'e2@example.com'}),
                            Data(data={'customer_id': 3, 'name': 'Josh Doe', 'email': 'e3@example.com'}),
                            Data(data={'customer_id': 4, 'name': 'Jane Doe', 'email': 'e4@example.com'}),
                        ],
                    ),
                    InsertData(
                        schema=SchemaReference(name='logs', version=Version.LATEST),
                        data=[
                            Data(data={'created_at': '2021-01-01 00:00:00', 'message': 'Lorem ipsum dolor sit amet'}),
                            Data(data={'created_at': '2021-01-02 00:00:00', 'message': 'consectetur adipiscing elit'}),
                            Data(data={'created_at': '2021-01-03 00:00:00', 'message': 'sed do eiusmod tempor'}),
                            Data(data={'created_at': '2021-01-04 00:00:00', 'message': 'ut labore et dolore magna'}),
                        ],
                    ),
                ],
            ),
        )
        ```
    """

    def execute(self, command: DataCommand) -> DataResult:
        """
        Executes the given data command.

        Args:
            command (DataCommand): The data command to be executed.

        Returns:
            DataResult: The result of the data command execution.
        """
        from amsdal_glue_core.containers import Container

        query_planner = Container.planners.get(DataCommandPlanner)
        plan = query_planner.plan_data_command(command)

        executor_manager = Container.managers.get(ExecutorManager)
        plan.executor = executor_manager.resolve_by_service(DataCommandService)

        try:
            plan.execute(transaction_id=command.root_transaction_id, lock_id=command.lock_id)
        except Exception as exc:  # noqa: BLE001
            return DataResult(success=False, message=str(exc), exception=exc)
        else:
            _data = plan.final_task.result if plan.final_task else plan.tasks[-1].result

        return DataResult(success=True, data=_data)


class PipelineDataCommandService(PipelineServiceMixin, DefaultDataCommandService): ...


class DefaultAsyncDataCommandService(AsyncDataCommandService):
    """
    DefaultAsyncDataCommandService is responsible for executing data commands.

    Example:
        Here is an example to run a create data command:

        ```python
        from amsdal_glue import init_default_containers
        from amsdal_glue import Container
        from amsdal_glue import DataCommand, Data, SchemaReference
        from amsdal_glue.services import AsyncDataCommandService

        # Register default containers
        init_default_containers()

        # Get the registered DefaultAsyncDataCommandService
        service = Container.services.get(AsyncDataCommandService)

        # Insert data into `customers` and `logs` schemas
        await service.execute(
            command=DataCommand(
                mutations=[
                    InsertData(
                        schema=SchemaReference(name='customers', version=Version.LATEST),
                        data=[
                            Data(data={'customer_id': 1, 'name': 'John Doe', 'email': 'e1@example.com'}),
                            Data(data={'customer_id': 2, 'name': 'Jane Doe', 'email': 'e2@example.com'}),
                            Data(data={'customer_id': 3, 'name': 'Josh Doe', 'email': 'e3@example.com'}),
                            Data(data={'customer_id': 4, 'name': 'Jane Doe', 'email': 'e4@example.com'}),
                        ],
                    ),
                    InsertData(
                        schema=SchemaReference(name='logs', version=Version.LATEST),
                        data=[
                            Data(data={'created_at': '2021-01-01 00:00:00', 'message': 'Lorem ipsum dolor sit amet'}),
                            Data(data={'created_at': '2021-01-02 00:00:00', 'message': 'consectetur adipiscing elit'}),
                            Data(data={'created_at': '2021-01-03 00:00:00', 'message': 'sed do eiusmod tempor'}),
                            Data(data={'created_at': '2021-01-04 00:00:00', 'message': 'ut labore et dolore magna'}),
                        ],
                    ),
                ],
            ),
        )
        ```
    """

    async def execute(self, command: DataCommand) -> DataResult:
        """
        Executes the given data command.

        Args:
            command (DataCommand): The data command to be executed.

        Returns:
            DataResult: The result of the data command execution.
        """
        from amsdal_glue_core.containers import Container

        query_planner = Container.planners.get(AsyncDataCommandPlanner)
        plan = await query_planner.plan_data_command(command)

        executor_manager = Container.managers.get(AsyncExecutorManager)
        plan.executor = executor_manager.resolve_by_service(AsyncDataCommandService)

        try:
            await plan.execute(transaction_id=command.root_transaction_id, lock_id=command.lock_id)
        except Exception as exc:  # noqa: BLE001
            return DataResult(success=False, message=str(exc), exception=exc)
        else:
            _data = plan.final_task.result if plan.final_task else plan.tasks[-1].result

        return DataResult(success=True, data=_data)


class PipelineAsyncDataCommandService(AsyncPipelineServiceMixin, DefaultAsyncDataCommandService): ...
