import logging
import sqlite3
import uuid
from datetime import date
from datetime import datetime
from pathlib import Path
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
from amsdal_glue_core.common.interfaces.connection import ConnectionBase
from amsdal_glue_core.common.operations.commands import SchemaCommand
from amsdal_glue_core.common.operations.commands import TransactionCommand
from amsdal_glue_core.common.operations.mutations.data import DataMutation
from amsdal_glue_core.common.operations.mutations.schema import AddConstraint
from amsdal_glue_core.common.operations.mutations.schema import DeleteConstraint
from amsdal_glue_core.common.operations.mutations.schema import RegisterSchema
from amsdal_glue_core.common.operations.mutations.schema import SchemaMutation
from amsdal_glue_core.common.operations.mutations.schema import UpdateProperty

from amsdal_glue_connections.sql.connections.sqlite_connection.base import get_sqlite_transform
from amsdal_glue_connections.sql.connections.sqlite_connection.base import SqliteConnectionMixin
from amsdal_glue_connections.sql.sql_builders.command_builder import build_sql_data_command
from amsdal_glue_connections.sql.sql_builders.query_builder import build_sql_query
from amsdal_glue_connections.sql.sql_builders.query_builder import build_where
from amsdal_glue_connections.sql.sql_builders.schema_builder import build_add_column
from amsdal_glue_connections.sql.sql_builders.schema_builder import build_create_indexes
from amsdal_glue_connections.sql.sql_builders.schema_builder import build_create_table
from amsdal_glue_connections.sql.sql_builders.schema_builder import build_drop_column
from amsdal_glue_connections.sql.sql_builders.schema_builder import build_migrate_column
from amsdal_glue_connections.sql.sql_builders.schema_builder import build_rename_column
from amsdal_glue_connections.sql.sql_builders.schema_builder import build_schema_mutation

logger = logging.getLogger(__name__)


