import logging
import re
import sqlite3
import uuid
from copy import copy
from datetime import date
from datetime import datetime
from pathlib import Path
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
from amsdal_glue_core.common.data_models.schema import PropertySchema
from amsdal_glue_core.common.data_models.schema import Schema
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.data_models.types import CustomType
from amsdal_glue_core.common.enums import ScalarType
from amsdal_glue_core.common.enums import Version
from amsdal_glue_core.common.exceptions import AmsdalGlueError
from amsdal_glue_core.common.exceptions import UniqueViolationError
from amsdal_glue_core.common.expressions.field_reference import FieldReferenceExpression
from amsdal_glue_core.common.expressions.raw import RawExpression
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
from amsdal_glue_connections.sql.connections.sqlite_connection.base import _REGISTRY_VIEW_SQL
from amsdal_glue_connections.sql.connections.sqlite_connection.base import SqliteConnectionMixin
from amsdal_glue_connections.sql.schema_registry import TABLE_REGISTRY

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

_DECIMAL_PARAMS_RE = re.compile(
    r'^(DECIMAL_TEXT|NUMERIC|DECIMAL)\s*\(\s*(\d+)\s*,\s*(\d+)\s*\)\s*$',
    re.IGNORECASE,
)


def _sqlite_type_to_field_type(type_name: str) -> ScalarType | CustomType:
    """Map a SQLite column type string to a FieldType."""
    # Detect parameterised decimal types before stripping parens.
    m = _DECIMAL_PARAMS_RE.match(type_name.strip())
    if m:
        base_name = m.group(1).upper()
        precision = int(m.group(2))
        scale = int(m.group(3))
        name = 'decimal_text' if base_name == 'DECIMAL_TEXT' else 'NUMERIC'
        return CustomType(name=name, params={'precision': precision, 'scale': scale})

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


