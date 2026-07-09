# Historical write lock: advisory vs `SELECT FOR UPDATE`

Analysis of how amsdal routes reads, writes, transactions and locks across the
**state** and **lakehouse (historical)** databases, and a comparison of the two
ways to implement the per-object write lock in the sql-rust glue: PostgreSQL
**advisory locks** vs row-level **`SELECT … FOR UPDATE`**.

All claims are backed by `file:line` references gathered from the code. Line
numbers are as of branches `feature/sql-rust` (amsdal_data / amsdal_models) and
`feature/sql-rust-impl` (glue) on 2026-07-09.

---

## 0. TL;DR

- The write lock exists to serialize a **non-atomic read-modify-write on the
  lakehouse version chain**: an update/delete first *reads* the current latest
  version, then *inserts* a successor row pointing at it (`prior_version`). Two
  concurrent writers reading the same `v(n)` both insert successors → a **forked
  version chain**, both rows compute `is_latest = true` → corruption.
- **Both** advisory and `FOR UPDATE` are ultimately **cooperative** here (they
  protect only writers that take the lock — and all writers go through
  `model_manager`). Neither is a magic DB-enforced guard against the
  insert-a-new-successor race, because the competitor inserts a *new* row rather
  than touching the locked one.
- **Recommendation: advisory.** It is simpler (one function call, no per-version
  loop, no Python SQL building), works regardless of whether rows exist, and maps
  cleanly onto the new `LockCommand` model. The one real advantage of `FOR UPDATE`
  (DB-enforced on the physical rows) is largely moot for this specific race.
- Hard constraints discovered for the advisory path (all code-verified below):
  **scope must be `TRANSACTION`** (the planner rejects `SESSION`), **`pool` must
  be `'DEFAULT'`**, and the **explicit `RELEASE` command must be removed**.
- Orthogonal systemic risk (affects *either* lock choice): there is **no cross-DB
  atomicity**. A commit that succeeds on lakehouse but fails on state leaves the
  two databases inconsistent with only an exception raised.

---

## 1. Architecture: two databases, one pipeline

amsdal runs two logical databases behind the ORM:

- **state** — the `default` container: a current-snapshot store, one row per
  object keyed by `partition_key`; no version metadata.
- **lakehouse / historical** — the `lakehouse` container: an append-only version
  history, many rows per object keyed by `range_key` (= `object_version`), with a
  companion `Metadata` row per version carrying `prior_version` / `is_deleted`.

They are **distinct containers with distinct `ConnectionManager`s / pools**
(`amsdal_data/application.py:28-29`, `:140-156`; container names
`DEFAULT_CONTAINER_NAME='default'`, `LAKEHOUSE_CONTAINER_NAME='lakehouse'`,
glue `applications/lakehouse.py:46-47`). Internal versioned tables
(`Metadata`, `reference`, `transaction`) are registered only on the lakehouse
alias (`application.py:172-178`).

### Pipeline fan-out (the key routing fact)

Command services are registered as **pipeline** services over **both** containers,
in the order `[lakehouse, default]`; query services target **only** `default`:

```
# glue applications/lakehouse.py:84-89 (async :222-227)
query_services   = [SchemaQueryService, DataQueryService]         -> [default]
command_services = [SchemaCommandService, DataCommandService,
                    TransactionCommandService, LockCommandService] -> [lakehouse, default]
```

`PipelineServiceMixin.execute` (`pipelines/services/router_mixin.py:6-51`) runs
the *same* command inside each container via `Container.switch(name)`, lakehouse
first. Registration of the `Pipeline*` variants: `glue initialize.py:249-282`.

Consequences:

- **Writes, schema changes, transaction commands, and LOCK commands all fan out
  to lakehouse then state.** (`LockCommand` is pipelined exactly like
  `DataCommand`.)
- **Reads do not fan out** — a read hits a single container.
- The mixin runs the first (lakehouse) container and **does not check its
  `success`** before running the second; it returns the lakehouse result on full
  success, or the state result if state failed (`router_mixin.py:13-27, 30-51`).

---

## 2. Read routing

- A read with no `using` defaults to **state** (`base_queryset.py:270`
  `_using = DEFAULT_DB_ALIAS`; routing fork `executor.py:207-208 / 285-292`).
- Reads forced to **lakehouse** (`.using(LAKEHOUSE_DB_ALIAS)`):
  `previous_version` / `next_version` / `get_specific_version`
  (`model_manager.py:86,111,131,151,174-215`), prefetch of related objects with
  `.latest()` (`prefetch_executor.py:227,323,422,…`), and **everything** when the
  deployment is `is_lakehouse_only` (`executor.py:208/242`,
  `application.py:112-123`).
