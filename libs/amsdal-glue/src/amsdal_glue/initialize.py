# mypy: disable-error-code="type-abstract"
# Register core services, managers and executors

from amsdal_glue.pipelines.containers import SubContainer


def init_default_containers(container: SubContainer | None = None) -> None:  # noqa: PLR0915
    """
    Initializes and registers the default containers for services, managers, and executors.

    This function sets up the default dependency injection containers by registering various
    services, managers, planners, and executors. It ensures that the application has the
    necessary components to function correctly.

    Registers:
        - [ConnectionManager][amsdal_glue.ConnectionManager]: Manages database connections.
        - [SequentialExecutor][amsdal_glue.interfaces.SequentialExecutor]: Executes tasks sequentially.
        - [ParallelExecutor][amsdal_glue.interfaces.ParallelExecutor]: Executes tasks in parallel using threads.
        - [DataQueryService][amsdal_glue.interfaces.DataQueryService]: Handles data query operations.
        - [SchemaQueryService][amsdal_glue.interfaces.SchemaQueryService]: Handles schema query operations.
        - [DataQueryPlanner][amsdal_glue.interfaces.DataQueryPlanner]: Plans data query operations.
        - [SchemaQueryPlanner][amsdal_glue.interfaces.SchemaQueryPlanner]: Plans schema query operations.
        - [FinalDataQueryExecutor][amsdal_glue.interfaces.FinalDataQueryExecutor]: Executes final data query operations.
        - [DataCommandService][amsdal_glue.interfaces.DataCommandService]: Handles data command operations.
        - [SchemaCommandService][amsdal_glue.interfaces.SchemaCommandService]: Handles schema command operations.
        - [DataCommandPlanner][amsdal_glue.interfaces.DataCommandPlanner]: Plans data command operations.
        - [SchemaCommandPlanner][amsdal_glue.interfaces.SchemaCommandPlanner]: Plans schema command operations.
        - [LockCommandService][amsdal_glue.interfaces.LockCommandService]: Handles lock command operations.
        - [LockCommandPlanner][amsdal_glue.interfaces.LockCommandPlanner]: Plans lock command operations.
        - [TransactionCommandService][amsdal_glue.interfaces.TransactionCommandService]: Handles transaction command.
        - [TransactionCommandPlanner][amsdal_glue.interfaces.TransactionCommandPlanner]: Plans transaction command.

    Example:
        Before using the application, you need to register all services, managers, planners, and executors.
        You can do this by calling the `init_default_containers` function that sets up the default containers.
        Or you can register them manually via [Container][amsdal_glue.Container] class.

        Here is an example of how to use the `init_default_containers` function:

        ```python
        from amsdal_glue import init_default_containers

        init_default_containers()
        ```
    """
    from amsdal_glue_core.common.executors.manager import AsyncExecutorManager
    from amsdal_glue_core.common.executors.manager import ExecutorManager

    from amsdal_glue import Container as DefaultContainer
    from amsdal_glue import DefaultAsyncConnectionManager
    from amsdal_glue import DefaultConnectionManager
    from amsdal_glue import Singleton
    from amsdal_glue.commands.planner.data_planner import DefaultAsyncDataCommandPlanner
    from amsdal_glue.commands.planner.data_planner import DefaultDataCommandPlanner
    from amsdal_glue.commands.planner.lock_planner import DefaultAsyncLockCommandPlanner
    from amsdal_glue.commands.planner.lock_planner import DefaultLockCommandPlanner
    from amsdal_glue.commands.planner.schema_planner import DefaultAsyncSchemaCommandPlanner
    from amsdal_glue.commands.planner.schema_planner import DefaultSchemaCommandPlanner
    from amsdal_glue.commands.planner.transaction_planner import DefaultAsyncTransactionCommandPlanner
    from amsdal_glue.commands.planner.transaction_planner import DefaultTransactionCommandPlanner
    from amsdal_glue.interfaces import AsyncConnectionManager
    from amsdal_glue.interfaces import AsyncDataCommandPlanner
    from amsdal_glue.interfaces import AsyncDataCommandService
    from amsdal_glue.interfaces import AsyncDataQueryPlanner
    from amsdal_glue.interfaces import AsyncDataQueryService
    from amsdal_glue.interfaces import AsyncFinalDataQueryExecutor
    from amsdal_glue.interfaces import AsyncLockCommandPlanner
    from amsdal_glue.interfaces import AsyncLockCommandService
    from amsdal_glue.interfaces import AsyncParallelExecutor
    from amsdal_glue.interfaces import AsyncSchemaCommandPlanner
    from amsdal_glue.interfaces import AsyncSchemaCommandService
    from amsdal_glue.interfaces import AsyncSchemaQueryPlanner
    from amsdal_glue.interfaces import AsyncSchemaQueryService
    from amsdal_glue.interfaces import AsyncSequentialExecutor
    from amsdal_glue.interfaces import AsyncTransactionCommandPlanner
    from amsdal_glue.interfaces import AsyncTransactionCommandService
    from amsdal_glue.interfaces import ConnectionManager
    from amsdal_glue.interfaces import DataCommandPlanner
    from amsdal_glue.interfaces import DataCommandService
    from amsdal_glue.interfaces import DataQueryPlanner
    from amsdal_glue.interfaces import DataQueryService
    from amsdal_glue.interfaces import FinalDataQueryExecutor
    from amsdal_glue.interfaces import LockCommandPlanner
    from amsdal_glue.interfaces import LockCommandService
    from amsdal_glue.interfaces import ParallelExecutor
    from amsdal_glue.interfaces import RuntimeManager
    from amsdal_glue.interfaces import SchemaCommandPlanner
    from amsdal_glue.interfaces import SchemaCommandService
    from amsdal_glue.interfaces import SchemaQueryPlanner
    from amsdal_glue.interfaces import SchemaQueryService
    from amsdal_glue.interfaces import SequentialExecutor
    from amsdal_glue.interfaces import TransactionCommandPlanner
    from amsdal_glue.interfaces import TransactionCommandService
    from amsdal_glue.managers.executor_manager import DefaultAsyncExecutorManager
    from amsdal_glue.managers.executor_manager import DefaultExecutorManager
    from amsdal_glue.queries.executors.palars_final_query_executor import AsyncPolarsFinalQueryDataExecutor
    from amsdal_glue.queries.executors.palars_final_query_executor import PolarsFinalQueryDataExecutor
    from amsdal_glue.queries.planner.data_query_planner import DefaultAsyncDataQueryPlanner
    from amsdal_glue.queries.planner.data_query_planner import DefaultDataQueryPlanner
    from amsdal_glue.queries.planner.schema_query_planner import DefaultAsyncSchemaQueryPlanner
    from amsdal_glue.queries.planner.schema_query_planner import DefaultSchemaQueryPlanner
    from amsdal_glue.services.data_command import DefaultAsyncDataCommandService
    from amsdal_glue.services.data_command import DefaultDataCommandService
    from amsdal_glue.services.data_query import DefaultAsyncDataQueryService
    from amsdal_glue.services.data_query import DefaultDataQueryService
    from amsdal_glue.services.lock_command import DefaultAsyncLockCommandService
    from amsdal_glue.services.lock_command import DefaultLockCommandService
    from amsdal_glue.services.schema_command import DefaultAsyncSchemaCommandService
    from amsdal_glue.services.schema_command import DefaultSchemaCommandService
    from amsdal_glue.services.schema_query import DefaultAsyncSchemaQueryService
    from amsdal_glue.services.schema_query import DefaultSchemaQueryService
    from amsdal_glue.services.transaction_command import DefaultAsyncTransactionCommandService
    from amsdal_glue.services.transaction_command import DefaultTransactionCommandService
    from amsdal_glue.task_executors.parallel_process_executor import AsyncioParallelExecutor
    from amsdal_glue.task_executors.parallel_thread_executor import ThreadParallelExecutor
    from amsdal_glue.task_executors.sequential_sync_executor import AsyncSequentialSyncExecutor
    from amsdal_glue.task_executors.sequential_sync_executor import SequentialSyncExecutor

    _container = container or DefaultContainer  # type: ignore[assignment]

    if _container is DefaultContainer:
        from amsdal_glue import DefaultRuntimeManager
        from amsdal_glue.interfaces import RuntimeManager

        _container.managers.register(RuntimeManager, Singleton(DefaultRuntimeManager))

    _container.managers.register(ExecutorManager, Singleton(DefaultExecutorManager))
    _container.managers.register(AsyncExecutorManager, Singleton(DefaultAsyncExecutorManager))

    _container.managers.register(ConnectionManager, Singleton(DefaultConnectionManager))
    _container.managers.register(AsyncConnectionManager, Singleton(DefaultAsyncConnectionManager))
    _container.executors.register(SequentialExecutor, SequentialSyncExecutor)
    _container.executors.register(AsyncSequentialExecutor, AsyncSequentialSyncExecutor)
    _container.executors.register(ParallelExecutor, ThreadParallelExecutor)
    _container.executors.register(AsyncParallelExecutor, AsyncioParallelExecutor)

    # Register default services, managers and executors for Queries
    _container.services.register(DataQueryService, DefaultDataQueryService)
    _container.services.register(AsyncDataQueryService, DefaultAsyncDataQueryService)
    _container.services.register(SchemaQueryService, DefaultSchemaQueryService)
    _container.services.register(AsyncSchemaQueryService, DefaultAsyncSchemaQueryService)
    _container.planners.register(DataQueryPlanner, DefaultDataQueryPlanner)
    _container.planners.register(AsyncDataQueryPlanner, DefaultAsyncDataQueryPlanner)
    _container.planners.register(SchemaQueryPlanner, DefaultSchemaQueryPlanner)
    _container.planners.register(AsyncSchemaQueryPlanner, DefaultAsyncSchemaQueryPlanner)
    _container.executors.register(FinalDataQueryExecutor, PolarsFinalQueryDataExecutor)
    _container.executors.register(AsyncFinalDataQueryExecutor, AsyncPolarsFinalQueryDataExecutor)

    # Register default services, managers and executors for Commands
    _container.services.register(DataCommandService, DefaultDataCommandService)

    _container.services.register(AsyncDataCommandService, DefaultAsyncDataCommandService)
    _container.services.register(SchemaCommandService, DefaultSchemaCommandService)
    _container.services.register(AsyncSchemaCommandService, DefaultAsyncSchemaCommandService)
    _container.planners.register(DataCommandPlanner, DefaultDataCommandPlanner)
    _container.planners.register(AsyncDataCommandPlanner, DefaultAsyncDataCommandPlanner)
    _container.planners.register(SchemaCommandPlanner, DefaultSchemaCommandPlanner)
    _container.planners.register(AsyncSchemaCommandPlanner, DefaultAsyncSchemaCommandPlanner)

    # Register default services, managers and executors for Lock Commands
    _container.services.register(LockCommandService, DefaultLockCommandService)
    _container.services.register(AsyncLockCommandService, DefaultAsyncLockCommandService)
    _container.planners.register(LockCommandPlanner, DefaultLockCommandPlanner)
    _container.planners.register(AsyncLockCommandPlanner, DefaultAsyncLockCommandPlanner)

    # Register default services, managers and executors for Transaction Commands
    _container.services.register(TransactionCommandService, DefaultTransactionCommandService)
    _container.services.register(AsyncTransactionCommandService, DefaultAsyncTransactionCommandService)
    _container.planners.register(TransactionCommandPlanner, DefaultTransactionCommandPlanner)
    _container.planners.register(AsyncTransactionCommandPlanner, DefaultAsyncTransactionCommandPlanner)


