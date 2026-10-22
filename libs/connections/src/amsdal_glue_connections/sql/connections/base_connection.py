"""Shared base mixin for the SQL dialect connection mixins.

`build_data`, the `_queries` / `_queries_params` capture buffers and their read-only properties are
identical across the Postgres and SQLite connection mixins, so they live here once and both dialect
mixins inherit them. Kept as a plain base (no cooperative ``super().__init__``) to preserve the exact
initialisation order of the existing connections.
"""

from __future__ import annotations

import contextlib
import json
from typing import Any
from typing import TYPE_CHECKING

from amsdal_glue_core.common.data_models.data import Data

if TYPE_CHECKING:
    from collections.abc import Container


class SqlConnectionMixinBase:
    """Query-capture buffers and `build_data`, shared by every SQL dialect connection mixin."""

    def __init__(self) -> None:
        self._queries: list[str] = []
        self._queries_params: list[tuple[Any, ...]] = []

    @staticmethod
    def build_data(data: dict[str, Any], text_columns: Container[str] = ()) -> Data:
        """
        Builds a Data object from a dictionary.

        A string that looks like a JSON object or array (`{...}` / `[...]`) is decoded: SQLite keeps JSON as text and
        a pgvector value arrives as `'[0.1, ...]'`. Two exceptions keep the string as read:

        - a column in `text_columns` - its declared type is a string type, so its value is text, whatever it looks
          like (source code such as `{ x: 1 }`, or text that happens to be valid JSON);
        - a value that does not parse - it was never JSON, and one such value must not fail the whole query.

        Args:
            data (dict[str, Any]): The data dictionary.
            text_columns (Container[str]): Columns declared with a string type, never decoded.

        Returns:
            Data: The built Data object.
        """
        for key, value in data.items():
            if key in text_columns or not isinstance(value, str):
                continue
            if (value.startswith('{') and value.endswith('}')) or (value.startswith('[') and value.endswith(']')):
                with contextlib.suppress(json.JSONDecodeError):
                    data[key] = json.loads(value)
        return Data(data=data)

    @property
    def queries(self) -> list[str]:
        """
        Returns the queries executed on this connection.

        Returns:
            list[str]: The queries executed.
        """
        return self._queries

    @property
    def queries_params(self) -> list[tuple[Any, ...]]:
        """
        Returns the parameters bound to each captured query, aligned by index with ``queries``.

        Returns:
            list[tuple[Any, ...]]: The query parameters, in the same order as ``queries``.
        """
        return self._queries_params
