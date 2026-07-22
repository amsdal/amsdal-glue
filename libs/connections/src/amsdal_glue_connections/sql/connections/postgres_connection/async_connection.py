import logging
from copy import copy
from typing import Any
from typing import TYPE_CHECKING

from amsdal_glue_core.common.data_models.data import Data
from amsdal_glue_core.common.data_models.field_reference import Field
from amsdal_glue_core.common.data_models.field_reference import FieldReference
from amsdal_glue_core.common.data_models.query import QueryStatement
from amsdal_glue_core.common.data_models.schema import Schema
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.exceptions import AmsdalGlueError
from amsdal_glue_core.common.exceptions import ForeignKeyViolationError
from amsdal_glue_core.common.exceptions import UniqueViolationError
from amsdal_glue_core.common.interfaces.connection import AsyncConnectionBase
from amsdal_glue_core.common.operations.commands import LockCommand
from amsdal_glue_core.common.operations.commands import SchemaCommand
from amsdal_glue_core.common.operations.commands import TransactionCommand
from amsdal_glue_core.common.operations.mutations.data import DataMutation
from amsdal_glue_core.common.operations.mutations.schema import RegisterSchema
from amsdal_glue_core.common.operations.mutations.schema import SchemaMutation

from amsdal_glue_connections._sql_core import SqlGenerator
from amsdal_glue_connections.sql.connections.base_view_introspection import AsyncSchemaAssemblyMixin
from amsdal_glue_connections.sql.connections.postgres_connection.base import bind_params
from amsdal_glue_connections.sql.connections.postgres_connection.base import PostgresConnectionMixin
from amsdal_glue_connections.sql.connections.postgres_connection.sync_connection import _CONSTRAINT_COLUMNS
from amsdal_glue_connections.sql.connections.postgres_connection.sync_connection import _INDEX_COLUMNS
from amsdal_glue_connections.sql.connections.postgres_connection.sync_connection import _PROPERTY_COLUMNS
from amsdal_glue_connections.sql.connections.postgres_connection.sync_connection import PostgresSchemaAssemblyMixin
from amsdal_glue_connections.sql.schema_registry import TABLE_CONSTRAINT_REGISTRY
from amsdal_glue_connections.sql.schema_registry import TABLE_INDEX_REGISTRY
from amsdal_glue_connections.sql.schema_registry import TABLE_PROPERTY_REGISTRY
from amsdal_glue_connections.sql.schema_registry import TABLE_REGISTRY

if TYPE_CHECKING:
    import psycopg

logger = logging.getLogger(__name__)


