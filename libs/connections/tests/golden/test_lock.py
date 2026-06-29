# libs/connections/tests/golden/test_lock.py
"""Golden-master tests for lock SQL paths.

Postgres sync (pg_record)
--------------------------
The sync PostgresConnection.acquire_lock() checks ``lock.mode == 'EXCLUSIVE'`` and, when true,
calls ``self.execute('BEGIN EXCLUSIVE')``.  release_lock does the same for ``self.execute('COMMIT')``.

KNOWN-DIVERGENCE (migration): the Postgres **sync** path emits SQLite-style ``BEGIN EXCLUSIVE``
/ ``COMMIT`` instead of the proper Postgres row-level lock (``SELECT … FOR UPDATE``).  The
**async** PostgresConnection correctly builds ``SELECT * FROM <table> [WHERE …] FOR UPDATE`` via
``build_where()``, but the async path is not reachable through the sync recording harness.
This divergence should be resolved when the Rust/unified backend is wired up.

SQLite sync (lite_record)
--------------------------
SQLite's acquire_lock / release_lock (EXCLUSIVE mode) call ``self.connection.execute(…)``
directly on the raw ``sqlite3.Connection`` object — not through the overridable ``execute()``
hook.  The recording harness never establishes a live DB connection, so ``self.connection``
raises ``ConnectionError('Connection not established')`` immediately.  These cases are marked
``xfail(strict=True)``.

SHARED-mode locks are no-ops for both backends: neither emits SQL, and the recording
connection captures nothing.
"""

import pytest
from amsdal_glue_core.commands.lock_command_node import ExecutionLockCommand
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.enums import FieldLookup
from amsdal_glue_core.common.enums import LockAction
from amsdal_glue_core.common.enums import LockMode
from amsdal_glue_core.common.enums import LockParameter
from amsdal_glue_core.common.enums import Version
from amsdal_glue_core.common.operations.commands import LockSchemaReference

from amsdal_glue_core.common.data_models.conditions import Condition
from amsdal_glue_core.common.data_models.conditions import Conditions
from amsdal_glue_core.common.data_models.field_reference import Field
from amsdal_glue_core.common.data_models.field_reference import FieldReference
from amsdal_glue_core.common.expressions.field_reference import FieldReferenceExpression
from amsdal_glue_core.common.expressions.value import Value

from ._harness import lite_record
from ._harness import pg_async_record
from ._harness import pg_record


def _lock(mode: LockMode, action: LockAction = LockAction.ACQUIRE) -> ExecutionLockCommand:
    """Helper — build a minimal ExecutionLockCommand for the given mode/action."""
    return ExecutionLockCommand(
        action=action,
        mode=mode,
        parameter=LockParameter.WAIT,
        locked_object=LockSchemaReference(
            schema=SchemaReference(name='users', version=Version.LATEST),
        ),
    )


# ---------------------------------------------------------------------------
# Postgres sync
# ---------------------------------------------------------------------------


def test_pg_acquire_lock_exclusive_emits_begin_exclusive() -> None:
    """KNOWN-DIVERGENCE (migration): Postgres sync emits SQLite-style 'BEGIN EXCLUSIVE'
    rather than a Postgres row-level lock.  The async path uses SELECT … FOR UPDATE."""
    conn = pg_record()
    result = conn.acquire_lock(_lock(LockMode.EXCLUSIVE, LockAction.ACQUIRE))
    assert result is True
    assert conn.captured == [('BEGIN EXCLUSIVE', [])]


def test_pg_acquire_lock_shared_is_noop() -> None:
    """Shared-mode acquire emits no SQL on the Postgres sync path."""
    conn = pg_record()
    result = conn.acquire_lock(_lock(LockMode.SHARED, LockAction.ACQUIRE))
    assert result is True
    assert conn.captured == []


def test_pg_release_lock_exclusive_emits_commit() -> None:
    """KNOWN-DIVERGENCE (migration): mirrors 'BEGIN EXCLUSIVE' — Postgres sync releases
    with a bare 'COMMIT' (SQLite syntax) rather than a Postgres-native release mechanism."""
    conn = pg_record()
    result = conn.release_lock(_lock(LockMode.EXCLUSIVE, LockAction.RELEASE))
    assert result is True
    assert conn.captured == [('COMMIT', [])]


