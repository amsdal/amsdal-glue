import logging
from typing import Any
from typing import TYPE_CHECKING

from amsdal_glue_core.commands.lock_command_node import ExecutionLockCommand
from amsdal_glue_core.common.data_models.conditions import Conditions
from amsdal_glue_core.common.data_models.constraints import BaseConstraint
from amsdal_glue_core.common.data_models.constraints import ForeignKeyConstraint
from amsdal_glue_core.common.data_models.constraints import PrimaryKeyConstraint
from amsdal_glue_core.common.data_models.constraints import UniqueConstraint
from amsdal_glue_core.common.data_models.data import Data
from amsdal_glue_core.common.data_models.indexes import IndexSchema
from amsdal_glue_core.common.data_models.query import QueryStatement
from amsdal_glue_core.common.data_models.schema import PropertySchema
from amsdal_glue_core.common.data_models.schema import Schema
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.enums import Version
from amsdal_glue_core.common.interfaces.connection import AsyncConnectionBase
from amsdal_glue_core.common.operations.commands import SchemaCommand
from amsdal_glue_core.common.operations.commands import TransactionCommand
from amsdal_glue_core.common.operations.mutations.data import DataMutation
from amsdal_glue_core.common.operations.mutations.schema import AddConstraint
from amsdal_glue_core.common.operations.mutations.schema import AddIndex
from amsdal_glue_core.common.operations.mutations.schema import AddProperty
from amsdal_glue_core.common.operations.mutations.schema import DeleteConstraint
from amsdal_glue_core.common.operations.mutations.schema import DeleteIndex
from amsdal_glue_core.common.operations.mutations.schema import DeleteProperty
from amsdal_glue_core.common.operations.mutations.schema import DeleteSchema
from amsdal_glue_core.common.operations.mutations.schema import RegisterSchema
from amsdal_glue_core.common.operations.mutations.schema import RenameProperty
from amsdal_glue_core.common.operations.mutations.schema import RenameSchema
from amsdal_glue_core.common.operations.mutations.schema import SchemaMutation
from amsdal_glue_core.common.operations.mutations.schema import UpdateProperty

from amsdal_glue_connections.sql.connections.postgres_connection.base import get_pg_transform
from amsdal_glue_connections.sql.connections.postgres_connection.base import PostgresConnectionMixin
from amsdal_glue_connections.sql.sql_builders.command_builder import build_sql_data_command
from amsdal_glue_connections.sql.sql_builders.query_builder import build_sql_query
from amsdal_glue_connections.sql.sql_builders.query_builder import build_where

if TYPE_CHECKING:
    import psycopg

logger = logging.getLogger(__name__)


