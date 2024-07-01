from dataclasses import dataclass
from typing import TYPE_CHECKING

from amsdal_glue_core.common.data_models.conditions import Conditions

if TYPE_CHECKING:
    from amsdal_glue_core.common.data_models.schema import SchemaReference


@dataclass(kw_only=True)
class BaseConstraint:
    name: str


@dataclass(kw_only=True)
class PrimaryKeyConstraint(BaseConstraint):
    fields: list[str]


@dataclass(kw_only=True)
class ForeignKeySchema(BaseConstraint):
    fields: list[str]
    reference_schema: 'SchemaReference'
    reference_fields: list[str]


@dataclass(kw_only=True)
class UniqueConstraint(BaseConstraint):
    fields: list[str]
    condition: Conditions | None = None


@dataclass(kw_only=True)
class CheckConstraint(BaseConstraint):
    condition: Conditions
