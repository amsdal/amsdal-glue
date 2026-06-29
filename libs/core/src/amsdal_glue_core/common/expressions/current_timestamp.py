from __future__ import annotations

from dataclasses import dataclass

from amsdal_glue_core.common.expressions.expression import Expression


@dataclass(kw_only=True)
class CurrentTimestamp(Expression):
    """SQL CURRENT_TIMESTAMP keyword (rendered without parentheses)."""


@dataclass(kw_only=True)
class CurrentDate(Expression):
    """SQL CURRENT_DATE keyword (rendered without parentheses)."""


@dataclass(kw_only=True)
class CurrentTime(Expression):
    """SQL CURRENT_TIME keyword (rendered without parentheses)."""
