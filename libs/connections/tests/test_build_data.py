from amsdal_glue_connections.sql.connections.base_connection import SqlConnectionMixinBase
from amsdal_glue_connections.sql.connections.postgres_connection.base import text_columns


def test_values_that_look_like_json_are_decoded() -> None:
    data = SqlConnectionMixinBase.build_data({'a': '{"k": 1}', 'b': '[1, 2]', 'c': 'x', 'd': 5})
    assert data.data == {'a': {'k': 1}, 'b': [1, 2], 'c': 'x', 'd': 5}


def test_a_value_that_does_not_parse_stays_a_string() -> None:
    """Before: `json.JSONDecodeError` from one value failed the whole query (SQLite has no column types to go by)."""
    data = SqlConnectionMixinBase.build_data({'body': '{ x: 1 }', 'list': '[not json'})
    assert data.data == {'body': '{ x: 1 }', 'list': '[not json'}


def test_text_columns_are_never_decoded() -> None:
    data = SqlConnectionMixinBase.build_data({'body': '{"a": 1}', 'meta': '{"a": 1}'}, text_columns={'body'})
    assert data.data == {'body': '{"a": 1}', 'meta': {'a': 1}}


def test_text_columns_by_postgres_type() -> None:
    description = [
        ('text', 25),
        ('varchar', 1043),
        ('char', 1042),
        ('name', 19),
        ('jsonb', 3802),
        ('int', 23),
        ('vector', 16385),
        ('untyped',),  # a fake cursor's bare (name,): nothing to go by
    ]
    assert text_columns(description) == {'text', 'varchar', 'char', 'name'}
    assert text_columns(None) == frozenset()