- **Latest-version resolution** (lakehouse only): an INNER join to a `Metadata`
  sub-query with a *correlated* `next_version` (the version whose `prior_version`
  points back at this row), filtered by `next_version IS NULL OR next_version=''`
  (`data_query_transform.py:67-186`, `metadata_query.py:9-119`,
  `historical_builder/base.py:97-122`). `is_latest` is **derived**, never stored
  (`amsdal_utils …/metadata.py:57-65`, `return self.next_version is None`).

---

## 3. Write semantics per backend, and WHY the lock exists

For `bulk_update(using=None)` the ORM builds one `UpdateData(schema, data,
query=build_pk_query(obj))` per object, wraps the batch in an EXCLUSIVE
`LockCommand` (ACQUIRE → data → RELEASE) and performs it through the pipelined
`perform_data_command` / `perform_lock_command` (`model_manager.py:477-550`).

- **lakehouse** rewrites the update into an **INSERT of a new version** (+ a new
  `Metadata` row), stamping a fresh `object_version = get_identifier()` and
  `prior_version = <old version>`; there is **no in-place update and no stored
  `next_version`** (`connections/historical/data_mutation_transform/sync_transform.py:92-98,
  316-371, 243-246`). Delete appends a **tombstone** version (`is_deleted=True`),
  guarded by `next_version IS NULL OR ''` (`sync_transform.py:100-142, 261-262`).
- **state** does a plain in-place SQL `UPDATE` / `DELETE` — `PostgresStateConnection`
  is a bare `glue.PostgresConnection` with no versioning transform
  (`connections/postgresql_state.py:8`).

### The race the lock protects (the real justification)

The lakehouse update/delete is a **read-then-write across two separate DB
round-trips at the Python level**, not one atomic SQL statement:

1. `_resolve_object_versions` / `_fetch_metadata` **reads** the current version
   from the DB (`sync_transform.py:176-184, 223-231`);
2. a new `object_version` is generated and **inserted** with `prior_version =`
   the value just read (`sync_transform.py:207-208, 243-246`;
   executed at `postgresql_historical.py:235-236 / 502-509`).

Two concurrent writers both read `v(n)`, both insert successors with
`prior_version = v(n)`. Because `next_version` is the correlated subquery "who
points at me as prior" (`data_query_transform.py:118-150`), `v(n)` gets **two**
successors and **both** report `is_latest = true` → forked chain / corruption.

**This — a non-atomic read-current-then-insert-next — is why the ORM wraps the
operation in an EXCLUSIVE lock on the object PK.** On the state side there is no
version chain; the same lock only serializes ordinary in-place UPDATE/DELETE.

---

## 4. Transaction model (affects both lock choices)

- Transactions are driven through the pipelined `TransactionCommandService`, so
  `BEGIN` / `COMMIT` / `ROLLBACK` **each fan out to `[lakehouse, default]`**
  (`transactions/manager.py`; connection SQL at
  `postgres_connection/async_connection.py:626-691`).
- These are **two independent per-connection DB transactions** sharing a
  `transaction_id`; there is **no two-phase commit and no cross-DB atomicity**.
- **Commit-failure gap:** `commit()` commits lakehouse first, then state. If
  state's commit fails for a **top-level** transaction, the manager falls into a
  `...` TODO no-op branch — the already-committed lakehouse write is **not
  compensated** (`transactions/manager.py:118-134`, async `:339-342`). The two
  DBs are left inconsistent with only an exception raised. **This risk is
  independent of whether the lock is advisory or `FOR UPDATE`.**

### Ordered operations for `bulk_aupdate(objs, using=None)`

Each line is one connection hit (LH = lakehouse, ST = state):

```
 1. BEGIN            LH        7. RELEASE lock     LH   (result discarded)
 2. BEGIN            ST        8. RELEASE lock     ST
 3. ACQUIRE lock     LH        9. (check data result)
 4. ACQUIRE lock     ST       10. INSERT tx-record LH   (lakehouse only)
 5. UpdateData       LH       11. COMMIT           LH
 6. UpdateData       ST       12. COMMIT           ST
```

(`model_manager.py:539-550` + pipeline order + `manager.py` begin/commit.)
Note the explicit `RELEASE` (7-8) sits **before** the commits (11-12).

---

## 5. The two lock implementations

### 5a. Advisory (recommended)

