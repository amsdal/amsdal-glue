from dataclasses import dataclass
from typing import Optional
from typing import TYPE_CHECKING

from amsdal_glue_core.common.expressions.common import Combinable

if TYPE_CHECKING:
    from amsdal_glue_core.common.expressions.field_reference import FieldReferenceExpression


@dataclass(kw_only=True)
class Field:
    name: str
    child: Optional['Field'] = None

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

    def __hash__(self) -> int:
        return hash(repr(self))


@dataclass(kw_only=True)
class FieldReference(Combinable):
    field: Field
    table_name: str
    namespace: str | None = None

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
