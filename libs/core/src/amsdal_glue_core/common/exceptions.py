class AmsdalGlueError(Exception):
    """Base exception for all amsdal-glue errors."""


class UniqueViolationError(AmsdalGlueError):
    """Raised when a write violates a UNIQUE constraint at the database level.

    Connection implementations translate backend-specific exceptions
    (sqlite3.IntegrityError with 'UNIQUE constraint failed', psycopg's
    UniqueViolation, etc.) into this typed exception so callers can detect
    and handle the situation without inspecting backend internals.
    """


class ForeignKeyViolationError(AmsdalGlueError):
    """Raised when a write violates a FOREIGN KEY constraint at the database level.

    Connection implementations translate backend-specific exceptions
    (sqlite3.IntegrityError with 'FOREIGN KEY constraint failed', psycopg's
    ForeignKeyViolation, etc.) into this typed exception so callers can detect
    and handle the situation without inspecting backend internals. The canonical
    case is deleting a row that is still referenced by another table.
    """
