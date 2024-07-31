from dataclasses import dataclass
from typing import Optional


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


@dataclass(kw_only=True)
class FieldReference:
    """Represents a reference to a field in a table.

    Attributes:
        field (Field): The field being referenced.
        table_name (str): The name of the table containing the field.
        namespace (str): The namespace of the field. Defaults to an empty string.
    """

    field: Field
    table_name: str
    namespace: str = ''

    def __repr__(self) -> str:
        return f'{self.table_name}.{self.field!r}'


@dataclass(kw_only=True)
class FieldReferenceAliased(FieldReference):
    """Represents a reference to a field in a table with an alias.

    Attributes:
        alias (str): The alias for the field reference.
    """

    alias: str
