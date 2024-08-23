from typing import ClassVar

from amsdal_glue import init_default_containers
from amsdal_glue.initialize import init_pipeline_containers
from amsdal_glue.pipelines.manager import PipelineManager
from amsdal_glue.task_executors.background_executors import BackgroundSequentialExecutor
from amsdal_glue_core.common.executors.manager import ExecutorManager
from amsdal_glue_core.common.interfaces.connection_manager import ConnectionManager
from amsdal_glue_core.common.interfaces.runtime_manager import RuntimeManager
from amsdal_glue_core.common.services.commands import DataCommandService
from amsdal_glue_core.common.services.commands import LockCommandService
from amsdal_glue_core.common.services.commands import SchemaCommandService
from amsdal_glue_core.common.services.commands import TransactionCommandService
from amsdal_glue_core.common.services.queries import DataQueryService
from amsdal_glue_core.common.services.queries import SchemaQueryService
from amsdal_glue_core.containers import Container


class CQRSApplication:
    QUERY_CONTAINER_NAME: ClassVar[str] = 'query'
    COMMAND_CONTAINER_NAME: ClassVar[str] = 'command'

    def __init__(self) -> None:
        self.query_container = Container.define_sub_container(self.QUERY_CONTAINER_NAME)
        self.command_container = Container.define_sub_container(self.COMMAND_CONTAINER_NAME)

        init_pipeline_containers()
        init_default_containers(self.query_container)
        init_default_containers(self.command_container)

        self.pipeline = Container.managers.get(PipelineManager)
        self.pipeline.registry.register(self.QUERY_CONTAINER_NAME, self.query_container)
        self.pipeline.registry.register(self.COMMAND_CONTAINER_NAME, self.command_container)

        query_services = [
            SchemaQueryService,
            DataQueryService,
        ]
        command_services = [
            SchemaCommandService,
            DataCommandService,
            TransactionCommandService,
            LockCommandService,
        ]

        for service in query_services:
            # Query services uses only the query container
            self.pipeline.define(service, [self.QUERY_CONTAINER_NAME])

        for service in command_services:
            # Command services uses command container and then query container
            self.pipeline.define(service, [self.COMMAND_CONTAINER_NAME, self.QUERY_CONTAINER_NAME])

            # background executor for query container for these services
            executor_manager = self.query_container.managers.get(ExecutorManager)
            executor_manager.register_for_service(service, BackgroundSequentialExecutor)

    @property
    def query_connection_manager(self) -> ConnectionManager:
        return self.query_container.managers.get(ConnectionManager)

    @property
    def command_connection_manager(self) -> ConnectionManager:
        return self.command_container.managers.get(ConnectionManager)

    def shutdown(self) -> None:
        with Container.root():
            runtime = Container.managers.get(RuntimeManager)
            runtime.shutdown()

        self.query_connection_manager.disconnect_all()
        self.command_connection_manager.disconnect_all()
