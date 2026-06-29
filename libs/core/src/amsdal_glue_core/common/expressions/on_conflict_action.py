from amsdal_glue_core.common.expressions.expression import Expression


class OnConflictAction(Expression):
    """Marker expression for per-row INSERT/UPDATE detection in UPSERT RETURNING.

    PostgreSQL: rendered as (xmax = 0)
    SQLite: triggers pre-SELECT emulation in connection adapter
    """
