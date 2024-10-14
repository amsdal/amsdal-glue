# mypy: disable-error-code="type-abstract"
from typing import ClassVar

from amsdal_glue_core.common.interfaces.connection_manager import ConnectionManager
from amsdal_glue_core.common.interfaces.runtime_manager import RuntimeManager
from amsdal_glue_core.common.services.commands import DataCommandService
from amsdal_glue_core.common.services.commands import LockCommandService
from amsdal_glue_core.common.services.commands import SchemaCommandService
from amsdal_glue_core.common.services.commands import TransactionCommandService
from amsdal_glue_core.common.services.queries import DataQueryService
from amsdal_glue_core.common.services.queries import SchemaQueryService

from amsdal_glue import Container
from amsdal_glue.initialize import init_default_containers
from amsdal_glue.initialize import init_pipeline_containers
from amsdal_glue.pipelines.manager import PipelineManager


class LakehouseApplication:
    """Lakehouse Application class to manage default and lakehouse containers.

    This class initializes and manages the default and lakehouse containers,
    registers services, and handles the shutdown process.

    Example:
        ```python
        from amsdal_glue.applications.lakehouse import LakehouseApplication

        app = LakehouseApplication()

        # Do usual operations via Container.services.get(service)
        ...

        # Shutdown the application
        app.shutdown()
        ```
    """

    DEFAULT_CONTAINER_NAME: ClassVar[str] = 'default'
    LAKEHOUSE_CONTAINER_NAME: ClassVar[str] = 'lakehouse'

    def __init__(self) -> None:
        """Initializes the LakehouseApplication with default and lakehouse containers.

        This method sets up the default and lakehouse containers, initializes
        pipeline containers, and registers services.

        Example:
            ```python
            from amsdal_glue.applications.lakehouse import LakehouseApplication

            app = LakehouseApplication()
            ```
        """
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

    @property
    def default_connection_manager(self) -> ConnectionManager:
        """Gets the connection manager for the default container.

        Returns:
            ConnectionManager: The connection manager for the default container.

        Example:
            ```python
            from amsdal_glue.applications.lakehouse import LakehouseApplication

            app = LakehouseApplication()
            app.default_connection_manager.register_connection_pool(
                DefaultConnectionPool(
                    PostgresConnection,
                    dsn='postgres://db_user:db_password@localhost:5433/default_db',
                ),
            )
            ```
        """
        return self.default_container.managers.get(ConnectionManager)

    @property
    def lakehouse_connection_manager(self) -> ConnectionManager:
        """Gets the connection manager for the lakehouse container.

        Returns:
            ConnectionManager: The connection manager for the lakehouse container.

        Example:
            ```python
            from amsdal_glue.applications.lakehouse import LakehouseApplication

            app = LakehouseApplication()
            app.lakehouse_connection_manager.register_connection_pool(
                DefaultConnectionPool(
                    PostgresConnection,
                    dsn='postgres://db_user:db_password@localhost:5433/lakehouse_db',
                ),
            )
            ```
        """
        return self.lakehouse_container.managers.get(ConnectionManager)

    def shutdown(self, *, skip_close_connections: bool = False) -> None:
        """Shuts down the application and disconnects all connections.

        This method shuts down the runtime manager and disconnects all
        connections unless `skip_close_connections` is True.

        Args:
            skip_close_connections (bool): If True, skips closing connections. Useful for testing.

        Example:
            ```python
            from amsdal_glue.applications.lakehouse import LakehouseApplication

            app = LakehouseApplication()
            app.shutdown(skip_close_connections=True)
            ```
        """

        with Container.root():
            runtime = Container.managers.get(RuntimeManager)
            runtime.shutdown()

        if skip_close_connections:
            return

        self.default_connection_manager.disconnect_all()
        self.lakehouse_connection_manager.disconnect_all()
