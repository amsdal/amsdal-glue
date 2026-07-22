"""JSON parameters bind as MINIFIED text.

Bare ``json.dumps`` produces spaced text (``{"a": 1}``). This binds the canonical minified form
(``{"a":1}``), written through ``json(?)``. Whole-column comparisons normalise both sides with
``jsonb()`` anyway, so old spaced rows still match; minifying merely stops NEW writes from carrying
redundant whitespace.
"""

import json
import sqlite3

from amsdal_glue_core.common.data_models.json_value import JsonValue
from amsdal_glue_core.common.enums import ScalarType

from amsdal_glue_connections.sql.connections.sqlite_connection.base import bind_params


def test_json_value_param_is_minified() -> None:
    (bound,) = bind_params((JsonValue({'a': 1, 'b': {'c': 2}}, ScalarType.JSONB),))

    assert bound == '{"a":1,"b":{"c":2}}'
    assert ', ' not in bound
    assert ': ' not in bound


def test_json_value_list_param_is_minified() -> None:
    (bound,) = bind_params((JsonValue(['x', {'y': 1}], ScalarType.JSONB),))

    assert bound == '["x",{"y":1}]'


def test_native_list_adapter_serialises_minified() -> None:
    """A raw Python ``list`` reaches the driver via the registered adapter, which must also minify."""
    adapter = sqlite3.adapters[(list, sqlite3.PrepareProtocol)]

    assert adapter(['x', {'y': 1}]) == '["x",{"y":1}]'


def test_non_json_params_pass_through_unchanged() -> None:
    assert bind_params((1, 'text', None)) == (1, 'text', None)


def test_minified_still_decodes_to_same_object() -> None:
    (bound,) = bind_params((JsonValue({'b': 2, 'a': 1}, ScalarType.JSONB),))

    assert json.loads(bound) == {'b': 2, 'a': 1}
