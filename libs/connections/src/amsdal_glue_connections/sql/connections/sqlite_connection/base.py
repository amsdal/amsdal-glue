import datetime as _dt
import json
import logging
import sqlite3
from decimal import Decimal
from typing import Any
from typing import ClassVar
from uuid import UUID

from amsdal_glue_core.common.data_models.json_value import JsonValue
from amsdal_glue_core.common.exceptions import ForeignKeyViolationError
from amsdal_glue_core.common.exceptions import UniqueViolationError

from amsdal_glue_connections.sql.connections.base_connection import SqlConnectionMixinBase
from amsdal_glue_connections.sql.schema_registry import TABLE_CONSTRAINT_REGISTRY
from amsdal_glue_connections.sql.schema_registry import TABLE_INDEX_REGISTRY
from amsdal_glue_connections.sql.schema_registry import TABLE_PROPERTY_REGISTRY
from amsdal_glue_connections.sql.schema_registry import TABLE_REGISTRY

logger = logging.getLogger(__name__)

# The stdlib sqlite3 driver only binds int/float/str/bytes/None natively. Since `Value` coerces
# typed params to canonical Python objects (Decimal for NUMERIC, uuid.UUID for UUID, date/datetime),
# register adapters so those bind as TEXT (date/datetime default adapters were deprecated in Python
# 3.12). Module-level so it also covers the async (aiosqlite) driver.
sqlite3.register_adapter(Decimal, str)
sqlite3.register_adapter(UUID, str)
sqlite3.register_adapter(_dt.date, _dt.date.isoformat)
# Use the default ISO 'T' separator so every datetime row shares one homogeneous format; a space
# separator (0x20 < 'T' 0x54) would corrupt ORDER BY/range/equality against 'T'-formatted rows.
sqlite3.register_adapter(_dt.datetime, _dt.datetime.isoformat)
# A Python ``list`` reaches the driver as a native list (the generator maps it to a SQL array), which
# sqlite3 cannot bind, so serialise it to JSON text. A ``dict`` needs no adapter: it is JSON by
# construction, so it arrives as a ``JsonValue`` marker and is bound by :func:`bind_params`. Minified
# output is compatible with older spaced rows: every query-time JSON comparison is wrapped in
# ``jsonb()``/``json()`` (see ``lower.rs``), which normalises whitespace, so spaced and minified rows
# compare equal and no migration is needed. (Postgres stays SPACED: psycopg's ``Json``/``Jsonb`` dump
# with spaces.)
#
# ``ensure_ascii`` stays at the stdlib default (TRUE): a non-ASCII string is stored escaped, e.g.
# `['alpha', 'бета']` becomes `["alpha","\u0431\u0435\u0442\u0430"]`. This is deliberate and NOT
# free to change -- `jsonb()`/`json()` normalise whitespace but NOT `\uXXXX` escapes (the escaped
# form does NOT compare equal to the literal UTF-8 one), so flipping the flag would make every
# existing non-ASCII row stop matching EQ against a newly-bound parameter. The cost of keeping it:
# a text match over the WHOLE column (`payload__contains='бета'`, which compares against this raw
# stored text) finds nothing on SQLite while Postgres, storing real UTF-8 in `jsonb`, matches.
# Extraction is unaffected -- `->>`/``json_extract`` unescape -- so nested text matches keep parity.
# See ``NON_ASCII_TEXT_MATCH_CASES`` in ``tests/sql/json_output_type_cases.py``.
_JSON_SEPARATORS = (',', ':')


def _dumps_minified(value: Any) -> str:
    return json.dumps(value, separators=_JSON_SEPARATORS)


sqlite3.register_adapter(list, _dumps_minified)


def bind_params(args: tuple[Any, ...]) -> tuple[Any, ...]:
    """Bind the generator's JSON-typed parameters as JSON text.

    SQLite has no JSON type: a JSON value is TEXT holding JSON, and that is what every JSON function
    and operator expects. ``Value(x, output_type=JSONB)`` therefore serialises here, whatever ``x`` is.

    Scalars compared against a native extraction never reach this path -- the generator has already
    unwrapped them, because `col ->> 'age'` yields INTEGER 36 and would otherwise be compared to TEXT.

    Serialised MINIFIED; ``jsonb()``/``json()`` normalisation at query time keeps older spaced rows
    matching, so no data migration is required.
    """
    return tuple(_dumps_minified(arg.value) if isinstance(arg, JsonValue) else arg for arg in args)


_NORM_ACTION = (
    "CASE {c} WHEN 'CASCADE' THEN 'CASCADE' WHEN 'SET NULL' THEN 'SET_NULL' "
    "WHEN 'SET DEFAULT' THEN 'SET_DEFAULT' WHEN 'RESTRICT' THEN 'RESTRICT' ELSE 'NO_ACTION' END"
)

