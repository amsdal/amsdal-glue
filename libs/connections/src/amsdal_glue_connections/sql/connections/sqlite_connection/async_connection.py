import logging
import sqlite3
import uuid
from copy import copy
from datetime import date
from datetime import datetime
from pathlib import Path
from typing import Any
from typing import TYPE_CHECKING

from amsdal_glue_core.common.data_models.constraints import BaseConstraint
from amsdal_glue_core.common.data_models.constraints import ForeignKeyConstraint
from amsdal_glue_core.common.data_models.constraints import PrimaryKeyConstraint
from amsdal_glue_core.common.data_models.data import Data
from amsdal_glue_core.common.data_models.field_reference import Field
from amsdal_glue_core.common.data_models.field_reference import FieldReference
from amsdal_glue_core.common.data_models.indexes import IndexField
from amsdal_glue_core.common.data_models.indexes import IndexSchema
from amsdal_glue_core.common.data_models.query import QueryStatement
from amsdal_glue_core.common.data_models.schema import PropertySchema
from amsdal_glue_core.common.data_models.schema import Schema
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.enums import Version
from amsdal_glue_core.common.exceptions import AmsdalGlueError
from amsdal_glue_core.common.exceptions import UniqueViolationError
from amsdal_glue_core.common.expressions.field_reference import FieldReferenceExpression
from amsdal_glue_core.common.expressions.raw import RawExpression
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
from amsdal_glue_connections.sql.connections.sqlite_connection.base import _REGISTRY_VIEW_SQL
from amsdal_glue_connections.sql.connections.sqlite_connection.base import SqliteConnectionMixin
from amsdal_glue_connections.sql.connections.sqlite_connection.sync_connection import _find_autoincrement_pk_col
from amsdal_glue_connections.sql.connections.sqlite_connection.sync_connection import _get_unique_constraints
from amsdal_glue_connections.sql.connections.sqlite_connection.sync_connection import _parse_collations
from amsdal_glue_connections.sql.connections.sqlite_connection.sync_connection import _parse_fk_name
from amsdal_glue_connections.sql.connections.sqlite_connection.sync_connection import _parse_generated_expressions
from amsdal_glue_connections.sql.connections.sqlite_connection.sync_connection import _parse_pk_name
from amsdal_glue_connections.sql.connections.sqlite_connection.sync_connection import _sqlite_type_to_field_type
from amsdal_glue_connections.sql.schema_registry import TABLE_REGISTRY

if TYPE_CHECKING:
    import aiosqlite

logger = logging.getLogger(__name__)


