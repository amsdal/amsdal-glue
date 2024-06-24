from dataclasses import dataclass


@dataclass(kw_only=True)
class ResultBase:
    success: bool
    message: str | None = None
    exception: Exception | None = None
