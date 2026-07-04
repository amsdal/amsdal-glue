"""Unit tests for Value output_type parameter coercion.

Acceptance table:
  Value('5',  INTEGER) → 5
  Value('abc', INTEGER) → raises ValueError
  Value(5, INTEGER)    → 5
  Value('5')           → '5' unchanged
  Value(None, INTEGER) → None  (SQL NULL passthrough)
"""

import datetime
import uuid
from decimal import Decimal

import pytest

from amsdal_glue_core.common.data_models.types import ArrayType
from amsdal_glue_core.common.enums import ScalarType
from amsdal_glue_core.common.expressions.value import Value

# ---------------------------------------------------------------------------
# Acceptance table
# ---------------------------------------------------------------------------


def test_str_to_integer_coercion():
    v = Value('5', output_type=ScalarType.INTEGER)
    assert v.value == 5
    assert isinstance(v.value, int)


def test_invalid_str_to_integer_raises():
    with pytest.raises(ValueError, match='expected a number'):
        Value('abc', output_type=ScalarType.INTEGER)


def test_int_identity_with_integer_type():
    v = Value(5, output_type=ScalarType.INTEGER)
    assert v.value == 5
    assert isinstance(v.value, int)


def test_no_output_type_leaves_value_unchanged():
    v = Value('5')
    assert v.value == '5'
    assert isinstance(v.value, str)


def test_none_passthrough_regardless_of_output_type():
    v = Value(None, output_type=ScalarType.INTEGER)
    assert v.value is None


# ---------------------------------------------------------------------------
# Float / Decimal
# ---------------------------------------------------------------------------


def test_str_to_float_coercion():
    v = Value('1.5', output_type=ScalarType.FLOAT)
    assert v.value == 1.5
    assert isinstance(v.value, float)


def test_invalid_str_to_float_raises():
    with pytest.raises(ValueError, match='expected a number'):
        Value('abc', output_type=ScalarType.FLOAT)


def test_int_to_float_coercion():
    v = Value(3, output_type=ScalarType.FLOAT)
    assert v.value == 3.0
    assert isinstance(v.value, float)


def test_str_to_decimal_coercion():
    v = Value('9.99', output_type=ScalarType.NUMERIC)
    assert v.value == Decimal('9.99')
    assert isinstance(v.value, Decimal)


def test_int_to_decimal_coercion():
    v = Value(10, output_type=ScalarType.NUMERIC)
    assert v.value == Decimal(10)


def test_decimal_identity():
    v = Value(Decimal('3.14'), output_type=ScalarType.NUMERIC)
    assert v.value == Decimal('3.14')


def test_bool_to_decimal_consistent_with_int_float():
    assert Value(True, output_type=ScalarType.NUMERIC).value == Decimal(1)  # noqa: FBT003
    assert Value(False, output_type=ScalarType.NUMERIC).value == Decimal(0)  # noqa: FBT003


# ---------------------------------------------------------------------------
# Boolean
# ---------------------------------------------------------------------------


def test_str_true_to_bool():
    v = Value('true', output_type=ScalarType.BOOLEAN)
    assert v.value is True


def test_str_false_to_bool():
    v = Value('false', output_type=ScalarType.BOOLEAN)
    assert v.value is False


def test_str_one_to_bool():
    v = Value('1', output_type=ScalarType.BOOLEAN)
    assert v.value is True


def test_str_zero_to_bool():
    v = Value('0', output_type=ScalarType.BOOLEAN)
    assert v.value is False


def test_int_one_to_bool():
    v = Value(1, output_type=ScalarType.BOOLEAN)
    assert v.value is True


def test_int_zero_to_bool():
    v = Value(0, output_type=ScalarType.BOOLEAN)
    assert v.value is False


def test_bool_identity():
    v = Value(True, output_type=ScalarType.BOOLEAN)  # noqa: FBT003
    assert v.value is True


def test_invalid_str_to_bool_raises():
    with pytest.raises(ValueError, match='expected a boolean'):
        Value('maybe', output_type=ScalarType.BOOLEAN)


def test_invalid_int_to_bool_raises():
    with pytest.raises(ValueError, match='expected a boolean'):
        Value(2, output_type=ScalarType.BOOLEAN)


# ---------------------------------------------------------------------------
# Text
# ---------------------------------------------------------------------------


def test_int_to_text_coercion():
    v = Value(42, output_type=ScalarType.TEXT)
    assert v.value == '42'
    assert isinstance(v.value, str)


def test_str_identity_with_text_type():
    v = Value('hello', output_type=ScalarType.TEXT)
    assert v.value == 'hello'


# ---------------------------------------------------------------------------
# UUID
# ---------------------------------------------------------------------------


def test_str_to_uuid_coercion():
    uid = '550e8400-e29b-41d4-a716-446655440000'
    v = Value(uid, output_type=ScalarType.UUID)
    assert isinstance(v.value, uuid.UUID)
    assert str(v.value) == uid


def test_uuid_identity():
    uid = uuid.UUID('550e8400-e29b-41d4-a716-446655440000')
    v = Value(uid, output_type=ScalarType.UUID)
    assert v.value == uid


