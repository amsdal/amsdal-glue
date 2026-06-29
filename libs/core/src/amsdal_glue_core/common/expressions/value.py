from __future__ import annotations

from dataclasses import dataclass
from typing import Any
from typing import TYPE_CHECKING

from amsdal_glue_core.common.expressions.expression import Expression

if TYPE_CHECKING:
    from amsdal_glue_core.common.data_models.types import FieldType


@dataclass(kw_only=True)
class Value(Expression):
    value: Any

    def __init__(self, value: Any, output_type: FieldType | None = None) -> None:
        super().__init__(output_type=output_type)
        self.value = value

    def __repr__(self) -> str:
        from amsdal_glue_core.common.enums import ScalarType

        if self.output_type == ScalarType.DATE:
            from datetime import date

            _value = self.value
            if isinstance(_value, date):
                _value = _value.isoformat()
            return f'DATE {_value!r}'

        if self.output_type == ScalarType.TIMESTAMP:
            from datetime import date
            from datetime import datetime

            _value = self.value
            if isinstance(_value, datetime):
                _value = _value.date().isoformat()
            elif isinstance(_value, date):
                _value = _value.isoformat()
            return f'TIMESTAMP {_value!r}'

        return repr(self.value)

    def __hash__(self):
        return hash(self.value)