def init_pipeline_containers() -> None:  # noqa: PLR0915
    from amsdal_glue import Container
    from amsdal_glue import DefaultRuntimeManager
    from amsdal_glue import Singleton
    from amsdal_glue.commands.planner.data_planner import DefaultAsyncDataCommandPlanner
    from amsdal_glue.commands.planner.data_planner import DefaultDataCommandPlanner
    from amsdal_glue.commands.planner.lock_planner import DefaultAsyncLockCommandPlanner
    from amsdal_glue.commands.planner.lock_planner import DefaultLockCommandPlanner
    from amsdal_glue.commands.planner.schema_planner import DefaultAsyncSchemaCommandPlanner
    from amsdal_glue.commands.planner.schema_planner import DefaultSchemaCommandPlanner
    from amsdal_glue.commands.planner.transaction_planner import DefaultAsyncTransactionCommandPlanner
    from amsdal_glue.commands.planner.transaction_planner import DefaultTransactionCommandPlanner
    from amsdal_glue.interfaces import AsyncDataCommandPlanner
    from amsdal_glue.interfaces import AsyncDataCommandService
    from amsdal_glue.interfaces import AsyncDataQueryPlanner
    from amsdal_glue.interfaces import AsyncDataQueryService
    from amsdal_glue.interfaces import AsyncFinalDataQueryExecutor
    from amsdal_glue.interfaces import AsyncLockCommandPlanner
    from amsdal_glue.interfaces import AsyncLockCommandService
    from amsdal_glue.interfaces import AsyncParallelExecutor
    from amsdal_glue.interfaces import AsyncSchemaCommandPlanner
    from amsdal_glue.interfaces import AsyncSchemaCommandService
    from amsdal_glue.interfaces import AsyncSchemaQueryPlanner
    from amsdal_glue.interfaces import AsyncSchemaQueryService
    from amsdal_glue.interfaces import AsyncSequentialExecutor
    from amsdal_glue.interfaces import AsyncTransactionCommandPlanner
    from amsdal_glue.interfaces import AsyncTransactionCommandService
    from amsdal_glue.interfaces import DataCommandPlanner
    from amsdal_glue.interfaces import DataCommandService
    from amsdal_glue.interfaces import DataQueryPlanner
    from amsdal_glue.interfaces import DataQueryService
    from amsdal_glue.interfaces import FinalDataQueryExecutor
    from amsdal_glue.interfaces import LockCommandPlanner
    from amsdal_glue.interfaces import LockCommandService
    from amsdal_glue.interfaces import ParallelExecutor
    from amsdal_glue.interfaces import RuntimeManager
    from amsdal_glue.interfaces import SchemaCommandPlanner
    from amsdal_glue.interfaces import SchemaCommandService
    from amsdal_glue.interfaces import SchemaQueryPlanner
    from amsdal_glue.interfaces import SchemaQueryService
    from amsdal_glue.interfaces import SequentialExecutor
    from amsdal_glue.interfaces import TransactionCommandPlanner
    from amsdal_glue.interfaces import TransactionCommandService
    from amsdal_glue.pipelines.manager import PipelineManager
    from amsdal_glue.queries.executors.palars_final_query_executor import AsyncPolarsFinalQueryDataExecutor
    from amsdal_glue.queries.executors.palars_final_query_executor import PolarsFinalQueryDataExecutor
    from amsdal_glue.queries.planner.data_query_planner import DefaultAsyncDataQueryPlanner
    from amsdal_glue.queries.planner.data_query_planner import DefaultDataQueryPlanner
    from amsdal_glue.queries.planner.schema_query_planner import DefaultAsyncSchemaQueryPlanner
    from amsdal_glue.queries.planner.schema_query_planner import DefaultSchemaQueryPlanner
    from amsdal_glue.services.data_command import PipelineAsyncDataCommandService
    from amsdal_glue.services.data_command import PipelineDataCommandService
    from amsdal_glue.services.data_query import PipelineAsyncDataQueryService
    from amsdal_glue.services.data_query import PipelineDataQueryService
    from amsdal_glue.services.lock_command import PipelineAsyncLockCommandService
    from amsdal_glue.services.lock_command import PipelineLockCommandService
    from amsdal_glue.services.schema_command import PipelineAsyncSchemaCommandService
    from amsdal_glue.services.schema_command import PipelineSchemaCommandService
    from amsdal_glue.services.schema_query import PipelineAsyncSchemaQueryService
    from amsdal_glue.services.schema_query import PipelineSchemaQueryService
    from amsdal_glue.services.transaction_command import PipelineAsyncTransactionCommandService
    from amsdal_glue.services.transaction_command import PipelineTransactionCommandService
    from amsdal_glue.task_executors.parallel_process_executor import AsyncioParallelExecutor
    from amsdal_glue.task_executors.parallel_process_executor import ProcessParallelExecutor
    from amsdal_glue.task_executors.sequential_sync_executor import AsyncSequentialSyncExecutor
    from amsdal_glue.task_executors.sequential_sync_executor import SequentialSyncExecutor

    Container.managers.register(RuntimeManager, Singleton(DefaultRuntimeManager))
    Container.managers.register(PipelineManager, Singleton(PipelineManager))

    Container.executors.register(SequentialExecutor, SequentialSyncExecutor)
    Container.executors.register(AsyncSequentialExecutor, AsyncSequentialSyncExecutor)
    Container.executors.register(ParallelExecutor, ProcessParallelExecutor)
    Container.executors.register(AsyncParallelExecutor, AsyncioParallelExecutor)

    # Register default services, managers and executors for Queries
    Container.services.register(DataQueryService, PipelineDataQueryService)

    Container.services.register(AsyncDataQueryService, PipelineAsyncDataQueryService)
    Container.services.register(SchemaQueryService, PipelineSchemaQueryService)
    Container.services.register(AsyncSchemaQueryService, PipelineAsyncSchemaQueryService)
    Container.planners.register(DataQueryPlanner, DefaultDataQueryPlanner)
    Container.planners.register(AsyncDataQueryPlanner, DefaultAsyncDataQueryPlanner)
    Container.planners.register(SchemaQueryPlanner, DefaultSchemaQueryPlanner)
    Container.planners.register(AsyncSchemaQueryPlanner, DefaultAsyncSchemaQueryPlanner)

    Container.executors.register(FinalDataQueryExecutor, PolarsFinalQueryDataExecutor)
    Container.executors.register(AsyncFinalDataQueryExecutor, AsyncPolarsFinalQueryDataExecutor)

    # Register default services, managers and executors for Commands
    Container.services.register(DataCommandService, PipelineDataCommandService)
    Container.services.register(AsyncDataCommandService, PipelineAsyncDataCommandService)
    Container.services.register(SchemaCommandService, PipelineSchemaCommandService)
    Container.services.register(AsyncSchemaCommandService, PipelineAsyncSchemaCommandService)
    Container.planners.register(DataCommandPlanner, DefaultDataCommandPlanner)
    Container.planners.register(AsyncDataCommandPlanner, DefaultAsyncDataCommandPlanner)
    Container.planners.register(SchemaCommandPlanner, DefaultSchemaCommandPlanner)
    Container.planners.register(AsyncSchemaCommandPlanner, DefaultAsyncSchemaCommandPlanner)

    # Register default services, managers and executors for Lock Commands
    Container.services.register(LockCommandService, PipelineLockCommandService)
    Container.services.register(AsyncLockCommandService, PipelineAsyncLockCommandService)
    Container.planners.register(LockCommandPlanner, DefaultLockCommandPlanner)
    Container.planners.register(AsyncLockCommandPlanner, DefaultAsyncLockCommandPlanner)

    # Register default services, managers and executors for Transaction Commands
    Container.services.register(TransactionCommandService, PipelineTransactionCommandService)
    Container.services.register(AsyncTransactionCommandService, PipelineAsyncTransactionCommandService)
    Container.planners.register(TransactionCommandPlanner, DefaultTransactionCommandPlanner)
    Container.planners.register(AsyncTransactionCommandPlanner, DefaultAsyncTransactionCommandPlanner)
