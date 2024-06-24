from dataclasses import dataclass
from typing import Any

from amsdal_glue_core.common.data_models.metadata import Metadata


@dataclass(kw_only=True)
class Data:
    data: dict[str, Any]
    metadata: Metadata | None = None
