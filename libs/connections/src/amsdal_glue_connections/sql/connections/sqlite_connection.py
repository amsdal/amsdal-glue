import logging
import sqlite3
from datetime import date
from datetime import datetime
from pathlib import Path
from typing import Any

from amsdal_glue_core.commands.lock_command_node import ExecutionLockCommand
from amsdal_glue_core.common.data_models.conditions import Conditions
from amsdal_glue_core.common.data_models.constraints import BaseConstraint
from amsdal_glue_core.common.data_models.constraints import ForeignKeySchema
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
from amsdal_glue_core.common.operations.mutations.schema import RegisterSchema
from amsdal_glue_core.common.operations.mutations.schema import SchemaMutation

from amsdal_glue_connections.sql.sql_builders.command_builder import build_sql_data_command
from amsdal_glue_connections.sql.sql_builders.query_builder import build_sql_query
from amsdal_glue_connections.sql.sql_builders.query_builder import build_where
from amsdal_glue_connections.sql.sql_builders.schema_builder import build_schema_mutation

logger = logging.getLogger(__name__)


class SqliteConnection(ConnectionBase):
    def __init__(self) -> None:
        self._connection: sqlite3.Connection | None = None

    @property
    def is_connected(self) -> bool:
        return self._connection is not None

    @property
    def connection(self) -> sqlite3.Connection:
        if self._connection is None:
            msg = 'Connection not established'
            raise ConnectionError(msg)

        return self._connection

    def query(self, query: QueryStatement) -> list[Data]:
        _stmt, _params = build_sql_query(query)

        try:
            cursor = self.execute(_stmt, *_params)
        except Exception as exc:
            logger.exception('Error executing query: %s with params: %s', _stmt, _params)
            msg = f'Error executing query: {_stmt} with params: {_params}'
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
        stmt = 'SELECT name FROM sqlite_master WHERE type="table"'

        if filters:
            where, values = build_where(filters)
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
        return [self._run_mutation(mutation) for mutation in mutations]

    def _run_mutation(self, mutation: DataMutation) -> list[Data] | None:
        _stmt, _params = build_sql_data_command(mutation)

        try:
            self.execute(_stmt, *_params)
        except Exception as exc:
            logger.exception('Error executing mutation: %s with params: %s', _stmt, _params)
            msg = f'Error executing mutation: {_stmt} with params: {_params}'
            raise ConnectionError(msg) from exc
        return None

    def run_schema_command(self, command: SchemaCommand) -> list[Schema | None]:
        result: list[Schema | None] = []

        for mutation in command.mutations:
            data = self._run_schema_mutation(mutation)
            result.append(data)

        return result

    @staticmethod
    def build_data(data: dict[str, Any]) -> Data:
        return Data(data=data)

    def connect(self, db_path: Path, **kwargs: Any) -> None:
        if self._connection is not None:
            msg = 'Connection already established'
            raise ConnectionError(msg)

        Path(db_path).parent.mkdir(parents=True, exist_ok=True)

        self._connection = sqlite3.connect(db_path, **kwargs)
        self._connection.isolation_level = None  # disable implicit transaction opening

    def disconnect(self) -> None:
        self.connection.close()
        self._connection = None

    def execute(self, query: str, *args: Any) -> sqlite3.Cursor:
        cursor = self.connection.cursor()

        try:
            cursor.execute(query, args)
        except sqlite3.Error as exc:
            msg = f'Error executing query: {query} with args: {args}'
            raise ConnectionError(msg) from exc

        return cursor

    def get_table_info(
        self,
        table_name: str,
    ) -> tuple[list[PropertySchema], list[BaseConstraint], list[IndexSchema]]:
        cursor = self.execute(f'PRAGMA table_info({table_name})')
        columns = cursor.fetchall()
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

        # Get constraints info
        cursor = self.execute(f'PRAGMA foreign_key_list({table_name})')
        foreign_keys = cursor.fetchall()
        cursor.close()

        constraints: list[BaseConstraint] = [
            ForeignKeySchema(
                name=fk[0],
                fields=[fk[3]],
                reference_schema=SchemaReference(
                    name=fk[2],
                    version=Version.LATEST,
                ),
                reference_fields=[fk[4]],
            )
            for fk in foreign_keys
        ]

        # Get indexes info
        cursor = self.execute(f'PRAGMA index_list({table_name})')
        indexes_list = cursor.fetchall()
        cursor.close()

        indexes = []

        for index in indexes_list:
            cursor = self.execute(f'PRAGMA index_info({index[1]})')
            index_info = cursor.fetchall()
            cursor.close()

            index_fields = [field[2] for field in index_info]
            indexes.append(
                IndexSchema(
                    name=index[1],
                    fields=index_fields,
                    condition=None,
                ),
            )

        return properties, constraints, indexes

    def acquire_lock(self, lock: ExecutionLockCommand) -> Any:
        if lock.mode == 'EXCLUSIVE':
            self.connection.execute('BEGIN EXCLUSIVE')

        return True

    def release_lock(self, lock: ExecutionLockCommand) -> Any:
        if lock.mode == 'EXCLUSIVE':
            self.connection.execute('COMMIT')

        return True

    def commit_transaction(self, transaction: TransactionCommand | str | None) -> Any:
        if isinstance(transaction, TransactionCommand) and transaction.parent_transaction_id:
            return None

        self.connection.execute('COMMIT')
        return True

    def rollback_transaction(self, transaction: TransactionCommand | str | None) -> Any:
        if isinstance(transaction, TransactionCommand) and transaction.parent_transaction_id:
            return None

        self.connection.execute('ROLLBACK')
        return True

    def begin_transaction(self, transaction: TransactionCommand | str | None) -> Any:  # pragma: no cover
        if isinstance(transaction, TransactionCommand) and transaction.parent_transaction_id:
            return None

        self.connection.execute('BEGIN')
        return True

    def revert_transaction(self, transaction: TransactionCommand | str | None) -> Any:  # pragma: no cover
        if isinstance(transaction, TransactionCommand) and transaction.parent_transaction_id:
            return None

        self.connection.execute('ROLLBACK')
        return True

    def _run_schema_mutation(self, mutation: SchemaMutation) -> Schema | None:
        statements = build_schema_mutation(mutation, type_transform=self.to_sql_type)

        for stmt in statements:
            self.execute(stmt)

        if isinstance(mutation, RegisterSchema):
            return mutation.schema

        return None

    @staticmethod
    def to_sql_type(property_type: Schema | SchemaReference | type[Any]) -> str:  # noqa: PLR0911
        if property_type is str:
            return 'TEXT'
        if property_type is int:
            return 'INTEGER'
        if property_type is float:
            return 'REAL'
        if property_type is bool:
            return 'BOOLEAN'
        if property_type is dict:
            return 'JSON'
        if property_type in (bytes, bytearray):
            return 'BLOB'
        if isinstance(property_type, Schema | SchemaReference):
            return 'TEXT'
        if property_type == datetime:
            return 'TIMESTAMP'
        if property_type == date:
            return 'DATE'

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
            return dict
        if sql_type == 'BLOB':
            return bytes
        if sql_type == 'TIMESTAMP':
            return datetime
        if sql_type == 'DATE':
            return date

        msg = f'Unsupported type: {sql_type}'
        raise ValueError(msg)