def test_invalid_str_to_uuid_raises():
    with pytest.raises(ValueError, match='expected a UUID'):
        Value('not-a-uuid', output_type=ScalarType.UUID)


# ---------------------------------------------------------------------------
# Date / Time / Datetime
# ---------------------------------------------------------------------------


def test_str_to_date_coercion():
    v = Value('2023-06-15', output_type=ScalarType.DATE)
    assert v.value == datetime.date(2023, 6, 15)
    assert isinstance(v.value, datetime.date)


def test_date_identity():
    d = datetime.date(2023, 6, 15)
    v = Value(d, output_type=ScalarType.DATE)
    assert v.value == d


def test_str_to_timestamp_coercion():
    v = Value('2023-06-15T12:30:00', output_type=ScalarType.TIMESTAMP)
    assert v.value == datetime.datetime(2023, 6, 15, 12, 30, 0)  # noqa: DTZ001


def test_datetime_identity_with_timestamp_type():
    dt = datetime.datetime(2023, 6, 15, 12, 30, 0)  # noqa: DTZ001
    v = Value(dt, output_type=ScalarType.TIMESTAMP)
    assert v.value == dt


# ---------------------------------------------------------------------------
# Integer sub-families
# ---------------------------------------------------------------------------


def test_bool_to_integer_coercion_true():
    v = Value(True, output_type=ScalarType.INTEGER)  # noqa: FBT003
    assert v.value == 1
    assert isinstance(v.value, int)


def test_bool_to_integer_coercion_false():
    v = Value(False, output_type=ScalarType.INTEGER)  # noqa: FBT003
    assert v.value == 0


def test_str_to_bigint_coercion():
    v = Value('999999999999', output_type=ScalarType.BIGINT)
    assert v.value == 999999999999
    assert isinstance(v.value, int)


def test_str_to_smallint_coercion():
    v = Value('32767', output_type=ScalarType.SMALLINT)
    assert v.value == 32767


def test_str_to_serial_coercion():
    v = Value('1', output_type=ScalarType.SERIAL)
    assert v.value == 1


# ---------------------------------------------------------------------------
# None passthrough (NULL) for various types
# ---------------------------------------------------------------------------


def test_none_passthrough_float():
    assert Value(None, output_type=ScalarType.FLOAT).value is None


def test_none_passthrough_boolean():
    assert Value(None, output_type=ScalarType.BOOLEAN).value is None


def test_none_passthrough_text():
    assert Value(None, output_type=ScalarType.TEXT).value is None


# ---------------------------------------------------------------------------
# ArrayType recursion
# ---------------------------------------------------------------------------


def test_array_element_coercion():
    arr_type = ArrayType(item_type=ScalarType.INTEGER)
    v = Value(['1', '2', '3'], output_type=arr_type)
    assert v.value == [1, 2, 3]
    assert all(isinstance(x, int) for x in v.value)


def test_array_element_invalid_raises():
    arr_type = ArrayType(item_type=ScalarType.INTEGER)
    with pytest.raises(ValueError, match='expected a number'):
        Value(['1', 'bad', '3'], output_type=arr_type)


def test_array_none_passthrough():
    arr_type = ArrayType(item_type=ScalarType.INTEGER)
    v = Value(None, output_type=arr_type)
    assert v.value is None


def test_array_non_list_value_raises():
    arr_type = ArrayType(item_type=ScalarType.INTEGER)
    with pytest.raises(ValueError, match='expected a list'):
        Value('not-a-list', output_type=arr_type)


# ---------------------------------------------------------------------------
# JSON / JSONB — coercion does NOT transform; serialisation is the
# connection/binding layer's responsibility. The value passes through as-is.
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    'json_type',
    [ScalarType.JSON, ScalarType.JSONB],
)
@pytest.mark.parametrize(
    'value',
    [{'a': 1}, [1, 2, 3], 'emil', 1, 1.5, True],
)
def test_json_value_passes_through_unchanged(json_type, value):
    v = Value(value, output_type=json_type)
    assert v.value == value
    assert type(v.value) is type(value)


def test_json_none_passthrough():
    assert Value(None, output_type=ScalarType.JSONB).value is None


# ---------------------------------------------------------------------------
# Non-finite numbers → clean error for INTEGER (valid float values for FLOAT)
# ---------------------------------------------------------------------------


@pytest.mark.parametrize('value', [float('inf'), float('-inf'), float('nan'), Decimal('NaN'), Decimal('Infinity')])
def test_non_finite_to_integer_raises_clean(value):
    with pytest.raises(ValueError, match=r'expected an? '):
        Value(value, output_type=ScalarType.INTEGER)


def test_infinity_is_valid_float():
    # inf is a valid IEEE-754 float value — accepted for a FLOAT column.
    assert Value(float('inf'), output_type=ScalarType.FLOAT).value == float('inf')


def test_nan_is_valid_float():
    import math

    assert math.isnan(Value(float('nan'), output_type=ScalarType.FLOAT).value)