`model_manager` builds `LockReference(reference=LockIdentifier(key, pool))`; the
base connection renders it via qcraft `compile_lock_command`
(`postgres_connection/sync_connection.py:793-826`). For `ACQUIRE / EXCLUSIVE /
WAIT / TRANSACTION` qcraft emits, per key (`extract.rs:2162-2219`):

```sql
SELECT pg_advisory_xact_lock(hashtextextended(%s, %s))   -- params: [key_str, 0]
```

The `str` key becomes the required `bigint` via **Postgres** `hashtextextended`
(not hashed in Rust). Function mapping (`advisory_fn_name`, `extract.rs:2221-2247`)
covers ACQUIRE×{EXCLUSIVE,SHARED}×{WAIT,NOWAIT}×{TRANSACTION,SESSION} and
RELEASE only for SESSION.

Timeline (`using=None`, per-connection; advisory taken on **both** because the
lock command is pipelined):

```
      LAKEHOUSE (version chain)                 STATE (snapshot)
t1    BEGIN                                      BEGIN
t2    SELECT pg_advisory_xact_lock(h(class:pk))  SELECT pg_advisory_xact_lock(h(class:pk))
t3    read latest version  ── inside the lock ──
t4    INSERT new version (prior=v(n))            UPDATE row in place
t5    (RELEASE removed — xact lock auto-releases)
t6    COMMIT  ← advisory auto-released           COMMIT ← advisory auto-released
```

A concurrent update/delete of the same object blocks at **t2** on the lakehouse
advisory until the first transaction commits at **t6** — the read-then-insert at
t3–t4 is serialized. Works even for objects whose rows do not yet exist.

**Hard constraints (code-verified):**

- **Scope must be `TRANSACTION`.** The planner **rejects `SESSION`** with
  `NotImplementedError` (`amsdal-glue …/planner/lock_planner.py:49-54`). Good news:
  `TRANSACTION` is exactly right — `pg_advisory_xact_lock` is held to commit,
  spanning the read-then-insert, and auto-releases on commit/rollback.
- **`pool` must be `'DEFAULT'`.** qcraft ignores `pool` (it only reads `key`,
  `extract.rs:2150-2152`), but the executor resolves the connection by `pool` as a
  **strict** dict lookup with **no DEFAULT fallback** for `LockIdentifier`
  (`lock_command_executor.py:46-53` → `RuntimeError` if missing). Under the
  pipeline the container already selects the DB; `pool` must simply name a key
  present in **both** containers — that is `'DEFAULT'` (`ConnectionAlias.DEFAULT`,
  registered with `schema_name=None`). A wrong `pool` → `RuntimeError` → failed
  `LockResult`.
- **Remove the explicit `RELEASE`.** qcraft rejects `RELEASE` on a
  `TRANSACTION`-scoped advisory lock (`extract.rs:2183-2191`); keeping
  `model_manager`'s `release_command` yields a guaranteed failed `LockResult` on
  every release. The lock auto-releases at commit/rollback.
- **Key derivation.** `key = f"{class_name}:{pk}"` (stable string from object
  identity — the same value the old `build_pk_query` predicate encoded). Update
  and delete of the same object must produce the **same** key.

**Problems / caveats:**

- **Cooperative:** only serializes writers that take the advisory lock. All
  mutation paths go through `model_manager`, so this holds — but a raw glue write
  bypassing it would not be serialized.
- **Hash collisions:** `hashtextextended` is 64-bit; two different keys could
  collide → occasional *false contention* (unnecessary blocking), never
  incorrect results.
- **SQLite:** unchanged — SQLite has no advisory locks; the SQLite connection
  keeps `BEGIN EXCLUSIVE` / `COMMIT` (`sqlite_connection/sync_connection.py:716-751`;
  qcraft rejects SQLite locks, `generator.rs:74-78`). This is dialect-inherent and
  identical under either option.

### 5b. `SELECT … FOR UPDATE`

The pre-migration lakehouse override
(`postgresql_historical.py:455-492`, on the **async** `AsyncPostgresHistoricalConnection`
only — the sync `PostgresHistoricalConnection` at `:126` has no override and
already inherits the qcraft base `acquire_lock`) FK-processes the PK predicate,
splits it per historical version, and per version runs
`SELECT * FROM <physical version table> WHERE <pk> FOR UPDATE`. To keep this in
the new glue it would be re-expressed via `QueryStatement.lock` (a `SelectLock`)
rendered by qcraft, since the old `sql_builders` (`build_from`/`build_where`) are
deleted.

Timeline (`using=None`):

