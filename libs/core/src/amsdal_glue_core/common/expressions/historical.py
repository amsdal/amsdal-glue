from __future__ import annotations

from typing import TYPE_CHECKING

from amsdal_glue_core.common.expressions.expression import Expression

if TYPE_CHECKING:
    from amsdal_glue_core.common.data_models.types import FieldType


class HistoricalField:
    """Known historical meta-field names.

    Use these constants with HistoricalFieldExpression — never string literals.
    Each historical driver maps these to its own physical columns.
    """

    IS_LATEST = 'is_latest'
    IS_DELETED = 'is_deleted'
    OP = 'op'
    TXN_ID = 'txn_id'
    TIMESTAMP = 'timestamp'
    SCHEMA_VERSION = 'schema_version'
    VERSION = 'version'


class HistoricalFieldExpression(Expression):
    """Reference to a historical meta-field.

    Used in Condition to filter by historical metadata. Driver transforms
    this into driver-specific physical column or JOIN.

    Always use HistoricalField constants for the name parameter::

        HistoricalFieldExpression(name=HistoricalField.IS_LATEST)
        HistoricalFieldExpression(name=HistoricalField.OP)
    """

    def __init__(self, name: str, output_type: FieldType | None = None) -> None:
        super().__init__(output_type=output_type)
        self.name = name

    def __repr__(self) -> str:
        return f'H({self.name!r})'
