import logging
import re
from copy import copy
from typing import Any
from typing import TYPE_CHECKING

from amsdal_glue_core.common.data_models.constraints import BaseConstraint
from amsdal_glue_core.common.data_models.constraints import CheckConstraint
from amsdal_glue_core.common.data_models.constraints import ExclusionConstraint
from amsdal_glue_core.common.data_models.constraints import ExclusionElement
from amsdal_glue_core.common.data_models.data import Data
from amsdal_glue_core.common.data_models.field_reference import Field
from amsdal_glue_core.common.data_models.field_reference import FieldReference
from amsdal_glue_core.common.data_models.query import QueryStatement
from amsdal_glue_core.common.data_models.schema import IdentityConfig
from amsdal_glue_core.common.data_models.schema import PropertySchema
from amsdal_glue_core.common.data_models.schema import Schema
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.data_models.types import ArrayType
from amsdal_glue_core.common.data_models.types import CustomType
from amsdal_glue_core.common.data_models.types import DecimalType
from amsdal_glue_core.common.data_models.types import VectorType
from amsdal_glue_core.common.enums import ScalarType
from amsdal_glue_core.common.enums import Version
from amsdal_glue_core.common.exceptions import AmsdalGlueError
from amsdal_glue_core.common.exceptions import ForeignKeyViolationError
from amsdal_glue_core.common.exceptions import UniqueViolationError
from amsdal_glue_core.common.interfaces.connection import ConnectionBase
from amsdal_glue_core.common.operations.commands import LockCommand
from amsdal_glue_core.common.operations.commands import SchemaCommand
from amsdal_glue_core.common.operations.commands import TransactionCommand
from amsdal_glue_core.common.operations.mutations.data import DataMutation
from amsdal_glue_core.common.operations.mutations.schema import RegisterSchema
from amsdal_glue_core.common.operations.mutations.schema import SchemaMutation

from amsdal_glue_connections._sql_core import SqlGenerator
from amsdal_glue_connections.sql.connections.base_view_introspection import SchemaAssemblyMixin
from amsdal_glue_connections.sql.connections.postgres_connection.base import bind_params
from amsdal_glue_connections.sql.connections.postgres_connection.base import PostgresConnectionMixin
from amsdal_glue_connections.sql.parsers.conditions import try_parse_conditions
from amsdal_glue_connections.sql.parsers.default import parse_pg_default
from amsdal_glue_connections.sql.schema_registry import TABLE_CONSTRAINT_REGISTRY
from amsdal_glue_connections.sql.schema_registry import TABLE_INDEX_REGISTRY
from amsdal_glue_connections.sql.schema_registry import TABLE_PROPERTY_REGISTRY
from amsdal_glue_connections.sql.schema_registry import TABLE_REGISTRY

if TYPE_CHECKING:
    from amsdal_glue_core.common.data_models.conditions import Conditions
    from amsdal_glue_core.common.data_models.indexes import IndexSchema
    from amsdal_glue_core.common.data_models.types import FieldType
    from amsdal_glue_core.common.expressions.expression import Expression

logger = logging.getLogger(__name__)


def _parse_exclusion_def(condef: str) -> tuple[list[ExclusionElement], str]:
    """Parse ``pg_get_constraintdef`` output for an EXCLUDE constraint.

    Example: ``'EXCLUDE USING gist (room_id WITH =)'``.
    Returns ``(elements, index_method)``.
    """
    elements: list[ExclusionElement] = []
    index_method = 'gist'

    if not condef:
        return elements, index_method

    try:
        using_idx = condef.index('USING')
        paren_start = condef.index('(', using_idx)
        # Extract index method between USING and (
        index_method = condef[using_idx + 5 : paren_start].strip()

        paren_end = condef.rindex(')')
        body = condef[paren_start + 1 : paren_end]

        for raw_part in body.split(','):
            tokens = raw_part.strip().rsplit(' WITH ', 1)
            if len(tokens) == 2:  # noqa: PLR2004
                elements.append(ExclusionElement(field=tokens[0].strip(), operator=tokens[1].strip()))
    except (ValueError, IndexError):  # noqa: S110
        pass

    return elements, index_method


def _parse_check_condition(condef: str) -> 'Conditions | None':
    """Parse ``pg_get_constraintdef`` output for a CHECK constraint.

    Example: ``'CHECK ((price > 0))'``.
    """
    if not condef:
        return None

    match = re.search(r'CHECK\s*\(\((.+)\)\)', condef, re.IGNORECASE)
    if match is None:
        return None

    # An unparseable CHECK predicate degrades to ``None`` rather than aborting schema introspection.
    return try_parse_conditions(match.group(1).strip())


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

