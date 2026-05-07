"""Tests for amsdal_glue_core.common.exceptions.

UniqueViolationError signals that a write violated a UNIQUE constraint at the
database level. Connection implementations raise it from `execute()` so callers
can distinguish constraint violations from generic connection failures without
parsing backend-specific error messages themselves.
"""

from amsdal_glue_core.common.exceptions import AmsdalGlueError
from amsdal_glue_core.common.exceptions import UniqueViolationError


def test_amsdal_glue_error_is_a_python_exception():
    assert issubclass(AmsdalGlueError, Exception)


def test_unique_violation_inherits_amsdal_glue_error():
    assert issubclass(UniqueViolationError, AmsdalGlueError)


def test_unique_violation_carries_message():
    msg = 'UNIQUE constraint failed: users.email'
    exc = UniqueViolationError(msg)
    assert str(exc) == msg


def test_unique_violation_can_be_raised_and_caught_as_amsdal_glue_error():
    msg = 'boom'
    try:
        raise UniqueViolationError(msg)
    except AmsdalGlueError as exc:
        assert str(exc) == msg
