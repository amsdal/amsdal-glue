"""Shared cross-dialect schema-assembly mixin fed by canonical registry rows.

`_assemble_indexes` and `_assemble_constraints_core` are the identical code path for every SQL
dialect this project supports -- the entire point of the canonical (identical-shape) registry
rows produced by `amsdal_glue_connections.sql.schema_registry`. Dialect specifics (scalar type
resolution, DDL-only overlays such as SQLite's partial-index ``WHERE`` clause or AUTOINCREMENT
identity, Postgres CHECK / exclusion constraints) live in the connection classes that mix this in.
"""

from __future__ import annotations

from collections import defaultdict
from typing import Any
from typing import TYPE_CHECKING

from amsdal_glue_core.common.data_models.conditions import Condition
from amsdal_glue_core.common.data_models.conditions import Conditions
from amsdal_glue_core.common.data_models.constraints import BaseConstraint
from amsdal_glue_core.common.data_models.constraints import ForeignKeyConstraint
from amsdal_glue_core.common.data_models.constraints import PrimaryKeyConstraint
from amsdal_glue_core.common.data_models.constraints import UniqueConstraint
from amsdal_glue_core.common.data_models.field_reference import Field
from amsdal_glue_core.common.data_models.field_reference import FieldReference
from amsdal_glue_core.common.data_models.indexes import IndexField
from amsdal_glue_core.common.data_models.indexes import IndexSchema
from amsdal_glue_core.common.data_models.query import QueryStatement
from amsdal_glue_core.common.data_models.schema import PropertySchema
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.enums import BuiltinIndexType
from amsdal_glue_core.common.enums import FieldLookup
from amsdal_glue_core.common.enums import OrderDirection
from amsdal_glue_core.common.enums import ReferentialAction
from amsdal_glue_core.common.enums import Version
from amsdal_glue_core.common.expressions.field_reference import FieldReferenceExpression
from amsdal_glue_core.common.expressions.value import Value

if TYPE_CHECKING:
    from collections.abc import Iterable
    from collections.abc import Iterator
    from collections.abc import Sequence

    from amsdal_glue_core.common.data_models.types import FieldType
    from amsdal_glue_core.common.expressions.expression import Expression

# Normalised action codes are identical on every dialect (the registry views emit these strings
# directly, see `TABLE_CONSTRAINT_REGISTRY`), so a single map covers FK overlays for all callers.
_NORMALISED_ACTION_MAP: dict[str | None, ReferentialAction] = {
    'NO_ACTION': ReferentialAction.NO_ACTION,
    'RESTRICT': ReferentialAction.RESTRICT,
    'CASCADE': ReferentialAction.CASCADE,
    'SET_NULL': ReferentialAction.SET_NULL,
    'SET_DEFAULT': ReferentialAction.SET_DEFAULT,
    None: ReferentialAction.NO_ACTION,
}

_INDEX_TYPE_MAP: dict[str, BuiltinIndexType] = {
    'btree': BuiltinIndexType.BTREE,
    'hash': BuiltinIndexType.HASH,
    'gin': BuiltinIndexType.GIN,
    'gist': BuiltinIndexType.GIST,
    'brin': BuiltinIndexType.BRIN,
}


def _registry_field(view: str, name: str) -> FieldReference:
    return FieldReference(field=Field(name=name), table_name=view)


