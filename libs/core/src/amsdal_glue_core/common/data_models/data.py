from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from amsdal_glue_core.common.expressions.expression import Expression


@dataclass(kw_only=True)
class Data:
    """A row on the way OUT: what a query returns.

    Values are plain Python objects. The row a mutation WRITES is :class:`DataInput`, whose values are
    expressions -- that is what lets a caller declare a value's SQL type (e.g.
    ``Value(x, output_type=ScalarType.JSONB)``).

    Attributes:
        data (dict[str, Any]): The actual data stored in a dictionary format.
        metadata (dict[str, Any] | None): Optional metadata associated with the data. Defaults to None.
    """

    data: dict[str, Any]
    metadata: dict[str, Any] | None = None

    def __copy__(self):
        return Data(data=self.data.copy(), metadata=self.metadata.copy() if self.metadata else None)


class DataInput:
    """A row on the way IN: what an ``InsertData`` / ``UpdateData`` writes.

    Values are expressions, not plain Python objects, so a caller can say what a value *is*:
    ``Value(x, output_type=ScalarType.JSONB)`` binds ``x`` as JSON whatever ``x`` happens to be, and a
    ``Func`` / ``Combined`` computes the value in SQL. A raw Python value has no room to carry that --
    which is why a bare scalar could never be written to a JSON column before this type existed.

    The constructor still ACCEPTS a plain value and wraps it in a ``Value``, so
    ``DataInput(data={'id': 1})`` reads exactly like the old ``Data(data={'id': 1})``. That is the
    reason this is not a plain dataclass: what may be passed in is wider than what is stored, and once
    constructed every value IS an ``Expression`` -- consumers can rely on it.

    ``metadata`` is the ROW's metadata (its primary-key fields, its foreign keys), and is deliberately
    NOT the same thing as ``DataMutation.metadata``, which describes the mutation itself. During a
    historical table migration the row carries the OLD schema's metadata while the mutation targets the
    NEW schema, so both levels are needed and neither can stand in for the other.
    """

    __slots__ = ('data', 'metadata')

    data: 'dict[str, Expression]'
    metadata: dict[str, Any] | None

    def __init__(
        self,
        *,
        data: Mapping[str, Any],
        metadata: dict[str, Any] | None = None,
    ) -> None:
        from amsdal_glue_core.common.expressions.expression import Expression
        from amsdal_glue_core.common.expressions.value import Value

        self.data = {name: value if isinstance(value, Expression) else Value(value) for name, value in data.items()}
        self.metadata = metadata

    def __repr__(self) -> str:
        return f'DataInput(data={self.data!r}, metadata={self.metadata!r})'

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, DataInput):
            return NotImplemented

        return self.data == other.data and self.metadata == other.metadata

    # A row is mutable, so it is not hashable -- the same choice ``@dataclass`` makes for ``Data``.
    __hash__ = None  # type: ignore[assignment]

    def __copy__(self) -> 'DataInput':
        return DataInput(data=self.data.copy(), metadata=self.metadata.copy() if self.metadata else None)

    def literals(self) -> dict[str, Any]:
        """The row's values as plain Python objects.

        For a back-end with no SQL to evaluate -- a CSV file, an Elasticsearch document -- a value must
        be a literal. Anything else (a ``Func``, a ``Combined``, a ``FieldReference``) describes a
        computation only a database can perform, so it is rejected here rather than silently written out
        as an expression object.
        """
        from amsdal_glue_core.common.expressions.value import Value

        literals: dict[str, Any] = {}

        for name, expression in self.data.items():
            if not isinstance(expression, Value):
                msg = (
                    f'Cannot write field {name!r}: {type(expression).__name__} is a SQL expression, and '
                    f'this connection has no SQL engine to evaluate it. Pass a literal Value instead.'
                )
                raise TypeError(msg)

            literals[name] = expression.value

        return literals
