# mypy: disable-error-code="type-abstract"
# Register core services, managers and executors

from amsdal_glue.pipelines.containers import SubContainer


def init_default_containers(container: SubContainer | None = None) -> None:
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
    from amsdal_glue.interfaces import DataCommandPlanner
    from amsdal_glue.interfaces import LockCommandPlanner
    from amsdal_glue.interfaces import SchemaCommandPlanner
    from amsdal_glue.interfaces import TransactionCommandPlanner
    from amsdal_glue.interfaces import FinalDataQueryExecutor
    from amsdal_glue.interfaces import ParallelExecutor
    from amsdal_glue.interfaces import SequentialExecutor
    from amsdal_glue.interfaces import DataCommandService
    from amsdal_glue.interfaces import LockCommandService
    from amsdal_glue.interfaces import SchemaCommandService
    from amsdal_glue.interfaces import TransactionCommandService
    from amsdal_glue.interfaces import ConnectionManager
    from amsdal_glue.interfaces import DataQueryService
    from amsdal_glue.interfaces import SchemaQueryService
    from amsdal_glue.interfaces import DataQueryPlanner
    from amsdal_glue.interfaces import SchemaQueryPlanner
    from amsdal_glue import Container as DefaultContainer
    from amsdal_glue import Singleton
    from amsdal_glue import DefaultConnectionManager

    from amsdal_glue.commands.planner.data_planner import DefaultDataCommandPlanner
    from amsdal_glue.commands.planner.lock_planner import DefaultLockCommandPlanner
    from amsdal_glue.commands.planner.schema_planner import DefaultSchemaCommandPlanner
    from amsdal_glue.commands.planner.transaction_planner import DefaultTransactionCommandPlanner
    from amsdal_glue.queries.executors.palars_final_query_executor import PolarsFinalQueryDataExecutor
    from amsdal_glue.queries.planner.data_query_planner import DefaultDataQueryPlanner
    from amsdal_glue.queries.planner.schema_query_planner import DefaultSchemaQueryPlanner
    from amsdal_glue.services.data_command import DefaultDataCommandService
    from amsdal_glue.services.data_query import DefaultDataQueryService
    from amsdal_glue.services.lock_command import DefaultLockCommandService
    from amsdal_glue.services.schema_command import DefaultSchemaCommandService
    from amsdal_glue.services.schema_query import DefaultSchemaQueryService
    from amsdal_glue.services.transaction_command import DefaultTransactionCommandService
    from amsdal_glue.task_executors.parallel_thread_executor import ThreadParallelExecutor
    from amsdal_glue.task_executors.sequential_sync_executor import SequentialSyncExecutor
    from amsdal_glue_core.common.executors.manager import ExecutorManager
    from amsdal_glue.managers.executor_manager import DefaultExecutorManager

    container = container or DefaultContainer

    if container is DefaultContainer:
        from amsdal_glue.interfaces import RuntimeManager
        from amsdal_glue import DefaultRuntimeManager

        container.managers.register(RuntimeManager, Singleton(DefaultRuntimeManager))

    container.managers.register(ExecutorManager, Singleton(DefaultExecutorManager))
    container.managers.register(ConnectionManager, Singleton(DefaultConnectionManager))
    container.executors.register(SequentialExecutor, SequentialSyncExecutor)
    container.executors.register(ParallelExecutor, ThreadParallelExecutor)

    # Register default services, managers and executors for Queries
    container.services.register(DataQueryService, DefaultDataQueryService)
    container.services.register(SchemaQueryService, DefaultSchemaQueryService)
    container.planners.register(DataQueryPlanner, DefaultDataQueryPlanner)
    container.planners.register(SchemaQueryPlanner, DefaultSchemaQueryPlanner)
    container.executors.register(FinalDataQueryExecutor, PolarsFinalQueryDataExecutor)

    # Register default services, managers and executors for Commands
    container.services.register(DataCommandService, DefaultDataCommandService)
    container.services.register(SchemaCommandService, DefaultSchemaCommandService)
    container.planners.register(DataCommandPlanner, DefaultDataCommandPlanner)
    container.planners.register(SchemaCommandPlanner, DefaultSchemaCommandPlanner)

    # Register default services, managers and executors for Lock Commands
    container.services.register(LockCommandService, DefaultLockCommandService)
    container.planners.register(LockCommandPlanner, DefaultLockCommandPlanner)

    # Register default services, managers and executors for Transaction Commands
    container.services.register(TransactionCommandService, DefaultTransactionCommandService)
    container.planners.register(TransactionCommandPlanner, DefaultTransactionCommandPlanner)


