from dataclasses import dataclass


@dataclass
class OutputType:
    type_name: str

    def __str__(self) -> str:
        return self.type_name
