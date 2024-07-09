import logging
from datetime import date
from datetime import datetime
from typing import Any

try:
    import psycopg2
except ImportError:
    msg = (
        '"psycopg2" package is required for PostgresConnection. '
        'Use "pip install amsdal-glue-connections[postgres]" to install it.'
    )
    raise ImportError(msg) from None

import psycopg2._psycopg
from amsdal_glue_core.commands.lock_command_node import ExecutionLockCommand
from amsdal_glue_core.common.data_models.conditions import Conditions
from amsdal_glue_core.common.data_models.constraints import BaseConstraint
from amsdal_glue_core.common.data_models.constraints import CheckConstraint
from amsdal_glue_core.common.data_models.constraints import ForeignKeySchema
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

from amsdal_glue_connections.sql.sql_builders.command_builder import build_sql_data_command
from amsdal_glue_connections.sql.sql_builders.operator_constructor import repr_operator_constructor
from amsdal_glue_connections.sql.sql_builders.query_builder import build_sql_query
from amsdal_glue_connections.sql.sql_builders.query_builder import build_where

logger = logging.getLogger(__name__)


class PostgresConnection(ConnectionBase):
    def __init__(self) -> None:
        self._connection: psycopg2._psycopg.connection | None = None

    @property
    def is_connected(self) -> bool:
        return self._connection is not None

    @property
    def connection(self) -> psycopg2._psycopg.connection:
        if self._connection is None:
            msg = 'Connection not established'
            raise ConnectionError(msg)

        return self._connection

    def connect(self, dsn: str | None = None, **kwargs: Any) -> None:
        if self._connection is not None:
            msg = 'Connection already established'
            raise ConnectionError(msg)

        self._connection = psycopg2.connect(dsn, **kwargs)

    def disconnect(self) -> None:
        self.connection.close()
        self._connection = None

    def query(self, query: QueryStatement) -> list[Data]:
        _stmt, _params = build_sql_query(query, value_placeholder='%s')

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
        stmt = "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"

        if filters:
            where, values = build_where(filters)
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

    def run_mutations(self, mutations: list[DataMutation]) -> list[list[Data] | None]:
        return [self._run_mutation(mutation) for mutation in mutations]

    def _run_mutation(self, mutation: DataMutation) -> list[Data] | None:
        _stmt, _params = build_sql_data_command(mutation, value_placeholder='%s')

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

    def execute(self, query: str, *args: Any) -> psycopg2._psycopg.cursor:
        cursor = self.connection.cursor()

        try:
            cursor.execute(query, args)
        except psycopg2.Error as exc:
            msg = f'Error executing query: {query} with args: {args}'
            raise ConnectionError(msg) from exc

        return cursor

    def get_table_info(
        self,
        table_name: str,
    ) -> tuple[list[PropertySchema], list[BaseConstraint], list[IndexSchema]]:
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
                required=column[3] == 1,
                description=None,
                default=column[4],
            )
            for column in columns
        ]
        fid_to_name: dict[int, str] = {column[0]: column[1] for column in columns}

        # Get constraints info
        cursor = self.execute(
            'SELECT conname, contype, confrelid, conkey, confkey '  # noqa: S608
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
                cursor = self.execute(
                    'SELECT ordinal_position, column_name '  # noqa: S608
                    'FROM information_schema.columns '
                    f"WHERE table_name = '{f_table_name}';"
                )
                f_table_fields = {row[0]: row[1] for row in cursor.fetchall()}
                cursor.close()

                constraints.append(
                    ForeignKeySchema(
                        name=raw_constrain[0],
                        fields=[fid_to_name.get(fk) for fk in raw_constrain[3]],
                        reference_schema=SchemaReference(
                            name=f_table_name,
                            version=Version.LATEST,
                        ),
                        reference_fields=[f_table_fields.get(fid) for fid in raw_constrain[4]],
                    )
                )

            if raw_constrain[1] == 'p':
                constraints.append(
                    PrimaryKeyConstraint(
                        name=raw_constrain[0],
                        fields=[fid_to_name.get(pk) for pk in raw_constrain[3]],
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
        ]

        return properties, constraints, indexes

    def acquire_lock(self, lock: ExecutionLockCommand) -> Any:
        if lock.mode == 'EXCLUSIVE':
            self.execute('BEGIN EXCLUSIVE')

        return True

    def release_lock(self, lock: ExecutionLockCommand) -> Any:
        if lock.mode == 'EXCLUSIVE':
            self.execute('COMMIT')

        return True

    def commit_transaction(self, transaction: TransactionCommand | str | None) -> Any:
        if isinstance(transaction, TransactionCommand) and transaction.parent_transaction_id:
            return True

        self.execute('COMMIT')
        return True

    def rollback_transaction(self, transaction: TransactionCommand | str | None) -> Any:
        if isinstance(transaction, TransactionCommand) and transaction.parent_transaction_id:
            self.execute(f'ROLLBACK TO SAVEPOINT "{transaction.transaction_id}"')
            return True

        self.execute('ROLLBACK')
        return True

    def begin_transaction(self, transaction: TransactionCommand | str | None) -> Any:  # pragma: no cover
        if isinstance(transaction, TransactionCommand) and transaction.parent_transaction_id:
            self.execute(f'SAVEPOINT "{transaction.transaction_id}"')
            return True

        self.execute('BEGIN')
        return True

    def revert_transaction(self, transaction: TransactionCommand | str | None) -> Any:  # pragma: no cover
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

        stmt = f'CREATE TABLE "{schema.name}" ('
        stmt += ', '.join(self._build_column(column) for column in schema.properties)

        if _constraint_stmts:
            stmt += ', '
            stmt += ', '.join(_constraint_stmts)

        stmt += ')'

        self.execute(stmt)

        for _index in schema.indexes or []:
            _index_stmt = self._build_index(schema.name, _index)
            self.execute(_index_stmt)

    def _drop_table(self, schema_reference: SchemaReference) -> None:
        stmt = f'DROP TABLE "{schema_reference.name}"'
        self.execute(stmt)

    def _rename_table(self, schema_reference: SchemaReference, new_schema_name: str) -> None:
        stmt = f'ALTER TABLE "{schema_reference.name}" RENAME TO "{new_schema_name}"'
        self.execute(stmt)

    def _add_column(self, schema_reference: SchemaReference, _property: PropertySchema) -> None:
        _column = self._build_column(_property)
        stmt = f'ALTER TABLE "{schema_reference.name}" ADD COLUMN {_column}'
        self.execute(stmt)

    def _drop_column(self, schema_reference: SchemaReference, property_name: str) -> None:
        stmt = f'ALTER TABLE "{schema_reference.name}" DROP COLUMN "{property_name}"'
        self.execute(stmt)

    def _rename_column(self, schema_reference: SchemaReference, old_name: str, new_name: str) -> None:
        stmt = f'ALTER TABLE "{schema_reference.name}" RENAME COLUMN "{old_name}" TO "{new_name}"'
        self.execute(stmt)

    def _update_column(self, schema_reference: SchemaReference, _property: PropertySchema) -> None:
        _column = self._build_column_update(_property)
        stmt = f'ALTER TABLE "{schema_reference.name}" ALTER COLUMN {_column}'
        self.execute(stmt)

    def _add_constraint(self, schema_reference: SchemaReference, constraint: BaseConstraint) -> None:
        _constraint_stmt = self._build_constraint(constraint)
        stmt = f'ALTER TABLE "{schema_reference.name}" ADD {_constraint_stmt}'
        self.execute(stmt)

    def _drop_constraint(self, schema_reference: SchemaReference, constraint_name: str) -> None:
        stmt = f'ALTER TABLE "{schema_reference.name}" DROP CONSTRAINT "{constraint_name}"'
        self.execute(stmt)

    def _add_index(self, schema_reference: SchemaReference, index: IndexSchema) -> None:
        _index_stmt = self._build_index(schema_reference.name, index)

        self.execute(_index_stmt)

    def _drop_index(self, schema_reference: SchemaReference, index_name: str) -> None:  # noqa: ARG002
        stmt = f'DROP INDEX "{index_name}"'
        self.execute(stmt)

    def _build_column(self, column: PropertySchema) -> str:
        return f'"{column.name}" {self._to_sql_type(column.type)}{" NOT NULL" if column.required else ""}'

    def _build_column_update(self, column: PropertySchema) -> str:
        return f'"{column.name}" TYPE {self._to_sql_type(column.type)}{" NOT NULL" if column.required else ""}'

    def _build_constraint(self, constraint: BaseConstraint) -> str:
        if isinstance(constraint, PrimaryKeyConstraint):
            return f'CONSTRAINT {constraint.name} ' f'PRIMARY KEY ({", ".join(constraint.fields)}) '
        if isinstance(constraint, ForeignKeySchema):
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

    def _build_index(self, schema_name: str, index: IndexSchema) -> str:
        _index = f'CREATE INDEX "{index.name}" ON "{schema_name}" ({", ".join(index.fields)})'

        if index.condition:
            where, _ = build_where(
                index.condition,
                operator_constructor=repr_operator_constructor,
                table_quote='"',
                field_quote='"',
            )
            _index += f' WHERE {where}'

        return _index

    def _to_sql_type(self, property_type: Schema | SchemaReference | type[Any]) -> str:  # noqa: PLR0911
        if property_type is str:
            return 'TEXT'
        if property_type is int:
            return 'BIGINT'
        if property_type is float:
            return 'DOUBLE PRECISION'
        if property_type is bool:
            return 'BOOLEAN'
        if property_type is dict:
            return 'JSON'
        if property_type in (bytes, bytearray):
            return 'BYTEA'
        if isinstance(property_type, Schema | SchemaReference):
            return 'TEXT'
        if property_type == datetime:
            return 'TIMESTAMP'
        if property_type == date:
            return 'DATE'

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
        if sql_type == 'TIMESTAMP':
            return datetime
        if sql_type == 'DATE':
            return date

        msg = f'Unsupported type: {sql_type}'
        raise ValueError(msg)