class SchemaAssemblyMixin:
    """Cross-dialect assembly of `Schema` pieces from canonical registry rows.

    Mixed into the SQL dialect connection classes (`SqliteConnection`, `PostgresConnection`, ...).
    `_run_registry` assumes the host class exposes `self._generator` (a `SqlGenerator`) and
    `self.execute(sql, *params) -> Cursor`, matching the existing connection classes. Both are
    declared for type checking only (see below); the connection base provides the real
    implementations, so this mixin can sit ahead of the connection base in the MRO.
    """

    _generator: Any

    # Overridable per-dialect cap on how many names go into a single `IN (...)` list issued by
    # `_run_registry`. `None` (the default) means "no chunking" -- one query for all `names`, which
    # is correct for backends without a low bound-parameter ceiling (e.g. Postgres via psycopg).
    # SQLite overrides this (see `SqliteConnection._MAX_IN_PARAMS`) because
    # `SQLITE_MAX_VARIABLE_NUMBER` can be as low as 999 on some builds.
    _MAX_IN_PARAMS: int | None = None

    if TYPE_CHECKING:
        # Declared for type checking only -- never defined at runtime, so it does not shadow the
        # real `execute` the connection base contributes when this mixin sits ahead of it.
        def execute(self, query: str, *args: Any) -> Any: ...

    def _type_to_field_type(self, row: dict[str, Any]) -> FieldType:
        """Resolve a property registry row's `type` column to a glue `FieldType`.

        Dialect-specific: SQLite's and Postgres' type systems, modifiers, array/vector/serial
        detection differ enough that this is the one hook every dialect subclass must supply.
        """
        msg = '_type_to_field_type() must be implemented by the connection class this mixin is mixed into'
        raise NotImplementedError(msg)

    def _parse_default_expression(self, raw: str | None, field_type: FieldType | None) -> Expression | None:
        """Parse a raw DEFAULT / GENERATED expression string into a glue `Expression`.

        Also dialect-specific: the literal/cast syntax Postgres and SQLite emit for column
        defaults and generated-column expressions differs (e.g. Postgres' `::type` casts and
        `nextval(...)` sequence defaults vs SQLite's untyped literals), so each dialect maps the
        shared expression AST (`amsdal_glue_connections.sql.parsers.default`) through its own
        mapper (`pg_mapper` / `sqlite_mapper`).
        """
        msg = '_parse_default_expression() must be implemented by the connection class this mixin is mixed into'
        raise NotImplementedError(msg)

    # ------------------------------------------------------------------ rows

    def _registry_query(self, view: str, columns: list[str], names: list[str]) -> QueryStatement:
        """Build the ``SELECT columns FROM view WHERE table_name IN (names)`` registry query.

        Uses a bound IN-list (`Value(list(...))`), never string concatenation, so arbitrary table
        names are safe.
        """
        return QueryStatement(
            table=SchemaReference(name=view, version=Version.LATEST),
            only=[_registry_field(view, column) for column in columns],
            where=Conditions(
                Condition(
                    left=FieldReferenceExpression(field_reference=_registry_field(view, 'table_name')),
                    lookup=FieldLookup.IN,
                    right=Value(list(names)),
                ),
            ),
        )

    def _iter_name_chunks(self, names: list[str]) -> Iterator[list[str]]:
        """Yield `names` in batches of at most `_MAX_IN_PARAMS` (a single batch when it is `None`).

        SQLite sets `_MAX_IN_PARAMS` because `SQLITE_MAX_VARIABLE_NUMBER` can be as low as 999 on some
        builds; Postgres leaves it `None`, so every name goes into one bound query.
        """
        size = self._MAX_IN_PARAMS
        if size is None or len(names) <= size:
            yield names
            return
        for start in range(0, len(names), size):
            yield names[start : start + size]

    def _run_registry(self, view: str, columns: list[str], names: list[str]) -> list[dict[str, Any]]:
        """Fetch canonical registry rows for `names` -- a constant, small number of statements.

        The `IN`-list is chunked by `_iter_name_chunks` so each statement stays under the backend's
        bound-parameter ceiling. The async connections override this with an awaiting twin; the query
        construction (`_registry_query`) and chunking are shared.
        """
        rows: list[dict[str, Any]] = []
        for chunk in self._iter_name_chunks(names):
            sql, params = self._generator.compile_query(self._registry_query(view, columns, chunk))
            cursor = self.execute(sql, *params)
            rows.extend(dict(zip(columns, row, strict=True)) for row in cursor.fetchall())
            cursor.close()
        return rows

    @staticmethod
    def _dedupe_names(rows: Iterable[Sequence[Any]]) -> list[str]:
        """Order-preserving de-dup of the single-column ``(name,)`` rows the registry-view scan returns."""
        return list(dict.fromkeys(name for (name,) in rows))

    def _group(self, rows: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
        """Group canonical rows by `table_name`, preserving row order within each group."""
        grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for row in rows:
            grouped[row['table_name']].append(row)
        return grouped

    # -------------------------------------------------------------- indexes

    def _assemble_indexes(self, rows: list[dict[str, Any]]) -> list[IndexSchema]:
        """Canonical index rows -> `IndexSchema`, grouped by index name in first-seen order.

        `is_included` / `op_class` are optional Postgres-only extras read via `.get(...)` so this
        single code path stays dialect-neutral -- SQLite rows simply omit them, which reads back
        as "not an INCLUDE column" / "default operator class".
        """
        rows_by_name: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for row in rows:
            rows_by_name[row['name']].append(row)

        indexes: list[IndexSchema] = []
        for name, name_rows in rows_by_name.items():
            index_rows = sorted(name_rows, key=lambda r: r['ordinal_position'])
            key_rows = [r for r in index_rows if not r.get('is_included')]
            included_rows = [r for r in index_rows if r.get('is_included')]

            # An index whose only key columns are expressions (e.g. ``(lower(a)) INCLUDE (b)``) yields
            # no key rows -- the expression columns produce no ``pg_attribute`` match. Such an index is
            # not representable from column rows alone, so skip it rather than crashing on ``key_rows[0]``.
            if not key_rows:
                continue

            fields = [
                IndexField(
                    name=row['column_name'],
                    direction=OrderDirection.DESC if row['is_descending'] else OrderDirection.ASC,
                    op_class=row.get('op_class'),
                )
                for row in key_rows
            ]

            indexes.append(
                IndexSchema(
                    name=name,
                    fields=fields,
                    unique=bool(key_rows[0]['is_unique']),
                    index_type=_INDEX_TYPE_MAP.get(key_rows[0]['index_type'], BuiltinIndexType.BTREE),
                    include=[row['column_name'] for row in included_rows] or None,
                ),
            )
        return indexes

    # ---------------------------------------------------------- constraints

    def _assemble_constraints_core(self, rows: list[dict[str, Any]]) -> list[BaseConstraint]:
        """Canonical constraint rows -> PK / FK / UNIQUE constraints.

        CHECK and exclusion constraints are Postgres-only (`type in ('c', 'x')`) and are not
        representable from the canonical rows alone (SQLite has no constraint catalog for them),
        so dialect subclasses append those on top of this core result from their own constraint
        definition source (e.g. `pg_get_constraintdef` / parsed table DDL).
        """
        constraints: list[BaseConstraint] = []

        def _grouped(type_code: str) -> list[list[dict[str, Any]]]:
            """Rows of the given constraint ``type`` grouped by name (first-seen order), each sorted."""
            groups: dict[str, list[dict[str, Any]]] = {}
            for row in rows:
                if row['type'] == type_code:
                    groups.setdefault(row['name'], []).append(row)
            return [sorted(group, key=lambda r: r['ordinal_position']) for group in groups.values()]

        pk_rows = sorted((r for r in rows if r['type'] == 'p'), key=lambda r: r['ordinal_position'])
        if pk_rows:
            constraints.append(
                PrimaryKeyConstraint(name=pk_rows[0]['name'], fields=[r['column_name'] for r in pk_rows]),
            )

        constraints.extend(
            ForeignKeyConstraint(
                name=ordered_fk_rows[0]['name'],
                fields=[r['column_name'] for r in ordered_fk_rows],
                reference_schema=SchemaReference(name=ordered_fk_rows[0]['ref_table'], version=Version.LATEST),
                reference_fields=[r['ref_column'] for r in ordered_fk_rows],
                on_update=_NORMALISED_ACTION_MAP.get(ordered_fk_rows[0]['on_update'], ReferentialAction.NO_ACTION),
                on_delete=_NORMALISED_ACTION_MAP.get(ordered_fk_rows[0]['on_delete'], ReferentialAction.NO_ACTION),
            )
            for ordered_fk_rows in _grouped('f')
        )

        constraints.extend(
            UniqueConstraint(name=ordered_uq_rows[0]['name'], fields=[r['column_name'] for r in ordered_uq_rows])
            for ordered_uq_rows in _grouped('u')
        )

        return constraints

    # ----------------------------------------------------------- properties

    def _assemble_property_core(self, row: dict[str, Any]) -> PropertySchema:
        """Dialect-neutral property core: ``name``, ``type``, ``required`` and ``default``.

        ``identity`` / ``generated`` / ``db_collation`` are dialect-specific overlays, not part of
        this core. SQLite's catalog exposes none of them (the registry view leaves them ``NULL``), so
        the SQLite connection parses them out of the table DDL and layers them on top of this result;
        Postgres builds its properties in its own ``_assemble_property`` (SERIAL detection is
        entangled with the field type and default there). Only the SQLite connection uses this core.
        """
        field_type = self._type_to_field_type(row)
        return PropertySchema(
            name=row['name'],
            type=field_type,
            required=row['is_nullable'] == 'NO',
            default=self._parse_default_expression(row.get('column_default'), field_type),
        )


class AsyncSchemaAssemblyMixin(SchemaAssemblyMixin):
    """Async counterpart of `SchemaAssemblyMixin`, mixed into the async connection classes.

    Only `_run_registry` needs an awaiting twin -- the query construction (`_registry_query`),
    chunking (`_iter_name_chunks`) and the pure assembly helpers are inherited unchanged. Placing it
    here keeps the single async fetch loop shared across dialects instead of copied per connection.
    """

    async def _run_registry(  # type: ignore[override]
        self, view: str, columns: list[str], names: list[str]
    ) -> list[dict[str, Any]]:
        rows: list[dict[str, Any]] = []
        for chunk in self._iter_name_chunks(names):
            sql, params = self._generator.compile_query(self._registry_query(view, columns, chunk))
            cursor = await self.execute(sql, *params)
            rows.extend(dict(zip(columns, row, strict=True)) for row in await cursor.fetchall())
            await cursor.close()
        return rows
