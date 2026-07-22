import logging
import re
import sqlite3
import uuid
from collections.abc import Iterable
from collections.abc import Sequence
from copy import copy
from datetime import date
from datetime import datetime
from decimal import Decimal
from pathlib import Path
from typing import Any
from typing import TYPE_CHECKING

from amsdal_glue_core.common.data_models.constraints import BaseConstraint
from amsdal_glue_core.common.data_models.constraints import CheckConstraint
from amsdal_glue_core.common.data_models.constraints import ForeignKeyConstraint
from amsdal_glue_core.common.data_models.constraints import PrimaryKeyConstraint
from amsdal_glue_core.common.data_models.constraints import UniqueConstraint
from amsdal_glue_core.common.data_models.data import Data
from amsdal_glue_core.common.data_models.data import DataInput
from amsdal_glue_core.common.data_models.field_reference import Field
from amsdal_glue_core.common.data_models.field_reference import FieldReference
from amsdal_glue_core.common.data_models.indexes import IndexSchema
from amsdal_glue_core.common.data_models.query import QueryStatement
from amsdal_glue_core.common.data_models.schema import PropertySchema
from amsdal_glue_core.common.data_models.schema import Schema
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.data_models.types import CustomType
from amsdal_glue_core.common.data_models.types import DecimalType
from amsdal_glue_core.common.enums import ScalarType
from amsdal_glue_core.common.enums import Version
from amsdal_glue_core.common.exceptions import AmsdalGlueError
from amsdal_glue_core.common.expressions.field_reference import FieldReferenceExpression
from amsdal_glue_core.common.interfaces.connection import ConnectionBase
from amsdal_glue_core.common.operations.commands import LockCommand
from amsdal_glue_core.common.operations.commands import SchemaCommand
from amsdal_glue_core.common.operations.commands import TransactionCommand
from amsdal_glue_core.common.operations.mutations.data import DataMutation
from amsdal_glue_core.common.operations.mutations.data import InsertFromSelect
from amsdal_glue_core.common.operations.mutations.data import UpdateData
from amsdal_glue_core.common.operations.mutations.schema import AddConstraint
from amsdal_glue_core.common.operations.mutations.schema import AddIndex
from amsdal_glue_core.common.operations.mutations.schema import AddProperty
from amsdal_glue_core.common.operations.mutations.schema import DeleteConstraint
from amsdal_glue_core.common.operations.mutations.schema import DeleteProperty
from amsdal_glue_core.common.operations.mutations.schema import DeleteSchema
from amsdal_glue_core.common.operations.mutations.schema import RegisterSchema
from amsdal_glue_core.common.operations.mutations.schema import RenameProperty
from amsdal_glue_core.common.operations.mutations.schema import RenameSchema
from amsdal_glue_core.common.operations.mutations.schema import SchemaMutation
from amsdal_glue_core.common.operations.mutations.schema import UpdateProperty

from amsdal_glue_connections._sql_core import SqlGenerator
from amsdal_glue_connections.sql.connections.base_view_introspection import SchemaAssemblyMixin
from amsdal_glue_connections.sql.connections.sqlite_connection.base import bind_params
from amsdal_glue_connections.sql.connections.sqlite_connection.base import SqliteConnectionMixin
from amsdal_glue_connections.sql.parsers.conditions import try_parse_conditions
from amsdal_glue_connections.sql.parsers.default import parse_sqlite_default
from amsdal_glue_connections.sql.parsers.default import parser as _default_parser
from amsdal_glue_connections.sql.parsers.default import sqlite_mapper as _sqlite_mapper
from amsdal_glue_connections.sql.schema_registry import TABLE_CONSTRAINT_REGISTRY
from amsdal_glue_connections.sql.schema_registry import TABLE_INDEX_REGISTRY
from amsdal_glue_connections.sql.schema_registry import TABLE_PROPERTY_REGISTRY
from amsdal_glue_connections.sql.schema_registry import TABLE_REGISTRY

if TYPE_CHECKING:
    from amsdal_glue_core.common.data_models.conditions import Conditions
    from amsdal_glue_core.common.expressions.expression import Expression

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# SQLite type mapping
# ---------------------------------------------------------------------------