```
      LAKEHOUSE (version chain)                 STATE (snapshot)
t1    BEGIN                                      BEGIN
t2    SELECT … WHERE pk FOR UPDATE   (per ver)   (FOR UPDATE not meaningful; see below)
t3    read latest version  ── inside the lock ──
t4    INSERT new version (prior=v(n))            UPDATE row in place
t5    COMMIT ← row locks released                COMMIT
```

**Problems / caveats:**

- **Still cooperative for this race.** The competitor does not modify `v(n)`'s
  row — it INSERTs a *new* successor. `FOR UPDATE` on `v(n)` only blocks it
  because the competitor *also* `FOR UPDATE`s `v(n)` first (via its own
  acquire step). So the DB-enforced-row-lock advantage does **not** translate into
  stronger protection for the insert-successor race than advisory gives.
- **Locks nothing if the row is absent** (e.g. a brand-new object) — no
  protection. Advisory always protects.
- **More moving parts:** per-version loop + `QueryStatement.lock` plumbing;
  reintroduces query-shape complexity the migration is removing.
- **State side gains nothing meaningful.** The pre-migration state connection's
  "lock" was `BEGIN EXCLUSIVE` — **SQLite syntax, not valid PostgreSQL**
  (`main:…/postgres_connection/sync_connection.py:474-503`). So on PG the state
  lock was historically a no-op/dubious; the real serialization came from the
  lakehouse `FOR UPDATE`. (Under advisory, state now gets a *real* advisory
  lock — a net improvement.)
- **SQLite:** same `BEGIN EXCLUSIVE` fallback as advisory — no difference.

### 5c. Side-by-side

| dimension | advisory | `FOR UPDATE` |
|---|---|---|
| serializes the version-chain read-modify-write | yes (block at ACQUIRE) | yes (block at row lock) |
| protects when object rows don't exist yet | **yes** | no (locks nothing) |
| cooperative (needs all writers to take it) | yes | yes (for this race) |
| DB-enforced against a *direct-SQL* writer of `v(n)` | no | yes (but no such path exists) |
| code complexity in the new glue | **low** (one call) | higher (per-version + `SelectLock`) |
| depends on deleted `sql_builders` | no | must re-express via `QueryStatement.lock` |
| held across read→insert | to commit (xact scope) | to commit (row lock) |
| SQLite behavior | `BEGIN EXCLUSIVE` (same) | `BEGIN EXCLUSIVE` (same) |
| new constraints | scope=TRANSACTION, pool=DEFAULT, drop RELEASE | per-version rewrite |

---

## 6. Recommendation & migration shape

Use **advisory** locks.

- **amsdal_models `model_manager.py`** (bulk update ~`:492-550`, bulk delete
  ~`:709-793`, and sync twins): build
  `LockReference(reference=LockIdentifier(key=f"{class_name}:{pk}", pool="DEFAULT"))`
  instead of `LockSchemaReference(query=…, schema=…)`; keep
  `mode=EXCLUSIVE, parameter=WAIT, scope=TRANSACTION` (default); **delete the
  `release_command` and its `perform_lock_command(release_command)` calls** (the
  xact lock auto-releases at commit).
- **amsdal_data `postgresql_historical.py`**: **remove the `acquire_lock`
  override** and the four broken imports (`get_pg_transform`, `build_from`,
  `build_where`, `ExecutionLockCommand`); the base connection renders advisory via
  qcraft.
- **Independent follow-up (not a lock concern):** the commit-failure gap in
  `transactions/manager.py:118-134` leaves lakehouse/state inconsistent on a
  partial commit. Worth tracking separately regardless of the lock choice.

---

## 7. Open / unconfirmed items

- Whether a deployment ever points state and lakehouse at the **same physical
  DB** (config-driven; `application.py:126,145-156`). If so, both fanned advisory
  calls hit one DB with the same key — harmless (idempotent re-entrant advisory in
  the same session), but noted.
- Exact SQL emitted by the base `glue.PostgresConnection` for `UpdateData` /
  `DeleteData` on the state path (lives in the glue lib; not opened here) — only
  the *absence* of a versioning transform on state is confirmed.
- The pre-migration base-Postgres `BEGIN EXCLUSIVE` lock was never confirmed to
  have run against real PG (invalid PG syntax).
- The `FOR UPDATE` override is **async-only**: it exists solely on
  `AsyncPostgresHistoricalConnection.acquire_lock` (`postgresql_historical.py:455`).
  The sync `PostgresHistoricalConnection` (`:126`) has no override and already
  routes through the qcraft base `acquire_lock`. So even before this migration the
  two paths were asymmetric — the per-version `FOR UPDATE` ran only on the async
  path.
