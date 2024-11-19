# mypy: disable-error-code="type-abstract"
from typing import ClassVar

from amsdal_glue_core.common.executors.manager import AsyncExecutorManager
from amsdal_glue_core.common.executors.manager import ExecutorManager
from amsdal_glue_core.common.interfaces.connection_manager import AsyncConnectionManager
from amsdal_glue_core.common.interfaces.connection_manager import ConnectionManager
from amsdal_glue_core.common.interfaces.runtime_manager import RuntimeManager
from amsdal_glue_core.common.services.commands import AsyncDataCommandService
from amsdal_glue_core.common.services.commands import AsyncLockCommandService
from amsdal_glue_core.common.services.commands import AsyncSchemaCommandService
from amsdal_glue_core.common.services.commands import AsyncTransactionCommandService
from amsdal_glue_core.common.services.commands import DataCommandService
from amsdal_glue_core.common.services.commands import LockCommandService
from amsdal_glue_core.common.services.commands import SchemaCommandService
from amsdal_glue_core.common.services.commands import TransactionCommandService
from amsdal_glue_core.common.services.queries import AsyncDataQueryService
from amsdal_glue_core.common.services.queries import AsyncSchemaQueryService
from amsdal_glue_core.common.services.queries import DataQueryService
from amsdal_glue_core.common.services.queries import SchemaQueryService
from amsdal_glue_core.containers import Container

from amsdal_glue import init_default_containers
from amsdal_glue.initialize import init_pipeline_containers
from amsdal_glue.pipelines.manager import PipelineManager
from amsdal_glue.task_executors.background_executors import BackgroundAsyncSequentialExecutor
from amsdal_glue.task_executors.background_executors import BackgroundSequentialExecutor


class CQRSApplication:
    """CQRS Application class to manage command and query containers.

    This class initializes and manages the command and query containers,
    registers services, and handles the shutdown process.

    Example:
        ```python
        from amsdal_glue.applications.cqrs import CQRSApplication

        app = CQRSApplication()

        # Do usual operations via Container.services.get(service)
        ...

        # Shutdown the application
        app.shutdown()"""

    QUERY_CONTAINER_NAME: ClassVar[str] = 'query'
    COMMAND_CONTAINER_NAME: ClassVar[str] = 'command'

    def __init__(self) -> None:
        """Initializes the CQRSApplication with command and query containers.

        This method sets up the command and query containers, initializes
        pipeline containers, and registers services.

        Example:
            ```python
            from amsdal_glue.applications.cqrs import CQRSApplication

            app = CQRSApplication()
            ```
        """
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
        """Gets the connection manager for the query container.

        Returns:
            ConnectionManager: The connection manager for the query container.

        Example:
            ```python
            from amsdal_glue.applications.cqrs import CQRSApplication

            app = CQRSApplication()
            app.query_connection_manager.register_connection_pool(
                DefaultConnectionPool(
                    PostgresConnection,
                    dsn='postgres://db_user:db_password@localhost:5433/read_db',
                ),
            )
            ```
        """
        return self.query_container.managers.get(ConnectionManager)

    @property
    def command_connection_manager(self) -> ConnectionManager:
        """Gets the connection manager for the command container.

        Returns:
            ConnectionManager: The connection manager for the command container.

        Example:
            ```python
            from amsdal_glue.applications.cqrs import CQRSApplication

            app = CQRSApplication()
            app.command_connection_manager.register_connection_pool(
                DefaultConnectionPool(
                    PostgresConnection,
                    dsn='postgres://db_user:db_password@localhost:5433/write_db',
                ),
            )
            ```
        """

        return self.command_container.managers.get(ConnectionManager)

    def shutdown(self, *, skip_close_connections: bool = False) -> None:
        """Shuts down the application and disconnects all connections.

        This method shuts down the runtime manager and disconnects all
        connections unless `skip_close_connections` is True.

        Args:
            skip_close_connections (bool): If True, skips closing connections. Useful for testing.

        Example:
            ```python
            from amsdal_glue.applications.cqrs import CQRSApplication

            app = CQRSApplication()
            app.shutdown(skip_close_connections=True)
            ```
        """
        with Container.root():
            runtime = Container.managers.get(RuntimeManager)
            runtime.shutdown()

        if skip_close_connections:
            return

        self.query_connection_manager.disconnect_all()
        self.command_connection_manager.disconnect_all()