_SQLITE_TYPE_MAP: dict[str, ScalarType] = {
    'text': ScalarType.TEXT,
    'varchar': ScalarType.TEXT,
    'character': ScalarType.TEXT,
    'char': ScalarType.TEXT,
    'nvarchar': ScalarType.TEXT,
    'clob': ScalarType.TEXT,
    'integer': ScalarType.INTEGER,
    'int': ScalarType.INTEGER,
    'bigint': ScalarType.BIGINT,
    'smallint': ScalarType.SMALLINT,
    'tinyint': ScalarType.SMALLINT,
    'real': ScalarType.FLOAT,
    'float': ScalarType.FLOAT,
    'double': ScalarType.DOUBLE,
    'double precision': ScalarType.DOUBLE,
    'numeric': ScalarType.NUMERIC,
    'decimal': ScalarType.NUMERIC,
    'boolean': ScalarType.BOOLEAN,
    'bool': ScalarType.BOOLEAN,
    'date': ScalarType.DATE,
    'time': ScalarType.TIME,
    'timestamp': ScalarType.TIMESTAMP,
    'timestamptz': ScalarType.TIMESTAMPTZ,
    'datetime': ScalarType.TIMESTAMP,
    'blob': ScalarType.BYTEA,
    'json': ScalarType.JSON,
    'jsonb': ScalarType.JSONB,
    'uuid': ScalarType.UUID,
}

# ---------------------------------------------------------------------------
# DDL parsing regexes
# ---------------------------------------------------------------------------

_PK_NAME_RE = re.compile(
    r'CONSTRAINT\s+["\']?(\w+)["\']?\s+PRIMARY\s+KEY',
    re.IGNORECASE,
)

_FK_NAME_RE = re.compile(
    r'CONSTRAINT\s+["\']?(?P<name>\w+)["\']?\s+FOREIGN\s+KEY\s*\(\s*(?P<fields>[^)]+)\)',
    re.IGNORECASE,
)

_FK_INLINE_RE = re.compile(
    r'(?P<field>\w+)\s+(?:\w+\s+)*CONSTRAINT\s+["\']?(?P<name>\w+)["\']?\s+REFERENCES',
    re.IGNORECASE,
)

_UNIQUE_BLOCK_RE = re.compile(
    r'CONSTRAINT\s+["\']?(?P<name>\w+)["\']?\s+UNIQUE\s*\((?P<fields>[^)]+)\)',
    re.IGNORECASE,
)

_UNIQUE_INLINE_RE = re.compile(
    r'["\']?(?P<name>\w+)["\']?\s+\w+(?:\([^)]*\))?\s*(?:NOT\s+NULL\s+|NULL\s+)?UNIQUE(?:\s|,|\)|$)',
    re.IGNORECASE,
)

_DECIMAL_TYPE_RE = re.compile(
    r'^(DECIMAL_TEXT|NUMERIC|DECIMAL)\s*(?:\(\s*(\d+)\s*(?:,\s*(\d+)\s*)?\))?\s*$',
    re.IGNORECASE,
)


def _sqlite_type_to_field_type(type_name: str) -> ScalarType | CustomType | DecimalType:
    """Map a SQLite column type string to a FieldType.

    ``DECIMAL_TEXT``/``NUMERIC``/``DECIMAL`` with an explicit ``(p[, s])`` modifier resolve to a
    dialect-agnostic ``DecimalType`` so a RegisterSchema→introspect cycle round-trips. A bare
    ``NUMERIC`` (no modifier) keeps mapping to ``ScalarType.NUMERIC``; a bare ``DECIMAL_TEXT``
    (the SQLite rendering of ``DecimalType()``) resolves back to ``DecimalType()``.
    """
    # Detect parameterised decimal types before stripping parens.
    m = _DECIMAL_TYPE_RE.match(type_name.strip())
    if m:
        base_name = m.group(1).upper()
        precision = int(m.group(2)) if m.group(2) is not None else None
        scale = int(m.group(3)) if m.group(3) is not None else None
        # Bare NUMERIC/DECIMAL (no modifier) stays a plain scalar for backwards compatibility;
        # only DECIMAL_TEXT or a modifier-bearing type resolves to the agnostic DecimalType.
        if precision is None and base_name != 'DECIMAL_TEXT':
            return ScalarType.NUMERIC
        return DecimalType(precision=precision, scale=scale)

    cleaned = re.sub(r'\(.*\)', '', type_name).strip().lower()

    scalar = _SQLITE_TYPE_MAP.get(cleaned)
    if scalar is not None:
        return scalar

    if not cleaned:
        return ScalarType.TEXT

    return CustomType(name=cleaned)


