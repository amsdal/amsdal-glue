from dataclasses import dataclass
from typing import Optional


@dataclass(kw_only=True)
class Field:
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
    field: Field
    table_name: str

    def __repr__(self) -> str:
        return f'{self.table_name}.{self.field!r}'


@dataclass(kw_only=True)
class FieldReferenceAliased(FieldReference):
    alias: str
