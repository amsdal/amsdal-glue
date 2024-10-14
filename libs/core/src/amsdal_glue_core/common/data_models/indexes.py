from copy import copy
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

    def __ne__(self, other):
        return not self.__eq__(other)

    def __eq__(self, other):
        if not isinstance(other, IndexSchema):
            return False

        return self.name == other.name and self.fields == other.fields and self.condition == other.condition

    def __repr__(self):
        return f'IndexSchema<{self.name}:{self.fields}:{self.condition}>'

    def __copy__(self):
        return IndexSchema(
            name=self.name,
            fields=copy(self.fields),
            condition=copy(self.condition) if self.condition is not None else None,
        )
