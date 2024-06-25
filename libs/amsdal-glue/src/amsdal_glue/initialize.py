# Register core services, managers and executors
from amsdal_glue_core.commands.planner.data_command_planner import DataCommandPlanner
from amsdal_glue_core.commands.planner.lock_command_planner import LockCommandPlanner
from amsdal_glue_core.commands.planner.schema_command_planner import SchemaCommandPlanner
from amsdal_glue_core.commands.planner.transaction_command_planner import TransactionCommandPlanner
from amsdal_glue_core.common.executors.interfaces import FinalDataQueryExecutor
from amsdal_glue_core.common.executors.interfaces import ParallelExecutor
from amsdal_glue_core.common.executors.interfaces import SequentialExecutor
from amsdal_glue_core.common.services.managers.connection import ConnectionManager
from amsdal_glue_core.containers import Container
from amsdal_glue_core.queries.planner.data_query_planner import DataQueryPlanner
from amsdal_glue_core.queries.planner.schema_query_planner import SchemaQueryPlanner

from amsdal_glue.commands.planner.data_planner import DefaultDataCommandPlanner
from amsdal_glue.commands.planner.lock_planner import DefaultLockCommandPlanner
from amsdal_glue.commands.planner.schema_planner import DefaultSchemaCommandPlanner
from amsdal_glue.commands.planner.transaction_planner import DefaultTransactionCommandPlanner
from amsdal_glue.queries.executors.palars_final_query_executor import PolarsFinalQueryDataExecutor
from amsdal_glue.queries.planner.data_query_planner import DefaultDataQueryPlanner
from amsdal_glue.queries.planner.schema_query_planner import DefaultSchemaQueryPlanner
from amsdal_glue.task_executors.parallel_thread_executor import ThreadParallelExecutor
from amsdal_glue.task_executors.sequential_sync_executor import SequentialSyncExecutor


def init_default_containers() -> None:
    Container.managers.register(ConnectionManager, ConnectionManager)
    Container.executors.register(SequentialExecutor, SequentialSyncExecutor)
    Container.executors.register(ParallelExecutor, ThreadParallelExecutor)

    # Register default services, managers and executors for Queries
    # Container.services.register(QueryService, DefaultQueryService)  # noqa: ERA001
    Container.planners.register(DataQueryPlanner, DefaultDataQueryPlanner)
    Container.planners.register(SchemaQueryPlanner, DefaultSchemaQueryPlanner)
    Container.executors.register(FinalDataQueryExecutor, PolarsFinalQueryDataExecutor)

    # Register default services, managers and executors for Commands
    # Container.services.register(DataCommandService, DefaultDataCommandService)  # noqa: ERA001
    # Container.services.register(SchemaCommandService, DefaultSchemaCommandService)  # noqa: ERA001
    Container.planners.register(DataCommandPlanner, DefaultDataCommandPlanner)
    Container.planners.register(SchemaCommandPlanner, DefaultSchemaCommandPlanner)

    # Register default services, managers and executors for Lock Commands
    # Container.services.register(LockCommandService, DefaultLockCommandService)  # noqa: ERA001
    Container.planners.register(LockCommandPlanner, DefaultLockCommandPlanner)

    # Register default services, managers and executors for Transaction Commands
    # Container.services.register(TransactionCommandService, DefaultTransactionCommandService)  # noqa: ERA001
    Container.planners.register(TransactionCommandPlanner, DefaultTransactionCommandPlanner)
