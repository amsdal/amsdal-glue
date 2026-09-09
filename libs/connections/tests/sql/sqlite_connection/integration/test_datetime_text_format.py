"""SQLite datetime TEXT format: must write the ``T`` separator.

Datetime TEXT must use the default ISO ``T`` separator; a regression wrote a space instead.
Because ``' '`` (0x20) sorts before ``'T'`` (0x54), a column that mixes both forms
sorts/ranges/compares by the separator byte instead of the real instant, corrupting ORDER BY, range
filters and equality. These tests pin the corrected ``T`` form on BOTH write paths -- the module-level
sqlite3 adapter (raw ``datetime`` bound through ``execute``) and the Rust generator param path
(``run_mutations``) -- and prove a mixed-format column behaves chronologically.

They FAIL on the space-writing code and PASS after the fix. The declared column TYPE (``timestamp``)
is intentionally left untouched -- only the VALUE text format changes.
"""

from datetime import datetime
from datetime import timezone

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


def test_rust_param_path_writes_t_separator(database_connection: SqliteConnection) -> None:
    """A datetime routed through the generator (run_mutations -> Rust extract) stores the ``T`` form."""
    schema_ref = _register_event(database_connection)

    database_connection.run_mutations([
        InsertData(
            schema=schema_ref,
            data=[DataInput(data={'id': 1, 'created_at': datetime(2021, 1, 2, 3, 4, 5)})],  # noqa: DTZ001
        ),
    ])

    # quote() shows the raw stored TEXT; offset-10 byte must be 'T', not a space.
    assert _quoted(database_connection, 1) == "'2021-01-02T03:04:05'"


def test_rust_param_path_writes_t_with_microseconds_and_tz(database_connection: SqliteConnection) -> None:
    """Lock the whole encoding (not just the separator) for a tz-aware microsecond datetime."""
    schema_ref = _register_event(database_connection)

    value = datetime(2021, 1, 2, 13, 14, 18, 99106, tzinfo=timezone.utc)
    database_connection.run_mutations([
        InsertData(schema=schema_ref, data=[DataInput(data={'id': 1, 'created_at': value})]),
    ])

    assert _quoted(database_connection, 1) == "'2021-01-02T13:14:18.099106+00:00'"


def test_sqlite3_adapter_path_writes_t_separator(database_connection: SqliteConnection) -> None:
    """A raw ``datetime`` bound through ``execute`` (module-level adapter path) stores the ``T`` form."""
    database_connection.execute('CREATE TABLE "raw_evt" ("id" integer, "created_at" timestamp)')
    database_connection.execute(
        'INSERT INTO "raw_evt" ("id", "created_at") VALUES (?, ?)',
        1,
        datetime(2021, 1, 2, 3, 4, 5),  # noqa: DTZ001
    )

    cur = database_connection.execute('SELECT quote("created_at") FROM "raw_evt" WHERE "id" = ?', 1)
    (value,) = cur.fetchone()
    cur.close()
    assert value == "'2021-01-02T03:04:05'"


def test_mixed_format_column_orders_and_ranges_chronologically(database_connection: SqliteConnection) -> None:
    """A legacy ``T`` row and freshly written rows sort/range as one homogeneous ``T`` column."""
    schema_ref = _register_event(database_connection)

    # Simulate a legacy row: raw INSERT of the 'T' TEXT form at real 09:00.
    database_connection.execute('INSERT INTO "event" ("id", "created_at") VALUES (?, ?)', 1, '2021-01-02T09:00:00')
    # Rows via the generator (also 'T'): 11:00 and 08:00.
    database_connection.run_mutations([
        InsertData(
            schema=schema_ref,
            data=[
                DataInput(data={'id': 2, 'created_at': datetime(2021, 1, 2, 11, 0, 0)}),  # noqa: DTZ001
                DataInput(data={'id': 3, 'created_at': datetime(2021, 1, 2, 8, 0, 0)}),  # noqa: DTZ001
            ],
        ),
    ])

    cur = database_connection.execute('SELECT "id" FROM "event" ORDER BY "created_at" ASC')
    order = [row[0] for row in cur.fetchall()]
    cur.close()
    assert order == [3, 1, 2]  # chronological: 08:00, 09:00, 11:00

    # Range: >= 10:00 must return only the 11:00 row (no false positive from the legacy row).
    cur = database_connection.execute(
        'SELECT "id" FROM "event" WHERE "created_at" >= ? ORDER BY "id"', '2021-01-02T10:00:00'
    )
    assert [row[0] for row in cur.fetchall()] == [2]
    cur.close()

    # Range: <= 10:00 must return 09:00 and 08:00 (no false negative).
    cur = database_connection.execute(
        'SELECT "id" FROM "event" WHERE "created_at" <= ? ORDER BY "id"', '2021-01-02T10:00:00'
    )
    assert [row[0] for row in cur.fetchall()] == [1, 3]
    cur.close()


def test_readback_parses_both_separators(database_connection: SqliteConnection) -> None:
    """Regression guard: fromisoformat re-hydrates a legacy space row AND a new ``T`` row (passes both)."""
    database_connection.execute('CREATE TABLE "evt2" ("id" integer, "created_at" timestamp)')
    database_connection.execute('INSERT INTO "evt2" VALUES (?, ?)', 1, '2021-01-02T03:04:05')  # T
    database_connection.execute('INSERT INTO "evt2" VALUES (?, ?)', 2, '2021-01-02 03:04:05')  # space

    cur = database_connection.execute('SELECT "id", "created_at" FROM "evt2" ORDER BY "id"')
    rows = cur.fetchall()
    cur.close()
    assert rows[0][1] == datetime(2021, 1, 2, 3, 4, 5)  # noqa: DTZ001
    assert rows[1][1] == datetime(2021, 1, 2, 3, 4, 5)  # noqa: DTZ001
