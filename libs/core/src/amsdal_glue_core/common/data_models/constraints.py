from copy import copy
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

    def __repr__(self):
        return f'BaseConstraint<{self.name}>'


@dataclass(kw_only=True)
class PrimaryKeyConstraint(BaseConstraint):
    """Represents a primary key constraint.

    Attributes:
        fields (list[str]): The list of fields that make up the primary key.
    """

    fields: list[str]

    def __ne__(self, other):
        return not self.__eq__(other)

    def __eq__(self, other):
        if not isinstance(other, PrimaryKeyConstraint):
            return False

        return self.name == other.name and self.fields == other.fields

    def __copy__(self):
        return PrimaryKeyConstraint(
            name=self.name,
            fields=copy(self.fields),
        )


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

    def __ne__(self, other):
        return not self.__eq__(other)

    def __eq__(self, other):
        if not isinstance(other, ForeignKeyConstraint):
            return False

        return (
            self.name == other.name
            and self.fields == other.fields
            and self.reference_schema == other.reference_schema
            and self.reference_fields == other.reference_fields
        )

    def __copy__(self):
        return ForeignKeyConstraint(
            name=self.name,
            fields=copy(self.fields),
            reference_schema=copy(self.reference_schema),
            reference_fields=copy(self.reference_fields),
        )


@dataclass(kw_only=True)
class UniqueConstraint(BaseConstraint):
    """Represents a unique constraint.

    Attributes:
        fields (list[str]): The list of fields that must be unique.
        condition (Conditions | None): The condition under which the constraint applies. Defaults to None.
    """

    fields: list[str]
    condition: Conditions | None = None

    def __ne__(self, other):
        return not self.__eq__(other)

    def __eq__(self, other):
        if not isinstance(other, UniqueConstraint):
            return False

        return self.name == other.name and self.fields == other.fields and self.condition == other.condition

    def __copy__(self):
        return UniqueConstraint(
            name=self.name,
            fields=copy(self.fields),
            condition=copy(self.condition),
        )


@dataclass(kw_only=True)
class CheckConstraint(BaseConstraint):
    """Represents a check constraint.

    Attributes:
        condition (Conditions): The condition that must be met for the constraint to be satisfied.
    """

    condition: Conditions

    def __ne__(self, other):
        return not self.__eq__(other)

    def __eq__(self, other):
        if not isinstance(other, CheckConstraint):
            return False

        return self.name == other.name and self.condition == other.condition

    def __copy__(self):
        return CheckConstraint(
            name=self.name,
            condition=copy(self.condition),
        )