# Canonical registry column projections plus the Postgres-only extras needed to reconstruct a
# `Schema` fully from the views: serial/identity sequence params (``seq_*``), the authoritative
# ``format_type`` modifiers, index INCLUDE / operator-class, and the constraint definition text
# (``def``). ``format_type`` carries every modifier ``information_schema`` drops (array element
# precision/scale) or never exposes (pgvector dimensions), so no separate base-type/precision
# columns are needed to resolve a column's ``FieldType``.
_PROPERTY_COLUMNS = [
    'table_name',
    'name',
    'type',
    'is_nullable',
    'column_default',
    'ordinal_position',
    'is_generated',
    'collation',
    'generation_expression',
    'is_identity',
    'identity_generation',
    'is_generated_raw',
    'is_identity_raw',
    'format_type',
    'seq_start',
    'seq_increment',
    'seq_min',
    'seq_max',
    'seq_cycle',
    'seq_cache',
]
_INDEX_COLUMNS = [
    'table_name',
    'name',
    'is_unique',
    'column_name',
    'ordinal_position',
    'is_descending',
    'index_type',
    'is_included',
    'op_class',
    'index_predicate',
]
_CONSTRAINT_COLUMNS = [
    'table_name',
    'name',
    'type',
    'column_name',
    'ordinal_position',
    'ref_table',
    'ref_column',
    'on_update',
    'on_delete',
    'def',
]


def parse_pg_type(type_str: str) -> ScalarType | CustomType | ArrayType | VectorType | DecimalType:
    """Parse a Postgres ``format_type(atttypid, atttypmod)`` string into a FieldType.

    ``format_type`` renders the fully-qualified type together with its modifiers exactly as
    Postgres would print them, e.g. ``vector(768)``, ``numeric(10,2)``, ``numeric(10,2)[]``,
    ``character varying(50)``, ``integer`` or ``text[]``. Parsing this single source recovers
    modifiers that ``information_schema`` drops (array element precision/scale) or never exposes
    (pgvector dimensions).

    Handling:
      * trailing ``[]``   -> ArrayType(item_type=<parse of the element type>)
      * ``vector(N)``     -> VectorType(dimensions=N) (``vector`` alone -> dimensions=0)
      * ``numeric(p[,s])``/``decimal(...)`` -> DecimalType(precision=p[, scale=s])
      * known scalar names via ``_PG_TYPE_MAP`` (e.g. ``character varying`` -> TEXT)
      * anything else     -> CustomType(name=...)
    """
    s = type_str.strip()

    # Arrays: format_type appends a single trailing '[]' even for multi-dimensional arrays.
    if s.endswith('[]'):
        return ArrayType(item_type=parse_pg_type(s[:-2]))

    # Split off an optional modifier group. It may sit at the end ('numeric(10,2)',
    # 'character varying(50)') or in the middle ('timestamp(6) without time zone').
    modifier: str | None = None
    match = re.search(r'\(([^)]*)\)', s)
    if match is not None:
        modifier = match.group(1).strip()
        s = s[: match.start()] + s[match.end() :]

    name = ' '.join(s.split())
    lookup = name.lower()

    if lookup == 'vector':
        return VectorType(dimensions=int(modifier) if modifier else 0)

    if lookup in ('numeric', 'decimal') and modifier:
        parts = [p.strip() for p in modifier.split(',')]
        scale = int(parts[1]) if len(parts) > 1 else None
        return DecimalType(precision=int(parts[0]), scale=scale)

    scalar = _PG_TYPE_MAP.get(lookup)
    if scalar is not None:
        return scalar

    return CustomType(name=name)


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


