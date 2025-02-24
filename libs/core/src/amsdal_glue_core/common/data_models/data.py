from dataclasses import dataclass
from typing import Any


@dataclass(kw_only=True)
class Data:
    """Represents a data entity.

    Attributes:
        data (dict[str, Any]): The actual data stored in a dictionary format.
        metadata (dict[str, Any] | None): Optional metadata associated with the data. Defaults to None.
    """

    data: dict[str, Any]
    metadata: dict[str, Any] | None = None

    def __copy__(self):
        return Data(data=self.data.copy(), metadata=self.metadata.copy() if self.metadata else None)
