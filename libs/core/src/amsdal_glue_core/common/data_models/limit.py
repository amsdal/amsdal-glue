from dataclasses import dataclass


@dataclass(kw_only=True)
class LimitQuery:
    """Represents a LIMIT query.

    Attributes:
        limit (int): The maximum number of records to return.
        offset (int): The number of records to skip before starting to return records. Defaults to 0.
    """

    limit: int
    offset: int = 0
