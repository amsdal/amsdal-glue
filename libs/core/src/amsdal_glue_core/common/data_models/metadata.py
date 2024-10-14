from dataclasses import dataclass


@dataclass(kw_only=True)
class Metadata:
    """Represents metadata for an object.

    Attributes:
        object_id (str): The unique identifier for the object.
        object_version (str | None): The version of the object. Defaults to None.
        created_at (str | None): The creation timestamp of the object. Defaults to None.
        updated_at (str | None): The last updated timestamp of the object. Defaults to None.
    """

    object_id: str
    object_version: str | None = None
    created_at: str | None = None
    updated_at: str | None = None

    def __copy__(self):
        return Metadata(
            object_id=self.object_id,
            object_version=self.object_version,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

    def copy(self) -> 'Metadata':
        return self.__copy__()
