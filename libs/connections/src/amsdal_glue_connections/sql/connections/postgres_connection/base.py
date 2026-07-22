import contextlib
import logging
from typing import Any
from typing import TYPE_CHECKING

from amsdal_glue_core.common.data_models.json_value import JsonValue
from amsdal_glue_core.common.enums import ScalarType

from amsdal_glue_connections.sql.connections.base_connection import SqlConnectionMixinBase
from amsdal_glue_connections.sql.schema_registry import TABLE_CONSTRAINT_REGISTRY
from amsdal_glue_connections.sql.schema_registry import TABLE_INDEX_REGISTRY
from amsdal_glue_connections.sql.schema_registry import TABLE_PROPERTY_REGISTRY
from amsdal_glue_connections.sql.schema_registry import TABLE_REGISTRY

if TYPE_CHECKING:
    from psycopg.sql import Composable

logger = logging.getLogger(__name__)

# A Python ``list`` reaches the driver as a native list (the generator maps it to a SQL array), and
# psycopg does not adapt one to ``jsonb`` by default. Register a global dumper — module-level (guarded,
# since psycopg is an optional dependency) so every connection inherits it, including subclasses that
# manage their own ``psycopg.connect`` (e.g. amsdal_data's historical connections) instead of calling
# ``super().connect``. A ``dict`` needs no such dumper: it is JSON by construction, so it arrives as a
# ``JsonValue`` marker and is bound by :func:`bind_params`.
with contextlib.suppress(ImportError):
    import psycopg
    from psycopg.types.json import JsonbBinaryDumper

    psycopg.adapters.register_dumper(list, JsonbBinaryDumper)


def bind_params(args: tuple[Any, ...]) -> tuple[Any, ...]:
    """Bind the generator's JSON-typed parameters as psycopg JSON wrappers.

    ``Value(x, output_type=JSONB)`` types the *parameter*, whatever ``x`` is — a scalar, a container,
    or ``None`` (a JSON ``null``). The generator cannot build ``psycopg.types.json.Jsonb`` itself, so it
    hands over a dialect-neutral :class:`JsonValue` and the wrapping happens here.
    """
    from psycopg.types.json import Json
    from psycopg.types.json import Jsonb

    return tuple(
        (Json(arg.value) if arg.scalar_type == ScalarType.JSON else Jsonb(arg.value))
        if isinstance(arg, JsonValue)
        else arg
        for arg in args
    )


