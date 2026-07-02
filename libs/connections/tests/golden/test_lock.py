# libs/connections/tests/golden/test_lock.py
"""Golden-master tests for the lock SQL path (post Rust migration — C-Lock).

The connection ``acquire_lock``/``release_lock`` now take a ``LockCommand`` and render through the
Rust ``compile_lock_command``:

- **Postgres (sync + async)** — a table lock (``LockReference(reference=SchemaReference)``) renders
  ``LOCK TABLE "<name>" IN <EXCLUSIVE|SHARE> MODE``. Release of a TRANSACTION-scope lock is a no-op
  (the lock auto-releases at COMMIT/ROLLBACK; the Rust generator raises ``UnsupportedFeatureError``
  for such a release, which the connection treats as a no-op).
- **SQLite** — keeps the ``BEGIN EXCLUSIVE`` hack (deliberate divergence, spec §3.5). It calls the raw
  ``sqlite3.Connection`` directly, so the recording harness (no live DB) raises ``ConnectionError``
  for the EXCLUSIVE branch — kept as ``xfail(strict=True)``. SHARED is a no-op.

Row-level locking (``SELECT … FOR UPDATE``) is NO LONGER part of the lock path — it is expressed on
``QueryStatement.lock`` (``SelectLock``) and rendered by ``compile_query`` in ``query()``.
"""

import pytest
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.enums import LockAction
from amsdal_glue_core.common.enums import LockMode
from amsdal_glue_core.common.enums import LockParameter
from amsdal_glue_core.common.enums import LockScope
from amsdal_glue_core.common.enums import Version
from amsdal_glue_core.common.operations.commands import LockCommand
from amsdal_glue_core.common.operations.commands import LockReference

from ._harness import lite_record
from ._harness import pg_async_record
from ._harness import pg_record


def _lock(mode: LockMode, action: LockAction = LockAction.ACQUIRE) -> LockCommand:
    """Helper — build a minimal table LockCommand for the given mode/action."""
    return LockCommand(
        action=action,
        mode=mode,
        parameter=LockParameter.WAIT,
        scope=LockScope.TRANSACTION,
        locked_objects=[LockReference(reference=SchemaReference(name='users', version=Version.LATEST))],
    )


# ---------------------------------------------------------------------------
# Postgres sync
# ---------------------------------------------------------------------------


def test_pg_acquire_lock_exclusive_emits_lock_table() -> None:
    conn = pg_record()
    result = conn.acquire_lock(_lock(LockMode.EXCLUSIVE, LockAction.ACQUIRE))
    assert result is True
    assert conn.captured == [('LOCK TABLE "users" IN EXCLUSIVE MODE', [])]


def test_pg_acquire_lock_shared_emits_lock_table_share() -> None:
    conn = pg_record()
    result = conn.acquire_lock(_lock(LockMode.SHARED, LockAction.ACQUIRE))
    assert result is True
    assert conn.captured == [('LOCK TABLE "users" IN SHARE MODE', [])]


def test_pg_release_lock_exclusive_is_noop() -> None:
    """A TRANSACTION-scope lock auto-releases at COMMIT — release emits no SQL."""
    conn = pg_record()
    result = conn.release_lock(_lock(LockMode.EXCLUSIVE, LockAction.RELEASE))
    assert result is True
    assert conn.captured == []


def test_pg_release_lock_shared_is_noop() -> None:
    conn = pg_record()
    result = conn.release_lock(_lock(LockMode.SHARED, LockAction.RELEASE))
    assert result is True
    assert conn.captured == []


# ---------------------------------------------------------------------------
# SQLite sync — BEGIN EXCLUSIVE hack (spec §3.5)
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
    """SQLite SHARED acquire_lock is a no-op — the EXCLUSIVE (BEGIN EXCLUSIVE) branch is never entered."""
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
    conn = lite_record()
    result = conn.release_lock(_lock(LockMode.SHARED, LockAction.RELEASE))
    assert result is True
    assert conn.captured == []


# ---------------------------------------------------------------------------
# Postgres async — table lock via compile_lock_command
# (row-level SELECT … FOR UPDATE moved to QueryStatement.lock; no longer a lock-path concern)
# ---------------------------------------------------------------------------


async def test_pg_async_acquire_lock_exclusive_emits_lock_table() -> None:
    conn = pg_async_record()
    result = await conn.acquire_lock(_lock(LockMode.EXCLUSIVE, LockAction.ACQUIRE))
    assert result is True
    assert conn.captured == [('LOCK TABLE "users" IN EXCLUSIVE MODE', [])]


async def test_pg_async_release_lock_is_noop() -> None:
    conn = pg_async_record()
    result = await conn.release_lock(_lock(LockMode.EXCLUSIVE, LockAction.RELEASE))
    assert result is True
    assert conn.captured == []
