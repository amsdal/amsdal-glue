from __future__ import annotations

from amsdal_glue_core.common.expressions.func import Func


class Now(Func):
    """Database-native now() function.

    PostgreSQL: now()
    SQLite: datetime('now')
    """

    def __init__(self) -> None:
        super().__init__(name='now', args=[])
