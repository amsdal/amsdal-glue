import copy
from dataclasses import dataclass
from typing import Any

from amsdal_glue_core.common.data_models.output_type import OutputType


@dataclass(kw_only=True)
class BaseExpression:
    output_type: type[Any] | OutputType | None = None

    def copy(self) -> 'BaseExpression':
        return copy.copy(self)