def init_pipeline_containers() -> None:
    from amsdal_glue.interfaces import DataCommandPlanner
    from amsdal_glue.interfaces import LockCommandPlanner
    from amsdal_glue.interfaces import SchemaCommandPlanner
    from amsdal_glue.interfaces import TransactionCommandPlanner
    from amsdal_glue.interfaces import FinalDataQueryExecutor
    from amsdal_glue.interfaces import ParallelExecutor
    from amsdal_glue.interfaces import SequentialExecutor
    from amsdal_glue.interfaces import DataCommandService
    from amsdal_glue.interfaces import LockCommandService
    from amsdal_glue.interfaces import SchemaCommandService
    from amsdal_glue.interfaces import TransactionCommandService
    from amsdal_glue.interfaces import DataQueryService
    from amsdal_glue.interfaces import SchemaQueryService
    from amsdal_glue.interfaces import DataQueryPlanner
    from amsdal_glue.interfaces import SchemaQueryPlanner
    from amsdal_glue import Container
    from amsdal_glue import Singleton

    from amsdal_glue.commands.planner.data_planner import DefaultDataCommandPlanner
    from amsdal_glue.commands.planner.lock_planner import DefaultLockCommandPlanner
    from amsdal_glue.commands.planner.schema_planner import DefaultSchemaCommandPlanner
    from amsdal_glue.commands.planner.transaction_planner import DefaultTransactionCommandPlanner
    from amsdal_glue.queries.executors.palars_final_query_executor import PolarsFinalQueryDataExecutor
    from amsdal_glue.queries.planner.data_query_planner import DefaultDataQueryPlanner
    from amsdal_glue.queries.planner.schema_query_planner import DefaultSchemaQueryPlanner
    from amsdal_glue.services.data_command import PipelineDataCommandService
    from amsdal_glue.services.data_query import PipelineDataQueryService
    from amsdal_glue.services.lock_command import PipelineLockCommandService
    from amsdal_glue.services.schema_command import PipelineSchemaCommandService
    from amsdal_glue.pipelines.manager import PipelineManager
    from amsdal_glue.services.schema_query import PipelineSchemaQueryService
    from amsdal_glue.services.transaction_command import PipelineTransactionCommandService
    from amsdal_glue.task_executors.parallel_process_executor import ProcessParallelExecutor
    from amsdal_glue.task_executors.sequential_sync_executor import SequentialSyncExecutor

    from amsdal_glue.interfaces import RuntimeManager
    from amsdal_glue import DefaultRuntimeManager

    Container.managers.register(RuntimeManager, Singleton(DefaultRuntimeManager))
    Container.managers.register(PipelineManager, Singleton(PipelineManager))

    Container.executors.register(SequentialExecutor, SequentialSyncExecutor)
    Container.executors.register(ParallelExecutor, ProcessParallelExecutor)

    # Register default services, managers and executors for Queries
    Container.services.register(DataQueryService, PipelineDataQueryService)
    Container.services.register(SchemaQueryService, PipelineSchemaQueryService)
    Container.planners.register(DataQueryPlanner, DefaultDataQueryPlanner)
    Container.planners.register(SchemaQueryPlanner, DefaultSchemaQueryPlanner)
    Container.executors.register(FinalDataQueryExecutor, PolarsFinalQueryDataExecutor)

    # Register default services, managers and executors for Commands
    Container.services.register(DataCommandService, PipelineDataCommandService)
    Container.services.register(SchemaCommandService, PipelineSchemaCommandService)
    Container.planners.register(DataCommandPlanner, DefaultDataCommandPlanner)
    Container.planners.register(SchemaCommandPlanner, DefaultSchemaCommandPlanner)

    # Register default services, managers and executors for Lock Commands
    Container.services.register(LockCommandService, PipelineLockCommandService)
    Container.planners.register(LockCommandPlanner, DefaultLockCommandPlanner)

    # Register default services, managers and executors for Transaction Commands
    Container.services.register(TransactionCommandService, PipelineTransactionCommandService)
    Container.planners.register(TransactionCommandPlanner, DefaultTransactionCommandPlanner)