def _find_autoincrement_pk_col(table_ddl: str) -> str | None:
    match = re.search(r'"(\w+)"\s+\w+[^,]*\bPRIMARY\s+KEY\s+AUTOINCREMENT\b', table_ddl, re.IGNORECASE)
    return match.group(1) if match else None


def _parse_collations(table_ddl: str) -> dict[str, str]:
    results: dict[str, str] = {}
    for match in re.finditer(r'"(\w+)"\s+\w+[^,]*\bCOLLATE\s+"?(\w+)"?', table_ddl, re.IGNORECASE):
        results[match.group(1)] = match.group(2)
    return results


def _parse_generated_expressions(table_ddl: str) -> dict[str, 'Expression']:
    results: dict[str, Expression] = {}
    for match in re.finditer(
        r'"(\w+)"\s+\w+[^,]*\bGENERATED\s+ALWAYS\s+AS\s*\((.+?)\)\s*(?:STORED|VIRTUAL)',
        table_ddl,
        re.IGNORECASE,
    ):
        node = _default_parser.parse(match.group(2).strip())
        results[match.group(1)] = _sqlite_mapper.map_node(node)
    return results


def _get_check_constraints(table_ddl: str) -> list[CheckConstraint]:
    """Parse named CHECK constraints from a SQLite table DDL."""
    constraints: list[CheckConstraint] = []
    for match in re.finditer(
        r'CONSTRAINT\s+"(\w+)"\s+CHECK\s*\((.+?)\)(?:\s*,|\s*\))',
        table_ddl,
        re.IGNORECASE,
    ):
        name = match.group(1)
        # An unparseable CHECK predicate degrades to ``condition=None`` rather than aborting the
        # whole schema introspection.
        condition = try_parse_conditions(match.group(2).strip())
        constraints.append(CheckConstraint(name=name, condition=condition))  # type: ignore[arg-type]
    return constraints


def _parse_pk_name(table_sql: str, table_name: str) -> str:
    match = _PK_NAME_RE.search(table_sql)
    if match:
        return match.group(1)
    return f'pk_{table_name}'


def _parse_fk_name(table_sql: str, field_name: str) -> str:
    for match in _FK_NAME_RE.finditer(table_sql):
        name = match.group('name')
        fields = [f.strip(' "\'') for f in match.group('fields').split(',')]
        if field_name in fields:
            return name

    for match in _FK_INLINE_RE.finditer(table_sql):
        if match.group('field') == field_name:
            return match.group('name')

    return ''


def _get_unique_constraints(
    table_name: str,
    table_sql: str,
    existing: list[BaseConstraint],
) -> list[UniqueConstraint]:
    existing_field_sets: list[list[str]] = [
        c.fields for c in existing if isinstance(c, PrimaryKeyConstraint | UniqueConstraint)
    ]

    constraints: list[UniqueConstraint] = []
    seen_field_sets: list[list[str]] = list(existing_field_sets)

    for match in _UNIQUE_BLOCK_RE.finditer(table_sql):
        name = match.group('name')
        fields = [f.strip(' "\'') for f in match.group('fields').split(',')]
        if fields not in seen_field_sets:
            seen_field_sets.append(fields)
            constraints.append(UniqueConstraint(name=name, fields=fields))

    for match in _UNIQUE_INLINE_RE.finditer(table_sql):
        field_name = match.group('name')
        if [field_name] not in seen_field_sets:
            seen_field_sets.append([field_name])
            constraints.append(UniqueConstraint(name=f'uq_{table_name}_{field_name}', fields=[field_name]))

    return constraints


