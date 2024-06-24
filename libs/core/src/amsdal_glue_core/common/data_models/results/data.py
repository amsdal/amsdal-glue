from dataclasses import dataclass
from typing import Any

from amsdal_glue_core.common.data_models.data import Data
from amsdal_glue_core.common.data_models.results.base import ResultBase


@dataclass(kw_only=True)
class DataResult(ResultBase):
    data: list[Data] | None = None


@dataclass(kw_only=True)
class LockResult(ResultBase):
    result: Any = None


@dataclass(kw_only=True)
class TransactionResult(ResultBase):
    result: Any = None
