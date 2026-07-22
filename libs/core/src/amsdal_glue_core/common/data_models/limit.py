from dataclasses import dataclass


@dataclass(kw_only=True)
class LimitQuery:
    """Represents a LIMIT query.

    Attributes:
        limit (int): The maximum number of records to return.
        offset (int): The number of records to skip before starting to return records. Defaults to 0.
        with_ties (bool): When True, emit FETCH FIRST … WITH TIES instead of LIMIT. Defaults to False.
    """

    limit: int
    offset: int = 0
    with_ties: bool = False
