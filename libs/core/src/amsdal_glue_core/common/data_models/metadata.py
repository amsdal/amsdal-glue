from dataclasses import dataclass


@dataclass(kw_only=True)
class Metadata:
    object_id: str
    object_version: str | None
    created_at: str | None
    updated_at: str | None
