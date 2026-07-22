import logging
import sqlite3
import uuid
from copy import copy
from datetime import date
from datetime import datetime
from decimal import Decimal
from pathlib import Path
from typing import Any
from typing import TYPE_CHECKING

from amsdal_glue_core.common.data_models.data import Data
from amsdal_glue_core.common.data_models.data import DataInput
from amsdal_glue_core.common.data_models.field_reference import Field
from amsdal_glue_core.common.data_models.field_reference import FieldReference
from amsdal_glue_core.common.data_models.query import QueryStatement
from amsdal_glue_core.common.data_models.schema import Schema
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.enums import Version
from amsdal_glue_core.common.exceptions import AmsdalGlueError
from amsdal_glue_core.common.expressions.field_reference import FieldReferenceExpression
from amsdal_glue_core.common.interfaces.connection import AsyncConnectionBase
from amsdal_glue_core.common.operations.commands import LockCommand
from amsdal_glue_core.common.operations.commands import SchemaCommand
from amsdal_glue_core.common.operations.commands import TransactionCommand
from amsdal_glue_core.common.operations.mutations.data import DataMutation
from amsdal_glue_core.common.operations.mutations.data import InsertFromSelect
from amsdal_glue_core.common.operations.mutations.data import UpdateData
from amsdal_glue_core.common.operations.mutations.schema import AddConstraint
from amsdal_glue_core.common.operations.mutations.schema import AddIndex
from amsdal_glue_core.common.operations.mutations.schema import AddProperty
from amsdal_glue_core.common.operations.mutations.schema import DeleteConstraint
from amsdal_glue_core.common.operations.mutations.schema import DeleteProperty
from amsdal_glue_core.common.operations.mutations.schema import DeleteSchema
from amsdal_glue_core.common.operations.mutations.schema import RegisterSchema
from amsdal_glue_core.common.operations.mutations.schema import RenameProperty
from amsdal_glue_core.common.operations.mutations.schema import RenameSchema
from amsdal_glue_core.common.operations.mutations.schema import SchemaMutation
from amsdal_glue_core.common.operations.mutations.schema import UpdateProperty

from amsdal_glue_connections._sql_core import SqlGenerator
from amsdal_glue_connections.sql.connections.base_view_introspection import AsyncSchemaAssemblyMixin
from amsdal_glue_connections.sql.connections.sqlite_connection.base import bind_params
from amsdal_glue_connections.sql.connections.sqlite_connection.base import SqliteConnectionMixin
from amsdal_glue_connections.sql.connections.sqlite_connection.sync_connection import _CONSTRAINT_COLUMNS
from amsdal_glue_connections.sql.connections.sqlite_connection.sync_connection import _INDEX_COLUMNS
from amsdal_glue_connections.sql.connections.sqlite_connection.sync_connection import _PROPERTY_COLUMNS
from amsdal_glue_connections.sql.connections.sqlite_connection.sync_connection import _SQLITE_MAX_IN
from amsdal_glue_connections.sql.connections.sqlite_connection.sync_connection import SqliteSchemaAssemblyMixin
from amsdal_glue_connections.sql.schema_registry import TABLE_CONSTRAINT_REGISTRY
from amsdal_glue_connections.sql.schema_registry import TABLE_INDEX_REGISTRY
from amsdal_glue_connections.sql.schema_registry import TABLE_PROPERTY_REGISTRY
from amsdal_glue_connections.sql.schema_registry import TABLE_REGISTRY

if TYPE_CHECKING:
    import aiosqlite

logger = logging.getLogger(__name__)