class SqliteConnection(SqliteConnectionMixin, ConnectionBase):
    """
    SqliteConnection is responsible for managing connections and executing queries and commands on a SQLite database.

    Example:
        Here is example of how to create a connection to a SQlite database:

        ```python
        from amsdal_glue_connections import SqliteConnection

        connection = SqliteConnection()
        connection.connect(
            db_path='my_db.sqlite',
            check_same_thread=False,
        )
        ```

        Note, the `check_same_thread` parameter has `True` as default value. Although, it is required to set it to
        `False` due to using the [ThreadParallelExecutor][amsdal_glue.executors.ThreadParallelExecutor].

        It's also possible to put any other parameters as a keyword arguments that are accepted by the
        [sqlite3.connect](https://docs.python.org/3/library/sqlite3.html#sqlite3.connect) function.

        Most of the time, you will use the [ConnectionManager][amsdal_glue.ConnectionManager]
        to manage connections instead of creating a connection directly.
    """

    def __init__(self) -> None:
        self._connection: sqlite3.Connection | None = None
        super().__init__()

    @property
    def is_connected(self) -> bool:
        """
        Checks if the connection to the SQLite database is established.

        Returns:
            bool: True if connected, False otherwise.
        """
        return self._connection is not None

    @property
    def is_alive(self) -> bool:
        """
        Checks if the connection to the SQLite database is alive.

        Returns:
            bool: True if alive, False otherwise.
        """
        if not self._connection:
            return False

        try:
            self._connection.execute('SELECT 1')
        except sqlite3.Error:
            return False

        return True

    @property
    def connection(self) -> sqlite3.Connection:
        """
        Gets the current SQLite connection.

        Returns:
            sqlite3.Connection: The current SQLite connection.

        Raises:
            ConnectionError: If the connection is not established.
        """
        if self._connection is None:
            msg = 'Connection not established'
            raise ConnectionError(msg)

        return self._connection

    def connect(self, db_path: Path, *, check_same_thread: bool = False, **kwargs: Any) -> None:
        """
        Establishes a connection to the SQLite database.

        Args:
            db_path (Path): The path to the SQLite database file.
            check_same_thread (bool, optional): Whether to check the same thread. Defaults to False.
            **kwargs (Any): Additional arguments for the SQLite connection.

        Raises:
            ConnectionError: If the connection is already established.
        """
        if self._connection is not None:
            msg = 'Connection already established'
            raise ConnectionError(msg)

        # Disable the deprecated adapters
        sqlite3.register_adapter(date, lambda val: val.isoformat())
        sqlite3.register_adapter(datetime, lambda val: val.isoformat())

        # Register converters if you need to read datetime from DB
        sqlite3.register_converter('DATE', lambda val: date.fromisoformat(val.decode()))
        sqlite3.register_converter('TIMESTAMP', lambda val: datetime.fromisoformat(val.decode()))

        Path(db_path).parent.mkdir(parents=True, exist_ok=True)

        self._db_path = Path(db_path)
        self._connection = sqlite3.connect(db_path, check_same_thread=check_same_thread, **kwargs)
        self._connection.isolation_level = None  # disable implicit transaction opening

    def disconnect(self) -> None:
        """
        Closes the connection to the SQLite database.
        """
        self.connection.close()
        self._connection = None

    def query(self, query: QueryStatement) -> list[Data]:
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
        _stmt, _params = build_sql_query(
            query,
            transform=get_sqlite_transform(),
        )

        try:
            cursor = self.execute(_stmt, *_params)
        except Exception as exc:
            msg = f'Error "{exc}" raised during executing query: {_stmt} with params: {_params}'
            raise ConnectionError(msg) from exc

        fields = []

        for column in cursor.description:
            if column[0] in fields:
                msg = f'Column name {column[0]} is duplicated'
                raise ValueError(msg)
            fields.append(column[0])

        result = [self.build_data(dict(zip(fields, row, strict=True))) for row in cursor.fetchall()]
        cursor.close()

        return result

    def query_schema(self, filters: Conditions | None = None) -> list[Schema]:
        """
        Queries the schema of the SQLite database.

        Args:
            filters (Conditions, optional): Filters to apply to the schema query. Defaults to None.

        Returns:
            list[Schema]: The list of schemas matching the filters.
        """
        stmt = self.TABLE_SQL

        if filters and filters.children:
            where, values = build_where(filters, transform=get_sqlite_transform())
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
        Runs a list of data mutations on the SQLite database.

        Args:
            mutations (list[DataMutation]): The list of data mutations to be executed.

        Returns:
            list[list[Data] | None]: The result of each mutation execution.
        """

        return [self._run_mutation(mutation) for mutation in mutations]

    def _run_mutation(self, mutation: DataMutation) -> list[Data] | None:
        _stmt, _params = build_sql_data_command(
            mutation,
            transform=get_sqlite_transform(),
        )

        try:
            self.execute(_stmt, *_params)
        except Exception as exc:
            msg = f'Mutation failed: {exc}'
            raise ConnectionError(msg) from exc
        return None

    def run_schema_command(self, command: SchemaCommand) -> list[Schema | None]:
        """
        Runs a schema command on the SQLite database.

        Args:
            command (SchemaCommand): The schema command to be executed.

        Returns:
            list[Schema | None]: The result of each schema mutation.
        """

        result: list[Schema | None] = []

        for mutation in command.mutations:
            data = self._run_schema_mutation(mutation)
            result.append(data)

        return result

    def execute(self, query: str, *args: Any) -> sqlite3.Cursor:
        """
        Executes a query on the SQLite database.

        Args:
            query (str): The query to be executed.
            *args (Any): The arguments for the query.

        Returns:
            sqlite3.Cursor: The cursor for the executed query.

        Raises:
            ConnectionError: If there is an error executing the query.
        """
        cursor = self.connection.cursor()

        try:
            if self.debug_queries:
                self._queries.append(query)

            cursor.execute(query, args)
        except sqlite3.Error as exc:
            msg = f'Error executing SQL: {query} with args: {args}. Exception: {exc}'
            raise ConnectionError(msg) from exc

        return cursor

    def get_table_info(
        self,
        table_name: str,
    ) -> tuple[list[PropertySchema], list[BaseConstraint], list[IndexSchema]]:
        """
        Gets the information of a table in the SQLite database.

        Args:
            table_name (str): The name of the table.

        Returns:
            tuple[list[PropertySchema], list[BaseConstraint], list[IndexSchema]]: The properties, constraints,
                                                                                  and indexes of the table.
        """
        cursor = self.execute(f"PRAGMA table_info('{table_name}')")
        columns = cursor.fetchall()
        cursor.close()

        cursor = self.execute(
            f"SELECT sql FROM sqlite_master WHERE type='table' AND name='{table_name}';"  # noqa: S608
        )
        table_sql = cursor.fetchone()[0]
        cursor.close()

        properties = [
            PropertySchema(
                name=column[1],
                type=self.to_python_type(column[2]),
                required=column[3] == 1,
                description=None,
                default=column[4],
            )
            for column in columns
        ]

        # Get primary keys
        constraints: list[BaseConstraint] = []

        pk_columns = [column[1] for column in columns if column[5]]
        if pk_columns:
            constraints.append(
                PrimaryKeyConstraint(
                    name=self._get_pk_name(table_sql) or f'pk_{table_name}',
                    fields=pk_columns,
                )
            )

        constraints.extend(self._get_unique_constrains(table_name, table_sql))

        # Get constraints info
        cursor = self.execute(f"PRAGMA foreign_key_list('{table_name}')")
        foreign_keys = cursor.fetchall()
        cursor.close()

        # Group foreign keys by their ID to handle composite foreign keys
        fk_groups = {}
        for fk in foreign_keys:
            fk_id = fk[0]  # ID of the foreign key constraint
            if fk_id not in fk_groups:
                fk_groups[fk_id] = {
                    'table': fk[2],  # Referenced table
                    'fields': [],  # Fields in this table
                    'ref_fields': [],  # Fields in referenced table
                }
            fk_groups[fk_id]['fields'].append(fk[3])
            fk_groups[fk_id]['ref_fields'].append(fk[4])

        # Create foreign key constraints
        for fk_group in fk_groups.values():
            # For composite keys, use the first field for naming if no constraint name is found
            primary_field = fk_group['fields'][0]
            constraint_name = self._get_fk_name(table_sql, field_name=primary_field)

            # If no constraint name is found, generate one based on the fields
            if not constraint_name:
                if len(fk_group['fields']) == 1:
                    constraint_name = f'fk_{primary_field}'
                else:
                    # For composite keys, include all field names in the constraint name
                    constraint_name = f'fk_{"_".join(fk_group["fields"])}'

            constraints.append(
                ForeignKeyConstraint(
                    name=constraint_name,
                    fields=fk_group['fields'],
                    reference_schema=SchemaReference(
                        name=fk_group['table'],
                        version=Version.LATEST,
                    ),
                    reference_fields=fk_group['ref_fields'],
                )
            )

        # Get indexes info
        cursor = self.execute(f"PRAGMA index_list('{table_name}')")
        indexes_list = cursor.fetchall()
        cursor.close()

        indexes = []

        for index in indexes_list:
            cursor = self.execute(f"PRAGMA index_info('{index[1]}')")
            index_info = cursor.fetchall()
            cursor.close()

            index_fields = [field[2] for field in index_info]

            if not self._is_constraint(index_fields, constraints) and not index[2]:
                if index[2]:
                    constraints.append(
                        UniqueConstraint(
                            name=index[1],
                            fields=index_fields,
                            condition=None,
                        ),
                    )
                else:
                    indexes.append(
                        IndexSchema(
                            name=index[1],
                            fields=index_fields,
                            condition=None,
                        ),
                    )

        return properties, constraints, indexes

    def acquire_lock(self, lock: ExecutionLockCommand) -> Any:
        """
        Acquires a lock on the SQLite database.

        Args:
            lock (ExecutionLockCommand): The lock command.

        Returns:
            Any: The result of the lock acquisition.
        """
        if lock.mode == 'EXCLUSIVE':
            self.connection.execute('BEGIN EXCLUSIVE')

        return True

    def release_lock(self, lock: ExecutionLockCommand) -> Any:
        """
        Releases a lock on the SQLite database.

        Args:
            lock (ExecutionLockCommand): The lock command.

        Returns:
            Any: The result of the lock release.
        """
        if lock.mode == 'EXCLUSIVE':
            self.connection.execute('COMMIT')

        return True

    def commit_transaction(self, transaction: TransactionCommand | str | None) -> Any:
        """
        Commits a transaction on the SQLite database.

        Args:
            transaction (TransactionCommand | str | None): The transaction command or transaction ID.

        Returns:
            Any: The result of the transaction commit.
        """
        if isinstance(transaction, TransactionCommand) and transaction.parent_transaction_id:
            self.connection.execute(f"RELEASE SAVEPOINT '{transaction.parent_transaction_id}'")
        else:
            self.connection.execute('COMMIT')
        return True

    def rollback_transaction(self, transaction: TransactionCommand | str | None) -> Any:
        """
        Rolls back a transaction on the SQLite database.

        Args:
            transaction (TransactionCommand | str | None): The transaction command or transaction ID.

        Returns:
            Any: The result of the transaction rollback.
        """
        if isinstance(transaction, TransactionCommand) and transaction.parent_transaction_id:
            self.connection.execute(f"ROLLBACK TO SAVEPOINT '{transaction.parent_transaction_id}'")
        else:
            self.connection.execute('ROLLBACK')
        return True

    def begin_transaction(self, transaction: TransactionCommand | str | None) -> Any:  # pragma: no cover
        """
        Begins a transaction on the SQLite database.

        Args:
            transaction (TransactionCommand | str | None): The transaction command or transaction ID.

        Returns:
            Any: The result of the transaction begin.
        """
        if isinstance(transaction, TransactionCommand) and transaction.parent_transaction_id:
            self.connection.execute(f"SAVEPOINT '{transaction.parent_transaction_id}'")
        else:
            self.connection.execute('BEGIN')
        return True

    def revert_transaction(self, transaction: TransactionCommand | str | None) -> Any:  # pragma: no cover
        """
        Reverts a transaction on the SQLite database.

        Args:
            transaction (TransactionCommand | str | None): The transaction command or transaction ID.

        Returns:
            Any: The result of the transaction revert.
        """
        if isinstance(transaction, TransactionCommand) and transaction.parent_transaction_id:
            self.connection.execute(f"ROLLBACK TO SAVEPOINT '{transaction.parent_transaction_id}'")
        else:
            self.connection.execute('ROLLBACK')
        return True

    def _run_schema_mutation(self, mutation: SchemaMutation) -> Schema | None:
        if isinstance(mutation, UpdateProperty):
            new_uuid = f'f{uuid.uuid4().hex}'

            new_property = mutation.property.__copy__()
            new_property.name = new_uuid

            if new_property.required and new_property.default is None:
                msg = (
                    f'Cannot update {mutation.property.name} column. '
                    f"SQLite doesn't support ALTER COLUMN with required=True and no default value."
                )
                raise ValueError(msg)

            statements = [
                build_add_column(mutation.schema_reference, new_property, type_transform=self.to_sql_type),
                build_migrate_column(mutation.schema_reference, mutation.property.name, new_uuid),
                build_drop_column(mutation.schema_reference, mutation.property.name),
                build_rename_column(mutation.schema_reference, new_uuid, mutation.property.name),
            ]
        elif isinstance(mutation, AddConstraint | DeleteConstraint):
            self._recreate_table_with_constraints(mutation)
            return None
        else:
            statements = build_schema_mutation(
                mutation,
                type_transform=self.to_sql_type,
                transform=get_sqlite_transform(),
            )

        for stmt, values in statements:
            self.execute(stmt, *values)

        if isinstance(mutation, RegisterSchema):
            return mutation.schema

        return None

    def _recreate_table_with_constraints(self, mutation: AddConstraint | DeleteConstraint) -> None:  # noqa: C901, PLR0912
        table_name = mutation.schema_reference.name
        namespace = mutation.schema_reference.namespace

        current_schemas = self.query_schema()
        current_schema = None
        for schema in current_schemas:
            schema_namespace = schema.namespace
            if schema.name == table_name and (
                (namespace is None and (schema_namespace is None or schema_namespace == ''))
                or (namespace == '' and (schema_namespace is None or schema_namespace == ''))
                or (namespace == schema_namespace)
            ):
                current_schema = schema
                break

        if current_schema is None:
            msg = f'Table {table_name} not found. Available tables: {[(s.name, s.namespace) for s in current_schemas]}'
            raise ValueError(msg)

        new_constraints = list(current_schema.constraints or [])

        if isinstance(mutation, AddConstraint):
            new_constraints.append(mutation.constraint)
        elif isinstance(mutation, DeleteConstraint):
            new_constraints = [c for c in new_constraints if c.name != mutation.constraint_name]

        new_schema = Schema(
            name=current_schema.name,
            namespace=current_schema.namespace,
            version=current_schema.version,
            properties=current_schema.properties,
            constraints=new_constraints,
            indexes=current_schema.indexes,
        )

        temp_table_name = f'temp_{table_name}_{uuid.uuid4().hex[:8]}'
        temp_schema = Schema(
            name=temp_table_name,
            namespace=namespace or '',
            version=new_schema.version,
            properties=new_schema.properties,
            constraints=new_schema.constraints,
            indexes=[],
        )

        # Check if we're already in a transaction by testing if we can start one
        # If we can't start a transaction, we're already in one
        in_transaction = False
        try:
            self.connection.execute('BEGIN')
        except sqlite3.OperationalError as e:
            if 'cannot start a transaction within a transaction' in str(e):
                in_transaction = True
            else:
                raise

        try:
            create_temp_stmt, create_temp_values = build_create_table(
                temp_schema,
                type_transform=self.to_sql_type,
                transform=get_sqlite_transform(),
            )
            self.execute(create_temp_stmt, *create_temp_values)

            namespace_prefix = f"'{namespace}'." if namespace else ''
            column_names = [prop.name for prop in current_schema.properties]
            columns_str_quoted = ', '.join(f"'{col}'" for col in column_names)
            columns_str_unquoted = ', '.join(f'"{col}"' for col in column_names)

            copy_stmt = (
                f"INSERT INTO {namespace_prefix}'{temp_table_name}' ({columns_str_quoted}) "  # noqa: S608
                f"SELECT {columns_str_unquoted} FROM {namespace_prefix}'{table_name}'"
            )
            self.execute(copy_stmt)

            drop_stmt = f"DROP TABLE {namespace_prefix}'{table_name}'"
            self.execute(drop_stmt)

            rename_stmt = f"ALTER TABLE {namespace_prefix}'{temp_table_name}' RENAME TO '{table_name}'"
            self.execute(rename_stmt)

            if current_schema.indexes:
                index_statements = build_create_indexes(
                    table_name,
                    namespace or '',
                    current_schema.indexes,
                    transform=get_sqlite_transform(),
                )
                for index_stmt, index_values in index_statements:
                    self.execute(index_stmt, *index_values)

            # Only commit if we started the transaction
            if not in_transaction:
                self.connection.execute('COMMIT')

        except Exception:
            # Only rollback if we started the transaction
            if not in_transaction:
                self.connection.execute('ROLLBACK')
            raise
