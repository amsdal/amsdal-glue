import json
import logging
from copy import copy
from datetime import date
from datetime import datetime
from typing import Any

from amsdal_glue_core.commands.lock_command_node import ExecutionLockCommand
from amsdal_glue_core.common.data_models.conditions import Condition
from amsdal_glue_core.common.data_models.conditions import Conditions
from amsdal_glue_core.common.data_models.constraints import BaseConstraint
from amsdal_glue_core.common.data_models.constraints import CheckConstraint
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

from amsdal_glue_connections.sql.constants import SCHEMA_REGISTRY_TABLE
from amsdal_glue_connections.sql.sql_builders.build_only_constructor import pg_build_only
from amsdal_glue_connections.sql.sql_builders.command_builder import build_sql_data_command
from amsdal_glue_connections.sql.sql_builders.operator_constructor import repr_operator_constructor
from amsdal_glue_connections.sql.sql_builders.pg_operator_cosntructor import pg_operator_constructor
from amsdal_glue_connections.sql.sql_builders.query_builder import build_sql_query
from amsdal_glue_connections.sql.sql_builders.query_builder import build_where

logger = logging.getLogger(__name__)


def pg_value_json_transform(value: Any) -> Any:
    from psycopg.types.json import Json
    from psycopg.types.json import Jsonb

    if isinstance(value, dict | list):
        return Jsonb(value)

    if isinstance(value, str) and value.startswith('"') and value.endswith('"'):
        return Json(value[1:-1])

    return value


def pg_field_json_transform(  # noqa: PLR0913
    table_alias: str,
    namespace: str,
    field: str,
    fields: list[str],
    value_type: Any = str,
    table_separator: str = '.',
    table_quote: str = "'",
    field_quote: str = "'",
) -> str:
    if value_type is int:
        _cast_type = 'integer'
    elif value_type is bool:
        _cast_type = 'boolean'
    elif value_type is float:
        _cast_type = 'real'
    else:
        _cast_type = 'text'

    nested_fields_selection = '->>'.join(f"'{_field}'" for _field in fields)
    _namespace_prefix = f'{table_quote}{namespace}{table_quote}{table_separator}' if namespace else ''
    _stmt = (
        f'cast(({_namespace_prefix}'
        f'{table_quote}{table_alias}{table_quote}{table_separator}'
        f'{field_quote}{field}{field_quote}::json->'
        f'{nested_fields_selection})::text as {_cast_type})'
    )

    if _cast_type == 'text':
        _stmt = f"trim('\"' FROM {_stmt})::text"

    return _stmt


