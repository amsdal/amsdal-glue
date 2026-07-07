from copy import copy
from dataclasses import dataclass
from typing import TYPE_CHECKING

from amsdal_glue_core.common.data_models.conditions import Conditions
from amsdal_glue_core.common.enums import ReferentialAction

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

    def __hash__(self) -> int:
        return hash((self.name, self.fields))


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
    on_delete: ReferentialAction = ReferentialAction.NO_ACTION
    on_update: ReferentialAction = ReferentialAction.NO_ACTION

    def __ne__(self, other):
        return not self.__eq__(other)

    def __eq__(self, other):
        if not isinstance(other, ForeignKeyConstraint):
            return False

        return (
            self.name == other.name
            and self.fields == other.fields
            and self.reference_schema.name == other.reference_schema.name
            and self.reference_fields == other.reference_fields
            and self.on_delete == other.on_delete
            and self.on_update == other.on_update
        )

    def __copy__(self):
        return ForeignKeyConstraint(
            name=self.name,
            fields=copy(self.fields),
            reference_schema=copy(self.reference_schema),
            reference_fields=copy(self.reference_fields),
            on_delete=self.on_delete,
            on_update=self.on_update,
        )

    def __hash__(self) -> int:
        return hash((self.name, self.fields, self.reference_schema, self.reference_fields))


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

    def __hash__(self) -> int:
        return hash((self.name, self.fields, self.condition))


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

    def __hash__(self) -> int:
        return hash((self.name, self.condition))


@dataclass(kw_only=True)
class ExclusionElement:
    """Represents a single element of an exclusion constraint.

    Attributes:
        field (str): The field (or expression) the exclusion applies to.
        operator (str): The operator used for the exclusion, e.g. '=', '&&', '<>'.
    """

    field: str
    operator: str  # '=', '&&', '<>', etc.


@dataclass(kw_only=True)
class ExclusionConstraint(BaseConstraint):
    """Represents an exclusion constraint.

    Attributes:
        elements (list[ExclusionElement]): The elements that make up the exclusion constraint.
        index_method (str): The index method used to enforce the constraint. Defaults to 'gist'.
        condition (Conditions | None): The condition under which the constraint applies. Defaults to None.
    """

    elements: list[ExclusionElement]
    index_method: str = 'gist'
    condition: Conditions | None = None

    def __ne__(self, other):
        return not self.__eq__(other)

    def __eq__(self, other):
        if not isinstance(other, ExclusionConstraint):
            return False

        return (
            self.name == other.name
            and self.elements == other.elements
            and self.index_method == other.index_method
            and self.condition == other.condition
        )

    def __copy__(self):
        return ExclusionConstraint(
            name=self.name,
            elements=copy(self.elements),
            index_method=self.index_method,
            condition=copy(self.condition),
        )

    def __hash__(self) -> int:
        return hash((self.name, tuple((e.field, e.operator) for e in self.elements), self.index_method, self.condition))
