class AmsdalGlueError(Exception):
    """Base exception for all amsdal-glue errors."""


class UniqueViolationError(AmsdalGlueError):
    """Raised when a write violates a UNIQUE constraint at the database level.

    Connection implementations translate backend-specific exceptions
    (sqlite3.IntegrityError with 'UNIQUE constraint failed', psycopg's
    UniqueViolation, etc.) into this typed exception so callers can detect
    and handle the situation without inspecting backend internals.
    """
