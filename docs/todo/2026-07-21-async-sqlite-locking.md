# Async SQLite exclusive locking

**Status:** open / design needed.

## Current state

The async SQLite connection's `acquire_lock` / `release_lock`
(`sqlite_connection/async_connection.py`) are no-ops (`return True`). The sync connection
(`sqlite_connection/sync_connection.py`) issues a real `BEGIN EXCLUSIVE` / `COMMIT` and serialises
writers across connections/processes (covered by
`amsdal-glue/tests/integration/sqlite/test_lock_execute.py::test_lock`). The async path has no
equivalent guarantee — two concurrent async writers to the same database file are not serialised
(lost-update risk that the sync path prevents).

## Why it is a no-op (confirmed empirically)

`BEGIN EXCLUSIVE` is *not* broken under async: aiosqlite keeps the transaction open on its worker
thread, so a separate connection is correctly blocked while the lock is held — identical to sync.

The real obstacle is the connection pool. For `transaction_id=None` operations the pool hands the
**same** connection to concurrently running coroutines. Issuing `BEGIN EXCLUSIVE` on that shared
connection breaks them:

- a second `acquire_lock` on the same connection raises `cannot start a transaction within a
  transaction`;
- an unrelated coroutine's write silently joins the lock holder's open transaction (no isolation,
  and its rows ride on someone else's commit/rollback).

The sync path avoids this only because it never interleaves coroutines on one connection. So the
prior comment ("`BEGIN EXCLUSIVE` does not work reliably in async") was imprecise: it works; it is
unsafe specifically on the shared pooled connection.

## What a correct fix needs

Async exclusive locking must acquire the lock on a **transaction-scoped connection used solely by
the lock holder** — not on the shared `transaction_id=None` pooled connection — so that the holder's
own writes go through the locked connection while other coroutines/processes are correctly blocked.
This is a design change to how locks interact with the async connection pool; scope it as its own
piece of work.
