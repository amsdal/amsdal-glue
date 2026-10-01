"""PostgreSQL ORDER BY and range filters agree with the SQLite instant-order contract."""

from amsdal_glue_connections.sql.connections.postgres_connection import PostgresConnection
from tests.sql.datetime_instant_order import assert_naive_datetime_insert_rejected
from tests.sql.datetime_instant_order import assert_offset_datetimes_order_by_instant


def test_offset_datetimes_order_and_range_by_instant(database_connection: PostgresConnection) -> None:
    assert_offset_datetimes_order_by_instant(database_connection)


def test_naive_datetime_insert_is_rejected(database_connection: PostgresConnection) -> None:
    assert_naive_datetime_insert_rejected(database_connection)
