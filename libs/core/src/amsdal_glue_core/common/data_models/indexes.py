from dataclasses import dataclass

from amsdal_glue_core.common.data_models.conditions import Conditions


@dataclass(kw_only=True)
class IndexSchema:
    name: str
    fields: list[str]
    condition: Conditions | None = None
