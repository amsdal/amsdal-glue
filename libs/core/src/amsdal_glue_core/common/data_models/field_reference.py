from dataclasses import dataclass
from typing import Optional
from typing import TYPE_CHECKING

from amsdal_glue_core.common.expressions.common import Combinable

if TYPE_CHECKING:
    from amsdal_glue_core.common.expressions.field_reference import FieldReferenceExpression


@dataclass(kw_only=True)
class Field:
    """Represents a field in a schema.

    Attributes:
        name (str): The name of the field.
        child (Optional[Field]): The child field, if any. Defaults to None.
        parent (Optional[Field]): The parent field, if any. Defaults to None.
    """

    name: str
    child: Optional['Field'] = None
    parent: Optional['Field'] = None

    def __repr__(self) -> str:
        root = self
        fields = [self.name]

        while root.child:
            root = root.child
            fields.append(root.name)

        return '__'.join(fields)

    def __eq__(self, other) -> bool:
        if not isinstance(other, Field):
            return False

        return self.name == other.name and repr(self) == repr(other)


@dataclass(kw_only=True)
class FieldReference(Combinable):
    """Represents a reference to a field in a table.

    This class provides a reference to a field within a specific table,
    including the namespace of the field. It extends from `Combinable` to
    support combinable operations on field references.

    Attributes:
        field (Field): The field being referenced.
        table_name (str): The name of the table containing the field.
        namespace (str): The namespace of the field. Defaults to an empty string.

    Example:
        ```python
        from amsdal_glue_core.common.data_models.field_reference import Field, FieldReference

        field = Field(name='age')
        field_ref = FieldReference(field=field, table_name='users')

        # Example of combining field references
        combined_expr = field_ref + 10  # Represents users.age + 10
        ```
    """

    field: Field
    table_name: str
    namespace: str = ''

    def to_expression(self) -> 'FieldReferenceExpression':
        from amsdal_glue_core.common.expressions.field_reference import FieldReferenceExpression

        return FieldReferenceExpression(field_reference=self)

    def __repr__(self) -> str:
        if self.namespace:
            return f'{self.namespace}.{self.table_name}.{self.field!r}'
        return f'{self.table_name}.{self.field!r}'

    def __hash__(self) -> int:
        return hash(repr(self))

    def __eq__(self, other) -> bool:
        if not isinstance(other, FieldReference):
            return False

        return self.namespace == other.namespace and self.table_name == other.table_name and self.field == other.field


@dataclass(kw_only=True)
class FieldReferenceAliased(FieldReference):
    """Represents a reference to a field in a table with an alias.

    Attributes:
        alias (str): The alias for the field reference.
    """

    alias: str

    def to_expression(self) -> 'FieldReferenceExpression':
        from amsdal_glue_core.common.expressions.field_reference import FieldReferenceExpression

        return FieldReferenceExpression(
            field_reference=FieldReference(
                field=self.field,
                table_name=self.table_name,
                namespace=self.namespace,
            ),
        )
