"""The cross-dialect portability contract for registry views.

``EXPECTED_COLUMNS`` pins the canonical column set each registry view must
expose on every dialect, so a caller's ``QueryStatement`` filtering on these
columns works unchanged on either SQLite or Postgres. This module is
fixture-free (no DB access) so it can be imported from both dialects'
integration test suites without pulling in either fixture.
"""

from amsdal_glue_connections.sql.schema_registry import TABLE_CONSTRAINT_REGISTRY
from amsdal_glue_connections.sql.schema_registry import TABLE_INDEX_REGISTRY
from amsdal_glue_connections.sql.schema_registry import TABLE_PROPERTY_REGISTRY
from amsdal_glue_connections.sql.schema_registry import TABLE_REGISTRY

EXPECTED_COLUMNS: dict[str, set[str]] = {
    TABLE_REGISTRY: {'name', 'table_name'},
    TABLE_PROPERTY_REGISTRY: {
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
    },
    TABLE_INDEX_REGISTRY: {
        'table_name',
        'name',
        'is_unique',
        'column_name',
        'ordinal_position',
        'is_descending',
        'index_type',
    },
    TABLE_CONSTRAINT_REGISTRY: {
        'table_name',
        'name',
        'type',
        'column_name',
        'ordinal_position',
        'ref_table',
        'ref_column',
        'on_update',
        'on_delete',
    },
}


def _view_columns(connection, view: str) -> set[str]:
    cur = connection.execute(f'SELECT * FROM "{view}" LIMIT 0')  # noqa: S608
    names = {d[0] for d in cur.description}
    cur.close()
    return names