def _parse_generated_expressions(table_ddl: str) -> dict[str, RawExpression]:
    results: dict[str, RawExpression] = {}
    for match in re.finditer(
        r'"(\w+)"\s+\w+[^,]*\bGENERATED\s+ALWAYS\s+AS\s*\((.+?)\)\s*(?:STORED|VIRTUAL)',
        table_ddl,
        re.IGNORECASE,
    ):
        results[match.group(1)] = RawExpression(value=match.group(2).strip())
    return results


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
            table_ddl = self._get_table_ddl(table_name)
            properties = self._introspect_columns(table_name, table_ddl)
            if not properties:
                continue

            constraints = self._introspect_constraints(table_name, table_ddl)
            indexes = self._introspect_indexes(table_name)

            schemas.append(
                Schema(
                    name=table_name,
                    version=Version.LATEST,
                    properties=properties,
                    constraints=constraints or None,
                    indexes=indexes or None,
                ),
            )

        return schemas

    def _ensure_schema_views(self) -> None:
        # The view DDL is idempotent (CREATE ... IF NOT EXISTS), so it is re-issued on every call
        # rather than gated by a per-object flag that would go stale across disconnect()/connect()
        # cycles (temporary views are per-connection, so a reconnect must recreate them).
        for sql in _REGISTRY_VIEW_SQL.values():
            self.execute(sql)

    def _get_table_ddl(self, table_name: str) -> str:
        cursor = self.execute(
            "SELECT sql FROM sqlite_master WHERE type='table' AND name=?",
            table_name,
        )
        row = cursor.fetchone()
        cursor.close()
        return row[0] if row else ''

    def _introspect_columns(self, table_name: str, table_ddl: str) -> list[PropertySchema]:
        cursor = self.execute(f'PRAGMA table_xinfo("{table_name}")')
        rows = cursor.fetchall()
        cursor.close()

        has_autoincrement = 'AUTOINCREMENT' in table_ddl.upper()
        pk_col = _find_autoincrement_pk_col(table_ddl) if has_autoincrement else None
        generated_exprs = _parse_generated_expressions(table_ddl)
        collations = _parse_collations(table_ddl)

        properties: list[PropertySchema] = []
        for _cid, col_name, col_type, notnull, dflt, _pk, _hidden in rows:
            field_type = _sqlite_type_to_field_type(col_type)
            default = RawExpression(value=dflt) if dflt is not None else None
            identity: bool | None = True if col_name == pk_col else None

            properties.append(
                PropertySchema(
                    name=col_name,
                    type=field_type,
                    required=bool(notnull),
                    default=default,
                    identity=identity,
                    generated=generated_exprs.get(col_name),
                    db_collation=collations.get(col_name),
                ),
            )

        return properties

    def _get_pk_fields(self, table_name: str) -> list[str]:
        cursor = self.execute(f'PRAGMA table_info("{table_name}")')
        rows = cursor.fetchall()
        cursor.close()

        pk_cols: list[tuple[int, str]] = []
        for _cid, col_name, _col_type, _notnull, _dflt, pk_idx in rows:
            if pk_idx > 0:
                pk_cols.append((pk_idx, col_name))

        pk_cols.sort()
        return [name for _, name in pk_cols]

    def _get_fk_constraints(self, table_name: str, table_sql: str) -> list[ForeignKeyConstraint]:
        cursor = self.execute(f'PRAGMA foreign_key_list("{table_name}")')
        rows = cursor.fetchall()
        cursor.close()

        if not rows:
            return []

        fk_groups: dict[int, dict[str, Any]] = {}
        for fk_id, _seq, ref_table, from_col, to_col, _on_update, _on_delete, _match in rows:
            if fk_id not in fk_groups:
                fk_groups[fk_id] = {'ref_table': ref_table, 'fields': [], 'ref_fields': []}
            fk_groups[fk_id]['fields'].append(from_col)
            fk_groups[fk_id]['ref_fields'].append(to_col)

        constraints: list[ForeignKeyConstraint] = []
        for fk_id, group in fk_groups.items():
            primary_field = group['fields'][0]
            fk_name = _parse_fk_name(table_sql, primary_field)
            if not fk_name:
                fk_name = f'fk_{table_name}_{fk_id}'

            constraints.append(
                ForeignKeyConstraint(
                    name=fk_name,
                    fields=group['fields'],
                    reference_schema=SchemaReference(name=group['ref_table'], version=Version.LATEST),
                    reference_fields=group['ref_fields'],
                ),
            )

        return constraints

    def _introspect_constraints(self, table_name: str, table_ddl: str) -> list[BaseConstraint]:
        constraints: list[BaseConstraint] = []

        pk_fields = self._get_pk_fields(table_name)
        if pk_fields:
            constraints.append(PrimaryKeyConstraint(name=_parse_pk_name(table_ddl, table_name), fields=pk_fields))

        constraints.extend(self._get_fk_constraints(table_name, table_ddl))
        constraints.extend(_get_unique_constraints(table_name, table_ddl, constraints))

        # CheckConstraint: skipped — no SQL→Conditions parser in prod (matches PG).

        return constraints

    def _introspect_indexes(self, table_name: str) -> list[IndexSchema]:
        cursor = self.execute(f'PRAGMA index_list("{table_name}")')
        idx_rows = cursor.fetchall()
        cursor.close()

        indexes: list[IndexSchema] = []
        for _seq, idx_name, is_unique, origin, _partial in idx_rows:
            if origin in ('u', 'pk'):
                continue

            cursor = self.execute(f'PRAGMA index_xinfo("{idx_name}")')
            info_rows = cursor.fetchall()
            cursor.close()

            idx_fields = [IndexField(name=row[2]) for row in info_rows if row[2] is not None]

            indexes.append(IndexSchema(name=idx_name, fields=idx_fields, unique=bool(is_unique)))

        return indexes

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

        try:
            if self.debug_queries:
                self._queries.append(query)
                self._queries_params.append(args)

            cursor.execute(query, args)
        except sqlite3.IntegrityError as exc:
            if 'UNIQUE constraint failed' in str(exc):
                raise UniqueViolationError(str(exc)) from exc
            msg = f'Error executing SQL: {query} with args: {args}. Exception: {exc}'
            raise ConnectionError(msg) from exc
        except sqlite3.Error as exc:
            msg = f'Error executing SQL: {query} with args: {args}. Exception: {exc}'
            raise ConnectionError(msg) from exc

        return cursor

    def acquire_lock(self, lock: LockCommand) -> Any:
        """
        Acquires a lock on the SQLite database.

        Deliberate divergence from the Rust ``compile_lock_command`` path: SQLite does not
        support ``LOCK TABLE`` syntax.  We keep the existing ``BEGIN EXCLUSIVE`` hack instead.
        TODO spec §3.5 — revisit whether SQLite should raise ``NotImplementedError`` (source parity).

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

        Deliberate divergence from the Rust ``compile_lock_command`` path — mirrors ``acquire_lock``.
        TODO spec §3.5.

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
        if isinstance(transaction, TransactionCommand) and transaction.parent_transaction_id:
            self.connection.execute(f"ROLLBACK TO SAVEPOINT '{transaction.parent_transaction_id}'")
        else:
            self.connection.execute('ROLLBACK')
        return True

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
                data={
                    new_uuid: FieldReferenceExpression(
                        field_reference=FieldReference(
                            field=Field(name=mutation.property.name),
                            table_name=ref.name,
                        )
                    )
                },
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
                (namespace is None and (schema_namespace is None or schema_namespace == ''))
                or (namespace == '' and (schema_namespace is None or schema_namespace == ''))
                or (namespace == schema_namespace)
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