class PostgresSchemaAssemblyMixin(SchemaAssemblyMixin):
    """Postgres row -> `Schema` reconstruction shared by the sync and async connections.

    The pure (no-I/O) Postgres specialisation of `SchemaAssemblyMixin`: the type/default hooks and the
    property/constraint assembly. Both `PostgresConnection` and `AsyncPostgresConnection` mix it in, so
    this logic is defined once.
    """

    # Set by the concrete connection classes (``PostgresConnection`` / ``AsyncPostgresConnection``);
    # declared here so this shared mixin can read the active search-path schema. Annotation only -- no
    # runtime assignment, so instances are unaffected.
    _schema: str

    def _type_to_field_type(self, row: dict[str, Any]) -> 'FieldType':
        """``SchemaAssemblyMixin`` hook: resolve a Postgres property row to a ``FieldType``.

        ``format_type`` is the authoritative source -- it carries the real modifiers
        ``information_schema`` drops (array element precision/scale) or never exposes (pgvector
        dimensions), and the property view always populates it (an inner join on ``pg_attribute``),
        so it resolves every column including ARRAY / USER-DEFINED. SERIAL columns are handled by the
        caller (`_assemble_property`), which detects them before falling back to this hook.
        """
        return parse_pg_type(row['format_type'])

    def _parse_default_expression(self, raw: str | None, field_type: 'FieldType | None') -> 'Expression | None':  # noqa: ARG002
        """``SchemaAssemblyMixin`` hook: parse a raw Postgres DEFAULT / GENERATED expression.

        ``nextval(...)`` serial defaults resolve to ``None`` (the identity is modelled by the SERIAL
        type instead); everything else is mapped through the shared Postgres expression mapper.
        """
        return parse_pg_default(raw)

    def _assemble_property(self, row: dict[str, Any]) -> PropertySchema:
        """Postgres property assembly: field type, identity, default/generated and sequence params.

        Kept Postgres-local rather than reusing ``_assemble_property_core`` because SERIAL detection
        governs both the field type and whether the ``nextval(...)`` default is dropped, and because
        identity columns are enriched with their sequence parameters from the view's ``seq_*`` columns
        -- neither fits the dialect-neutral core without detecting SERIAL a second time.
        """
        serial_type = _detect_serial(row['type'], row['column_default'])
        field_type = serial_type if serial_type is not None else self._type_to_field_type(row)
        identity = (
            _resolve_identity(row['is_identity_raw'], row['identity_generation']) if serial_type is None else None
        )
        default = self._parse_default_expression(row['column_default'], field_type) if serial_type is None else None
        generated = (
            self._parse_default_expression(row['generation_expression'], field_type)
            if row['is_generated_raw'] == 'ALWAYS'
            else None
        )

        prop = PropertySchema(
            name=row['name'],
            type=field_type,
            identity=identity,
            required=row['is_nullable'] == 'NO',
            default=default,
            generated=generated,
            db_collation=row['collation'],
        )

        if isinstance(prop.identity, IdentityConfig) and row['seq_start'] is not None:
            prop.identity.start = int(row['seq_start'])
            prop.identity.increment = int(row['seq_increment']) if row['seq_increment'] is not None else None
            prop.identity.min_value = int(row['seq_min']) if row['seq_min'] is not None else None
            prop.identity.max_value = int(row['seq_max']) if row['seq_max'] is not None else None
            prop.identity.cycle = bool(row['seq_cycle'])
            prop.identity.cache = int(row['seq_cache']) if row['seq_cache'] is not None else None

        return prop

    def _assemble_constraints(self, constraint_rows: list[dict[str, Any]]) -> list[BaseConstraint]:
        """Shared PK/FK/UNIQUE core plus Postgres CHECK (``type='c'``) and exclusion (``type='x'``).

        CHECK and exclusion constraints are reconstructed from the ``pg_get_constraintdef`` text in the
        registry view's ``def`` column (deduped by name), which the dialect-neutral core cannot express.
        """
        constraints: list[BaseConstraint] = self._assemble_constraints_core(constraint_rows)

        seen: set[str] = set()
        for row in constraint_rows:
            if row['type'] not in ('c', 'x') or row['name'] in seen:
                continue
            seen.add(row['name'])
            if row['type'] == 'c':
                condition = _parse_check_condition(row['def'])
                if condition is not None:
                    constraints.append(CheckConstraint(name=row['name'], condition=condition))
            else:
                elements, index_method = _parse_exclusion_def(row['def'])
                constraints.append(ExclusionConstraint(name=row['name'], elements=elements, index_method=index_method))

        return constraints

    def _assemble_indexes_with_conditions(self, rows: list[dict[str, Any]]) -> 'list[IndexSchema]':
        """Shared index assembly plus the Postgres partial-index ``WHERE`` overlay from the catalog.

        Mirrors SQLite's ``_assemble_indexes_with_conditions``: the ``index_predicate`` column carries
        ``pg_get_expr(indpred, ...)`` (NULL for a non-partial index). A predicate the parser cannot
        represent degrades to ``None`` (index reported without its condition) rather than aborting.
        """
        predicates: dict[str, str] = {}
        for row in rows:
            predicate = row.get('index_predicate')
            if predicate:
                predicates.setdefault(row['name'], predicate)

        indexes = self._assemble_indexes(rows)
        for index in indexes:
            predicate = predicates.get(index.name)
            if predicate is not None:
                condition = try_parse_conditions(predicate)
                if condition is not None:
                    index.condition = condition
        return indexes

    def _build_schemas(
        self,
        table_names: list[str],
        properties_by_table: dict[str, list[dict[str, Any]]],
        constraints_by_table: dict[str, list[dict[str, Any]]],
        indexes_by_table: dict[str, list[dict[str, Any]]],
    ) -> list[Schema]:
        """Pure (no-I/O) assembly of the grouped registry rows into ``Schema`` objects.

        Identical for the sync and async connections, so it lives here and each variant calls it
        after its own (awaited or not) registry fetches.
        """
        schemas: list[Schema] = []
        for table_name in table_names:
            table_property_rows = sorted(properties_by_table.get(table_name, []), key=lambda r: r['ordinal_position'])
            if not table_property_rows:
                continue

            schemas.append(
                Schema(
                    name=table_name,
                    version=Version.LATEST,
                    # Introspection returns the canonical dialect-neutral ``None`` for the default schema
                    # so it round-trips against registered schemas (which author ``None``); a genuinely
                    # non-default schema (e.g. ``schema='foo'``) is preserved as-is.
                    namespace=None if self._schema in (None, '', 'public') else self._schema,
                    properties=[self._assemble_property(row) for row in table_property_rows],
                    constraints=self._assemble_constraints(constraints_by_table.get(table_name, [])) or None,
                    indexes=self._assemble_indexes_with_conditions(indexes_by_table.get(table_name, [])) or None,
                ),
            )

        return schemas


