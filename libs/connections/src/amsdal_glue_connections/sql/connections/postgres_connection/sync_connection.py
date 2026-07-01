import logging
from copy import copy
from typing import Any

from amsdal_glue_core.common.data_models.constraints import BaseConstraint
from amsdal_glue_core.common.data_models.constraints import ForeignKeyConstraint
from amsdal_glue_core.common.data_models.constraints import PrimaryKeyConstraint
from amsdal_glue_core.common.data_models.constraints import UniqueConstraint
from amsdal_glue_core.common.data_models.data import Data
from amsdal_glue_core.common.data_models.field_reference import Field
from amsdal_glue_core.common.data_models.field_reference import FieldReference
from amsdal_glue_core.common.data_models.indexes import IndexField
from amsdal_glue_core.common.data_models.indexes import IndexSchema
from amsdal_glue_core.common.data_models.query import QueryStatement
from amsdal_glue_core.common.data_models.schema import IdentityConfig
from amsdal_glue_core.common.data_models.schema import PropertySchema
from amsdal_glue_core.common.data_models.schema import Schema
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.data_models.types import ArrayType
from amsdal_glue_core.common.data_models.types import CustomType
from amsdal_glue_core.common.data_models.types import VectorType
from amsdal_glue_core.common.enums import ScalarType
from amsdal_glue_core.common.enums import Version
from amsdal_glue_core.common.exceptions import AmsdalGlueError
from amsdal_glue_core.common.exceptions import UniqueViolationError
from amsdal_glue_core.common.expressions.raw import RawExpression
from amsdal_glue_core.common.interfaces.connection import ConnectionBase
from amsdal_glue_core.common.operations.commands import LockCommand
from amsdal_glue_core.common.operations.commands import SchemaCommand
from amsdal_glue_core.common.operations.commands import TransactionCommand
from amsdal_glue_core.common.operations.mutations.data import DataMutation
from amsdal_glue_core.common.operations.mutations.schema import RegisterSchema
from amsdal_glue_core.common.operations.mutations.schema import SchemaMutation

from amsdal_glue_connections._sql_core import SqlGenerator
from amsdal_glue_connections.sql.connections.postgres_connection.base import _REGISTRY_VIEW_SQL
from amsdal_glue_connections.sql.connections.postgres_connection.base import PostgresConnectionMixin
from amsdal_glue_connections.sql.schema_registry import TABLE_REGISTRY

logger = logging.getLogger(__name__)

_PG_TYPE_MAP: dict[str, ScalarType] = {
    'text': ScalarType.TEXT,
    'character varying': ScalarType.TEXT,
    'varchar': ScalarType.TEXT,
    'char': ScalarType.TEXT,
    'character': ScalarType.TEXT,
    'name': ScalarType.TEXT,
    'integer': ScalarType.INTEGER,
    'int': ScalarType.INTEGER,
    'int4': ScalarType.INTEGER,
    'bigint': ScalarType.BIGINT,
    'int8': ScalarType.BIGINT,
    'smallint': ScalarType.SMALLINT,
    'int2': ScalarType.SMALLINT,
    'real': ScalarType.FLOAT,
    'float4': ScalarType.FLOAT,
    'double precision': ScalarType.DOUBLE,
    'float8': ScalarType.DOUBLE,
    'numeric': ScalarType.NUMERIC,
    'decimal': ScalarType.NUMERIC,
    'boolean': ScalarType.BOOLEAN,
    'bool': ScalarType.BOOLEAN,
    'date': ScalarType.DATE,
    'time without time zone': ScalarType.TIME,
    'time': ScalarType.TIME,
    'timestamp without time zone': ScalarType.TIMESTAMP,
    'timestamp': ScalarType.TIMESTAMP,
    'timestamp with time zone': ScalarType.TIMESTAMPTZ,
    'timestamptz': ScalarType.TIMESTAMPTZ,
    'interval': ScalarType.INTERVAL,
    'bytea': ScalarType.BYTEA,
    'json': ScalarType.JSON,
    'jsonb': ScalarType.JSONB,
    'uuid': ScalarType.UUID,
    'smallserial': ScalarType.SMALLSERIAL,
    'serial': ScalarType.SERIAL,
    'bigserial': ScalarType.BIGSERIAL,
    'tsvector': ScalarType.TSVECTOR,
    'tsquery': ScalarType.TSQUERY,
    'int4range': ScalarType.INT4RANGE,
    'int8range': ScalarType.INT8RANGE,
    'numrange': ScalarType.NUMRANGE,
    'daterange': ScalarType.DATERANGE,
    'tsrange': ScalarType.TSRANGE,
    'tstzrange': ScalarType.TSTZRANGE,
}

