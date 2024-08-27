from typing import ClassVar

from amsdal_glue import Container
from amsdal_glue.initialize import init_default_containers
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


class LakehouseApp:
    DEFAULT_CONTAINER_NAME: ClassVar[str] = 'default'
    LAKEHOUSE_CONTAINER_NAME: ClassVar[str] = 'lakehouse'

    def __init__(self) -> None:
        self.default_container = Container.define_sub_container(self.DEFAULT_CONTAINER_NAME)
        self.lakehouse_container = Container.define_sub_container(self.LAKEHOUSE_CONTAINER_NAME)

        init_pipeline_containers()
        init_default_containers(self.default_container)
        init_default_containers(self.lakehouse_container)

        self.pipeline = Container.managers.get(PipelineManager)
        self.pipeline.registry.register(self.DEFAULT_CONTAINER_NAME, self.default_container)
        self.pipeline.registry.register(self.LAKEHOUSE_CONTAINER_NAME, self.lakehouse_container)

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
            self.pipeline.define(service, [self.DEFAULT_CONTAINER_NAME])

        for service in command_services:
            # Command services uses command container and then query container
            self.pipeline.define(service, [self.LAKEHOUSE_CONTAINER_NAME, self.DEFAULT_CONTAINER_NAME])

            # background executor for command container for these services
            executor_manager = self.default_container.managers.get(ExecutorManager)
            executor_manager.register_for_service(service, BackgroundSequentialExecutor)

    @property
    def default_connection_manager(self) -> ConnectionManager:
        return self.default_container.managers.get(ConnectionManager)

    @property
    def lakehouse_connection_manager(self) -> ConnectionManager:
        return self.lakehouse_container.managers.get(ConnectionManager)

    def shutdown(self) -> None:
        with Container.root():
            runtime = Container.managers.get(RuntimeManager)
            runtime.shutdown()

        self.default_connection_manager.disconnect_all()
        self.lakehouse_connection_manager.disconnect_all()