class AsyncSqliteConnection(SqliteConnectionMixin, AsyncConnectionBase):
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
        resolved.only = [FieldReference(field=Field(name='name'), table_name=ref_name)]

        sql, params = self._generator.compile_query(resolved)
        cursor = await self.execute(sql, *params)
        rows = await cursor.fetchall()
        await cursor.close()

        seen: set[str] = set()
        table_names: list[str] = []
        for (name,) in rows:
            if name not in seen:
                seen.add(name)
                table_names.append(name)

        schemas: list[Schema] = []
        for table_name in table_names:
            table_ddl = await self._get_table_ddl(table_name)
            properties = await self._introspect_columns(table_name, table_ddl)
            if not properties:
                continue

            constraints = await self._introspect_constraints(table_name, table_ddl)
            indexes = await self._introspect_indexes(table_name)

            schemas.append(
                Schema(
                    name=table_name,
                    version=Version.LATEST,
                    properties=properties,
                    constraints=constraints or None,
                    indexes=indexes or None,
                ),
            )

        return schemas

    async def _ensure_schema_views(self) -> None:
        # The view DDL is idempotent (CREATE ... IF NOT EXISTS), so it is re-issued on every call
        # rather than gated by a per-object flag that would go stale across disconnect()/connect()
        # cycles (temporary views are per-connection, so a reconnect must recreate them).
        for sql in _REGISTRY_VIEW_SQL.values():
            await self.execute(sql)

    async def _get_table_ddl(self, table_name: str) -> str:
        cursor = await self.execute(
            "SELECT sql FROM sqlite_master WHERE type='table' AND name=?",
            table_name,
        )
        row = await cursor.fetchone()
        await cursor.close()
        return row[0] if row else ''

    async def _introspect_columns(self, table_name: str, table_ddl: str) -> list[PropertySchema]:
        cursor = await self.execute(f'PRAGMA table_xinfo("{table_name}")')
        rows = await cursor.fetchall()
        await cursor.close()

        has_autoincrement = 'AUTOINCREMENT' in table_ddl.upper()
        pk_col = _find_autoincrement_pk_col(table_ddl) if has_autoincrement else None
        generated_exprs = _parse_generated_expressions(table_ddl)
        collations = _parse_collations(table_ddl)

        properties: list[PropertySchema] = []
        for _cid, col_name, col_type, notnull, dflt, _pk, _hidden in rows:
            field_type = _sqlite_type_to_field_type(col_type)
            default = RawExpression(value=dflt) if dflt is not None else None
            identity: bool | None = True if col_name == pk_col else None

            properties.append(
                PropertySchema(
                    name=col_name,
                    type=field_type,
                    required=bool(notnull),
                    default=default,
                    identity=identity,
                    generated=generated_exprs.get(col_name),
                    db_collation=collations.get(col_name),
                ),
            )

        return properties

    async def _get_pk_fields(self, table_name: str) -> list[str]:
        cursor = await self.execute(f'PRAGMA table_info("{table_name}")')
        rows = await cursor.fetchall()
        await cursor.close()

        pk_cols: list[tuple[int, str]] = []
        for _cid, col_name, _col_type, _notnull, _dflt, pk_idx in rows:
            if pk_idx > 0:
                pk_cols.append((pk_idx, col_name))

        pk_cols.sort()
        return [name for _, name in pk_cols]

    async def _get_fk_constraints(self, table_name: str, table_sql: str) -> list[ForeignKeyConstraint]:
        cursor = await self.execute(f'PRAGMA foreign_key_list("{table_name}")')
        rows = await cursor.fetchall()
        await cursor.close()

        if not rows:
            return []

        fk_groups: dict[int, dict[str, Any]] = {}
        for fk_id, _seq, ref_table, from_col, to_col, _on_update, _on_delete, _match in rows:
            if fk_id not in fk_groups:
                fk_groups[fk_id] = {'ref_table': ref_table, 'fields': [], 'ref_fields': []}
            fk_groups[fk_id]['fields'].append(from_col)
            fk_groups[fk_id]['ref_fields'].append(to_col)

        constraints: list[ForeignKeyConstraint] = []
        for fk_id, group in fk_groups.items():
            primary_field = group['fields'][0]
            fk_name = _parse_fk_name(table_sql, primary_field)
            if not fk_name:
                fk_name = f'fk_{table_name}_{fk_id}'

            constraints.append(
                ForeignKeyConstraint(
                    name=fk_name,
                    fields=group['fields'],
                    reference_schema=SchemaReference(name=group['ref_table'], version=Version.LATEST),
                    reference_fields=group['ref_fields'],
                ),
            )

        return constraints

    async def _introspect_constraints(self, table_name: str, table_ddl: str) -> list[BaseConstraint]:
        constraints: list[BaseConstraint] = []

        pk_fields = await self._get_pk_fields(table_name)
        if pk_fields:
            constraints.append(PrimaryKeyConstraint(name=_parse_pk_name(table_ddl, table_name), fields=pk_fields))

        constraints.extend(await self._get_fk_constraints(table_name, table_ddl))
        constraints.extend(_get_unique_constraints(table_name, table_ddl, constraints))

        # CheckConstraint: skipped — no SQL→Conditions parser in prod (matches PG).

        return constraints

    async def _introspect_indexes(self, table_name: str) -> list[IndexSchema]:
        cursor = await self.execute(f'PRAGMA index_list("{table_name}")')
        idx_rows = await cursor.fetchall()
        await cursor.close()

        indexes: list[IndexSchema] = []
        for _seq, idx_name, is_unique, origin, _partial in idx_rows:
            if origin in ('u', 'pk'):
                continue

            cursor = await self.execute(f'PRAGMA index_xinfo("{idx_name}")')
            info_rows = await cursor.fetchall()
            await cursor.close()

            idx_fields = [IndexField(name=row[2]) for row in info_rows if row[2] is not None]

            indexes.append(IndexSchema(name=idx_name, fields=idx_fields, unique=bool(is_unique)))

        return indexes

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

        try:
            if self.debug_queries:
                self._queries.append(query)
                self._queries_params.append(args)

            await cursor.execute(query, args)
        except aiosqlite.IntegrityError as exc:
            if 'UNIQUE constraint failed' in str(exc):
                raise UniqueViolationError(str(exc)) from exc
            msg = f'Error executing SQL: {query} with args: {args}. Exception: {exc}'
            raise ConnectionError(msg) from exc
        except aiosqlite.Error as exc:
            msg = f'Error executing SQL: {query} with args: {args}. Exception: {exc}'
            raise ConnectionError(msg) from exc

        return cursor

    async def acquire_lock(self, lock: LockCommand) -> Any:  # noqa: ARG002
        """
        Acquires a lock on the SQLite database.

        Deliberate divergence from the Rust ``compile_lock_command`` path: SQLite does not
        support ``LOCK TABLE`` syntax.  TODO spec §3.5.

        Note: ``BEGIN EXCLUSIVE`` is not attempted here — it does not work reliably when the same
        connection is shared across async contexts.

        Args:
            lock (LockCommand): The lock command.

        Returns:
            Any: The result of the lock acquisition.
        """
        return True

    async def release_lock(self, lock: LockCommand) -> Any:  # noqa: ARG002
        """
        Releases a lock on the SQLite database.

        Deliberate divergence from the Rust ``compile_lock_command`` path — mirrors ``acquire_lock``.
        TODO spec §3.5.

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
        if isinstance(transaction, TransactionCommand) and transaction.parent_transaction_id:
            await self.connection.execute(f"ROLLBACK TO SAVEPOINT '{transaction.parent_transaction_id}'")
        else:
            await self.connection.execute('ROLLBACK')
        return True

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
                data={
                    new_uuid: FieldReferenceExpression(
                        field_reference=FieldReference(
                            field=Field(name=mutation.property.name),
                            table_name=ref.name,
                        )
                    )
                },
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
                (namespace is None and (schema_namespace is None or schema_namespace == ''))
                or (namespace == '' and (schema_namespace is None or schema_namespace == ''))
                or (namespace == schema_namespace)
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