_SERIAL_TYPE_MAP: dict[str, ScalarType] = {
    'smallint': ScalarType.SMALLSERIAL,
    'integer': ScalarType.SERIAL,
    'bigint': ScalarType.BIGSERIAL,
}


def _pg_type_to_field_type(type_name: str) -> ScalarType | CustomType | ArrayType | VectorType:
    if type_name.startswith('_') or type_name.endswith('[]'):
        base = type_name.lstrip('_').rstrip('[]')
        item_type = _PG_TYPE_MAP.get(base, CustomType(name=base))
        return ArrayType(item_type=item_type)

    if type_name == 'vector':
        return VectorType(dimensions=0)

    scalar = _PG_TYPE_MAP.get(type_name)
    if scalar is not None:
        return scalar

    return CustomType(name=type_name)


def _detect_serial(data_type: str, column_default: str | None) -> ScalarType | None:
    """Detect SMALLSERIAL/SERIAL/BIGSERIAL from integer type + nextval() default."""
    if column_default is not None and 'nextval(' in column_default:
        return _SERIAL_TYPE_MAP.get(data_type)
    return None


def _resolve_identity(
    is_identity_col: str,
    identity_generation: str | None,
) -> IdentityConfig | None:
    if is_identity_col == 'YES':
        always = identity_generation == 'ALWAYS'
        return IdentityConfig(always=always)
    return None


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
        self._views_created = False
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

    def query_schema(self, query: QueryStatement) -> list[Schema]:
        """
        Queries the schema of the PostgreSQL database.

        Args:
            query (QueryStatement): The query statement referencing the registry view.

        Returns:
            list[Schema]: The result of the schema query.
        """
        return self.introspect_schema(query)

    def introspect_schema(self, query: QueryStatement) -> list[Schema]:
        self._ensure_schema_views()

        ref_name = query.table.alias or query.table.name if isinstance(query.table, SchemaReference) else TABLE_REGISTRY

        resolved = copy(query)
        resolved.only = [FieldReference(field=Field(name='name'), table_name=ref_name)]

        sql, params = self._generator.compile_query(resolved)
        cursor = self.execute(sql, *params)
        rows = cursor.fetchall()
        cursor.close()

        seen: set[str] = set()
        table_names: list[str] = []
        for (name,) in rows:
            if name not in seen:
                seen.add(name)
                table_names.append(name)

        schemas: list[Schema] = []
        for table_name in table_names:
            properties = self._introspect_columns(table_name)
            if not properties:
                continue

            constraints = self._introspect_constraints(table_name)
            indexes = self._introspect_indexes(table_name)

            schemas.append(
                Schema(
                    name=table_name,
                    version=Version.LATEST,
                    namespace='public',
                    properties=properties,
                    constraints=constraints or None,
                    indexes=indexes or None,
                ),
            )

        return schemas

    def _ensure_schema_views(self) -> None:
        if self._views_created:
            return

        for sql in _REGISTRY_VIEW_SQL.values():
            self.execute(sql)

        self._views_created = True

    def _introspect_columns(self, table_name: str) -> list[PropertySchema]:
        sql = (
            'SELECT column_name, data_type, udt_name, is_nullable, column_default, '
            'is_identity, identity_generation, collation_name, generation_expression, is_generated '
            'FROM information_schema.columns '
            "WHERE table_name = %s AND table_schema = 'public' "
            'ORDER BY ordinal_position'
        )
        cursor = self.execute(sql, table_name)
        rows = cursor.fetchall()
        cursor.close()

        properties: list[PropertySchema] = []
        for (
            column_name,
            data_type,
            udt_name,
            is_nullable,
            column_default,
            is_identity_col,
            identity_generation,
            collation_name,
            generation_expression,
            is_generated,
        ) in rows:
            serial_type = _detect_serial(data_type, column_default)
            identity = _resolve_identity(is_identity_col, identity_generation) if serial_type is None else None

            if serial_type is not None:
                field_type: ScalarType | CustomType | ArrayType | VectorType = serial_type
            elif data_type in ('ARRAY', 'USER-DEFINED'):
                field_type = _pg_type_to_field_type(udt_name)
            else:
                field_type = _pg_type_to_field_type(data_type)

            default = (
                RawExpression(value=column_default) if serial_type is None and column_default is not None else None
            )
            generated = RawExpression(value=generation_expression) if is_generated == 'ALWAYS' else None

            properties.append(
                PropertySchema(
                    name=column_name,
                    type=field_type,
                    identity=identity,
                    required=is_nullable == 'NO',
                    default=default,
                    generated=generated,
                    db_collation=collation_name,
                ),
            )

        self._enrich_identity_params(table_name, properties)
        return properties

    def _enrich_identity_params(self, table_name: str, properties: list[PropertySchema]) -> None:
        identity_cols = [p for p in properties if p.identity is not None]
        if not identity_cols:
            return

        for prop in identity_cols:
            seq_name_sql = 'SELECT pg_get_serial_sequence(%s, %s)'
            cursor = self.execute(seq_name_sql, table_name, prop.name)
            row = cursor.fetchone()
            cursor.close()
            if row is None or row[0] is None:
                continue

            seq_qualified = row[0]
            sql = (
                'SELECT start_value, increment_by, min_value, max_value, cycle, cache_size '
                'FROM pg_sequences '
                "WHERE schemaname || '.' || sequencename = %s"
            )
            cursor = self.execute(sql, seq_qualified)
            row = cursor.fetchone()
            cursor.close()
            if row is None:
                continue

            start, increment, min_value, max_value, cycle, cache = row
            if not isinstance(prop.identity, IdentityConfig):  # pragma: no cover
                continue
            prop.identity.start = int(start) if start is not None else None
            prop.identity.increment = int(increment) if increment is not None else None
            prop.identity.min_value = int(min_value) if min_value is not None else None
            prop.identity.max_value = int(max_value) if max_value is not None else None
            prop.identity.cycle = bool(cycle)
            prop.identity.cache = int(cache) if cache is not None else None

    def _introspect_constraints(self, table_name: str) -> list[BaseConstraint]:
        sql = (
            'SELECT '
            '  con.conname, con.contype, '
            '  array_agg(att.attname ORDER BY u.pos) AS fields, '
            '  con.confrelid::regclass::text AS ref_table, '
            '  array_agg(ref_att.attname ORDER BY u.pos) FILTER (WHERE ref_att.attname IS NOT NULL) AS ref_fields, '
            '  con.confupdtype, con.confdeltype, '
            '  pg_get_constraintdef(con.oid) AS def, '
            '  con.conexclop '
            'FROM pg_constraint con '
            'JOIN pg_class cls ON cls.oid = con.conrelid '
            "JOIN pg_namespace nsp ON nsp.oid = cls.relnamespace AND nsp.nspname = 'public' "
            'CROSS JOIN LATERAL unnest(con.conkey) WITH ORDINALITY AS u(attnum, pos) '
            'JOIN pg_attribute att ON att.attrelid = con.conrelid AND att.attnum = u.attnum '
            'LEFT JOIN LATERAL unnest(con.confkey) WITH ORDINALITY AS fk(attnum, pos) '
            '  ON fk.pos = u.pos '
            'LEFT JOIN pg_attribute ref_att '
            '  ON ref_att.attrelid = con.confrelid AND ref_att.attnum = fk.attnum '
            'WHERE cls.relname = %s '
            'GROUP BY con.oid, con.conname, con.contype, con.confrelid, con.confupdtype, con.confdeltype, con.conexclop'
        )
        cursor = self.execute(sql, table_name)
        rows = cursor.fetchall()
        cursor.close()

        constraints: list[BaseConstraint] = []
        for conname, contype, fields, ref_table, ref_fields, _confupdtype, _confdeltype, _condef, _conexclop in rows:
            if contype == 'p':
                constraints.append(PrimaryKeyConstraint(name=conname, fields=list(fields)))
            elif contype == 'u':
                constraints.append(UniqueConstraint(name=conname, fields=list(fields)))
            elif contype == 'f':
                constraints.append(
                    ForeignKeyConstraint(
                        name=conname,
                        fields=list(fields),
                        reference_schema=SchemaReference(name=ref_table, version=Version.LATEST),
                        reference_fields=list(ref_fields) if ref_fields else [],
                    ),
                )

        return constraints

    def _introspect_indexes(self, table_name: str) -> list[IndexSchema]:
        sql = (
            'SELECT '
            '  ic.relname AS index_name, '
            '  ix.indisunique, '
            '  am.amname AS index_type, '
            '  ix.indnkeyatts, '
            '  array_agg(att.attname ORDER BY k.pos) AS fields, '
            '  array_agg(CASE WHEN ix.indoption[k.pos - 1] & 1 = 1 THEN %s ELSE %s END ORDER BY k.pos) AS directions, '
            '  array_agg(opc.opcname ORDER BY k.pos) AS opclasses, '
            '  array_agg(COALESCE(opc.opcdefault, true) ORDER BY k.pos) AS opclass_defaults '
            'FROM pg_index ix '
            'JOIN pg_class tc ON tc.oid = ix.indrelid '
            'JOIN pg_class ic ON ic.oid = ix.indexrelid '
            'JOIN pg_am am ON am.oid = ic.relam '
            "JOIN pg_namespace nsp ON nsp.oid = tc.relnamespace AND nsp.nspname = 'public' "
            'CROSS JOIN LATERAL unnest(ix.indkey) WITH ORDINALITY AS k(attnum, pos) '
            'JOIN pg_attribute att ON att.attrelid = tc.oid AND att.attnum = k.attnum '
            'LEFT JOIN pg_opclass opc ON opc.oid = ix.indclass[k.pos - 1] '
            'WHERE tc.relname = %s '
            '  AND NOT ix.indisprimary '
            '  AND NOT EXISTS ('
            '    SELECT 1 FROM pg_constraint con '
            '    WHERE con.conindid = ix.indexrelid AND con.contype = %s'
            '  ) '
            'GROUP BY ic.relname, ix.indisunique, am.amname, ix.indnkeyatts'
        )
        cursor = self.execute(sql, 'DESC', 'ASC', table_name, 'u')
        rows = cursor.fetchall()
        cursor.close()

        indexes: list[IndexSchema] = []
        for row in rows:
            index_name, is_unique, _index_type_name, n_key_atts, fields = row[0], row[1], row[2], row[3], row[4]
            key_fields = list(fields[:n_key_atts])
            indexes.append(
                IndexSchema(
                    name=index_name,
                    fields=[IndexField(name=f) for f in key_fields],
                    unique=bool(is_unique),
                ),
            )

        return indexes

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

    def acquire_lock(self, lock: LockCommand) -> Any:
        """
        Acquires a lock on the PostgreSQL database via ``compile_lock_command``.

        Args:
            lock (LockCommand): The lock command to be executed.

        Returns:
            Any: The result of the lock acquisition.
        """
        sql, params = self._generator.compile_lock_command(lock)
        self.execute(sql, *params)
        return True

    def release_lock(self, lock: LockCommand) -> Any:
        """
        Releases a lock on the PostgreSQL database via ``compile_lock_command``.

        TRANSACTION-scope table locks and ``pg_advisory_xact_lock`` auto-release at COMMIT/ROLLBACK
        — the Rust generator raises ``UnsupportedFeatureError`` for these cases, which is caught and
        treated as a no-op (the lock will release when the enclosing transaction ends).

        Args:
            lock (LockCommand): The lock command to be released.

        Returns:
            Any: The result of the lock release.
        """
        from amsdal_glue_connections._sql_core import UnsupportedFeatureError

        try:
            sql, params = self._generator.compile_lock_command(lock)
            self.execute(sql, *params)
        except UnsupportedFeatureError:  # noqa: S110
            # TRANSACTION-scope locks auto-release at transaction end — no SQL needed;
            # the Rust generator raises UnsupportedFeatureError precisely for these cases.
            pass
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
