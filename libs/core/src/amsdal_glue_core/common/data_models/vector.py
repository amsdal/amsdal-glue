from dataclasses import dataclass


@dataclass(kw_only=True)
class Vector:
    """Represents a vector.

    Attributes:
        values (list[float | int]): The values of the vector.
    """

    values: list[float | int]

    def __str__(self) -> str:
        return str(self.values)