class AsyncPostgresConnection(PostgresConnectionMixin, AsyncConnectionBase):
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

        self._connection = await psycopg.AsyncConnection.connect(dsn, autocommit=autocommit, **kwargs)
        await self._connection.execute("SELECT set_config('TimeZone', %s, false)", [timezone])

        if schema:
            await self._connection.execute(f'SET search_path TO {schema}')

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
        _stmt, _params = build_sql_query(
            query,
            transform=get_pg_transform(),
        )

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

    async def query_schema(self, filters: Conditions | None = None) -> list[Schema]:
        """
        Queries the schema of the PostgreSQL database.

        Args:
            filters (Conditions | None): The filters to be applied to the schema query.

        Returns:
            list[Schema]: The result of the schema query.
        """
        stmt = self.TABLE_SQL

        if filters and filters.children:
            where, values = build_where(
                filters,
                transform=get_pg_transform(),
            )
            stmt += f' WHERE {where}'
        else:
            values = []

        cursor = await self.execute(stmt, *values)
        tables = await cursor.fetchall()
        await cursor.close()
        result = []

        for table in tables:
            table_name = table[0]
            properties, constraints, indexes = await self.get_table_info(table_name)
            schema = Schema(
                name=table_name,
                version=Version.LATEST,
                properties=properties,
                constraints=constraints,
                indexes=indexes,
            )
            result.append(schema)

        return result

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
        _stmt, _params = build_sql_data_command(
            mutation,
            transform=get_pg_transform(),
        )

        try:
            await self.execute(_stmt, *_params)
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

        try:
            if self.debug_queries:
                self._queries.append(query)

            cursor = await self.connection.execute(query, args)
        except psycopg.Error as exc:
            msg = f'Error executing SQL: {query} with args: {args}. Exception: {exc}'
            raise ConnectionError(msg) from exc
        return cursor

    async def get_table_info(
        self,
        table_name: str,
    ) -> tuple[list[PropertySchema], list[BaseConstraint], list[IndexSchema]]:
        """
        Gets the information of a table in the PostgreSQL database.

        Args:
            table_name (str): The name of the table.

        Returns:
            tuple[list[PropertySchema], list[BaseConstraint], list[IndexSchema]]: The properties, constraints,
                                                                                  and indexes of the table.
        """
        cursor = await self.execute(
            'SELECT ordinal_position, column_name, data_type, is_nullable, column_default '  # noqa: S608
            'FROM information_schema.columns '
            f"WHERE table_name = '{table_name}';"
        )
        columns = await cursor.fetchall()
        await cursor.close()

        properties: list[PropertySchema] = []
        for column in columns:
            column_name = column[1]
            info = await (
                await self.execute(
                    'SELECT c.relname as table_name, a.attname AS column_name, t.typname AS data_type, '  # noqa: S608
                    'a.atttypmod AS typmod '
                    'FROM pg_attribute a '
                    'JOIN pg_class c ON a.attrelid = c.oid '
                    'JOIN pg_type t ON a.atttypid = t.oid '
                    f"WHERE c.relname = '{table_name}' "
                    f"AND a.attname = '{column_name}';"
                )
            ).fetchone()

            _info = (
                {
                    'table_name': info[0],
                    'column_name': info[1],
                    'data_type': info[2],
                    'typmod': info[3],
                }
                if info
                else {}
            )
            udt_name = column[5] if len(column) > 5 else None  # noqa: PLR2004

            properties.append(
                PropertySchema(
                    name=column[1],
                    type=self._to_python_type(column[2], udt_name, _info),
                    required=column[3].lower() == 'no',  # means is nullable
                    description=None,
                    default=column[4],
                )
            )

        fid_to_name: dict[int, str] = {column[0]: column[1] for column in columns}

        # Get constraints info
        cursor = await self.execute(
            'SELECT conname, contype, confrelid, conkey, confkey, con.oid '  # noqa: S608
            'FROM pg_catalog.pg_constraint con '
            'INNER JOIN pg_catalog.pg_class rel ON rel.oid = con.conrelid '
            'INNER JOIN pg_catalog.pg_namespace nsp ON nsp.oid = connamespace '
            f"WHERE rel.relname = '{table_name}';"
        )
        raw_constrains = await cursor.fetchall()
        await cursor.close()

        constraints: list[BaseConstraint] = []
        for raw_constrain in raw_constrains:
            if raw_constrain[1] == 'f':
                f_table_id = raw_constrain[2]
                cursor = await self.execute(
                    f'SELECT relname FROM pg_catalog.pg_class WHERE oid = {f_table_id};'  # noqa: S608
                )
                f_table_name = (await cursor.fetchall())[0][0]
                await cursor.close()
                cursor = await self.execute(
                    'SELECT ordinal_position, column_name '  # noqa: S608
                    'FROM information_schema.columns '
                    f"WHERE table_name = '{f_table_name}';"
                )
                f_table_fields = {row[0]: row[1] for row in await cursor.fetchall()}
                await cursor.close()

                constraints.append(
                    ForeignKeyConstraint(
                        name=raw_constrain[0],
                        fields=[fid_to_name.get(fk) for fk in raw_constrain[3]],  # type: ignore[misc]
                        reference_schema=SchemaReference(
                            name=f_table_name,
                            version=Version.LATEST,
                        ),
                        reference_fields=[f_table_fields.get(fid) for fid in raw_constrain[4]],  # type: ignore[misc]
                    )
                )

            elif raw_constrain[1] == 'p':
                constraints.append(
                    PrimaryKeyConstraint(
                        name=raw_constrain[0],
                        fields=[fid_to_name.get(pk) for pk in raw_constrain[3]],  # type: ignore[misc]
                    )
                )

            elif raw_constrain[1] == 'u':
                constraints.append(
                    UniqueConstraint(
                        name=raw_constrain[0],
                        fields=[fid_to_name.get(u) for u in raw_constrain[3]],  # type: ignore[misc]
                    )
                )

        # Get indexes info
        cursor = await self.execute(
            'SELECT i.relname AS index_name, array_agg(a.attname ORDER BY ord.n) AS column_names '  # noqa: S608
            'FROM pg_class t '
            'JOIN pg_index x ON t.oid = x.indrelid '
            'JOIN pg_class i ON i.oid = x.indexrelid '
            'JOIN generate_subscripts(x.indkey, 1) AS ord(n) ON TRUE '
            'JOIN pg_attribute a ON a.attnum = x.indkey[ord.n] AND a.attrelid = t.oid '
            f"WHERE t.relname = '{table_name}' "
            'GROUP BY t.relname, i.relname'
        )
        indexes_list = await cursor.fetchall()
        await cursor.close()

        indexes = [
            IndexSchema(
                name=index_name,
                fields=index_fields,
                condition=None,
            )
            for index_name, index_fields in indexes_list
            if not self._is_constraint(index_fields, constraints)
        ]

        return properties, constraints, indexes

    async def acquire_lock(self, lock: ExecutionLockCommand) -> Any:
        """
        Acquires a lock on the PostgreSQL database.

        Args:
            lock (ExecutionLockCommand): The lock command to be executed.

        Returns:
            Any: The result of the lock acquisition.
        """
        if lock.locked_object.query:
            locked_object = lock.locked_object
            where, values = build_where(
                locked_object.query,
                transform=get_pg_transform(),
            )
            _query = f'SELECT * FROM {self._table_name_from_schema_reference(locked_object.schema)}'  # noqa: S608

            if where:
                _query += f' WHERE {where}'

            _query += ' FOR UPDATE'

            await self.execute(_query, *values)

        return True

    async def release_lock(self, lock: ExecutionLockCommand) -> Any:
        """
        Releases a lock on the PostgreSQL database.

        Args:
            lock (ExecutionLockCommand): The lock command to be released.

        Returns:
            Any: The result of the lock release.
        """
        if lock.mode == 'EXCLUSIVE':
            return True

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
        if isinstance(transaction, TransactionCommand) and transaction.parent_transaction_id:
            await self.execute(f'ROLLBACK TO SAVEPOINT "{transaction.transaction_id}"')
            return True

        await self.execute('ROLLBACK')
        return True

    async def _run_schema_mutation(self, migration: SchemaMutation) -> Schema | None:  # noqa: PLR0911, C901
        if isinstance(migration, RegisterSchema):
            schema = migration.schema
            await self._create_table(schema)

            return schema

        if isinstance(migration, DeleteSchema):
            await self._drop_table(migration.schema_reference)

            return None

        if isinstance(migration, RenameSchema):
            schema_reference = migration.schema_reference
            new_schema_name = migration.new_schema_name
            await self._rename_table(schema_reference, new_schema_name)

            return None

        if isinstance(migration, AddProperty):
            schema_reference = migration.schema_reference
            _property = migration.property
            await self._add_column(schema_reference, _property)

            return None

        if isinstance(migration, DeleteProperty):
            schema_reference = migration.schema_reference
            property_name = migration.property_name
            await self._drop_column(schema_reference, property_name)

            return None

        if isinstance(migration, RenameProperty):
            schema_reference = migration.schema_reference
            old_name = migration.old_name
            new_name = migration.new_name
            await self._rename_column(schema_reference, old_name, new_name)

            return None

        if isinstance(migration, UpdateProperty):
            schema_reference = migration.schema_reference
            _property = migration.property
            await self._update_column(schema_reference, _property)

            return None

        if isinstance(migration, AddConstraint):
            schema_reference = migration.schema_reference
            constraint = migration.constraint
            await self._add_constraint(schema_reference, constraint)

            return None

        if isinstance(migration, DeleteConstraint):
            schema_reference = migration.schema_reference
            constraint_name = migration.constraint_name
            await self._drop_constraint(schema_reference, constraint_name)

            return None

        if isinstance(migration, AddIndex):
            schema_reference = migration.schema_reference
            index = migration.index
            await self._add_index(schema_reference, index)

            return None

        if isinstance(migration, DeleteIndex):
            schema_reference = migration.schema_reference
            index_name = migration.index_name
            await self._drop_index(schema_reference, index_name)

            return None

        msg = f'Unsupported schema mutation: {type(migration)}'
        raise ValueError(msg)

    async def _create_table(self, schema: Schema) -> None:
        _constraint_stmts = []

        for _constraint in schema.constraints or []:
            _constraint_stmt = self._build_constraint(_constraint)
            _constraint_stmts.append(_constraint_stmt)

        _namespace_prefix = f'"{schema.namespace}".' if schema.namespace else ''

        stmt = f'CREATE TABLE {_namespace_prefix}"{schema.name}" ('
        stmt += ', '.join(self._build_column(column) for column in schema.properties)

        if _constraint_stmts:
            stmt += ', '
            stmt += ', '.join(_constraint_stmts)

        stmt += ')'

        await self.execute(stmt)

        for _index in schema.indexes or []:
            _index_stmt = self._build_index(schema.name, schema.namespace, _index)
            await self.execute(_index_stmt)

    def _table_name_from_schema_reference(self, schema_reference: SchemaReference) -> str:
        _namespace_prefix = f'"{schema_reference.namespace}".' if schema_reference.namespace else ''

        return f'{_namespace_prefix}"{schema_reference.name}"'

    async def _drop_table(self, schema_reference: SchemaReference) -> None:
        stmt = f'DROP TABLE {self._table_name_from_schema_reference(schema_reference)}'
        await self.execute(stmt)

    async def _rename_table(self, schema_reference: SchemaReference, new_schema_name: str) -> None:
        _namespace_prefix = f'"{schema_reference.namespace}".' if schema_reference.namespace else ''

        stmt = f'ALTER TABLE {_namespace_prefix}"{schema_reference.name}" RENAME TO "{new_schema_name}"'
        await self.execute(stmt)

    async def _add_column(self, schema_reference: SchemaReference, _property: PropertySchema) -> None:
        _column = self._build_column(_property, force_nullable=True)
        _namespace_prefix = f'"{schema_reference.namespace}".' if schema_reference.namespace else ''

        stmt = f'ALTER TABLE {_namespace_prefix}"{schema_reference.name}" ADD COLUMN {_column}'
        await self.execute(stmt)

    async def _drop_column(self, schema_reference: SchemaReference, property_name: str) -> None:
        _namespace_prefix = f'"{schema_reference.namespace}".' if schema_reference.namespace else ''

        stmt = f'ALTER TABLE {_namespace_prefix}"{schema_reference.name}" DROP COLUMN "{property_name}"'
        await self.execute(stmt)

    async def _rename_column(self, schema_reference: SchemaReference, old_name: str, new_name: str) -> None:
        _namespace_prefix = f'"{schema_reference.namespace}".' if schema_reference.namespace else ''

        stmt = f'ALTER TABLE "{schema_reference.name}" RENAME COLUMN "{old_name}" TO "{new_name}"'
        await self.execute(stmt)

    async def _update_column(self, schema_reference: SchemaReference, _property: PropertySchema) -> None:
        _column = self._build_column_update(_property)
        _namespace_prefix = f'"{schema_reference.namespace}".' if schema_reference.namespace else ''

        stmt = f'ALTER TABLE {_namespace_prefix}"{schema_reference.name}" {_column}'
        await self.execute(stmt)

    async def _add_constraint(self, schema_reference: SchemaReference, constraint: BaseConstraint) -> None:
        _constraint_stmt = self._build_constraint(constraint)
        _namespace_prefix = f'"{schema_reference.namespace}".' if schema_reference.namespace else ''
        stmt = f'ALTER TABLE {_namespace_prefix}"{schema_reference.name}" ADD {_constraint_stmt}'
        await self.execute(stmt)

    async def _drop_constraint(self, schema_reference: SchemaReference, constraint_name: str) -> None:
        _namespace_prefix = f'"{schema_reference.namespace}".' if schema_reference.namespace else ''
        stmt = f'ALTER TABLE {_namespace_prefix}"{schema_reference.name}" DROP CONSTRAINT "{constraint_name}"'
        await self.execute(stmt)

    async def _add_index(self, schema_reference: SchemaReference, index: IndexSchema) -> None:
        _index_stmt = self._build_index(schema_reference.name, schema_reference.namespace or '', index)

        await self.execute(_index_stmt)

    async def _drop_index(self, schema_reference: SchemaReference, index_name: str) -> None:
        _namespace_prefix = f'"{schema_reference.namespace}".' if schema_reference.namespace else ''
        stmt = f'DROP INDEX {_namespace_prefix}"{index_name}"'
        await self.execute(stmt)
