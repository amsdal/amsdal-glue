import json
import logging
import re
import sqlite3
import uuid
from copy import copy
from datetime import date
from datetime import datetime
from pathlib import Path
from typing import Any

from amsdal_glue_core.commands.lock_command_node import ExecutionLockCommand
from amsdal_glue_core.common.data_models.conditions import Condition
from amsdal_glue_core.common.data_models.conditions import Conditions
from amsdal_glue_core.common.data_models.constraints import BaseConstraint
from amsdal_glue_core.common.data_models.constraints import ForeignKeyConstraint
from amsdal_glue_core.common.data_models.constraints import PrimaryKeyConstraint
from amsdal_glue_core.common.data_models.constraints import UniqueConstraint
from amsdal_glue_core.common.data_models.data import Data
from amsdal_glue_core.common.data_models.indexes import IndexSchema
from amsdal_glue_core.common.data_models.query import QueryStatement
from amsdal_glue_core.common.data_models.schema import ArraySchemaModel
from amsdal_glue_core.common.data_models.schema import DictSchemaModel
from amsdal_glue_core.common.data_models.schema import NestedSchemaModel
from amsdal_glue_core.common.data_models.schema import PropertySchema
from amsdal_glue_core.common.data_models.schema import Schema
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.enums import Version
from amsdal_glue_core.common.interfaces.connection import ConnectionBase
from amsdal_glue_core.common.operations.commands import SchemaCommand
from amsdal_glue_core.common.operations.commands import TransactionCommand
from amsdal_glue_core.common.operations.mutations.data import DataMutation
from amsdal_glue_core.common.operations.mutations.schema import RegisterSchema
from amsdal_glue_core.common.operations.mutations.schema import SchemaMutation
from amsdal_glue_core.common.operations.mutations.schema import UpdateProperty

from amsdal_glue_connections.sql.constants import SCHEMA_REGISTRY_TABLE
from amsdal_glue_connections.sql.sql_builders.command_builder import build_sql_data_command
from amsdal_glue_connections.sql.sql_builders.math_operator_transform import sqlite_math_operator_transform
from amsdal_glue_connections.sql.sql_builders.query_builder import build_sql_query
from amsdal_glue_connections.sql.sql_builders.query_builder import build_where
from amsdal_glue_connections.sql.sql_builders.schema_builder import build_add_column
from amsdal_glue_connections.sql.sql_builders.schema_builder import build_drop_column
from amsdal_glue_connections.sql.sql_builders.schema_builder import build_migrate_column
from amsdal_glue_connections.sql.sql_builders.schema_builder import build_rename_column
from amsdal_glue_connections.sql.sql_builders.schema_builder import build_schema_mutation

logger = logging.getLogger(__name__)

UNIQUE_CONSTRAINT_RE = re.compile(r'CONSTRAINT ["\'](?P<name>\w+)["\'] UNIQUE \((?P<fields>[^)]+)\)')
PRIMARY_KEY_RE = re.compile(r'CONSTRAINT ["\'](?P<name>\w+)["\'] PRIMARY KEY')
FIELDS_RE = re.compile(r'["\'](?P<name>\w+)["\']')


def sqlite_value_json_transform(value: Any) -> Any:
    if isinstance(value, dict | list):
        return json.dumps(value)

    return value


def sqlite_field_json_transform(  # noqa: PLR0913
    table_alias: str,
    namespace: str,  # noqa: ARG001
    field: str,
    fields: list[str],
    value_type: Any = str,
    table_separator: str = '.',
    table_quote: str = "'",
    field_quote: str = "'",
) -> str:
    nested_fields_selection = '.'.join([
        '$',
        *fields,
    ])

    if value_type in (int, bool):
        _cast_type = 'integer'
    elif value_type is float:
        _cast_type = 'real'
    else:
        _cast_type = 'text'

    _table_reference = f'{table_quote}{table_alias}{table_quote}{table_separator}' if table_alias else ''
    _stmt = f"cast(json_extract({_table_reference}{field_quote}{field}{field_quote}, '{nested_fields_selection}')"

    if _cast_type:
        _stmt += f' as {_cast_type})'

    return _stmt


class JsonTypeMeta(type):
    def __eq__(cls, other: object) -> bool:
        return other in (list, dict)


class JsonType(dict, metaclass=JsonTypeMeta): ...  # type: ignore[misc]


