from dataclasses import dataclass

from amsdal_glue_core.common.data_models.conditions import Conditions


@dataclass(kw_only=True)
class IndexSchema:
    """Represents an index schema.

    Attributes:
        name (str): The name of the index.
        fields (list[str]): The list of fields included in the index.
        condition (Conditions | None): The condition under which the index applies. Defaults to None.
    """

    name: str
    fields: list[str]
    condition: Conditions | None = None
