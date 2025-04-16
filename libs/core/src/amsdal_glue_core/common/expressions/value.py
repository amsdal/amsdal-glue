from dataclasses import dataclass
from datetime import date
from datetime import datetime
from typing import Any

from amsdal_glue_core.common.expressions.expression import Expression


@dataclass(kw_only=True)
class Value(Expression):
    """Represents a value expression.

    Attributes:
        value (Any): The value of the expression.
    """

    value: Any

    def __init__(self, value: Any, output_type: type[Any] | None = None) -> None:
        super().__init__(output_type=output_type)
        self.value = value

    def __repr__(self) -> str:
        if self.output_type in (date, datetime):
            _value = self.value

            if isinstance(_value, datetime):
                _value = _value.date().isoformat()
            elif isinstance(_value, date):
                _value = _value.isoformat()

            if self.output_type is date:
                return f'DATE {_value!r}'
            return f'TIMESTAMP {_value!r}'
        return repr(self.value)

    def __hash__(self):
        return hash(self.value)