class SqliteConnection(ConnectionBase):
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
        self._queries: list[str] = []

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
            table_quote="'",
            field_quote="'",
            value_transform=sqlite_value_json_transform,
            nested_field_transform=sqlite_field_json_transform,
            math_operator_transform=sqlite_math_operator_transform,
        )

        try:
            cursor = self.execute(_stmt, *_params)
        except Exception as exc:
            logger.exception('Error executing query: %s with params: %s', _stmt, _params)
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
        stmt = 'SELECT name FROM sqlite_master WHERE type="table"'

        if filters and filters.children:
            _filters = self._replace_table_name(filters, 'sqlite_master')
            where, values = build_where(_filters)
            stmt += f' AND {where}'
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
            table_quote="'",
            field_quote="'",
            value_transform=sqlite_value_json_transform,
            nested_field_transform=sqlite_field_json_transform,
        )

        try:
            self.execute(_stmt, *_params)
        except Exception as exc:
            logger.exception('Error executing mutation: %s with params: %s', _stmt, _params)
            msg = f'Error executing mutation: {_stmt} with params: {_params}'
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

    @staticmethod
    def build_data(data: dict[str, Any]) -> Data:
        """
        Builds a Data object from a dictionary.

        Args:
            data (dict[str, Any]): The data dictionary.

        Returns:
            Data: The Data object.
        """
        for key, value in data.items():
            if isinstance(value, str) and (
                (value.startswith('{') and value.endswith('}')) or (value.startswith('[') and value.endswith(']'))
            ):
                data[key] = json.loads(value)

        return Data(data=data)

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
            msg = f'Error executing query: {query} with args: {args}. Exception: {exc}'
            logger.exception(msg)
            raise ConnectionError(msg) from exc

        return cursor

    def _get_unique_constrains(self, table_sql: str) -> list[UniqueConstraint]:
        unique_constraints = []

        for constraint_name, field_names in UNIQUE_CONSTRAINT_RE.findall(table_sql):
            fields = FIELDS_RE.findall(field_names)
            unique_constraints.append(
                UniqueConstraint(
                    name=constraint_name,
                    fields=fields,
                    condition=None,
                )
            )

        return unique_constraints

    def _get_pk_name(self, table_sql: str) -> str:
        for constraint_name in PRIMARY_KEY_RE.findall(table_sql):
            return constraint_name

        return ''

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

        constraints.extend(self._get_unique_constrains(table_sql))

        # Get constraints info
        cursor = self.execute(f"PRAGMA foreign_key_list('{table_name}')")
        foreign_keys = cursor.fetchall()
        cursor.close()

        constraints.extend(
            [
                ForeignKeyConstraint(
                    name=fk[0],
                    fields=[fk[3]],
                    reference_schema=SchemaReference(
                        name=fk[2],
                        version=Version.LATEST,
                    ),
                    reference_fields=[fk[4]],
                )
                for fk in foreign_keys
            ],
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

    @staticmethod
    def _is_constraint(index_fields: list[str], constraints: list[BaseConstraint]) -> bool:
        for constraint in constraints:
            if not isinstance(constraint, PrimaryKeyConstraint | ForeignKeyConstraint | UniqueConstraint):
                continue

            if index_fields == constraint.fields:
                return True
        return False

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

            if new_property.required:
                logger.warning('Trying to update a property to required, which is not supported. Setting it to False.')
                new_property.required = False

            statements = [
                build_add_column(mutation.schema_reference, new_property, type_transform=self.to_sql_type),
                build_migrate_column(mutation.schema_reference, mutation.property.name, new_uuid),
                build_drop_column(mutation.schema_reference, mutation.property.name),
                build_rename_column(mutation.schema_reference, new_uuid, mutation.property.name),
            ]
        else:
            statements = build_schema_mutation(mutation, type_transform=self.to_sql_type)

        for stmt in statements:
            self.execute(stmt)

        if isinstance(mutation, RegisterSchema):
            return mutation.schema

        return None

    @staticmethod
    def to_sql_type(  # noqa: C901, PLR0911
        property_type: Schema | SchemaReference | NestedSchemaModel | ArraySchemaModel | DictSchemaModel | type[Any],
    ) -> str:
        if property_type is str:
            return 'TEXT'
        if property_type is int:
            return 'INTEGER'
        if property_type is float:
            return 'REAL'
        if property_type is bool:
            return 'BOOLEAN'
        if property_type in (dict, list):
            return 'JSON'
        if property_type in (bytes, bytearray):
            return 'BLOB'
        if isinstance(property_type, Schema | SchemaReference):
            return 'TEXT'
        if property_type == datetime:
            return 'TIMESTAMP'
        if property_type == date:
            return 'DATE'
        if isinstance(property_type, NestedSchemaModel | ArraySchemaModel | DictSchemaModel):
            logger.warning('Unsupported type: %s. Using JSON instead.', property_type)
            return 'JSON'

        msg = f'Unsupported type: {property_type}'
        raise ValueError(msg)

    def to_python_type(self, sql_type: str) -> type[Any]:  # noqa: PLR0911
        sql_type = sql_type.upper()

        if sql_type == 'TEXT' or sql_type.startswith('VARCHAR'):
            return str
        if sql_type in ('INTEGER', 'INT'):
            return int
        if sql_type == 'REAL':
            return float
        if sql_type == 'BOOLEAN':
            return bool
        if sql_type == 'JSON':
            return JsonType
        if sql_type == 'BLOB':
            return bytes
        if sql_type == 'TIMESTAMP':
            return datetime
        if sql_type == 'DATE':
            return date

        msg = f'Unsupported type: {sql_type}'
        raise ValueError(msg)

    def _replace_table_name(self, conditions: Conditions, replace_name: str) -> Conditions:
        _childs: list[Conditions | Condition] = []

        for _child in conditions.children:
            if isinstance(_child, Conditions):
                _childs.append(self._replace_table_name(_child, replace_name))
            elif _child.field.table_name == SCHEMA_REGISTRY_TABLE:
                _copy = copy(_child)
                _copy.field.table_name = replace_name
                _childs.append(_copy)

        return Conditions(*_childs, connector=conditions.connector, negated=conditions.negated)

    @property
    def queries(self) -> list[str]:
        """
        Returns the queries executed on this connection.

        Returns:
            list[str]: The queries executed.
        """
        return self._queries