class AsyncPostgresConnection(
    AsyncSchemaAssemblyMixin, PostgresSchemaAssemblyMixin, PostgresConnectionMixin, AsyncConnectionBase
):
    """
    PostgresConnection is responsible for managing connections and executing queries and commands on
    a PostgreSQL database.

    Example:
        Here is example of how to create a connection to a PostgreSQL database:

        ```python
        from amsdal_glue_connections import AsyncPostgresConnection

        connection = AsyncPostgresConnection()
        await connection.connect(
            dsn='postgresql://user:password@localhost:5432/mydatabase',
            schema='public',
            timezone='UTC',
        )
        ```

        Note, it's also possible to put any extra connection parameters as keyword arguments supported by
        [psycopg](https://www.psycopg.org/psycopg3/docs/api/connections.html#psycopg.Connection.connect).
        Also, be aware that the `autocommit` parameter is set to `True` by default.

        Most of the time, you will use the [ConnectionManager][amsdal_glue.ConnectionManager]
        to manage connections instead of creating a connection directly.
    """

    def __init__(self) -> None:
        self._connection: psycopg.AsyncConnection | None = None
        self._generator = SqlGenerator('postgresql', param_style='format')
        self._schema = 'public'
        super().__init__()

    @property
    async def is_connected(self) -> bool:
        """
        Checks if the connection to the PostgreSQL database is established.

        Returns:
            bool: True if connected, False otherwise.
        """
        return self._connection is not None

    @property
    async def is_alive(self) -> bool:
        """
        Checks if the connection to the PostgreSQL database is alive.

        Returns:
            bool: True if alive, False otherwise.
        """
        try:
            import psycopg
        except ImportError:
            _msg = (
                '"psycopg" package is required for PostgresConnection. '
                'Use "pip install amsdal-glue-connections[postgres]" to install it.'
            )
            raise ImportError(_msg) from None

        if not await self.is_connected:
            return False

        try:
            await self._connection.execute('SELECT 1')  # type: ignore[union-attr]
        except psycopg.Error:
            return False

        return True

    @property
    def connection(self) -> 'psycopg.AsyncConnection':
        """
        Gets the current connection to the PostgreSQL database.

        Returns:
            psycopg.AsyncConnection: The current connection.

        Raises:
            ConnectionError: If the connection is not established.
        """
        if self._connection is None:
            msg = 'Connection not established'
            raise ConnectionError(msg)

        return self._connection

    async def connect(
        self,
        dsn: str = '',
        schema: str | None = None,
        timezone: str = 'UTC',
        *,
        autocommit: bool = True,
        **kwargs: Any,
    ) -> None:
        """
        Establishes a connection to the PostgreSQL database.

        Args:
            dsn (str): The Data Source Name for the connection.
            schema (str | None): The default schema to be used for the connection. If None,
                                 the default schema usually is 'public'.
            timezone (str): The timezone to be used for the connection.
            autocommit (bool): Whether to enable autocommit mode.
            **kwargs: Additional connection parameters.

        Raises:
            ConnectionError: If the connection is already established.
            ImportError: If the 'psycopg' package is not installed.
        """
        try:
            import psycopg
        except ImportError:
            _msg = (
                '"psycopg" package is required for PostgresConnection. '
                'Use "pip install amsdal-glue-connections[async-postgres]" to install it.'
            )
            raise ImportError(_msg) from None

        if self._connection is not None:
            msg = 'Connection already established'
            raise ConnectionError(msg)

        from psycopg import sql

        self._connection = await psycopg.AsyncConnection.connect(dsn, autocommit=autocommit, **kwargs)
        await self._connection.execute("SELECT set_config('TimeZone', %s, false)", [timezone])

        self._schema = schema or 'public'

        if schema:
            # ``SET`` cannot take a bind parameter, so the schema identifier is quoted via
            # psycopg's SQL composition instead of being f-string interpolated (injection-safe).
            await self._connection.execute(sql.SQL('SET search_path TO {}').format(sql.Identifier(schema)))

    async def disconnect(self) -> None:
        """
        Closes the connection to the PostgreSQL database.
        """
        await self.connection.close()
        self._connection = None

    async def query(self, query: QueryStatement) -> list[Data]:
        """
        Executes a query on the PostgreSQL database.

        Args:
            query (QueryStatement): The query to be executed.

        Returns:
            list[Data]: The result of the query execution.

        Raises:
            ConnectionError: If there is an error executing the query.
        """
        _stmt, _params = self._generator.compile_query(query)

        try:
            cursor = await self.execute(_stmt, *_params)
        except Exception as exc:
            logger.debug('Error executing query: %s with params: %s', _stmt, _params)
            msg = f'Query failed: {exc}'
            raise ConnectionError(msg) from exc

        fields = []

        for column in cursor.description or []:
            if column[0] in fields:
                msg = f'Column name {column[0]} is duplicated'
                raise ValueError(msg)
            fields.append(column[0])

        result = [self.build_data(dict(zip(fields, row, strict=True))) for row in await cursor.fetchall()]
        await cursor.close()

        return result

    async def query_schema(self, query: QueryStatement) -> list[Schema]:
        """
        Queries the schema of the PostgreSQL database.

        Args:
            query (QueryStatement): The query statement referencing the registry view.

        Returns:
            list[Schema]: The result of the schema query.
        """
        return await self.introspect_schema(query)

    async def introspect_schema(self, query: QueryStatement) -> list[Schema]:
        await self._ensure_schema_views()

        ref_name = query.table.alias or query.table.name if isinstance(query.table, SchemaReference) else TABLE_REGISTRY

        resolved = copy(query)
        resolved.only = [FieldReference(field=Field(name='table_name'), table_name=ref_name)]

        sql, params = self._generator.compile_query(resolved)
        cursor = await self.execute(sql, *params)
        rows = await cursor.fetchall()
        await cursor.close()

        table_names = self._dedupe_names(rows)

        if not table_names:
            return []

        # One bound registry query per catalog aspect -- a constant number of statements regardless
        # of how many tables match. Every fact is reconstructed from the canonical views (no per-table
        # ``information_schema`` / ``pg_get_serial_sequence`` reads), so there is no N+1 catalog storm.
        property_rows = await self._run_registry(TABLE_PROPERTY_REGISTRY, _PROPERTY_COLUMNS, table_names)
        constraint_rows = await self._run_registry(TABLE_CONSTRAINT_REGISTRY, _CONSTRAINT_COLUMNS, table_names)
        index_rows = await self._run_registry(TABLE_INDEX_REGISTRY, _INDEX_COLUMNS, table_names)

        return self._build_schemas(
            table_names,
            self._group(property_rows),
            self._group(constraint_rows),
            self._group(index_rows),
        )

    async def _ensure_schema_views(self) -> None:
        # The view DDL is idempotent (CREATE OR REPLACE), so it is re-issued on every call rather
        # than gated by a per-object flag that would go stale across disconnect()/connect() cycles.
        for stmt in self._build_registry_view_sql(self._schema).values():
            await self.execute(stmt.as_string(self.connection))

    async def run_mutations(self, mutations: list[DataMutation]) -> list[list[Data] | None]:
        """
        Executes a list of data mutations on the PostgreSQL database.

        Args:
            mutations (list[DataMutation]): The list of data mutations to be executed.

        Returns:
            list[list[Data] | None]: The result of the data mutations execution.
        """
        return [await self._run_mutation(mutation) for mutation in mutations]

    async def _run_mutation(self, mutation: DataMutation) -> list[Data] | None:
        _stmt, _params = self._generator.compile_mutation(mutation)

        try:
            await self.execute(_stmt, *_params)
        except AmsdalGlueError:
            # Typed glue errors (e.g. UniqueViolationError) bubble unchanged.
            raise
        except Exception as exc:
            logger.debug('Error executing mutation: %s with params: %s', _stmt, _params)
            msg = f'Mutation failed: {exc}'
            raise ConnectionError(msg) from exc
        return None

    async def run_schema_command(self, command: SchemaCommand) -> list[Schema | None]:
        """
        Executes a schema command on the PostgreSQL database.

        Args:
            command (SchemaCommand): The schema command to be executed.

        Returns:
            list[Schema | None]: The result of the schema command execution.
        """
        result: list[Schema | None] = []

        for mutation in command.mutations:
            data = await self._run_schema_mutation(mutation)
            result.append(data)

        return result

    async def execute(self, query: str, *args: Any) -> 'psycopg.AsyncCursor':
        """
        Executes a query on the PostgreSQL database.

        Args:
            query (str): The query to be executed.
            *args (Any): The query parameters.

        Returns:
            psycopg.Cursor: The cursor for the executed query.

        Raises:
            ConnectionError: If there is an error executing the query.
        """
        import psycopg

        args = bind_params(args)

        try:
            if self.debug_queries:
                self._queries.append(query)
                self._queries_params.append(args)

            cursor = await self.connection.execute(query, args)
        except psycopg.errors.UniqueViolation as exc:
            raise UniqueViolationError(str(exc)) from exc
        except psycopg.errors.ForeignKeyViolation as exc:
            raise ForeignKeyViolationError(str(exc)) from exc
        except psycopg.Error as exc:
            msg = f'Error executing SQL: {query} with args: {args}. Exception: {exc}'
            raise ConnectionError(msg) from exc
        return cursor

    async def acquire_lock(self, lock: LockCommand) -> Any:
        """
        Acquires a lock on the PostgreSQL database via ``compile_lock_command``.

        Args:
            lock (LockCommand): The lock command to be executed.

        Returns:
            Any: The result of the lock acquisition.
        """
        sql, params = self._generator.compile_lock_command(lock)
        await self.execute(sql, *params)
        return True

    async def release_lock(self, lock: LockCommand) -> Any:
        """
        Releases a lock on the PostgreSQL database via ``compile_lock_command``.

        A TRANSACTION-scoped lock (table lock or ``pg_advisory_xact_lock``) CANNOT be released
        explicitly — Postgres holds it until COMMIT/ROLLBACK and offers no unlock counterpart. The
        Rust generator raises ``UnsupportedFeatureError`` for such a release, and that error is
        propagated: asking to release a transaction-scoped lock is a caller mistake (the lock is not
        released early, so silently returning success would be misleading). Only SESSION-scoped
        advisory locks have a real unlock.

        Args:
            lock (LockCommand): The lock command to be released.

        Returns:
            Any: The result of the lock release.
        """
        sql, params = self._generator.compile_lock_command(lock)
        await self.execute(sql, *params)
        return True

    async def commit_transaction(self, transaction: TransactionCommand | str | None) -> Any:
        """
        Commits a transaction on the PostgreSQL database.

        Args:
            transaction (TransactionCommand | str | None): The transaction to be committed.

        Returns:
            Any: The result of the transaction commit.
        """
        if isinstance(transaction, TransactionCommand) and transaction.parent_transaction_id:
            return True

        await self.execute('COMMIT')
        return True

    async def rollback_transaction(self, transaction: TransactionCommand | str | None) -> Any:
        """
        Rolls back a transaction on the PostgreSQL database.

        Args:
            transaction (TransactionCommand | str | None): The transaction to be rolled back.

        Returns:
            Any: The result of the transaction rollback.
        """
        if isinstance(transaction, TransactionCommand) and transaction.parent_transaction_id:
            await self.execute(f'ROLLBACK TO SAVEPOINT "{transaction.transaction_id}"')
            return True

        await self.execute('ROLLBACK')
        return True

    async def begin_transaction(self, transaction: TransactionCommand | str | None) -> Any:  # pragma: no cover
        """
        Begins a transaction on the PostgreSQL database.

        Args:
            transaction (TransactionCommand | str | None): The transaction to be begun.

        Returns:
            Any: The result of the transaction begin.
        """
        if isinstance(transaction, TransactionCommand) and transaction.parent_transaction_id:
            await self.execute(f'SAVEPOINT "{transaction.transaction_id}"')
            return True

        await self.execute('BEGIN')
        return True

    async def revert_transaction(self, transaction: TransactionCommand | str | None) -> Any:  # pragma: no cover
        """
        Reverts a transaction on the PostgreSQL database.

        Args:
            transaction (TransactionCommand | str | None): The transaction to be reverted.

        Returns:
            Any: The result of the transaction revert.
        """
        return await self.rollback_transaction(transaction)

    async def _run_schema_mutation(self, migration: SchemaMutation) -> Schema | None:
        sql_params_list = self._generator.compile_schema_mutation(migration)

        for sql, params in sql_params_list:
            await self.execute(sql, *params)

        if isinstance(migration, RegisterSchema):
            return migration.schema
        return None
