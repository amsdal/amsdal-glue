import logging
from typing import Any

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
from amsdal_glue_core.common.exceptions import AmsdalGlueError
from amsdal_glue_core.common.exceptions import UniqueViolationError
from amsdal_glue_core.common.interfaces.connection import ConnectionBase
from amsdal_glue_core.common.operations.commands import SchemaCommand
from amsdal_glue_core.common.operations.commands import TransactionCommand
from amsdal_glue_core.common.operations.mutations.data import DataMutation
from amsdal_glue_core.common.operations.mutations.schema import RegisterSchema
from amsdal_glue_core.common.operations.mutations.schema import SchemaMutation

from amsdal_glue_connections._sql_core import SqlGenerator
from amsdal_glue_connections.sql.connections.postgres_connection.base import get_pg_transform
from amsdal_glue_connections.sql.connections.postgres_connection.base import PostgresConnectionMixin
from amsdal_glue_connections.sql.sql_builders.query_builder import build_where

logger = logging.getLogger(__name__)


class PostgresConnection(PostgresConnectionMixin, ConnectionBase):
    """
    PostgresConnection is responsible for managing connections and executing queries and commands on
    a PostgreSQL database.

    Example:
        Here is example of how to create a connection to a PostgreSQL database:

        ```python
        from amsdal_glue_connections import PostgresConnection

        connection = PostgresConnection()
        connection.connect(
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
        self._connection: Any = None
        self._generator = SqlGenerator('postgresql', param_style='format')
        super().__init__()

    @property
    def is_connected(self) -> bool:
        """
        Checks if the connection to the PostgreSQL database is established.

        Returns:
            bool: True if connected, False otherwise.
        """
        return self._connection is not None

    @property
    def is_alive(self) -> bool:
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

        if not self.is_connected:
            return False

        try:
            self._connection.execute('SELECT 1')
        except psycopg.Error:
            return False

        return True

    @property
    def connection(self) -> Any:
        """
        Gets the current connection to the PostgreSQL database.

        Returns:
            psycopg.Connection: The current connection.

        Raises:
            ConnectionError: If the connection is not established.
        """
        if self._connection is None:
            msg = 'Connection not established'
            raise ConnectionError(msg)

        return self._connection

    def connect(
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
                'Use "pip install amsdal-glue-connections[postgres]" to install it.'
            )
            raise ImportError(_msg) from None

        if self._connection is not None:
            msg = 'Connection already established'
            raise ConnectionError(msg)

        self._connection = psycopg.connect(dsn, autocommit=autocommit, **kwargs)
        self._connection.execute("SELECT set_config('TimeZone', %s, false)", [timezone])

        if schema:
            self._connection.execute(f'SET search_path TO {schema}')

    def disconnect(self) -> None:
        """
        Closes the connection to the PostgreSQL database.
        """
        self.connection.close()
        self._connection = None

    def query(self, query: QueryStatement) -> list[Data]:
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
            cursor = self.execute(_stmt, *_params)
        except Exception as exc:
            msg = f'Query failed: {exc}'
            raise ConnectionError(msg) from exc

        fields = []

        for column in cursor.description or []:
            if column[0] in fields:
                msg = f'Column name {column[0]} is duplicated'
                raise ValueError(msg)
            fields.append(column[0])

        result = [self.build_data(dict(zip(fields, row, strict=True))) for row in cursor.fetchall()]
        cursor.close()

        return result

    def query_schema(self, filters: Conditions | None = None) -> list[Schema]:
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

        cursor = self.execute(stmt, *values)
        tables = cursor.fetchall()
        cursor.close()
        result = []

        for table in tables:
            table_name = table[0]
            properties, constraints, indexes = self.get_table_info(table_name)
            schema = Schema(
                name=table_name,
                version=Version.LATEST,
                properties=properties,
                constraints=constraints,
                indexes=indexes,
            )
            result.append(schema)

        return result

    def run_mutations(self, mutations: list[DataMutation]) -> list[list[Data] | None]:
        """
        Executes a list of data mutations on the PostgreSQL database.

        Args:
            mutations (list[DataMutation]): The list of data mutations to be executed.

        Returns:
            list[list[Data] | None]: The result of the data mutations execution.
        """
        return [self._run_mutation(mutation) for mutation in mutations]

    def _run_mutation(self, mutation: DataMutation) -> list[Data] | None:
        _stmt, _params = self._generator.compile_mutation(mutation)

        try:
            self.execute(_stmt, *_params)
        except AmsdalGlueError:
            # Typed glue errors (e.g. UniqueViolationError) bubble unchanged.
            raise
        except Exception as exc:
            msg = f'Mutation failed: {exc}'
            raise ConnectionError(msg) from exc
        return None

    def run_schema_command(self, command: SchemaCommand) -> list[Schema | None]:
        """
        Executes a schema command on the PostgreSQL database.

        Args:
            command (SchemaCommand): The schema command to be executed.

        Returns:
            list[Schema | None]: The result of the schema command execution.
        """
        result: list[Schema | None] = []

        for mutation in command.mutations:
            data = self._run_schema_mutation(mutation)
            result.append(data)

        return result

    def execute(self, query: str, *args: Any) -> Any:
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
                self._queries_params.append(args)

            cursor = self.connection.execute(query, args)
        except psycopg.errors.UniqueViolation as exc:
            raise UniqueViolationError(str(exc)) from exc
        except psycopg.Error as exc:
            msg = f'Error executing SQL: {query} with args: {args}. Exception: {exc}'
            raise ConnectionError(msg) from exc
        return cursor

    def get_table_info(
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
        cursor = self.execute(
            'SELECT ordinal_position, column_name, data_type, is_nullable, column_default, udt_name '  # noqa: S608
            'FROM information_schema.columns '
            f"WHERE table_name = '{table_name}';"
        )
        columns = cursor.fetchall()
        cursor.close()

        properties: list[PropertySchema] = []
        for column in columns:
            column_name = column[1]
            info = self.execute(
                'SELECT c.relname as table_name, a.attname AS column_name, t.typname AS data_type, '  # noqa: S608
                'a.atttypmod AS typmod '
                'FROM pg_attribute a '
                'JOIN pg_class c ON a.attrelid = c.oid '
                'JOIN pg_type t ON a.atttypid = t.oid '
                f"WHERE c.relname = '{table_name}' "
                f"AND a.attname = '{column_name}';"
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
        cursor = self.execute(
            'SELECT conname, contype, confrelid, conkey, confkey, con.oid '  # noqa: S608
            'FROM pg_catalog.pg_constraint con '
            'INNER JOIN pg_catalog.pg_class rel ON rel.oid = con.conrelid '
            'INNER JOIN pg_catalog.pg_namespace nsp ON nsp.oid = connamespace '
            f"WHERE rel.relname = '{table_name}';"
        )
        raw_constrains = cursor.fetchall()
        cursor.close()

        constraints: list[BaseConstraint] = []
        for raw_constrain in raw_constrains:
            if raw_constrain[1] == 'f':
                f_table_id = raw_constrain[2]
                cursor = self.execute(
                    f'SELECT relname FROM pg_catalog.pg_class WHERE oid = {f_table_id};'  # noqa: S608
                )
                f_table_name = cursor.fetchall()[0][0]
                cursor.close()
                cursor = self.execute(
                    'SELECT ordinal_position, column_name '  # noqa: S608
                    'FROM information_schema.columns '
                    f"WHERE table_name = '{f_table_name}';"
                )
                f_table_fields = {row[0]: row[1] for row in cursor.fetchall()}
                cursor.close()

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
        cursor = self.execute(
            'SELECT i.relname AS index_name, array_agg(a.attname ORDER BY ord.n) AS column_names '  # noqa: S608
            'FROM pg_class t '
            'JOIN pg_index x ON t.oid = x.indrelid '
            'JOIN pg_class i ON i.oid = x.indexrelid '
            'JOIN generate_subscripts(x.indkey, 1) AS ord(n) ON TRUE '
            'JOIN pg_attribute a ON a.attnum = x.indkey[ord.n] AND a.attrelid = t.oid '
            f"WHERE t.relname = '{table_name}' "
            'GROUP BY t.relname, i.relname'
        )
        indexes_list = cursor.fetchall()
        cursor.close()

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

    def acquire_lock(self, lock: ExecutionLockCommand) -> Any:
        """
        Acquires a lock on the PostgreSQL database.

        Args:
            lock (ExecutionLockCommand): The lock command to be executed.

        Returns:
            Any: The result of the lock acquisition.
        """
        if lock.mode == 'EXCLUSIVE':
            self.execute('BEGIN EXCLUSIVE')

        return True

    def release_lock(self, lock: ExecutionLockCommand) -> Any:
        """
        Releases a lock on the PostgreSQL database.

        Args:
            lock (ExecutionLockCommand): The lock command to be released.

        Returns:
            Any: The result of the lock release.
        """
        if lock.mode == 'EXCLUSIVE':
            self.execute('COMMIT')

        return True

    def commit_transaction(self, transaction: TransactionCommand | str | None) -> Any:
        """
        Commits a transaction on the PostgreSQL database.

        Args:
            transaction (TransactionCommand | str | None): The transaction to be committed.

        Returns:
            Any: The result of the transaction commit.
        """
        if isinstance(transaction, TransactionCommand) and transaction.parent_transaction_id:
            return True

        self.execute('COMMIT')
        return True

    def rollback_transaction(self, transaction: TransactionCommand | str | None) -> Any:
        """
        Rolls back a transaction on the PostgreSQL database.

        Args:
            transaction (TransactionCommand | str | None): The transaction to be rolled back.

        Returns:
            Any: The result of the transaction rollback.
        """
        if isinstance(transaction, TransactionCommand) and transaction.parent_transaction_id:
            self.execute(f'ROLLBACK TO SAVEPOINT "{transaction.transaction_id}"')
            return True

        self.execute('ROLLBACK')
        return True

    def begin_transaction(self, transaction: TransactionCommand | str | None) -> Any:  # pragma: no cover
        """
        Begins a transaction on the PostgreSQL database.

        Args:
            transaction (TransactionCommand | str | None): The transaction to be begun.

        Returns:
            Any: The result of the transaction begin.
        """
        if isinstance(transaction, TransactionCommand) and transaction.parent_transaction_id:
            self.execute(f'SAVEPOINT "{transaction.transaction_id}"')
            return True

        self.execute('BEGIN')
        return True

    def revert_transaction(self, transaction: TransactionCommand | str | None) -> Any:  # pragma: no cover
        """
        Reverts a transaction on the PostgreSQL database.

        Args:
            transaction (TransactionCommand | str | None): The transaction to be reverted.

        Returns:
            Any: The result of the transaction revert.
        """
        if isinstance(transaction, TransactionCommand) and transaction.parent_transaction_id:
            self.execute(f'ROLLBACK TO SAVEPOINT "{transaction.transaction_id}"')
            return True

        self.execute('ROLLBACK')
        return True

    def _run_schema_mutation(self, migration: SchemaMutation) -> Schema | None:
        sql_params_list = self._generator.compile_schema_mutation(migration)

        for sql, params in sql_params_list:
            self.execute(sql, *params)

        if isinstance(migration, RegisterSchema):
            return migration.schema
        return None
