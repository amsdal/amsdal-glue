from dataclasses import dataclass


@dataclass(kw_only=True)
class LimitQuery:
    limit: int
    offset: int = 0
