import logging
from copy import copy
from typing import Any
from typing import TYPE_CHECKING

from amsdal_glue_core.common.data_models.constraints import BaseConstraint
from amsdal_glue_core.common.data_models.constraints import CheckConstraint
from amsdal_glue_core.common.data_models.constraints import ExclusionConstraint
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
from amsdal_glue_core.common.enums import BuiltinIndexType
from amsdal_glue_core.common.enums import OrderDirection
from amsdal_glue_core.common.enums import ReferentialAction
from amsdal_glue_core.common.enums import Version
from amsdal_glue_core.common.exceptions import AmsdalGlueError
from amsdal_glue_core.common.exceptions import ForeignKeyViolationError
from amsdal_glue_core.common.exceptions import UniqueViolationError
from amsdal_glue_core.common.interfaces.connection import AsyncConnectionBase
from amsdal_glue_core.common.operations.commands import LockCommand
from amsdal_glue_core.common.operations.commands import SchemaCommand
from amsdal_glue_core.common.operations.commands import TransactionCommand
from amsdal_glue_core.common.operations.mutations.data import DataMutation
from amsdal_glue_core.common.operations.mutations.schema import RegisterSchema
from amsdal_glue_core.common.operations.mutations.schema import SchemaMutation

from amsdal_glue_connections._sql_core import SqlGenerator
from amsdal_glue_connections.sql.connections.postgres_connection.base import build_registry_view_sql
from amsdal_glue_connections.sql.connections.postgres_connection.base import PostgresConnectionMixin
from amsdal_glue_connections.sql.connections.postgres_connection.sync_connection import _detect_serial
from amsdal_glue_connections.sql.connections.postgres_connection.sync_connection import _INDEX_TYPE_MAP
from amsdal_glue_connections.sql.connections.postgres_connection.sync_connection import _parse_check_condition
from amsdal_glue_connections.sql.connections.postgres_connection.sync_connection import _parse_exclusion_def
from amsdal_glue_connections.sql.connections.postgres_connection.sync_connection import _pg_type_to_field_type
from amsdal_glue_connections.sql.connections.postgres_connection.sync_connection import _REFERENTIAL_ACTION_MAP
from amsdal_glue_connections.sql.connections.postgres_connection.sync_connection import _resolve_identity
from amsdal_glue_connections.sql.connections.postgres_connection.sync_connection import parse_pg_type
from amsdal_glue_connections.sql.parsers.default import parse_pg_default
from amsdal_glue_connections.sql.parsers.default import parser as _default_parser
from amsdal_glue_connections.sql.parsers.default import pg_mapper as _pg_mapper
from amsdal_glue_connections.sql.schema_registry import TABLE_REGISTRY

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
        self._generator = SqlGenerator('postgresql', param_style='format')
        self._schema = 'public'
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

        from psycopg import sql

        self._connection = await psycopg.AsyncConnection.connect(dsn, autocommit=autocommit, **kwargs)
        await self._connection.execute("SELECT set_config('TimeZone', %s, false)", [timezone])

        self._schema = schema or 'public'

        if schema:
            # ``SET`` cannot take a bind parameter, so the schema identifier is quoted via
            # psycopg's SQL composition instead of being f-string interpolated (injection-safe).
            await self._connection.execute(sql.SQL('SET search_path TO {}').format(sql.Identifier(schema)))

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
        _stmt, _params = self._generator.compile_query(query)

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

    async def query_schema(self, query: QueryStatement) -> list[Schema]:
        """
        Queries the schema of the PostgreSQL database.

        Args:
            query (QueryStatement): The query statement referencing the registry view.

        Returns:
            list[Schema]: The result of the schema query.
        """
        return await self.introspect_schema(query)

    async def introspect_schema(self, query: QueryStatement) -> list[Schema]:
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
            properties = await self._introspect_columns(table_name)
            if not properties:
                continue

            constraints = await self._introspect_constraints(table_name)
            indexes = await self._introspect_indexes(table_name)

            schemas.append(
                Schema(
                    name=table_name,
                    version=Version.LATEST,
                    namespace=self._schema,
                    properties=properties,
                    constraints=constraints or None,
                    indexes=indexes or None,
                ),
            )

        return schemas

    async def _ensure_schema_views(self) -> None:
        # The view DDL is idempotent (CREATE OR REPLACE), so it is re-issued on every call rather
        # than gated by a per-object flag that would go stale across disconnect()/connect() cycles.
        for stmt in build_registry_view_sql(self._schema).values():
            await self.execute(stmt.as_string(self.connection))

    async def _introspect_columns(self, table_name: str) -> list[PropertySchema]:
        sql = (
            'SELECT c.column_name, c.data_type, c.udt_name, c.is_nullable, c.column_default, '
            'c.is_identity, c.identity_generation, c.collation_name, c.generation_expression, c.is_generated, '
            'c.numeric_precision, c.numeric_scale, '
            '(SELECT format_type(a.atttypid, a.atttypmod) '
            ' FROM pg_attribute a '
            ' JOIN pg_class cl ON cl.oid = a.attrelid '
            ' JOIN pg_namespace n ON n.oid = cl.relnamespace '
            ' WHERE n.nspname = %s AND cl.relname = c.table_name '
            '   AND a.attname = c.column_name AND a.attnum > 0 AND NOT a.attisdropped) AS format_type '
            'FROM information_schema.columns c '
            'WHERE c.table_name = %s AND c.table_schema = %s '
            'ORDER BY c.ordinal_position'
        )
        cursor = await self.execute(sql, self._schema, table_name, self._schema)
        rows = await cursor.fetchall()
        await cursor.close()

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
            numeric_precision,
            numeric_scale,
            format_type_str,
        ) in rows:
            serial_type = _detect_serial(data_type, column_default)
            identity = _resolve_identity(is_identity_col, identity_generation) if serial_type is None else None

            if serial_type is not None:
                field_type = serial_type
            elif format_type_str is not None:
                # format_type carries the real modifiers (vector dims, numeric precision/scale,
                # array element modifiers), so it is the authoritative source for the type.
                field_type = parse_pg_type(format_type_str)  # type: ignore[assignment]
            elif data_type in ('ARRAY', 'USER-DEFINED'):
                field_type = _pg_type_to_field_type(udt_name)  # type: ignore[assignment]
            else:
                field_type = _pg_type_to_field_type(data_type, numeric_precision, numeric_scale)  # type: ignore[assignment]

            default = parse_pg_default(column_default) if serial_type is None else None
            if is_generated == 'ALWAYS':
                generated = _pg_mapper.map_node(_default_parser.parse(generation_expression))
            else:
                generated = None

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

        await self._enrich_identity_params(table_name, properties)
        return properties

    async def _enrich_identity_params(self, table_name: str, properties: list[PropertySchema]) -> None:
        identity_cols = [p for p in properties if p.identity is not None]
        if not identity_cols:
            return

        for prop in identity_cols:
            seq_name_sql = 'SELECT pg_get_serial_sequence(%s, %s)'
            cursor = await self.execute(seq_name_sql, table_name, prop.name)
            row = await cursor.fetchone()
            await cursor.close()
            if row is None or row[0] is None:
                continue

            seq_qualified = row[0]
            sql = (
                'SELECT start_value, increment_by, min_value, max_value, cycle, cache_size '
                'FROM pg_sequences '
                "WHERE schemaname || '.' || sequencename = %s"
            )
            cursor = await self.execute(sql, seq_qualified)
            row = await cursor.fetchone()
            await cursor.close()
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

    async def _introspect_constraints(self, table_name: str) -> list[BaseConstraint]:
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
            'JOIN pg_namespace nsp ON nsp.oid = cls.relnamespace AND nsp.nspname = %s '
            'CROSS JOIN LATERAL unnest(con.conkey) WITH ORDINALITY AS u(attnum, pos) '
            'JOIN pg_attribute att ON att.attrelid = con.conrelid AND att.attnum = u.attnum '
            'LEFT JOIN LATERAL unnest(con.confkey) WITH ORDINALITY AS fk(attnum, pos) '
            '  ON fk.pos = u.pos '
            'LEFT JOIN pg_attribute ref_att '
            '  ON ref_att.attrelid = con.confrelid AND ref_att.attnum = fk.attnum '
            'WHERE cls.relname = %s '
            'GROUP BY con.oid, con.conname, con.contype, con.confrelid, con.confupdtype, con.confdeltype, con.conexclop'
        )
        cursor = await self.execute(sql, self._schema, table_name)
        rows = await cursor.fetchall()
        await cursor.close()

        constraints: list[BaseConstraint] = []
        for conname, contype, fields, ref_table, ref_fields, confupdtype, confdeltype, condef, _conexclop in rows:
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
                        on_update=_REFERENTIAL_ACTION_MAP.get(confupdtype or 'a', ReferentialAction.NO_ACTION),
                        on_delete=_REFERENTIAL_ACTION_MAP.get(confdeltype or 'a', ReferentialAction.NO_ACTION),
                    ),
                )
            elif contype == 'c':
                check_condition = _parse_check_condition(condef)
                if check_condition is not None:
                    constraints.append(CheckConstraint(name=conname, condition=check_condition))
            elif contype == 'x':
                elements, index_method = _parse_exclusion_def(condef)
                constraints.append(ExclusionConstraint(name=conname, elements=elements, index_method=index_method))

        return constraints

    async def _introspect_indexes(self, table_name: str) -> list[IndexSchema]:
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
            'JOIN pg_namespace nsp ON nsp.oid = tc.relnamespace AND nsp.nspname = %s '
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
        cursor = await self.execute(sql, 'DESC', 'ASC', self._schema, table_name, 'u')
        rows = await cursor.fetchall()
        await cursor.close()

        indexes: list[IndexSchema] = []
        for index_name, is_unique, index_type_name, n_key_atts, fields, directions, opclasses, opclass_defaults in rows:
            idx_type = _INDEX_TYPE_MAP.get(index_type_name, BuiltinIndexType.BTREE)

            key_fields = fields[:n_key_atts]
            key_dirs = directions[:n_key_atts]
            key_opclasses = opclasses[:n_key_atts]
            key_opclass_defaults = opclass_defaults[:n_key_atts]
            include_fields = fields[n_key_atts:]

            idx_fields = [
                IndexField(
                    name=f,
                    direction=OrderDirection.DESC if d == 'DESC' else OrderDirection.ASC,
                    op_class=opc if not opc_default else None,
                )
                for f, d, opc, opc_default in zip(
                    key_fields, key_dirs, key_opclasses, key_opclass_defaults, strict=True
                )
            ]

            indexes.append(
                IndexSchema(
                    name=index_name,
                    fields=idx_fields,
                    unique=bool(is_unique),
                    index_type=idx_type,
                    include=list(include_fields) or None,
                ),
            )

        return indexes

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
        _stmt, _params = self._generator.compile_mutation(mutation)

        try:
            await self.execute(_stmt, *_params)
        except AmsdalGlueError:
            # Typed glue errors (e.g. UniqueViolationError) bubble unchanged.
            raise
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
                self._queries_params.append(args)

            cursor = await self.connection.execute(query, args)
        except psycopg.errors.UniqueViolation as exc:
            raise UniqueViolationError(str(exc)) from exc
        except psycopg.errors.ForeignKeyViolation as exc:
            raise ForeignKeyViolationError(str(exc)) from exc
        except psycopg.Error as exc:
            msg = f'Error executing SQL: {query} with args: {args}. Exception: {exc}'
            raise ConnectionError(msg) from exc
        return cursor

    async def acquire_lock(self, lock: LockCommand) -> Any:
        """
        Acquires a lock on the PostgreSQL database via ``compile_lock_command``.

        Args:
            lock (LockCommand): The lock command to be executed.

        Returns:
            Any: The result of the lock acquisition.
        """
        sql, params = self._generator.compile_lock_command(lock)
        await self.execute(sql, *params)
        return True

    async def release_lock(self, lock: LockCommand) -> Any:
        """
        Releases a lock on the PostgreSQL database via ``compile_lock_command``.

        A TRANSACTION-scoped lock (table lock or ``pg_advisory_xact_lock``) CANNOT be released
        explicitly — Postgres holds it until COMMIT/ROLLBACK and offers no unlock counterpart. The
        Rust generator raises ``UnsupportedFeatureError`` for such a release, and that error is
        propagated: asking to release a transaction-scoped lock is a caller mistake (the lock is not
        released early, so silently returning success would be misleading). Only SESSION-scoped
        advisory locks have a real unlock.

        Args:
            lock (LockCommand): The lock command to be released.

        Returns:
            Any: The result of the lock release.
        """
        sql, params = self._generator.compile_lock_command(lock)
        await self.execute(sql, *params)
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

    async def _run_schema_mutation(self, migration: SchemaMutation) -> Schema | None:
        sql_params_list = self._generator.compile_schema_mutation(migration)

        for sql, params in sql_params_list:
            await self.execute(sql, *params)

        if isinstance(migration, RegisterSchema):
            return migration.schema
        return None