_REGISTRY_VIEW_SQL: dict[str, str] = {
    TABLE_REGISTRY: (
        f'CREATE TEMPORARY VIEW IF NOT EXISTS "{TABLE_REGISTRY}" AS '  # noqa: S608
        'SELECT name, name AS table_name FROM sqlite_master '
        "WHERE type='table' AND name NOT LIKE 'sqlite_%'"
    ),
    TABLE_PROPERTY_REGISTRY: (
        f'CREATE TEMPORARY VIEW IF NOT EXISTS "{TABLE_PROPERTY_REGISTRY}" AS '  # noqa: S608
        'SELECT m.name AS table_name, p.name AS name, p.type AS type, '
        "CASE WHEN p.\"notnull\" THEN 'NO' ELSE 'YES' END AS is_nullable, "
        'p.dflt_value AS column_default, p.cid AS ordinal_position, '
        'CASE WHEN p.hidden IN (2, 3) THEN 1 ELSE 0 END AS is_generated, '
        'NULL AS collation, NULL AS generation_expression, NULL AS is_identity '
        'FROM sqlite_master m, pragma_table_xinfo(m.name) p '
        "WHERE m.type='table' AND m.name NOT LIKE 'sqlite_%'"
    ),
    TABLE_INDEX_REGISTRY: (
        f'CREATE TEMPORARY VIEW IF NOT EXISTS "{TABLE_INDEX_REGISTRY}" AS '  # noqa: S608
        'SELECT m.name AS table_name, il.name AS name, il."unique" AS is_unique, '
        'ix.name AS column_name, ix.seqno AS ordinal_position, ix."desc" AS is_descending, '
        "'btree' AS index_type "
        'FROM sqlite_master m JOIN pragma_index_list(m.name) il JOIN pragma_index_xinfo(il.name) ix '
        # ``ix.name IS NOT NULL`` drops expression columns; ``ix.key = 1`` drops auxiliary (non-key)
        # columns -- notably a WITHOUT ROWID table's PK columns, which have real names and would
        # otherwise be over-reported as extra index columns.
        "WHERE m.type='table' AND m.name NOT LIKE 'sqlite_%' AND il.origin='c' "
        'AND ix.name IS NOT NULL AND ix.key = 1'
    ),
    TABLE_CONSTRAINT_REGISTRY: (
        # SQLite has no constraint catalog, so approximate one from pragmas. `type` reuses the same
        # single-char codes Postgres exposes via ``pg_constraint.contype`` ('p' primary key,
        # 'u' unique, 'f' foreign key) so the SAME QueryStatement works on both back-ends. Only
        # PK/UNIQUE/FK are representable this way; CHECK/exclusion constraints are out of scope.
        f'CREATE TEMPORARY VIEW IF NOT EXISTS "{TABLE_CONSTRAINT_REGISTRY}" AS '  # noqa: S608
        "SELECT m.name AS table_name, 'pk_' || m.name AS name, 'p' AS type, "
        'p.name AS column_name, p.pk - 1 AS ordinal_position, '
        'NULL AS ref_table, NULL AS ref_column, NULL AS on_update, NULL AS on_delete '
        'FROM sqlite_master m, pragma_table_xinfo(m.name) p '
        "WHERE m.type='table' AND m.name NOT LIKE 'sqlite_%' AND p.pk > 0 "
        'UNION ALL '
        "SELECT m.name, 'fk_' || m.name || '_' || fk.\"id\", 'f', "
        'fk."from", fk.seq, fk."table", fk."to", '
        f'{_NORM_ACTION.format(c="fk.on_update")}, {_NORM_ACTION.format(c="fk.on_delete")} '
        'FROM sqlite_master m, pragma_foreign_key_list(m.name) fk '
        "WHERE m.type='table' AND m.name NOT LIKE 'sqlite_%' "
        'UNION ALL '
        "SELECT m.name, il.name, 'u', ii.name, ii.seqno, NULL, NULL, NULL, NULL "
        'FROM sqlite_master m JOIN pragma_index_list(m.name) il JOIN pragma_index_info(il.name) ii '
        "WHERE m.type='table' AND m.name NOT LIKE 'sqlite_%' AND il.origin='u'"
    ),
}


class SqliteConnectionMixin(SqlConnectionMixinBase):
    # Registry-view DDLs used by ``_ensure_schema_views``. Exposed as an overridable class attribute
    # so a subclass (e.g. a versioned / lakehouse connection) can redefine one or more views -- it is
    # read via ``self`` so the override takes effect.
    _REGISTRY_VIEW_SQL: ClassVar[dict[str, str]] = _REGISTRY_VIEW_SQL

    @staticmethod
    def _map_integrity_error(exc: Exception) -> None:
        """Translate a recognised SQLite ``IntegrityError`` into the typed glue error.

        Raises the matching :class:`UniqueViolationError` / :class:`ForeignKeyViolationError`; returns
        (so the caller falls through to a generic ``ConnectionError``) for anything unrecognised.
        Shared by the sync and async ``execute`` implementations.
        """
        text = str(exc)
        if 'UNIQUE constraint failed' in text:
            raise UniqueViolationError(text) from exc
        if 'FOREIGN KEY constraint failed' in text:
            raise ForeignKeyViolationError(text) from exc