class PostgresConnection(ConnectionBase):
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
        self._queries: list[str] = []

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
        _stmt, _params = build_sql_query(
            query,
            operator_constructor=pg_operator_constructor,
            value_transform=pg_value_json_transform,
            nested_field_transform=pg_field_json_transform,
            value_placeholder='%s',
            table_quote='"',
            field_quote='"',
            build_only=pg_build_only,
        )

        try:
            cursor = self.execute(_stmt, *_params)
        except Exception as exc:
            logger.exception('Error executing query: %s with params: %s', _stmt, _params)
            msg = f'Error executing query: {_stmt} with params: {_params}'
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

    @classmethod
    def _adjust_schema_filters(cls, filters: Conditions | None) -> None:
        """
        Transform "name" attribute of the filters to the correct column name: "table_name"
        """

        if filters is None:
            return

        for _filter in filters.children:
            if isinstance(_filter, Conditions):
                cls._adjust_schema_filters(_filter)

            elif _filter.field.field.name == 'name':
                _filter.field.field.name = 'table_name'

    def query_schema(self, filters: Conditions | None = None) -> list[Schema]:
        """
        Queries the schema of the PostgreSQL database.

        Args:
            filters (Conditions | None): The filters to be applied to the schema query.

        Returns:
            list[Schema]: The result of the schema query.
        """
        self._adjust_schema_filters(filters)

        stmt = "SELECT table_name FROM information_schema.tables AS inf_schema WHERE table_schema = 'public'"

        if filters and filters.children:
            _filters = self._replace_table_name(filters, 'inf_schema')
            where, values = build_where(
                _filters,
                operator_constructor=pg_operator_constructor,
                value_transform=pg_value_json_transform,
                nested_field_transform=pg_field_json_transform,
                value_placeholder='%s',
                table_quote='"',
                field_quote='"',
            )
            stmt += f' AND ({where})'
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
        _stmt, _params = build_sql_data_command(
            mutation,
            operator_constructor=pg_operator_constructor,
            value_transform=pg_value_json_transform,
            nested_field_transform=pg_field_json_transform,
            value_placeholder='%s',
            table_quote='"',
            field_quote='"',
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

    @staticmethod
    def build_data(data: dict[str, Any]) -> Data:
        """
        Builds a Data object from a dictionary.

        Args:
            data (dict[str, Any]): The data dictionary.

        Returns:
            Data: The built Data object.
        """
        for key, value in data.items():
            if isinstance(value, str) and (
                (value.startswith('{') and value.endswith('}')) or (value.startswith('[') and value.endswith(']'))
            ):
                data[key] = json.loads(value)
        return Data(data=data)

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

            cursor = self.connection.execute(query, args)
        except psycopg.Error as exc:
            msg = f'Error executing query: {query} with args: {args}'
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
            'SELECT ordinal_position, column_name, data_type, is_nullable, column_default '  # noqa: S608
            'FROM information_schema.columns '
            f"WHERE table_name = '{table_name}';"
        )
        columns = cursor.fetchall()
        cursor.close()

        properties = [
            PropertySchema(
                name=column[1],
                type=self._to_python_type(column[2]),
                required=column[3].lower() == 'no',  # means is nullable
                description=None,
                default=column[4],
            )
            for column in columns
        ]
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
            'SELECT i.relname as index_name, array_agg(a.attname) as column_names '  # noqa: S608
            'FROM pg_class t, pg_class i, pg_index ix, pg_attribute a '
            'WHERE t.oid = ix.indrelid AND i.oid = ix.indexrelid AND a.attrelid = t.oid '
            f"AND a.attnum = ANY(ix.indkey) AND t.relkind = 'r' AND t.relname = '{table_name}' "
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

    def _run_schema_mutation(self, migration: SchemaMutation) -> Schema | None:  # noqa: PLR0911, C901
        if isinstance(migration, RegisterSchema):
            schema = migration.schema
            self._create_table(schema)

            return schema

        if isinstance(migration, DeleteSchema):
            self._drop_table(migration.schema_reference)

            return None

        if isinstance(migration, RenameSchema):
            schema_reference = migration.schema_reference
            new_schema_name = migration.new_schema_name
            self._rename_table(schema_reference, new_schema_name)

            return None

        if isinstance(migration, AddProperty):
            schema_reference = migration.schema_reference
            _property = migration.property
            self._add_column(schema_reference, _property)

            return None

        if isinstance(migration, DeleteProperty):
            schema_reference = migration.schema_reference
            property_name = migration.property_name
            self._drop_column(schema_reference, property_name)

            return None

        if isinstance(migration, RenameProperty):
            schema_reference = migration.schema_reference
            old_name = migration.old_name
            new_name = migration.new_name
            self._rename_column(schema_reference, old_name, new_name)

            return None

        if isinstance(migration, UpdateProperty):
            schema_reference = migration.schema_reference
            _property = migration.property
            self._update_column(schema_reference, _property)

            return None

        if isinstance(migration, AddConstraint):
            schema_reference = migration.schema_reference
            constraint = migration.constraint
            self._add_constraint(schema_reference, constraint)

            return None

        if isinstance(migration, DeleteConstraint):
            schema_reference = migration.schema_reference
            constraint_name = migration.constraint_name
            self._drop_constraint(schema_reference, constraint_name)

            return None

        if isinstance(migration, AddIndex):
            schema_reference = migration.schema_reference
            index = migration.index
            self._add_index(schema_reference, index)

            return None

        if isinstance(migration, DeleteIndex):
            schema_reference = migration.schema_reference
            index_name = migration.index_name
            self._drop_index(schema_reference, index_name)

            return None

        msg = f'Unsupported schema mutation: {type(migration)}'
        raise ValueError(msg)

    def _create_table(self, schema: Schema) -> None:
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

        self.execute(stmt)

        for _index in schema.indexes or []:
            _index_stmt = self._build_index(schema.name, schema.namespace, _index)
            self.execute(_index_stmt)

    def _drop_table(self, schema_reference: SchemaReference) -> None:
        _namespace_prefix = f'"{schema_reference.namespace}".' if schema_reference.namespace else ''
        stmt = f'DROP TABLE {_namespace_prefix}"{schema_reference.name}"'
        self.execute(stmt)

    def _rename_table(self, schema_reference: SchemaReference, new_schema_name: str) -> None:
        _namespace_prefix = f'"{schema_reference.namespace}".' if schema_reference.namespace else ''

        stmt = f'ALTER TABLE {_namespace_prefix}"{schema_reference.name}" RENAME TO "{new_schema_name}"'
        self.execute(stmt)

    def _add_column(self, schema_reference: SchemaReference, _property: PropertySchema) -> None:
        _column = self._build_column(_property, force_nullable=True)
        _namespace_prefix = f'"{schema_reference.namespace}".' if schema_reference.namespace else ''

        stmt = f'ALTER TABLE {_namespace_prefix}"{schema_reference.name}" ADD COLUMN {_column}'
        self.execute(stmt)

    def _drop_column(self, schema_reference: SchemaReference, property_name: str) -> None:
        _namespace_prefix = f'"{schema_reference.namespace}".' if schema_reference.namespace else ''

        stmt = f'ALTER TABLE {_namespace_prefix}"{schema_reference.name}" DROP COLUMN "{property_name}"'
        self.execute(stmt)

    def _rename_column(self, schema_reference: SchemaReference, old_name: str, new_name: str) -> None:
        _namespace_prefix = f'"{schema_reference.namespace}".' if schema_reference.namespace else ''

        stmt = f'ALTER TABLE "{schema_reference.name}" RENAME COLUMN "{old_name}" TO "{new_name}"'
        self.execute(stmt)

    def _update_column(self, schema_reference: SchemaReference, _property: PropertySchema) -> None:
        _column = self._build_column_update(_property)
        _namespace_prefix = f'"{schema_reference.namespace}".' if schema_reference.namespace else ''

        stmt = f'ALTER TABLE {_namespace_prefix}"{schema_reference.name}" ALTER COLUMN {_column}'
        self.execute(stmt)

    def _add_constraint(self, schema_reference: SchemaReference, constraint: BaseConstraint) -> None:
        _constraint_stmt = self._build_constraint(constraint)
        _namespace_prefix = f'"{schema_reference.namespace}".' if schema_reference.namespace else ''
        stmt = f'ALTER TABLE {_namespace_prefix}"{schema_reference.name}" ADD {_constraint_stmt}'
        self.execute(stmt)

    def _drop_constraint(self, schema_reference: SchemaReference, constraint_name: str) -> None:
        _namespace_prefix = f'"{schema_reference.namespace}".' if schema_reference.namespace else ''
        stmt = f'ALTER TABLE {_namespace_prefix}"{schema_reference.name}" DROP CONSTRAINT "{constraint_name}"'
        self.execute(stmt)

    def _add_index(self, schema_reference: SchemaReference, index: IndexSchema) -> None:
        _index_stmt = self._build_index(schema_reference.name, schema_reference.namespace or '', index)

        self.execute(_index_stmt)

    def _drop_index(self, schema_reference: SchemaReference, index_name: str) -> None:
        _namespace_prefix = f'"{schema_reference.namespace}".' if schema_reference.namespace else ''
        stmt = f'DROP INDEX {_namespace_prefix}"{index_name}"'
        self.execute(stmt)

    def _build_column(self, column: PropertySchema, *, force_nullable: bool = False) -> str:
        return (
            f'"{column.name}" {self._to_sql_type(column.type)}'
            f'{" NOT NULL" if column.required and not force_nullable else ""}'
        )

    def _build_column_update(self, column: PropertySchema) -> str:
        return f'"{column.name}" TYPE {self._to_sql_type(column.type)}{" NOT NULL" if column.required else ""}'

    def _build_constraint(self, constraint: BaseConstraint) -> str:
        if isinstance(constraint, PrimaryKeyConstraint):
            return f'CONSTRAINT {constraint.name} ' f'PRIMARY KEY ({", ".join(constraint.fields)}) '
        if isinstance(constraint, ForeignKeyConstraint):
            return (
                f'CONSTRAINT "{constraint.name}" '
                f'FOREIGN KEY ({", ".join(constraint.fields)}) '
                f'REFERENCES {constraint.reference_schema.name} ({", ".join(constraint.reference_fields)})'
            )
        if isinstance(constraint, UniqueConstraint):
            return f'CONSTRAINT {constraint.name} ' f'UNIQUE ({", ".join(constraint.fields)})'
        if isinstance(constraint, CheckConstraint):
            _where, _ = build_where(
                constraint.condition,
                operator_constructor=repr_operator_constructor,
                value_placeholder='%s',
                table_quote='"',
                field_quote='"',
            )

            return f'CONSTRAINT {constraint.name} ' f'CHECK ({_where})'

        msg = f'Unsupported constraint: {type(constraint)}'
        raise ValueError(msg)

    def _build_index(self, schema_name: str, namespace: str, index: IndexSchema) -> str:
        _namespace_prefix = f'"{namespace}".' if namespace else ''
        _index = (
            f'CREATE INDEX {_namespace_prefix}"{index.name}" '
            f'ON {_namespace_prefix}"{schema_name}" ({", ".join(index.fields)})'
        )

        if index.condition:
            where, _ = build_where(
                index.condition,
                operator_constructor=repr_operator_constructor,
                table_quote='"',
                field_quote='"',
            )
            _index += f' WHERE {where}'

        return _index

    def _to_sql_type(  # noqa: C901, PLR0911
        self,
        property_type: Schema | SchemaReference | NestedSchemaModel | ArraySchemaModel | DictSchemaModel | type[Any],
    ) -> str:
        if property_type is str:
            return 'TEXT'
        if property_type is int:
            return 'BIGINT'
        if property_type is float:
            return 'DOUBLE PRECISION'
        if property_type is bool:
            return 'BOOLEAN'
        if property_type in (dict, list):
            return 'JSON'
        if property_type in (bytes, bytearray):
            return 'BYTEA'
        if isinstance(property_type, Schema | SchemaReference):
            return 'TEXT'
        if property_type == datetime:
            return 'TIMESTAMP WITH TIME ZONE'
        if property_type == date:
            return 'DATE'
        if isinstance(property_type, NestedSchemaModel | ArraySchemaModel | DictSchemaModel):
            logger.warning('Unsupported type: %s. Using JSON instead.', property_type)
            return 'JSON'

        msg = f'Unsupported type: {property_type}'
        raise ValueError(msg)

    def _to_python_type(self, sql_type: str) -> type[Any]:  # noqa: PLR0911
        sql_type = sql_type.upper()

        if sql_type in ['TEXT', 'CHARACTER VARYING'] or sql_type.startswith('VARCHAR'):
            return str
        if sql_type in ('BIGINT', 'INT', 'INTEGER', 'SMALLINT'):
            return int
        if sql_type in ('DOUBLE PRECISION', 'REAL', 'NUMERIC', 'DECIMAL'):
            return float
        if sql_type == 'BOOLEAN':
            return bool
        if sql_type == 'JSON':
            return dict
        if sql_type == 'BYTEA':
            return bytes
        if sql_type == 'TIMESTAMP' or sql_type.startswith('TIMESTAMP'):
            return datetime
        if sql_type == 'DATE':
            return date

        msg = f'Unsupported type: {sql_type}'
        raise ValueError(msg)

    @property
    def queries(self) -> list[str]:
        """
        Returns the queries executed on this connection.

        Returns:
            list[str]: The queries executed.
        """
        return self._queries
