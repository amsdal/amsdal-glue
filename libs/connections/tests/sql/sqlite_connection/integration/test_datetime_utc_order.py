"""SQLite ORDER BY and range filters follow instant order, not the original ISO text."""

from amsdal_glue_connections.sql.connections.sqlite_connection import SqliteConnection
from tests.sql.datetime_instant_order import assert_naive_datetime_insert_rejected
from tests.sql.datetime_instant_order import assert_offset_datetimes_order_by_instant


def test_offset_datetimes_order_and_range_by_instant(database_connection: SqliteConnection) -> None:
    assert_offset_datetimes_order_by_instant(database_connection)

    cur = database_connection.execute('SELECT quote("happened_at") FROM "event" WHERE "id" = ?', 1)
    (stored,) = cur.fetchone()
    cur.close()
    # 22:00+04 is 18:00 UTC, fixed-width, never Z.
    assert stored == "'2026-09-22T18:00:00.000000+00:00'"


def test_naive_datetime_insert_is_rejected(database_connection: SqliteConnection) -> None:
    assert_naive_datetime_insert_rejected(database_connection)
