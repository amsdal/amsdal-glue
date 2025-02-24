from dataclasses import dataclass

from amsdal_glue_core.common.data_models.field_reference import FieldReference


@dataclass(kw_only=True)
class GroupByQuery:
    """Represents a GROUP BY query.

    Attributes:
        field (FieldReference): The field to group by.
    """

    field: FieldReference

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, GroupByQuery):
            return False

        return self.field == other.field