# Canonical registry column projections, in the fixed order the assembly path expects. They mirror
# the columns exposed by the SQLite registry views (see ``_REGISTRY_VIEW_SQL`` in ``base.py``).
_PROPERTY_COLUMNS = [
    'table_name',
    'name',
    'type',
    'is_nullable',
    'column_default',
    'ordinal_position',
]
_INDEX_COLUMNS = ['table_name', 'name', 'is_unique', 'column_name', 'ordinal_position', 'is_descending', 'index_type']
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
]


# `SQLITE_MAX_VARIABLE_NUMBER` defaults to 999 on older SQLite builds (newer builds raise it to
# 32766, but we cannot rely on that at runtime). `_run_registry`'s IN-list binds one parameter per
# name, so 400 stays comfortably under 999. `_batch_ddls` binds `names` twice (once for the table
# match, once for the index match), so it chunks at the same 400 -- 2 * 400 = 800 < 999.
_SQLITE_MAX_IN = 400


def _parse_index_condition(index_ddl: str | None) -> 'Conditions | None':
    """Extract a partial-index ``WHERE`` clause from an index's ``CREATE INDEX`` DDL, if any."""
    if not index_ddl:
        return None

    match = re.search(r'\bWHERE\s+(.+)$', index_ddl, re.IGNORECASE)
    if match is None:
        return None

    # A partial-index WHERE that the parser cannot represent degrades to ``None`` (the index is still
    # reported, just without its predicate) rather than aborting the whole schema introspection.
    return try_parse_conditions(match.group(1).strip())


