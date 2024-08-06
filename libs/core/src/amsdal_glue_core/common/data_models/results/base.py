from dataclasses import dataclass


@dataclass(kw_only=True)
class ResultBase:
    """Base class for representing the result of an operation.

    Attributes:
        success (bool): Indicates whether the operation was successful.
        message (str | None): Optional message providing additional information about the result.
        exception (Exception | None): Optional exception that was raised during the operation, if any.
    """

    success: bool
    message: str | None = None
    exception: Exception | None = None