class PostgresConnection(PostgresSchemaAssemblyMixin, PostgresConnectionMixin, ConnectionBase):
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
        self._schema = 'public'
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

        from psycopg import sql

        self._connection = psycopg.connect(dsn, autocommit=autocommit, **kwargs)
        self._connection.execute("SELECT set_config('TimeZone', %s, false)", [timezone])

        self._schema = schema or 'public'

        if schema:
            # ``SET`` cannot take a bind parameter, so the schema identifier is quoted via
            # psycopg's SQL composition instead of being f-string interpolated (injection-safe).
            self._connection.execute(sql.SQL('SET search_path TO {}').format(sql.Identifier(schema)))

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
        resolved.only = [FieldReference(field=Field(name='table_name'), table_name=ref_name)]

        sql, params = self._generator.compile_query(resolved)
        cursor = self.execute(sql, *params)
        rows = cursor.fetchall()
        cursor.close()

        table_names = self._dedupe_names(rows)

        if not table_names:
            return []

        # One bound registry query per catalog aspect -- a constant number of statements regardless
        # of how many tables match. Every fact is reconstructed from the canonical views (no per-table
        # ``information_schema`` / ``pg_get_serial_sequence`` reads), so there is no N+1 catalog storm.
        property_rows = self._run_registry(TABLE_PROPERTY_REGISTRY, _PROPERTY_COLUMNS, table_names)
        constraint_rows = self._run_registry(TABLE_CONSTRAINT_REGISTRY, _CONSTRAINT_COLUMNS, table_names)
        index_rows = self._run_registry(TABLE_INDEX_REGISTRY, _INDEX_COLUMNS, table_names)

        return self._build_schemas(
            table_names,
            self._group(property_rows),
            self._group(constraint_rows),
            self._group(index_rows),
        )

    def _ensure_schema_views(self) -> None:
        # The view DDL is idempotent (CREATE OR REPLACE), so it is re-issued on every call rather
        # than gated by a per-object flag that would go stale across disconnect()/connect() cycles.
        for stmt in self._build_registry_view_sql(self._schema).values():
            self.execute(stmt.as_string(self.connection))

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

        args = bind_params(args)

        try:
            if self.debug_queries:
                self._queries.append(query)
                self._queries_params.append(args)

            cursor = self.connection.execute(query, args)
        except psycopg.errors.UniqueViolation as exc:
            raise UniqueViolationError(str(exc)) from exc
        except psycopg.errors.ForeignKeyViolation as exc:
            raise ForeignKeyViolationError(str(exc)) from exc
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
        self.execute(sql, *params)
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
        return self.rollback_transaction(transaction)

    def _run_schema_mutation(self, migration: SchemaMutation) -> Schema | None:
        sql_params_list = self._generator.compile_schema_mutation(migration)

        for sql, params in sql_params_list:
            self.execute(sql, *params)

        if isinstance(migration, RegisterSchema):
            return migration.schema
        return None