def build_registry_view_sql(schema: str) -> 'dict[str, Composable]':
    """Build the registry-view DDL for a specific connection schema.

    The schema is a value compared against ``information_schema`` / ``pg_namespace`` columns
    (``table_schema = 'public'`` / ``nspname = 'public'``), so it is injected as a properly quoted
    SQL literal via ``psycopg.sql.Literal`` — never f-string interpolated — closing the same
    injection hole handled for ``SET search_path``. The view names are equally quoted via
    ``psycopg.sql.Identifier`` so the whole DDL is composition-safe.
    """
    from psycopg import sql

    schema_literal = sql.Literal(schema)

    return {
        TABLE_REGISTRY: sql.SQL(
            'CREATE OR REPLACE TEMPORARY VIEW {view} AS '
            'SELECT table_name AS name, table_name '
            'FROM information_schema.tables '
            "WHERE table_schema = {schema} AND table_type = 'BASE TABLE'"
        ).format(view=sql.Identifier(TABLE_REGISTRY), schema=schema_literal),
        TABLE_PROPERTY_REGISTRY: sql.SQL(
            'CREATE OR REPLACE TEMPORARY VIEW {view} AS '
            'SELECT c.table_name, c.column_name AS name, c.data_type AS type, '
            'c.is_nullable, c.column_default, c.ordinal_position, '
            "CASE WHEN c.is_generated = 'ALWAYS' THEN 1 ELSE 0 END AS is_generated, "
            'c.collation_name AS collation, c.generation_expression, '
            "CASE WHEN c.is_identity = 'YES' THEN 1 ELSE 0 END AS is_identity, "
            'c.identity_generation, c.is_generated AS is_generated_raw, '
            'c.is_identity AS is_identity_raw, '
            'format_type(a.atttypid, a.atttypmod) AS format_type, '
            'seq.start_value AS seq_start, seq.increment_by AS seq_increment, '
            'seq.min_value AS seq_min, seq.max_value AS seq_max, '
            'seq.cycle AS seq_cycle, seq.cache_size AS seq_cache '
            'FROM information_schema.columns c '
            'JOIN pg_namespace n ON n.nspname = c.table_schema '
            'JOIN pg_class cl ON cl.relname = c.table_name AND cl.relnamespace = n.oid '
            'JOIN pg_attribute a ON a.attrelid = cl.oid AND a.attname = c.column_name '
            'AND a.attnum > 0 AND NOT a.attisdropped '
            'LEFT JOIN LATERAL ( '
            'SELECT s.start_value, s.increment_by, s.min_value, s.max_value, s.cycle, s.cache_size '
            'FROM pg_sequences s '
            "WHERE (s.schemaname || '.' || s.sequencename) = "
            "pg_get_serial_sequence(quote_ident(c.table_schema) || '.' || quote_ident(c.table_name), c.column_name) "
            ') seq ON true '
            'WHERE c.table_schema = {schema}'
        ).format(view=sql.Identifier(TABLE_PROPERTY_REGISTRY), schema=schema_literal),
        TABLE_CONSTRAINT_REGISTRY: sql.SQL(
            'CREATE OR REPLACE TEMPORARY VIEW {view} AS '
            'SELECT cls.relname AS table_name, con.conname AS name, con.contype AS type, '
            'att.attname AS column_name, (u.pos - 1) AS ordinal_position, '
            'refc.relname AS ref_table, ref_att.attname AS ref_column, '
            "CASE con.confupdtype WHEN 'a' THEN 'NO_ACTION' WHEN 'r' THEN 'RESTRICT' WHEN 'c' THEN 'CASCADE' "
            "WHEN 'n' THEN 'SET_NULL' WHEN 'd' THEN 'SET_DEFAULT' END AS on_update, "
            "CASE con.confdeltype WHEN 'a' THEN 'NO_ACTION' WHEN 'r' THEN 'RESTRICT' WHEN 'c' THEN 'CASCADE' "
            "WHEN 'n' THEN 'SET_NULL' WHEN 'd' THEN 'SET_DEFAULT' END AS on_delete, "
            'pg_get_constraintdef(con.oid) AS def '
            'FROM pg_constraint con '
            'JOIN pg_class cls ON cls.oid = con.conrelid '
            'JOIN pg_namespace nsp ON nsp.oid = cls.relnamespace AND nsp.nspname = {schema} '
            'LEFT JOIN LATERAL unnest(con.conkey) WITH ORDINALITY AS u(attnum, pos) ON true '
            'LEFT JOIN pg_attribute att ON att.attrelid = con.conrelid AND att.attnum = u.attnum '
            'LEFT JOIN pg_class refc ON refc.oid = con.confrelid '
            'LEFT JOIN LATERAL unnest(con.confkey) WITH ORDINALITY AS fk(attnum, pos) ON fk.pos = u.pos '
            'LEFT JOIN pg_attribute ref_att ON ref_att.attrelid = con.confrelid AND ref_att.attnum = fk.attnum'
        ).format(view=sql.Identifier(TABLE_CONSTRAINT_REGISTRY), schema=schema_literal),
        TABLE_INDEX_REGISTRY: sql.SQL(
            'CREATE OR REPLACE TEMPORARY VIEW {view} AS '
            'SELECT tc.relname AS table_name, ic.relname AS name, '
            'CASE WHEN ix.indisunique THEN 1 ELSE 0 END AS is_unique, '
            'att.attname AS column_name, (k.pos - 1) AS ordinal_position, '
            'CASE WHEN ix.indoption[k.pos - 1] & 1 = 1 THEN 1 ELSE 0 END AS is_descending, '
            'am.amname AS index_type, '
            'CASE WHEN k.pos > ix.indnkeyatts THEN 1 ELSE 0 END AS is_included, '
            'CASE WHEN opc.opcdefault THEN NULL ELSE opc.opcname END AS op_class, '
            # Partial-index WHERE predicate (NULL for a non-partial index); overlaid as the index
            # ``condition`` during assembly, mirroring the SQLite partial-index WHERE capture.
            'pg_get_expr(ix.indpred, ix.indrelid) AS index_predicate '
            'FROM pg_index ix '
            'JOIN pg_class tc ON tc.oid = ix.indrelid '
            'JOIN pg_class ic ON ic.oid = ix.indexrelid '
            'JOIN pg_am am ON am.oid = ic.relam '
            'JOIN pg_namespace nsp ON nsp.oid = tc.relnamespace AND nsp.nspname = {schema} '
            'CROSS JOIN LATERAL unnest(ix.indkey) WITH ORDINALITY AS k(attnum, pos) '
            'JOIN pg_attribute att ON att.attrelid = tc.oid AND att.attnum = k.attnum '
            'LEFT JOIN pg_opclass opc ON opc.oid = ix.indclass[k.pos - 1] '
            'WHERE NOT ix.indisprimary '
            'AND NOT EXISTS (SELECT 1 FROM pg_constraint con '
            "WHERE con.conindid = ix.indexrelid AND con.contype = 'u')"
        ).format(view=sql.Identifier(TABLE_INDEX_REGISTRY), schema=schema_literal),
    }


class PostgresConnectionMixin(SqlConnectionMixinBase):
    def _build_registry_view_sql(self, schema: str) -> 'dict[str, Composable]':
        """Overridable registry-view DDL builder used by ``_ensure_schema_views``.

        A subclass (e.g. a versioned / lakehouse connection) can override this to redefine one or more
        views; the default delegates to the module-level :func:`build_registry_view_sql`.
        """
        return build_registry_view_sql(schema)
