"""Unit tests for ``parse_pg_type`` — the pure parser that recovers Postgres type
modifiers from a ``format_type(atttypid, atttypmod)`` string (M18).

These pin the behaviour that ``information_schema``-based introspection lost:
  * ``vector(768)`` dimensions (previously hardcoded to 0),
  * ``numeric(p,s)`` precision/scale for scalars AND array elements.

They run without a live database.
"""

from amsdal_glue_core.common.data_models.types import ArrayType
from amsdal_glue_core.common.data_models.types import CustomType
from amsdal_glue_core.common.data_models.types import VectorType
from amsdal_glue_core.common.enums import ScalarType

from amsdal_glue_connections.sql.connections.postgres_connection.sync_connection import parse_pg_type


def test_vector_preserves_dimensions() -> None:
    # Regression: old path returned VectorType(dimensions=0) regardless of the real size.
    assert parse_pg_type('vector(768)') == VectorType(dimensions=768)


def test_vector_without_dimensions_defaults_to_zero() -> None:
    assert parse_pg_type('vector') == VectorType(dimensions=0)


def test_numeric_scalar_preserves_precision_and_scale() -> None:
    assert parse_pg_type('numeric(10,2)') == CustomType(name='NUMERIC', params={'precision': 10, 'scale': 2})


def test_numeric_scalar_precision_only() -> None:
    assert parse_pg_type('numeric(10)') == CustomType(name='NUMERIC', params={'precision': 10})


def test_bare_numeric_stays_scalar() -> None:
    assert parse_pg_type('numeric') == ScalarType.NUMERIC


def test_numeric_array_preserves_element_precision_and_scale() -> None:
    # Regression: array element modifiers were lost because information_schema exposes
    # numeric_precision as NULL for array columns.
    assert parse_pg_type('numeric(10,2)[]') == ArrayType(
        item_type=CustomType(name='NUMERIC', params={'precision': 10, 'scale': 2}),
    )


def test_text_array() -> None:
    assert parse_pg_type('text[]') == ArrayType(item_type=ScalarType.TEXT)


def test_integer_scalar() -> None:
    assert parse_pg_type('integer') == ScalarType.INTEGER


def test_character_varying_with_length_maps_to_text() -> None:
    assert parse_pg_type('character varying(50)') == ScalarType.TEXT


def test_timestamp_with_precision_maps_to_timestamp() -> None:
    # format_type renders the modifier in the middle: 'timestamp(6) without time zone'.
    assert parse_pg_type('timestamp(6) without time zone') == ScalarType.TIMESTAMP


def test_double_precision_scalar() -> None:
    assert parse_pg_type('double precision') == ScalarType.DOUBLE


def test_unknown_type_falls_back_to_custom_type() -> None:
    assert parse_pg_type('mood') == CustomType(name='mood')


def test_vector_array_preserves_dimensions() -> None:
    assert parse_pg_type('vector(3)[]') == ArrayType(item_type=VectorType(dimensions=3))