class AsyncCQRSApplication:
    """CQRS Application class to manage command and query containers.

    This class initializes and manages the command and query containers,
    registers services, and handles the shutdown process.

    Example:
        ```python
        from amsdal_glue.applications.cqrs import AsyncCQRSApplication

        app = AsyncCQRSApplication()

        # Do usual operations via Container.services.get(service)
        ...

        # Shutdown the application
        await app.shutdown()"""

    QUERY_CONTAINER_NAME: ClassVar[str] = 'query'
    COMMAND_CONTAINER_NAME: ClassVar[str] = 'command'

    def __init__(self) -> None:
        """Initializes the CQRSApplication with command and query containers.

        This method sets up the command and query containers, initializes
        pipeline containers, and registers services.

        Example:
            ```python
            from amsdal_glue.applications.cqrs import AsyncCQRSApplication

            app = AsyncCQRSApplication()
            ```
        """
        self.query_container = Container.define_sub_container(self.QUERY_CONTAINER_NAME)
        self.command_container = Container.define_sub_container(self.COMMAND_CONTAINER_NAME)

        init_pipeline_containers()
        init_default_containers(self.query_container)
        init_default_containers(self.command_container)

        self.pipeline = Container.managers.get(PipelineManager)
        self.pipeline.registry.register(self.QUERY_CONTAINER_NAME, self.query_container)
        self.pipeline.registry.register(self.COMMAND_CONTAINER_NAME, self.command_container)

        query_services = [
            AsyncSchemaQueryService,
            AsyncDataQueryService,
        ]
        command_services = [
            AsyncSchemaCommandService,
            AsyncDataCommandService,
            AsyncTransactionCommandService,
            AsyncLockCommandService,
        ]

        for service in query_services:
            # Query services uses only the query container
            self.pipeline.define(service, [self.QUERY_CONTAINER_NAME])

        for service in command_services:
            # Command services uses command container and then query container
            self.pipeline.define(service, [self.COMMAND_CONTAINER_NAME, self.QUERY_CONTAINER_NAME])

            # background executor for query container for these services
            executor_manager = self.query_container.managers.get(AsyncExecutorManager)
            executor_manager.register_for_service(service, BackgroundAsyncSequentialExecutor)

    @property
    def query_connection_manager(self) -> AsyncConnectionManager:
        """Gets the connection manager for the query container.

        Returns:
            AsyncConnectionManager: The connection manager for the query container.

        Example:
            ```python
            from amsdal_glue.applications.cqrs import AsyncCQRSApplication

            app = AsyncCQRSApplication()
            app.query_connection_manager.register_connection_pool(
                DefaultAsyncConnectionPool(
                    PostgresAsyncConnection,
                    dsn='postgres://db_user:db_password@localhost:5433/read_db',
                ),
            )
            ```
        """
        return self.query_container.managers.get(AsyncConnectionManager)

    @property
    def command_connection_manager(self) -> AsyncConnectionManager:
        """Gets the connection manager for the command container.

        Returns:
            AsyncConnectionManager: The connection manager for the command container.

        Example:
            ```python
            from amsdal_glue.applications.cqrs import AsyncCQRSApplication

            app = AsyncCQRSApplication()
            app.command_connection_manager.register_connection_pool(
                DefaultAsyncConnectionPool(
                    PostgresAsyncConnection,
                    dsn='postgres://db_user:db_password@localhost:5433/write_db',
                ),
            )
            ```
        """

        return self.command_container.managers.get(AsyncConnectionManager)

    async def shutdown(self, *, skip_close_connections: bool = False) -> None:
        """Shuts down the application and disconnects all connections.

        This method shuts down the runtime manager and disconnects all
        connections unless `skip_close_connections` is True.

        Args:
            skip_close_connections (bool): If True, skips closing connections. Useful for testing.

        Example:
            ```python
            from amsdal_glue.applications.cqrs import AsyncCQRSApplication

            app = AsyncCQRSApplication()
            await app.shutdown(skip_close_connections=True)
            ```
        """
        with Container.root():
            runtime = Container.managers.get(RuntimeManager)
            runtime.shutdown()

        if skip_close_connections:
            return

        await self.query_connection_manager.disconnect_all()
        await self.command_connection_manager.disconnect_all()