def test_pg_release_lock_shared_is_noop() -> None:
    """Shared-mode release emits no SQL on the Postgres sync path."""
    conn = pg_record()
    result = conn.release_lock(_lock(LockMode.SHARED, LockAction.RELEASE))
    assert result is True
    assert conn.captured == []


# ---------------------------------------------------------------------------
# SQLite sync
# ---------------------------------------------------------------------------


@pytest.mark.xfail(
    strict=True,
    reason=(
        'SQLite acquire_lock (EXCLUSIVE) calls self.connection.execute() on the raw '
        'sqlite3.Connection — not through the overridable execute() hook — so '
        'ConnectionError is raised by the recording harness (no live DB).'
    ),
)
def test_lite_acquire_lock_exclusive_xfail() -> None:
    conn = lite_record()
    conn.acquire_lock(_lock(LockMode.EXCLUSIVE, LockAction.ACQUIRE))


def test_lite_acquire_lock_shared_is_noop() -> None:
    """SQLite SHARED acquire_lock is a no-op — the EXCLUSIVE branch is never entered."""
    conn = lite_record()
    result = conn.acquire_lock(_lock(LockMode.SHARED, LockAction.ACQUIRE))
    assert result is True
    assert conn.captured == []


@pytest.mark.xfail(
    strict=True,
    reason=(
        'SQLite release_lock (EXCLUSIVE) calls self.connection.execute() on the raw '
        'sqlite3.Connection — not through the overridable execute() hook — so '
        'ConnectionError is raised by the recording harness (no live DB).'
    ),
)
def test_lite_release_lock_exclusive_xfail() -> None:
    conn = lite_record()
    conn.release_lock(_lock(LockMode.EXCLUSIVE, LockAction.RELEASE))


def test_lite_release_lock_shared_is_noop() -> None:
    """SQLite SHARED release_lock is a no-op — the EXCLUSIVE branch is never entered."""
    conn = lite_record()
    result = conn.release_lock(_lock(LockMode.SHARED, LockAction.RELEASE))
    assert result is True
    assert conn.captured == []


# ---------------------------------------------------------------------------
# Postgres async — row-level locking (SELECT … FOR UPDATE)
# ---------------------------------------------------------------------------


def _where_id_eq(table: str, value: int) -> Conditions:
    """Build a single-condition Conditions: <table>.id = <value>."""
    return Conditions(
        Condition(
            left=FieldReferenceExpression(
                field_reference=FieldReference(field=Field(name='id'), table_name=table),
            ),
            lookup=FieldLookup.EQ,
            right=Value(value=value),
        )
    )


async def test_pg_async_acquire_lock_emits_for_update() -> None:
    """Async PG acquire_lock with a WHERE query emits SELECT * FROM … WHERE … FOR UPDATE."""
    lock = ExecutionLockCommand(
        action=LockAction.ACQUIRE,
        mode=LockMode.EXCLUSIVE,
        parameter=LockParameter.WAIT,
        locked_object=LockSchemaReference(
            schema=SchemaReference(name='users', version=Version.LATEST),
            query=_where_id_eq('users', 42),
        ),
    )
    conn = pg_async_record()
    result = await conn.acquire_lock(lock)
    assert result is True
    assert conn.captured == [
        ('SELECT * FROM "users" WHERE "users"."id" = %s FOR UPDATE', [42]),
    ]


async def test_pg_async_acquire_lock_no_query_is_noop() -> None:
    """Async PG acquire_lock without a query (locked_object.query is None) emits no SQL."""
    lock = ExecutionLockCommand(
        action=LockAction.ACQUIRE,
        mode=LockMode.EXCLUSIVE,
        parameter=LockParameter.WAIT,
        locked_object=LockSchemaReference(
            schema=SchemaReference(name='users', version=Version.LATEST),
        ),
    )
    conn = pg_async_record()
    result = await conn.acquire_lock(lock)
    assert result is True
    assert conn.captured == []


async def test_pg_async_release_lock_is_noop() -> None:
    """Async PG release_lock emits no SQL — both branches in release_lock just return True."""
    lock = ExecutionLockCommand(
        action=LockAction.RELEASE,
        mode=LockMode.EXCLUSIVE,
        parameter=LockParameter.WAIT,
        locked_object=LockSchemaReference(
            schema=SchemaReference(name='users', version=Version.LATEST),
        ),
    )
    conn = pg_async_record()
    result = await conn.release_lock(lock)
    assert result is True
    assert conn.captured == []