class AsyncSqliteConnection(
    AsyncSchemaAssemblyMixin, SqliteSchemaAssemblyMixin, SqliteConnectionMixin, AsyncConnectionBase
):
    # `SchemaAssemblyMixin._run_registry` hook: chunk IN-lists at `_SQLITE_MAX_IN` (see comment on
    # that constant in the sync connection) instead of issuing one unbounded `IN (...)` per table.
    _MAX_IN_PARAMS = _SQLITE_MAX_IN

    def __init__(self) -> None:
        self._connection: aiosqlite.Connection | None = None
        self._generator = SqlGenerator('sqlite', param_style='qmark')
        super().__init__()

    @property
    async def is_connected(self) -> bool:
        """
        Checks if the connection to the SQLite database is established.

        Returns:
            bool: True if connected, False otherwise.
        """
        return self._connection is not None

    @property
    async def is_alive(self) -> bool:
        """
        Checks if the connection to the SQLite database is alive.

        Returns:
            bool: True if alive, False otherwise.
        """
        try:
            import aiosqlite
        except ImportError:
            _msg = (
                '"aiosqlite" package is required for AsyncSqliteConnection. '
                'Use "pip install amsdal-glue-connections[async-sqlite]" to install it.'
            )
            raise ImportError(_msg) from None

        if not self._connection:
            return False

        try:
            await self._connection.execute('SELECT 1')
        except aiosqlite.Error:
            return False

        return True

    @property
    def connection(self) -> 'aiosqlite.Connection':
        """
        Gets the current SQLite connection.

        Returns:
            aiosqlite.Connection: The current SQLite connection.

        Raises:
            ConnectionError: If the connection is not established.
        """
        if self._connection is None:
            msg = 'Connection not established'
            raise ConnectionError(msg)

        return self._connection

    async def connect(self, db_path: Path, *, check_same_thread: bool = False, **kwargs: Any) -> None:
        """
        Establishes a connection to the SQLite database.

        Args:
            db_path (Path): The path to the SQLite database file.
            check_same_thread (bool, optional): Whether to check the same thread. Defaults to False.
            **kwargs (Any): Additional arguments for the SQLite connection.

        Raises:
            ConnectionError: If the connection is already established.
        """
        try:
            import aiosqlite
        except ImportError:
            _msg = (
                '"aiosqlite" package is required for AsyncSqliteConnection. '
                'Use "pip install amsdal-glue-connections[async-sqlite]" to install it.'
            )
            raise ImportError(_msg) from None

        if self._connection is not None:
            msg = 'Connection already established'
            raise ConnectionError(msg)

        # date/datetime adapters are registered once, module-level, in base.py (single source of
        # truth, matching the Rust value serialisation). Only the read-back converters are per-connection.
        sqlite3.register_converter('DATE', lambda val: date.fromisoformat(val.decode()))
        sqlite3.register_converter('TIMESTAMP', lambda val: datetime.fromisoformat(val.decode()))
        # A TIMESTAMPTZ-declared column stores a datetime the same way TIMESTAMP does; register the
        # converter under its declared-type name too so read-back re-hydrates a Python datetime
        # (``fromisoformat`` restores the tzinfo offset) instead of leaving it a raw ISO string.
        sqlite3.register_converter('TIMESTAMPTZ', lambda val: datetime.fromisoformat(val.decode()))
        # DECIMAL_TEXT is the TEXT-affinity SQLite rendering of DecimalType; re-hydrate the stored
        # decimal string back into an exact Decimal so glue returns a typed value, not a str.
        sqlite3.register_converter('DECIMAL_TEXT', lambda val: Decimal(val.decode()))

        Path(db_path).parent.mkdir(parents=True, exist_ok=True)

        # Enable PARSE_DECLTYPES so the DATE/TIMESTAMP converters above actually fire on read-back.
        # aiosqlite forwards detect_types to the underlying sqlite3.connect.
        # Respect a caller-supplied detect_types (only default it when absent).
        kwargs.setdefault('detect_types', sqlite3.PARSE_DECLTYPES)

        self._db_path = Path(db_path)
        self._connection = await aiosqlite.connect(db_path, check_same_thread=check_same_thread, **kwargs)
        self._connection.isolation_level = None  # disable implicit transaction opening

    async def disconnect(self) -> None:
        """
        Closes the connection to the SQLite database.
        """
        await self.connection.close()
        self._connection = None

    async def query(self, query: QueryStatement) -> list[Data]:
        """
        Executes a query on the SQLite database.

        Args:
            query (QueryStatement): The query to be executed.

        Returns:
            list[Data]: The result of the query execution.

        Raises:
            ConnectionError: If there is an error executing the query.
            ValueError: If a column name is duplicated.
        """
        _stmt, _params = self._generator.compile_query(query)

        try:
            cursor = await self.execute(_stmt, *_params)
        except Exception as exc:
            msg = f'Error "{exc}" raised during executing query: {_stmt} with params: {_params}'
            raise ConnectionError(msg) from exc

        fields = []

        for column in cursor.description:
            if column[0] in fields:
                msg = f'Column name {column[0]} is duplicated'
                raise ValueError(msg)
            fields.append(column[0])

        result = [self.build_data(dict(zip(fields, row, strict=True))) for row in await cursor.fetchall()]
        await cursor.close()

        return result

    async def query_schema(self, query: QueryStatement) -> list[Schema]:
        """
        Queries the schema of the SQLite database.

        Args:
            query (QueryStatement): The query statement referencing the registry view.

        Returns:
            list[Schema]: The list of schemas matching the filters.
        """
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

        # One bound registry query per catalog aspect plus one batched DDL read -- a constant,
        # small number of statements regardless of how many tables match (no per-table PRAGMA
        # N+1). Beyond `_SQLITE_MAX_IN` tables, `_run_registry`/`_batch_ddls` transparently chunk
        # the IN-list to stay under SQLite's bound-parameter ceiling.
        property_rows = await self._run_registry(TABLE_PROPERTY_REGISTRY, _PROPERTY_COLUMNS, table_names)
        index_rows = await self._run_registry(TABLE_INDEX_REGISTRY, _INDEX_COLUMNS, table_names)
        constraint_rows = await self._run_registry(TABLE_CONSTRAINT_REGISTRY, _CONSTRAINT_COLUMNS, table_names)
        table_ddls, index_ddls = await self._batch_ddls(table_names)

        return self._build_schemas(
            table_names,
            self._group(property_rows),
            self._group(constraint_rows),
            self._group(index_rows),
            table_ddls,
            index_ddls,
        )

    async def _batch_ddls(self, names: list[str]) -> tuple[dict[str, str], dict[str, str]]:
        """Read every table and index DDL for `names` from ``sqlite_master`` (async, chunked).

        Returns ``(table_ddl_by_name, index_ddl_by_name)``. `names` is bound twice per query (table
        match + index match), so this chunks at `_SQLITE_MAX_IN` -- 2 * 400 = 800 bound params per
        statement, under `SQLITE_MAX_VARIABLE_NUMBER`'s lowest observed default of 999.
        """
        table_ddls: dict[str, str] = {}
        index_ddls: dict[str, str] = {}
        for start in range(0, len(names), _SQLITE_MAX_IN):
            chunk = names[start : start + _SQLITE_MAX_IN]
            cursor = await self.execute(self._batch_ddls_query(chunk), *chunk, *chunk)
            self._collect_ddl_rows(await cursor.fetchall(), table_ddls, index_ddls)
            await cursor.close()
        return table_ddls, index_ddls

    async def _ensure_schema_views(self) -> None:
        # The view DDL is idempotent (CREATE ... IF NOT EXISTS), so it is re-issued on every call
        # rather than gated by a per-object flag that would go stale across disconnect()/connect()
        # cycles (temporary views are per-connection, so a reconnect must recreate them).
        for sql in self._REGISTRY_VIEW_SQL.values():
            await self.execute(sql)

    async def run_mutations(self, mutations: list[DataMutation]) -> list[list[Data] | None]:
        """
        Runs a list of data mutations on the SQLite database.

        Args:
            mutations (list[DataMutation]): The list of data mutations to be executed.

        Returns:
            list[list[Data] | None]: The result of each mutation execution.
        """

        return [(await self._run_mutation(mutation)) for mutation in mutations]

    async def _run_mutation(self, mutation: DataMutation) -> list[Data] | None:
        _stmt, _params = self._generator.compile_mutation(mutation)

        try:
            await self.execute(_stmt, *_params)
        except AmsdalGlueError:
            # Typed glue errors (e.g. UniqueViolationError) bubble unchanged.
            raise
        except Exception as exc:
            msg = f'Mutation failed: {exc}'
            raise ConnectionError(msg) from exc
        return None

    async def run_schema_command(self, command: SchemaCommand) -> list[Schema | None]:
        """
        Runs a schema command on the SQLite database.

        Args:
            command (SchemaCommand): The schema command to be executed.

        Returns:
            list[Schema | None]: The result of each schema mutation.
        """

        result: list[Schema | None] = []

        for mutation in command.mutations:
            data = await self._run_schema_mutation(mutation)
            result.append(data)

        return result

    async def execute(self, query: str, *args: Any) -> 'aiosqlite.Cursor':
        """
        Executes a query on the SQLite database.

        Args:
            query (str): The query to be executed.
            *args (Any): The arguments for the query.

        Returns:
            aiosqlite.Cursor: The cursor for the executed query.

        Raises:
            ConnectionError: If there is an error executing the query.
        """
        try:
            import aiosqlite
        except ImportError:
            _msg = (
                '"aiosqlite" package is required for AsyncSqliteConnection. '
                'Use "pip install amsdal-glue-connections[async-sqlite]" to install it.'
            )
            raise ImportError(_msg) from None

        cursor = await self.connection.cursor()
        args = bind_params(args)

        try:
            if self.debug_queries:
                self._queries.append(query)
                self._queries_params.append(args)

            await cursor.execute(query, args)
        except aiosqlite.IntegrityError as exc:
            self._map_integrity_error(exc)
            msg = f'Error executing SQL: {query} with args: {args}. Exception: {exc}'
            raise ConnectionError(msg) from exc
        except aiosqlite.Error as exc:
            msg = f'Error executing SQL: {query} with args: {args}. Exception: {exc}'
            raise ConnectionError(msg) from exc

        return cursor

    async def acquire_lock(self, lock: LockCommand) -> Any:  # noqa: ARG002
        """
        Acquires a lock on the SQLite database.

        This is a no-op. ``BEGIN EXCLUSIVE`` itself DOES work across async contexts -- aiosqlite
        keeps the transaction open on its worker thread and blocks other connections/processes,
        exactly like the sync path. It is not issued here because of the connection pool: for
        ``transaction_id=None`` operations the pool hands the SAME connection to concurrently
        running coroutines, so a ``BEGIN EXCLUSIVE`` on it breaks them -- a second acquirer raises
        ``cannot start a transaction within a transaction`` and an unrelated coroutine's write
        silently joins the open transaction (losing isolation). The sync path avoids this only
        because it never interleaves coroutines on one connection. Correct async locking needs a
        transaction-scoped connection used solely by the lock holder.

        Args:
            lock (LockCommand): The lock command.

        Returns:
            Any: The result of the lock acquisition.
        """
        return True

    async def release_lock(self, lock: LockCommand) -> Any:  # noqa: ARG002
        """
        Releases a lock on the SQLite database.

        No-op mirror of ``acquire_lock`` (see there for why async locking is not issued on the
        shared pooled connection).

        Args:
            lock (LockCommand): The lock command.

        Returns:
            Any: The result of the lock release.
        """
        return True

    async def commit_transaction(self, transaction: TransactionCommand | str | None) -> Any:
        """
        Commits a transaction on the SQLite database.

        Args:
            transaction (TransactionCommand | str | None): The transaction command or transaction ID.

        Returns:
            Any: The result of the transaction commit.
        """
        if isinstance(transaction, TransactionCommand) and transaction.parent_transaction_id:
            await self.connection.execute(f"RELEASE SAVEPOINT '{transaction.parent_transaction_id}'")
        else:
            await self.connection.execute('COMMIT')
        return True

    async def rollback_transaction(self, transaction: TransactionCommand | str | None) -> Any:
        """
        Rolls back a transaction on the SQLite database.

        Args:
            transaction (TransactionCommand | str | None): The transaction command or transaction ID.

        Returns:
            Any: The result of the transaction rollback.
        """
        if isinstance(transaction, TransactionCommand) and transaction.parent_transaction_id:
            await self.connection.execute(f"ROLLBACK TO SAVEPOINT '{transaction.parent_transaction_id}'")
        else:
            await self.connection.execute('ROLLBACK')
        return True

    async def begin_transaction(self, transaction: TransactionCommand | str | None) -> Any:  # pragma: no cover
        """
        Begins a transaction on the SQLite database.

        Args:
            transaction (TransactionCommand | str | None): The transaction command or transaction ID.

        Returns:
            Any: The result of the transaction begin.
        """
        if isinstance(transaction, TransactionCommand) and transaction.parent_transaction_id:
            await self.connection.execute(f"SAVEPOINT '{transaction.parent_transaction_id}'")
        else:
            await self.connection.execute('BEGIN')
        return True

    async def revert_transaction(self, transaction: TransactionCommand | str | None) -> Any:  # pragma: no cover
        """
        Reverts a transaction on the SQLite database.

        Args:
            transaction (TransactionCommand | str | None): The transaction command or transaction ID.

        Returns:
            Any: The result of the transaction revert.
        """
        return await self.rollback_transaction(transaction)

    async def _run_schema_mutation(self, mutation: SchemaMutation) -> Schema | None:
        if isinstance(mutation, UpdateProperty):
            await self._update_property(mutation)
            return None
        if isinstance(mutation, AddConstraint | DeleteConstraint):
            await self._recreate_table_with_constraints(mutation)
            return None

        sql_params_list = self._generator.compile_schema_mutation(mutation)

        for sql, params in sql_params_list:
            await self.execute(sql, *params)

        if isinstance(mutation, RegisterSchema):
            return mutation.schema

        return None

    async def _update_property(self, mutation: UpdateProperty) -> None:
        """Port UpdateProperty to SQLite via ADD / UPDATE / DROP / RENAME column sequence."""
        if mutation.property.required and mutation.property.default is None:
            msg = (
                f'Cannot update {mutation.property.name} column. '
                "SQLite doesn't support ALTER COLUMN with required=True and no default value."
            )
            raise ValueError(msg)

        new_uuid = f'f{uuid.uuid4().hex}'
        new_prop = copy(mutation.property)
        new_prop.name = new_uuid

        ref = mutation.schema_ref

        # a. Add new column with the requested type under a temporary name.
        for sql, params in self._generator.compile_schema_mutation(AddProperty(schema_ref=ref, property=new_prop)):
            await self.execute(sql, *params)

        # b. Copy data from the old column into the new one.
        copy_stmt, copy_params = self._generator.compile_mutation(
            UpdateData(
                schema=ref,
                data=DataInput(
                    data={
                        new_uuid: FieldReferenceExpression(
                            field_reference=FieldReference(
                                field=Field(name=mutation.property.name),
                                table_name=ref.name,
                            )
                        )
                    },
                ),
            )
        )
        await self.execute(copy_stmt, *copy_params)

        # c. Drop the old column.
        for sql, params in self._generator.compile_schema_mutation(
            DeleteProperty(schema_ref=ref, property_name=mutation.property.name)
        ):
            await self.execute(sql, *params)

        # d. Rename the temporary column to the original name.
        for sql, params in self._generator.compile_schema_mutation(
            RenameProperty(schema_ref=ref, old_name=new_uuid, new_name=mutation.property.name)
        ):
            await self.execute(sql, *params)

    async def _recreate_table_with_constraints(  # noqa: C901, PLR0912
        self, mutation: AddConstraint | DeleteConstraint
    ) -> None:
        """Rebuild the table under a temp name to apply AddConstraint / DeleteConstraint on SQLite."""
        table_name = mutation.schema_ref.name
        namespace = mutation.schema_ref.namespace

        # Introspect the current schema.
        all_schemas = await self.query_schema(
            QueryStatement(table=SchemaReference(name=TABLE_REGISTRY, version=Version.LATEST))
        )
        current_schema: Schema | None = None
        for schema in all_schemas:
            schema_namespace = schema.namespace
            if schema.name == table_name and (
                (not namespace and not schema_namespace) or namespace == schema_namespace
            ):
                current_schema = schema
                break

        if current_schema is None:
            msg = f'Table {table_name} not found. Available tables: {[(s.name, s.namespace) for s in all_schemas]}'
            raise ValueError(msg)

        # Compute the new constraint list.
        new_constraints = list(current_schema.constraints or [])
        if isinstance(mutation, AddConstraint):
            new_constraints.append(mutation.constraint)
        else:
            new_constraints = [c for c in new_constraints if c.name != mutation.constraint_name]

        # Build the temp-table schema.
        temp_table_name = f'temp_{table_name}_{uuid.uuid4().hex[:8]}'
        temp_ref = SchemaReference(name=temp_table_name, version=Version.LATEST)
        orig_ref = SchemaReference(name=table_name, version=Version.LATEST, namespace=namespace)
        temp_schema = Schema(
            name=temp_table_name,
            namespace=namespace,
            version=current_schema.version,
            properties=current_schema.properties,
            constraints=new_constraints or None,
            indexes=[],
        )

        # Detect whether we are already inside a transaction.
        in_transaction = False
        try:
            await self.connection.execute('BEGIN')
        except Exception as exc:  # aiosqlite wraps sqlite3.OperationalError
            if 'cannot start a transaction within a transaction' in str(exc):
                in_transaction = True
            else:
                raise

        try:
            # a. CREATE temp table.
            for sql, params in self._generator.compile_schema_mutation(
                RegisterSchema(schema_ref=temp_ref, schema=temp_schema)
            ):
                await self.execute(sql, *params)

            # b. Copy all rows from the original table into the temp table.
            col_names = [prop.name for prop in current_schema.properties]
            insert_mut = InsertFromSelect(
                schema=temp_ref,
                query=QueryStatement(
                    table=orig_ref,
                    only=[FieldReference(field=Field(name=c), table_name=table_name) for c in col_names],
                ),
                columns=[FieldReference(field=Field(name=c), table_name=temp_table_name) for c in col_names],
            )
            copy_sql, copy_params = self._generator.compile_mutation(insert_mut)
            await self.execute(copy_sql, *copy_params)

            # c. DROP the original table.
            for sql, params in self._generator.compile_schema_mutation(DeleteSchema(schema_ref=orig_ref)):
                await self.execute(sql, *params)

            # d. RENAME temp → original.
            for sql, params in self._generator.compile_schema_mutation(
                RenameSchema(schema_ref=temp_ref, new_name=table_name)
            ):
                await self.execute(sql, *params)

            # e. Recreate indexes on the renamed table.
            renamed_ref = SchemaReference(name=table_name, version=Version.LATEST, namespace=namespace)
            for idx in current_schema.indexes or []:
                for sql, params in self._generator.compile_schema_mutation(AddIndex(schema_ref=renamed_ref, index=idx)):
                    await self.execute(sql, *params)

            if not in_transaction:
                await self.connection.execute('COMMIT')

        except Exception:
            if not in_transaction:
                await self.connection.execute('ROLLBACK')
            raise
