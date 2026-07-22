from dataclasses import dataclass
from dataclasses import field
from typing import Any

from amsdal_glue_core.common.enums import ScalarType


@dataclass(frozen=True)
class JsonValue:
    """A parameter the generator has typed as JSON/JSONB, for the connection to bind.

    The generator cannot build the driver-specific wrapper itself: ``psycopg.types.json.Jsonb`` is a
    psycopg object, and SQLite has no JSON type at all. So a JSON-typed parameter crosses the Rust
    boundary as this dialect-neutral marker, and each connection binds it its own way -- psycopg wraps
    it in ``Jsonb``/``Json``, SQLite serialises it with ``json.dumps``.

    ``value`` holds the raw Python object, so ``JsonValue(None)`` is a JSON ``null`` -- distinct from
    a plain ``Value(None)``, which is SQL ``NULL``.
    """

    value: Any
    scalar_type: ScalarType = field(default=ScalarType.JSONB)
