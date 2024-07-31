from dataclasses import dataclass
from typing import TYPE_CHECKING

from amsdal_glue_core.common.data_models.conditions import Conditions

if TYPE_CHECKING:
    from amsdal_glue_core.common.data_models.schema import SchemaReference


@dataclass(kw_only=True)
class BaseConstraint:
    """Represents a base constraint.

    Attributes:
        name (str): The name of the constraint.
    """

    name: str


@dataclass(kw_only=True)
class PrimaryKeyConstraint(BaseConstraint):
    """Represents a primary key constraint.

    Attributes:
        fields (list[str]): The list of fields that make up the primary key.
    """

    fields: list[str]


@dataclass(kw_only=True)
class ForeignKeyConstraint(BaseConstraint):
    """Represents a foreign key constraint.

    Attributes:
        fields (list[str]): The list of fields that make up the foreign key.
        reference_schema (SchemaReference): The schema that the foreign key references.
        reference_fields (list[str]): The list of fields in the referenced schema.
    """

    fields: list[str]
    reference_schema: 'SchemaReference'
    reference_fields: list[str]


@dataclass(kw_only=True)
class UniqueConstraint(BaseConstraint):
    """Represents a unique constraint.

    Attributes:
        fields (list[str]): The list of fields that must be unique.
        condition (Conditions | None): The condition under which the constraint applies. Defaults to None.
    """

    fields: list[str]
    condition: Conditions | None = None


@dataclass(kw_only=True)
class CheckConstraint(BaseConstraint):
    """Represents a check constraint.

    Attributes:
        condition (Conditions): The condition that must be met for the constraint to be satisfied.
    """

    condition: Conditions
