from dataclasses import dataclass
from typing import Any

from amsdal_glue_core.common.data_models.data import Data
from amsdal_glue_core.common.data_models.results.base import ResultBase


@dataclass(kw_only=True)
class DataResult(ResultBase):
    """Represents the result of a data query operation.

    Attributes:
        success (bool): Indicates whether the operation was successful.
        message (str | None): Optional message providing additional information about the result.
        exception (Exception | None): Optional exception that was raised during the operation, if any.
        data (list[Data] | None): The data returned by the query operation, if any.
    """

    data: list[Data] | None = None


@dataclass(kw_only=True)
class LockResult(ResultBase):
    """Represents the result of a lock operation.

    Attributes:
        success (bool): Indicates whether the operation was successful.
        message (str | None): Optional message providing additional information about the result.
        exception (Exception | None): Optional exception that was raised during the operation, if any.
        result (Any): The result of the lock operation, if any.
    """

    result: Any = None


@dataclass(kw_only=True)
class TransactionResult(ResultBase):
    """Represents the result of a transaction operation.

    Attributes:
        success (bool): Indicates whether the operation was successful.
        message (str | None): Optional message providing additional information about the result.
        exception (Exception | None): Optional exception that was raised during the operation, if any.
        result (Any): The result of the transaction operation, if any.
    """

    result: Any = None
