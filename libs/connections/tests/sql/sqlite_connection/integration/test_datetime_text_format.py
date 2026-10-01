from datetime import datetime
from datetime import timezone

import pytest
from amsdal_glue_core.common.data_models.data import DataInput
from amsdal_glue_core.common.data_models.schema import PropertySchema
from amsdal_glue_core.common.data_models.schema import Schema
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.enums import ScalarType
from amsdal_glue_core.common.enums import Version
from amsdal_glue_core.common.operations.commands import SchemaCommand
from amsdal_glue_core.common.operations.mutations.data import InsertData
from amsdal_glue_core.common.operations.mutations.schema import RegisterSchema

from amsdal_glue_connections.sql.connections.sqlite_connection import SqliteConnection


def _register_event(database_connection: SqliteConnection) -> SchemaReference:
    database_connection.run_schema_command(
        SchemaCommand(
            mutations=[
                RegisterSchema(
                    schema_ref=SchemaReference(name='event', version=Version.LATEST),
                    schema=Schema(
                        name='event',
                        version=Version.LATEST,
                        properties=[
                            PropertySchema(name='id', type=ScalarType.INTEGER, required=True),
                            PropertySchema(name='created_at', type=ScalarType.TIMESTAMP, required=True),
                        ],
                    ),
                ),
            ],
        ),
    )
    return SchemaReference(name='event', version=Version.LATEST)


def _quoted(database_connection: SqliteConnection, id_: int) -> str:
    cur = database_connection.execute('SELECT quote("created_at") FROM "event" WHERE "id" = ?', id_)
    (value,) = cur.fetchone()
    cur.close()
    return value


def test_rust_param_path_writes_canonical_utc(database_connection: SqliteConnection) -> None:
    schema_ref = _register_event(database_connection)

    database_connection.run_mutations([
        InsertData(
            schema=schema_ref,
            data=[DataInput(data={'id': 1, 'created_at': datetime(2021, 1, 2, 3, 4, 5, tzinfo=timezone.utc)})],
        ),
    ])

    assert _quoted(database_connection, 1) == "'2021-01-02T03:04:05.000000+00:00'"


def test_rust_param_path_writes_t_with_microseconds_and_tz(database_connection: SqliteConnection) -> None:
    schema_ref = _register_event(database_connection)

    value = datetime(2021, 1, 2, 13, 14, 18, 99106, tzinfo=timezone.utc)
    database_connection.run_mutations([
        InsertData(schema=schema_ref, data=[DataInput(data={'id': 1, 'created_at': value})]),
    ])

    assert _quoted(database_connection, 1) == "'2021-01-02T13:14:18.099106+00:00'"


def test_sqlite3_adapter_path_writes_canonical_utc(database_connection: SqliteConnection) -> None:
    database_connection.execute('CREATE TABLE "raw_evt" ("id" integer, "created_at" timestamp)')
    database_connection.execute(
        'INSERT INTO "raw_evt" ("id", "created_at") VALUES (?, ?)',
        1,
        datetime(2021, 1, 2, 3, 4, 5, tzinfo=timezone.utc),
    )

    cur = database_connection.execute('SELECT quote("created_at") FROM "raw_evt" WHERE "id" = ?', 1)
    (value,) = cur.fetchone()
    cur.close()
    assert value == "'2021-01-02T03:04:05.000000+00:00'"


def test_sqlite3_adapter_rejects_naive_datetime(database_connection: SqliteConnection) -> None:
    database_connection.execute('CREATE TABLE "raw_evt" ("id" integer, "created_at" timestamp)')
    with pytest.raises(ValueError, match='naive values are not treated as UTC'):
        database_connection.execute(
            'INSERT INTO "raw_evt" ("id", "created_at") VALUES (?, ?)',
            1,
            datetime(2021, 1, 2, 3, 4, 5),  # noqa: DTZ001
        )


def test_mixed_format_column_orders_and_ranges_chronologically(database_connection: SqliteConnection) -> None:
    schema_ref = _register_event(database_connection)

    database_connection.execute('INSERT INTO "event" ("id", "created_at") VALUES (?, ?)', 1, '2021-01-02T09:00:00')
    database_connection.run_mutations([
        InsertData(
            schema=schema_ref,
            data=[
                DataInput(data={'id': 2, 'created_at': datetime(2021, 1, 2, 11, 0, tzinfo=timezone.utc)}),
                DataInput(data={'id': 3, 'created_at': datetime(2021, 1, 2, 8, 0, tzinfo=timezone.utc)}),
            ],
        ),
    ])

    cur = database_connection.execute('SELECT "id" FROM "event" ORDER BY "created_at" ASC')
    order = [row[0] for row in cur.fetchall()]
    cur.close()
    assert order == [3, 1, 2]

    cur = database_connection.execute(
        'SELECT "id" FROM "event" WHERE "created_at" >= ? ORDER BY "id"', '2021-01-02T10:00:00'
    )
    assert [row[0] for row in cur.fetchall()] == [2]
    cur.close()

    cur = database_connection.execute(
        'SELECT "id" FROM "event" WHERE "created_at" <= ? ORDER BY "id"', '2021-01-02T10:00:00'
    )
    assert [row[0] for row in cur.fetchall()] == [1, 3]
    cur.close()


def test_readback_parses_both_separators(database_connection: SqliteConnection) -> None:
    database_connection.execute('CREATE TABLE "evt2" ("id" integer, "created_at" timestamp)')
    database_connection.execute('INSERT INTO "evt2" VALUES (?, ?)', 1, '2021-01-02T03:04:05')
    database_connection.execute('INSERT INTO "evt2" VALUES (?, ?)', 2, '2021-01-02 03:04:05')

    cur = database_connection.execute('SELECT "id", "created_at" FROM "evt2" ORDER BY "id"')
    rows = cur.fetchall()
    cur.close()
    expected = datetime(2021, 1, 2, 3, 4, 5, tzinfo=timezone.utc)
    assert rows[0][1] == expected
    assert rows[1][1] == expected