class SqliteSchemaAssemblyMixin(SchemaAssemblyMixin):
    """SQLite row -> `Schema` reconstruction shared by the sync and async connections.

    The pure (no-I/O) SQLite specialisation of `SchemaAssemblyMixin`: the type/default hooks and the
    property/constraint/index assembly, including the DDL-text overlays (real constraint names,
    AUTOINCREMENT identity, ``COLLATE``, generated expressions, partial-index ``WHERE``) that SQLite's
    catalog cannot express. Both `SqliteConnection` and `AsyncSqliteConnection` mix it in, so this
    logic is defined once. The DDL text itself is fetched by each connection's own `_batch_ddls`.
    """

    def _type_to_field_type(self, row: dict[str, Any]) -> ScalarType | CustomType | DecimalType:
        """`SchemaAssemblyMixin` hook: map a SQLite property row's declared type to a `FieldType`."""
        return _sqlite_type_to_field_type(row['type'])

    def _parse_default_expression(self, raw: str | None, field_type: Any) -> 'Expression | None':
        """`SchemaAssemblyMixin` hook: parse a raw SQLite DEFAULT/GENERATED literal to an `Expression`."""
        return parse_sqlite_default(raw, field_type)

    def _assemble_properties(self, rows: list[dict[str, Any]], table_ddl: str) -> list[PropertySchema]:
        """Shared property core plus the SQLite DDL-only overlays SQLite exposes no catalog for.

        `identity` (AUTOINCREMENT PK), `generated` (``GENERATED ALWAYS AS (...)``) and `db_collation`
        (``COLLATE``) are unreadable from the registry views (they are ``NULL`` there), so they are
        parsed out of the table DDL and layered on top of `_assemble_property_core`.
        """
        has_autoincrement = 'AUTOINCREMENT' in table_ddl.upper()
        autoincrement_pk_col = _find_autoincrement_pk_col(table_ddl) if has_autoincrement else None
        generated_exprs = _parse_generated_expressions(table_ddl)
        collations = _parse_collations(table_ddl)

        properties: list[PropertySchema] = []
        for row in rows:
            prop = self._assemble_property_core(row)
            if row['name'] == autoincrement_pk_col:
                prop.identity = True
            if row['name'] in generated_exprs:
                prop.generated = generated_exprs[row['name']]
            if row['name'] in collations:
                prop.db_collation = collations[row['name']]
            properties.append(prop)
        return properties

    def _assemble_constraints(
        self, table_name: str, table_ddl: str, constraint_rows: list[dict[str, Any]]
    ) -> list[BaseConstraint]:
        """Shared PK/FK core with SQLite DDL overlays for real names, plus UNIQUE + CHECK from DDL.

        The registry views synthesise PK/FK/UNIQUE names (``pk_<t>`` / ``fk_<t>_<id>`` / index name);
        the real declared names live only in the table DDL, so PK and FK names are swapped in from
        there. The synthetic UNIQUE constraints are dropped in favour of the DDL-parsed UNIQUE
        constraints (real names), and CHECK constraints -- which have no catalog at all -- are
        appended straight from the DDL.
        """
        core = self._assemble_constraints_core(constraint_rows)

        constraints: list[BaseConstraint] = []
        for constraint in core:
            if isinstance(constraint, PrimaryKeyConstraint):
                constraints.append(
                    PrimaryKeyConstraint(name=_parse_pk_name(table_ddl, table_name), fields=constraint.fields),
                )
            elif isinstance(constraint, ForeignKeyConstraint):
                fk_name = _parse_fk_name(table_ddl, constraint.fields[0]) or constraint.name
                constraints.append(
                    ForeignKeyConstraint(
                        name=fk_name,
                        fields=constraint.fields,
                        reference_schema=constraint.reference_schema,
                        reference_fields=constraint.reference_fields,
                        on_update=constraint.on_update,
                        on_delete=constraint.on_delete,
                    ),
                )
            elif isinstance(constraint, UniqueConstraint):
                continue  # SQLite takes UNIQUE constraints from the DDL below (real names).

        constraints.extend(_get_unique_constraints(table_name, table_ddl, constraints))
        constraints.extend(_get_check_constraints(table_ddl))
        return constraints

    def _assemble_indexes_with_conditions(
        self, rows: list[dict[str, Any]], index_ddls: dict[str, str]
    ) -> list[IndexSchema]:
        """Shared index assembly plus the SQLite partial-index ``WHERE`` overlay from the DDL."""
        indexes = self._assemble_indexes(rows)
        for index in indexes:
            condition = _parse_index_condition(index_ddls.get(index.name))
            if condition is not None:
                index.condition = condition
        return indexes

    @staticmethod
    def _batch_ddls_query(chunk: list[str]) -> str:
        """Build the ``sqlite_master`` DDL-read statement for one chunk (bound twice: table + index)."""
        placeholders = ', '.join('?' for _ in chunk)
        return (
            'SELECT type, name, tbl_name, sql FROM sqlite_master '  # noqa: S608
            f"WHERE (type='table' AND name IN ({placeholders})) "
            f"OR (type='index' AND tbl_name IN ({placeholders}))"
        )

    @staticmethod
    def _collect_ddl_rows(
        rows: Iterable[Sequence[Any]], table_ddls: dict[str, str], index_ddls: dict[str, str]
    ) -> None:
        """Split ``sqlite_master`` rows into the table- and index-DDL maps (shared by sync + async)."""
        for row_type, name, _tbl_name, sql_text in rows:
            target = table_ddls if row_type == 'table' else index_ddls
            target[name] = sql_text or ''

    def _build_schemas(
        self,
        table_names: list[str],
        properties_by_table: dict[str, list[dict[str, Any]]],
        constraints_by_table: dict[str, list[dict[str, Any]]],
        indexes_by_table: dict[str, list[dict[str, Any]]],
        table_ddls: dict[str, str],
        index_ddls: dict[str, str],
    ) -> list[Schema]:
        """Pure (no-I/O) assembly of the grouped registry rows + DDL overlays into ``Schema`` objects.

        Identical for the sync and async connections, so it lives here and each variant calls it
        after its own (awaited or not) registry / DDL fetches.
        """
        schemas: list[Schema] = []
        for table_name in table_names:
            table_property_rows = sorted(properties_by_table.get(table_name, []), key=lambda r: r['ordinal_position'])
            if not table_property_rows:
                continue

            table_ddl = table_ddls.get(table_name, '')
            schemas.append(
                Schema(
                    name=table_name,
                    version=Version.LATEST,
                    properties=self._assemble_properties(table_property_rows, table_ddl),
                    constraints=self._assemble_constraints(
                        table_name, table_ddl, constraints_by_table.get(table_name, [])
                    )
                    or None,
                    indexes=self._assemble_indexes_with_conditions(indexes_by_table.get(table_name, []), index_ddls)
                    or None,
                ),
            )

        return schemas


