from __future__ import annotations

from typing import TYPE_CHECKING

from amsdal_glue_connections.sql.parsers.default import parser
from amsdal_glue_connections.sql.parsers.default import pg_mapper
from amsdal_glue_connections.sql.parsers.default import sqlite_mapper

if TYPE_CHECKING:
    from amsdal_glue_core.common.data_models.types import FieldType
    from amsdal_glue_core.common.expressions.expression import Expression


def parse_pg_default(raw: str | None) -> Expression | None:
    if raw is None:
        return None

    # Serial/sequence defaults are handled separately
    if raw.startswith('nextval('):
        return None

    node = parser.parse(raw)
    return pg_mapper.map_node(node)


def parse_sqlite_default(raw: str | None, field_type: FieldType | None = None) -> Expression | None:
    if raw is None:
        return None

    node = parser.parse(raw)
    return sqlite_mapper.map_node(node, field_type)