class SqliteConnection(SqliteSchemaAssemblyMixin, SqliteConnectionMixin, ConnectionBase):
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

    # `SchemaAssemblyMixin._run_registry` hook: chunk IN-lists at `_SQLITE_MAX_IN` (see comment on
    # that constant above) instead of issuing one unbounded `IN (...)` for every matched table.
    _MAX_IN_PARAMS = _SQLITE_MAX_IN

    def __init__(self) -> None:
        self._connection: sqlite3.Connection | None = None
        self._generator = SqlGenerator('sqlite', param_style='qmark')
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

        # date/datetime adapters are registered once, module-level, in base.py (single source of
        # truth, matching the Rust value serialisation). Only the read-back converters are per-connection.
        sqlite3.register_converter('DATE', lambda val: date.fromisoformat(val.decode()))
        sqlite3.register_converter('TIMESTAMP', lambda val: datetime.fromisoformat(val.decode()))
        # A TIMESTAMPTZ-declared column stores a datetime the same way TIMESTAMP does; register the
        # converter under its declared-type name too so read-back re-hydrates a Python datetime
        # (``fromisoformat`` restores the tzinfo offset) instead of leaving it a raw ISO string.
        sqlite3.register_converter('TIMESTAMPTZ', lambda val: datetime.fromisoformat(val.decode()))
        # DECIMAL_TEXT is the TEXT-affinity SQLite rendering of DecimalType; re-hydrate the stored
        # decimal string back into an exact Decimal so glue returns a typed value, not a str.
        sqlite3.register_converter('DECIMAL_TEXT', lambda val: Decimal(val.decode()))

        Path(db_path).parent.mkdir(parents=True, exist_ok=True)

        # Enable PARSE_DECLTYPES so the DATE/TIMESTAMP converters above actually fire on read-back.
        # Respect a caller-supplied detect_types (only default it when absent).
        kwargs.setdefault('detect_types', sqlite3.PARSE_DECLTYPES)

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
        _stmt, _params = self._generator.compile_query(query)

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

    def query_schema(self, query: QueryStatement) -> list[Schema]:
        """
        Queries the schema of the SQLite database.

        Args:
            query (QueryStatement): The query statement referencing the registry view.

        Returns:
            list[Schema]: The list of schemas matching the filters.
        """
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

        # One bound registry query per catalog aspect plus one batched DDL read -- a constant,
        # small number of statements regardless of how many tables match (no per-table PRAGMA
        # N+1). Beyond `_SQLITE_MAX_IN` tables, `_run_registry`/`_batch_ddls` transparently chunk
        # the IN-list to stay under SQLite's bound-parameter ceiling, so the statement count grows
        # with table count only past that threshold, never per table.
        property_rows = self._run_registry(TABLE_PROPERTY_REGISTRY, _PROPERTY_COLUMNS, table_names)
        index_rows = self._run_registry(TABLE_INDEX_REGISTRY, _INDEX_COLUMNS, table_names)
        constraint_rows = self._run_registry(TABLE_CONSTRAINT_REGISTRY, _CONSTRAINT_COLUMNS, table_names)
        table_ddls, index_ddls = self._batch_ddls(table_names)

        return self._build_schemas(
            table_names,
            self._group(property_rows),
            self._group(constraint_rows),
            self._group(index_rows),
            table_ddls,
            index_ddls,
        )

    def _batch_ddls(self, names: list[str]) -> tuple[dict[str, str], dict[str, str]]:
        """Read every table and index DDL for `names` from ``sqlite_master``.

        Returns ``(table_ddl_by_name, index_ddl_by_name)`` -- the table DDL feeds the constraint /
        property overlays (real constraint names, AUTOINCREMENT, COLLATE, generated expressions) and
        the index DDL feeds the partial-index ``WHERE`` overlay.

        `names` is bound twice per query (once for the table match, once for the index match), so
        this chunks at `_SQLITE_MAX_IN` -- 2 * 400 = 800 bound params per statement, comfortably
        under `SQLITE_MAX_VARIABLE_NUMBER`'s lowest observed default of 999 -- merging the per-chunk
        dicts instead of issuing one unbounded query for every matched table.
        """
        table_ddls: dict[str, str] = {}
        index_ddls: dict[str, str] = {}
        for start in range(0, len(names), _SQLITE_MAX_IN):
            chunk = names[start : start + _SQLITE_MAX_IN]
            cursor = self.execute(self._batch_ddls_query(chunk), *chunk, *chunk)
            self._collect_ddl_rows(cursor.fetchall(), table_ddls, index_ddls)
            cursor.close()
        return table_ddls, index_ddls

    def _ensure_schema_views(self) -> None:
        # The view DDL is idempotent (CREATE ... IF NOT EXISTS), so it is re-issued on every call
        # rather than gated by a per-object flag that would go stale across disconnect()/connect()
        # cycles (temporary views are per-connection, so a reconnect must recreate them).
        for sql in self._REGISTRY_VIEW_SQL.values():
            self.execute(sql)

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
        args = bind_params(args)

        try:
            if self.debug_queries:
                self._queries.append(query)
                self._queries_params.append(args)

            cursor.execute(query, args)
        except sqlite3.IntegrityError as exc:
            self._map_integrity_error(exc)
            msg = f'Error executing SQL: {query} with args: {args}. Exception: {exc}'
            raise ConnectionError(msg) from exc
        except sqlite3.Error as exc:
            msg = f'Error executing SQL: {query} with args: {args}. Exception: {exc}'
            raise ConnectionError(msg) from exc

        return cursor

    def acquire_lock(self, lock: LockCommand) -> Any:
        """
        Acquires a lock on the SQLite database.

        SQLite has no ``LOCK TABLE`` syntax, so ``EXCLUSIVE`` mode uses ``BEGIN EXCLUSIVE`` instead.

        Args:
            lock (LockCommand): The lock command.

        Returns:
            Any: The result of the lock acquisition.
        """
        if lock.mode == 'EXCLUSIVE':
            self.connection.execute('BEGIN EXCLUSIVE')

        return True

    def release_lock(self, lock: LockCommand) -> Any:
        """
        Releases a lock on the SQLite database.

        Mirrors ``acquire_lock``: ``EXCLUSIVE`` mode commits the ``BEGIN EXCLUSIVE`` transaction.

        Args:
            lock (LockCommand): The lock command.

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
        return self.rollback_transaction(transaction)

    def _run_schema_mutation(self, mutation: SchemaMutation) -> Schema | None:
        if isinstance(mutation, UpdateProperty):
            self._update_property(mutation)
            return None
        if isinstance(mutation, AddConstraint | DeleteConstraint):
            self._recreate_table_with_constraints(mutation)
            return None

        sql_params_list = self._generator.compile_schema_mutation(mutation)

        for sql, params in sql_params_list:
            self.execute(sql, *params)

        if isinstance(mutation, RegisterSchema):
            return mutation.schema

        return None

    def _update_property(self, mutation: UpdateProperty) -> None:
        """Port UpdateProperty to SQLite via ADD / UPDATE / DROP / RENAME column sequence."""
        if mutation.property.required and mutation.property.default is None:
            msg = (
                f'Cannot update {mutation.property.name} column. '
                "SQLite doesn't support ALTER COLUMN with required=True and no default value."
            )
            raise ValueError(msg)

        new_uuid = f'f{uuid.uuid4().hex}'
        new_prop = copy(mutation.property)
        new_prop.name = new_uuid

        ref = mutation.schema_ref

        # a. Add new column with the requested type under a temporary name.
        for sql, params in self._generator.compile_schema_mutation(AddProperty(schema_ref=ref, property=new_prop)):
            self.execute(sql, *params)

        # b. Copy data from the old column into the new one.
        copy_stmt, copy_params = self._generator.compile_mutation(
            UpdateData(
                schema=ref,
                data=DataInput(
                    data={
                        new_uuid: FieldReferenceExpression(
                            field_reference=FieldReference(
                                field=Field(name=mutation.property.name),
                                table_name=ref.name,
                            )
                        )
                    },
                ),
            )
        )
        self.execute(copy_stmt, *copy_params)

        # c. Drop the old column.
        for sql, params in self._generator.compile_schema_mutation(
            DeleteProperty(schema_ref=ref, property_name=mutation.property.name)
        ):
            self.execute(sql, *params)

        # d. Rename the temporary column to the original name.
        for sql, params in self._generator.compile_schema_mutation(
            RenameProperty(schema_ref=ref, old_name=new_uuid, new_name=mutation.property.name)
        ):
            self.execute(sql, *params)

    def _recreate_table_with_constraints(  # noqa: C901, PLR0912
        self, mutation: AddConstraint | DeleteConstraint
    ) -> None:
        """Rebuild the table under a temp name to apply AddConstraint / DeleteConstraint on SQLite."""
        table_name = mutation.schema_ref.name
        namespace = mutation.schema_ref.namespace

        # Introspect the current schema.
        all_schemas = self.query_schema(
            QueryStatement(table=SchemaReference(name=TABLE_REGISTRY, version=Version.LATEST))
        )
        current_schema: Schema | None = None
        for schema in all_schemas:
            schema_namespace = schema.namespace
            if schema.name == table_name and (
                (not namespace and not schema_namespace) or namespace == schema_namespace
            ):
                current_schema = schema
                break

        if current_schema is None:
            msg = f'Table {table_name} not found. Available tables: {[(s.name, s.namespace) for s in all_schemas]}'
            raise ValueError(msg)

        # Compute the new constraint list.
        new_constraints = list(current_schema.constraints or [])
        if isinstance(mutation, AddConstraint):
            new_constraints.append(mutation.constraint)
        else:
            new_constraints = [c for c in new_constraints if c.name != mutation.constraint_name]

        # Build the temp-table schema.
        temp_table_name = f'temp_{table_name}_{uuid.uuid4().hex[:8]}'
        temp_ref = SchemaReference(name=temp_table_name, version=Version.LATEST)
        orig_ref = SchemaReference(name=table_name, version=Version.LATEST, namespace=namespace)
        temp_schema = Schema(
            name=temp_table_name,
            namespace=namespace,
            version=current_schema.version,
            properties=current_schema.properties,
            constraints=new_constraints or None,
            indexes=[],
        )

        # Detect whether we are already inside a transaction.
        in_transaction = False
        try:
            self.connection.execute('BEGIN')
        except sqlite3.OperationalError as exc:
            if 'cannot start a transaction within a transaction' in str(exc):
                in_transaction = True
            else:
                raise

        try:
            # a. CREATE temp table.
            for sql, params in self._generator.compile_schema_mutation(
                RegisterSchema(schema_ref=temp_ref, schema=temp_schema)
            ):
                self.execute(sql, *params)

            # b. Copy all rows from the original table into the temp table.
            col_names = [prop.name for prop in current_schema.properties]
            insert_mut = InsertFromSelect(
                schema=temp_ref,
                query=QueryStatement(
                    table=orig_ref,
                    only=[FieldReference(field=Field(name=c), table_name=table_name) for c in col_names],
                ),
                columns=[FieldReference(field=Field(name=c), table_name=temp_table_name) for c in col_names],
            )
            copy_sql, copy_params = self._generator.compile_mutation(insert_mut)
            self.execute(copy_sql, *copy_params)

            # c. DROP the original table.
            for sql, params in self._generator.compile_schema_mutation(DeleteSchema(schema_ref=orig_ref)):
                self.execute(sql, *params)

            # d. RENAME temp → original.
            for sql, params in self._generator.compile_schema_mutation(
                RenameSchema(schema_ref=temp_ref, new_name=table_name)
            ):
                self.execute(sql, *params)

            # e. Recreate indexes on the renamed table.
            renamed_ref = SchemaReference(name=table_name, version=Version.LATEST, namespace=namespace)
            for idx in current_schema.indexes or []:
                for sql, params in self._generator.compile_schema_mutation(AddIndex(schema_ref=renamed_ref, index=idx)):
                    self.execute(sql, *params)

            if not in_transaction:
                self.connection.execute('COMMIT')

        except Exception:
            if not in_transaction:
                self.connection.execute('ROLLBACK')
            raise
