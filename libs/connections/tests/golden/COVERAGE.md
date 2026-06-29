# Golden-Master SQL Test Coverage

This document is the canonical reference for Plan 1 golden-master test coverage.
It consolidates the feature matrix, corpus inventory, registered divergences,
coverage gaps, and Plan 3 normalization requirements.

---

## 1. Synthetic Feature Matrix (Tasks 2–14)

Each cell shows: **covered** | `xfail:<reason>` | `skip:<reason>` | **DIVERGENCE (see §3)**.

| Feature / Category | PG (sync) | SQLite (sync) | Notes |
|--------------------|-----------|---------------|-------|
| **SELECT — star** | covered | covered | `test_select.py` |
| **SELECT — column list** | covered | covered | `test_select.py` |
| **SELECT — aliased column** | covered | covered | `test_select.py` |
| **SELECT — DISTINCT** | DIVERGENCE | DIVERGENCE | builder silently ignores `distinct`; see §3-D1 |
| **SELECT — DISTINCT ON** | DIVERGENCE | n/a | PG-only; builder silently ignores; see §3-D1 |
| **WHERE — EQ/NEQ/GT/GTE/LT/LTE** | covered | covered | `test_where_operators.py` |
| **WHERE — IN** | DIVERGENCE | covered | PG triple-nested params bug; see §3-D2 |
| **WHERE — CONTAINS** | DIVERGENCE | covered (GLOB) | PG uses `*oo*` not `%oo%`; see §3-D3 |
| **WHERE — ICONTAINS** | covered | covered | |
| **WHERE — STARTSWITH/ENDSWITH** | covered | covered (GLOB) | |
| **WHERE — ISTARTSWITH/IENDSWITH** | covered | covered | |
| **WHERE — REGEX/IREGEX** | covered | covered | |
| **WHERE — ISNULL** | covered | covered | |
| **WHERE — EXACT** | covered | covered | `IS` semantics |
| **Conditions — AND** | covered | covered | `test_conditions.py` |
| **Conditions — OR** | covered | covered | |
| **Conditions — nested AND/OR** | covered | covered | |
| **Conditions — NOT (single)** | covered | covered | |
| **Conditions — NOT (group)** | covered | covered | |
| **Conditions — double negation** | covered | covered | elim. correct |
| **JOINs — INNER** | covered | covered | `test_joins.py` |
| **JOINs — LEFT** | covered | covered | |
| **JOINs — RIGHT** | covered | covered | SQLite ≥3.39.0; floor ≥3.45.0 (JSONB) means emitting is always correct — see §3-D4 |
| **JOINs — FULL** | covered | covered | SQLite ≥3.39.0; floor ≥3.45.0 (JSONB) means emitting is always correct — see §3-D4 |
| **JOINs — multiple** | covered | covered | |
| **JOINs — subquery** | covered | covered | |
| **Aggregations — COUNT/SUM/AVG/MIN/MAX** | covered | covered | `test_aggregations.py` |
| **GROUP BY — single field** | covered | covered | |
| **GROUP BY — multi field** | by-design | covered | `SELECT *` under GROUP BY is caller's responsibility (use `only=[...]`); see §3-D5 |
| **GROUP BY — multi field + agg** | covered | covered | realistic case |
| **ORDER BY — ASC/DESC** | covered | covered | `test_order_limit.py` |
| **ORDER BY — multi field** | covered | covered | |
| **LIMIT only** | covered | covered | values inlined (not parameterised) |
| **LIMIT + OFFSET** | covered | covered | values inlined |
| **Annotations — value** | covered | covered | `test_annotations.py` |
| **Annotations — expression (field ref)** | covered | covered | |
| **Annotations — subquery** | covered | covered | |
| **INSERT — single row** | covered | covered | `test_insert.py` |
| **INSERT — multi-row** | covered | covered | |
| **UPDATE — with WHERE** | covered | covered | `test_update.py` |
| **UPDATE — without WHERE** | covered | covered | |
| **DELETE — with WHERE** | covered | covered | `test_delete.py` |
| **DELETE — without WHERE** | covered | covered | |
| **CREATE TABLE — columns + defaults** | covered | covered | `test_create_table.py` |
| **CREATE TABLE — PRIMARY KEY** | DIVERGENCE | covered | PG: unquoted name + trailing space; see §3-D6 |
| **CREATE TABLE — UNIQUE** | DIVERGENCE | covered | PG: unquoted name; see §3-D7 |
| **CREATE TABLE — FOREIGN KEY** | covered | DIVERGENCE | SQLite: `reference_fields` unquoted; see §3-D8 |
| **CREATE TABLE — CHECK** | DIVERGENCE | covered | PG: unquoted name; see §3-D9 |
| **CREATE INDEX (standalone AddIndex)** | covered | covered | |
| **ALTER — AddProperty** | covered | covered | `test_alter_table.py` |
| **ALTER — DeleteProperty** | covered | covered | |
| **ALTER — RenameProperty** | covered | covered | |
| **ALTER — UpdateProperty** | DIVERGENCE | covered (shape) | PG: multi-ALTER comma-join; SQLite: UUID temp col |
| **ALTER — AddConstraint (UniqueConstraint)** | DIVERGENCE | `xfail`: live-DB | PG: unquoted name; see §3-D7; SQLite needs live DB |
| **ALTER — AddConstraint (PrimaryKeyConstraint)** | DIVERGENCE | `xfail`: live-DB | PG: unquoted name + trailing space; see §3-D12; SQLite needs live DB |
| **ALTER — AddConstraint (ForeignKeyConstraint)** | covered | `xfail`: live-DB | PG: clean; SQLite needs live DB |
| **ALTER — AddConstraint (CheckConstraint)** | DIVERGENCE | `xfail`: live-DB | PG: unquoted name; see §3-D13; SQLite needs live DB |
| **ALTER — DeleteConstraint** | covered | `xfail`: live-DB | SQLite needs live DB |
| **ALTER — AddIndex** | covered | covered | |
| **ALTER — DeleteIndex** | covered | covered | |
| **DROP TABLE (DeleteSchema)** | covered | covered | |
| **RENAME TABLE (RenameSchema)** | covered | covered | |
| **Lock — EXCLUSIVE acquire** | DIVERGENCE | `xfail`: live-DB | PG sync: `BEGIN EXCLUSIVE`; see §3-D10 |
| **Lock — EXCLUSIVE release** | DIVERGENCE | `xfail`: live-DB | PG sync: `COMMIT`; see §3-D10 |
| **Lock — SHARED (acquire/release)** | covered (no-op) | covered (no-op) | |
| **Lock — async PG SELECT…FOR UPDATE** | covered | n/a | `test_lock.py` async tests; see §3 for clean characterization |

**Golden suite (current):** 155 passed, 4 xfailed.

**async variants:** the async PG lock path (`SELECT … FOR UPDATE`) is now covered by synthetic
tests via `_RecordingAsyncPG` in the recording harness (Task 21). All other async PG/SQLite
paths are SQL-text captured by the corpus (Tasks 16–17) — params are not asserted by the
corpus gate (see §4.1).

---

## 2. Corpus Inventory (Tasks 16–18)

### 2.1 `corpus/glue.jsonl`

- **Rows:** 696
- **Distinct nodeids:** 117
- **Connection types (`fn`):** `sqlite` 258, `sqlite_async` 249, `pg` 189
- **SQL shape by leading keyword:** SELECT 240, PRAGMA 196, CREATE 150, INSERT 102, UPDATE 4, DELETE 4
- **`_metadata` rows:** 0 (glue unit/integration tests do not exercise the amsdal_data `_metadata` pattern)
- **Source:** `libs/connections/tests/` (unit + integration), excluding Elasticsearch (no container) and CSV (no SQL)

### 2.2 `corpus/amsdal_data.jsonl`

- **Rows:** 2094
- **Distinct nodeids:** 41
- **Connection types (`fn`):** `sqlite` 782, `sqlite_async` 543, `pg` 397, `pg_async` 372
- **SQL shape by leading keyword:** SELECT 965, CREATE 585, PRAGMA 254, INSERT 252, ALTER 32, UPDATE 4, DROP 2
- **`_metadata` rows:** 263 — real multi-join `_metadata` table patterns from the ORM
- **Notable shape:** multi-join SELECT across `_metadata` + domain tables, all 4 dialects
- **Plan 3 requirement:** volatile `__v__<hex32>` identifiers appear in 463 rows (see §5)

### 2.3 `corpus/amsdal_models.jsonl`

- **Rows:** 108
- **Distinct nodeids:** 18
- **Connection types (`fn`):** `sqlite` 108 (SQLite only; amsdal_models uses only SQLite backend)
- **SQL shape by leading keyword:** CREATE 72, SELECT 36
- **`_metadata` rows:** 36

### 2.4 Corpus totals

~2,898 rows across 176 distinct nodeids, 4 connection types, 3 packages.

### 2.5 Areas NOT captured in any corpus

| Area | Reason |
|------|--------|
| Elasticsearch tests (22 tests) | No ES container available at capture time |
| CSV backend | Emits no SQL (file-based, not SQL-backed) |
| 2 top-level unit files | Excluded: no SQL-generating code paths |
| amsdal_data/amsdal_models `pg_async` DeleteConstraint / AddConstraint | Not exercised by those packages' test suites |

---

## 3. Registered KNOWN-DIVERGENCES

All are documented as `KNOWN-DIVERGENCE (migration):` in the test source. The assertions
**lock the current (buggy) output** — they FAIL on correct Rust output and must be
re-baselined in Plan 3.

| ID | File : Lines | Current (buggy) output | Correct SQL after migration |
|----|-------------|------------------------|----------------------------|
| D1 | `test_select.py:38,47,82` | `SELECT * FROM "users"` / `SELECT * FROM 'users'` (no DISTINCT) | `SELECT DISTINCT * FROM …` / `SELECT DISTINCT ON (…) * FROM …`; see §3.1 |
| D2 | `test_where_operators.py:60-64` | PG IN params `[[[1, 2, 3]]]` | `[[1, 2, 3]]` |
| D3 | `test_where_operators.py:65-70` | PG CONTAINS: `LIKE %s` with `'*oo*'` | `LIKE %s` with `'%oo%'`; see §3.1 |
| D4 | `test_joins.py:54-78` | SQLite emits `RIGHT JOIN` / `FULL JOIN` — characterization only (**NOT a divergence**) | NOT a bug — tests document correct behaviour; see §3.1 |
| D5 | `test_aggregations.py:92-98` | PG `SELECT * FROM "orders" GROUP BY …` — by-design (**caller must supply `only`**) | by-design — caller's responsibility; not a generator bug; see §3.1 |
| D6 | `test_create_table.py:113-128` | PG PrimaryKeyConstraint: `CONSTRAINT pk_person PRIMARY KEY ("id") ` (unquoted + trailing space) | `CONSTRAINT "pk_person" PRIMARY KEY ("id")` |
| D7 | `test_create_table.py:179-195`, `test_alter_table.py:184-190` | PG UniqueConstraint: `CONSTRAINT uq_person_email UNIQUE (…)` (unquoted) | `CONSTRAINT "uq_person_email" UNIQUE (…)` |
| D8 | `test_create_table.py:223-234` | SQLite FK reference_fields: `(id)` unquoted | `('id')` |
| D9 | `test_create_table.py:328-344` | PG CheckConstraint: `CONSTRAINT chk_age_positive CHECK (…)` (unquoted) | `CONSTRAINT "chk_age_positive" CHECK (…)` |
| D10 | `test_lock.py:9,58,75` | PG sync `acquire_lock` emits `BEGIN EXCLUSIVE`; `release_lock` emits `COMMIT` | PG native: `SELECT … FOR UPDATE` / `COMMIT` (transaction context); see §3.1 |
| D11 | `test_alter_table.py:149` | PG UpdateProperty: `ALTER TABLE … ALTER COLUMN TYPE …, ALTER COLUMN … DROP NOT NULL` (comma-joined) | correct multi-ALTER syntax — verify at re-baseline |
| D12 | `test_alter_table.py:233-235` | PG PrimaryKeyConstraint ALTER-AddConstraint: `CONSTRAINT pk_person PRIMARY KEY ("id") ` (unquoted name + trailing space) | `CONSTRAINT "pk_person" PRIMARY KEY ("id")` (quoted, no trailing space) |
| D13 | `test_alter_table.py:272-274` | PG CheckConstraint ALTER-AddConstraint: `CONSTRAINT chk_age_positive CHECK ("Person"."age" > 0)` (unquoted name) | `CONSTRAINT "chk_age_positive" CHECK ("Person"."age" > 0)` |

**Total registered divergences: 13** (D1 covers 3 test lines, D4 covers 2 dialect branches, D7 covers 2 files).
**Real-bug count after reclassification: 11** — D4 and D5 are non-bugs; their characterization tests document correct behaviour and must NOT be re-baselined for correct Rust output.

### 3.1 Classification notes

**D1 — refined description:**
DISTINCT (and DISTINCT ON) are dropped ONLY when only is empty (SELECT *), for BOTH dialects — build_only_constructor.py returns None before the distinct branch. Safe to fix additively: amsdal never forwards distinct into glue QueryStatement (confirmed: no distinct= kwarg reaches glue.QueryStatement(...) in amsdal_models/amsdal_data).

**D3 — CONTAINS operator (SQLite path is correct):**
SQLite path is CORRECT — GLOB uses '*' as its wildcard (operator_constructor.py:158). Only the PG path is wrong (postgres_utils/operator_constructor.py:76-78 uses LIKE with '*' instead of '%').

**D4 — NOT a divergence (characterization only):**
SQLite floor enforced at >=3.45.0 (amsdal_data sqlite_historical.py:38 / async_sqlite_historical.py:46, JSONB requirement); RIGHT/FULL JOIN need only 3.39.0, so emitting them is always correct. The existing characterization tests now document correct behaviour, not a bug.

**D5 — by-design (caller must supply only):**
The generator renders the QueryStatement literally; SELECT * under GROUP BY is invalid in PG, but choosing the projection is the caller's responsibility (set only=[...]). The Rust generator emits the same SELECT *. Not a generator bug.

**D10 — migration design requirement:**
LockCommand is intended to map to an advisory lock (e.g. pg_advisory_lock); none exists in the stack today (grep found no advisory/pg_advisory/GET_LOCK). Row-level SELECT ... FOR UPDATE will be added later as a QueryStatement, not a LockCommand. Both the sync BEGIN EXCLUSIVE and the async historical FOR UPDATE override (amsdal_data postgresql_historical.py:455) diverge from this intent: AsyncPostgresHistoricalConnection overrides acquire_lock with FOR UPDATE, while the SYNC PostgresHistoricalConnection inherits glue's broken BEGIN EXCLUSIVE.

---

## 4. Coverage Gaps / Not-Captured Areas

| Gap | Source | Impact for Plan 3 |
|-----|--------|-------------------|
| SQLite `AddConstraint` / `DeleteConstraint` (any constraint type) | Requires live DB (`_recreate_table_with_constraints` hits `self.connection.execute('BEGIN')` on raw sqlite3.Connection); marked `xfail(strict=True)` | Must verify via corpus/integration tests post-migration |
| No namespace-prefix variants | `_rename_column` computes a namespace prefix but never uses it (latent bug noted in Task 13); no golden tests with non-default namespace | Document as open risk; verify manually |
| Elasticsearch (22 tests) | No ES container | Out of scope for SQL golden tests |
| CSV backend | No SQL emitted | Out of scope |
| `PRAGMA` statements | 196 (glue) + 254 (amsdal_data) corpus rows are PRAGMA; not in synthetic suite | SQLite-specific; covered by corpus only |
| `LIMIT`/`OFFSET` inlining | Values inlined (not parameterised); if Rust switches to parameterised LIMIT/OFFSET, corpus rows will mismatch | Watch during Plan 3 re-baseline |

**CLOSED gaps (no longer open):**

| Gap | Closed by |
|-----|-----------|
| Async PG `SELECT … FOR UPDATE` (lock path) | `test_lock.py`: `test_pg_async_acquire_lock_emits_for_update`, `test_pg_async_acquire_lock_no_query_is_noop`, `test_pg_async_release_lock_is_noop` (Task 21) |
| PG `AddConstraint` — PrimaryKeyConstraint / ForeignKeyConstraint / CheckConstraint not exercised | `test_alter_table.py`: `test_add_constraint_pg_primary_key`, `test_add_constraint_pg_foreign_key`, `test_add_constraint_pg_check` (Task 21) |

### 4.1 Parity gate limitations

The corpus assert-gate (`capture_plugin` assert-mode) compares **SQL text only — query parameters are captured but NOT compared**. A migration that changes parameterization while leaving SQL text identical passes the gate silently.

- Synthetic per-feature tests (§1) assert the full `(sql, params)` tuple, so the feature categories they cover are param-safe.
- The param blind spot applies to corpus-only paths: async pg/sqlite, `_metadata` multi-joins, and PRAGMA statements. These are SQL-text captured (params not asserted) — do NOT treat them as fully covered by the corpus.
- Plan 3 follow-up: extend the gate to compare params too, which REQUIRES normalizing volatile param content (uuids, timestamps, and `__v__<hex>` version hashes) the same way SQL text will be normalized.

**Gate activation:** The assert-gate is INERT unless BOTH `-p tests.golden.capture_plugin` (or `-p capture_plugin` with `PYTHONPATH=.../tests/golden`) AND `--assert-sql=<corpus>` are passed, and it must run serial (`-n0`). With the flags omitted the golden tests pass trivially.

---

## 5. Plan 3 Requirements

### 5.1 Version-hash normalisation (amsdal_data corpus)

`amsdal_data` embeds volatile version identifiers of the form `__v__<32 hex chars>` in
table names and column references (e.g. `__v__a3f9c12b…`). These are generated fresh each
test run, so the stored corpus SQL and the re-run SQL will always differ in those tokens.

**Out of 2094 amsdal_data rows, 463 contain at least one `__v__<hex>` token.**

Plan 3's assert-mode pass (re-run with `--assert-sql`) **must normalise** both the stored
corpus SQL and the live observed SQL before comparison. Recommended regex:

```python
import re


def normalise(sql: str) -> str:
    return re.sub(r'__v__[0-9a-f]{32}', '__v__HASH', sql)
```

Apply in the plugin's `_record` function (capture mode: normalise before writing) and in
`pytest_configure` (assert mode: normalise stored corpus at load time).

### 5.2 Plugin load recipe

When capturing or asserting from packages outside `libs/connections/tests/`:

```bash
PYTHONPATH=/path/to/libs/connections:$PYTHONPATH \
  python -m pytest -p tests.golden.capture_plugin -n0 \
    --capture-sql=corpus/<package>.jsonl \
    <target test directory>
```

**Important:** `PYTHONPATH` must point to `libs/connections` (not `libs/connections/tests/`).
Using `tests/` causes the local `tests/csv/` subpackage to shadow the stdlib `csv` module.

### 5.3 Re-baseline procedure for each Rust-fixed divergence

1. Run the golden suite with the new Rust generator: identify which DIVERGENCE tests now
   fail (expected output changed).
2. Run `--capture-sql` with the new generator to refresh the expected value.
3. Update the test assertion and remove the `# KNOWN-DIVERGENCE` comment.
4. Re-run `hatch run all` to gate style/typing.

---

## 6. Test File to Feature Mapping

| Synthetic test file | Feature area |
|---------------------|--------------|
| `test_select.py` | SELECT *, column list, aliases, DISTINCT |
| `test_where_operators.py` | All WHERE lookup operators (15 + ISNULL) |
| `test_conditions.py` | AND, OR, nested, NOT, double negation |
| `test_joins.py` | INNER, LEFT, RIGHT, FULL, multiple, subquery |
| `test_aggregations.py` | COUNT/SUM/AVG/MIN/MAX, GROUP BY (single/multi/agg) |
| `test_order_limit.py` | ORDER BY ASC/DESC/multi, LIMIT, OFFSET |
| `test_annotations.py` | ValueAnnotation, ExpressionAnnotation, SubQueryAnnotation |
| `test_insert.py` | INSERT single/multi, both dialects |
| `test_update.py` | UPDATE with/without WHERE, both dialects |
| `test_delete.py` | DELETE with/without WHERE, both dialects |
| `test_create_table.py` | CREATE TABLE + PK/UNIQUE/FK/CHECK + CREATE INDEX |
| `test_alter_table.py` | AddProperty/DeleteProperty/RenameProperty/UpdateProperty/AddConstraint/DeleteConstraint/AddIndex/DeleteIndex/DeleteSchema/RenameSchema |
| `test_lock.py` | acquire_lock/release_lock EXCLUSIVE/SHARED, PG+SQLite |
| `_harness.py` | Shared recording-connection infrastructure |
| `capture_plugin.py` | Corpus capture/assert plugin (Track B) |
| `test_harness_selftest.py` | Harness smoke tests |
| `test_capture_plugin_selftest.py` | Plugin self-tests (roundtrip, order-independence, two-sided) |
| `corpus/glue.jsonl` | Real traffic from `libs/connections` tests (696 rows, 117 nodeids) |
| `corpus/amsdal_data.jsonl` | Real traffic from `amsdal_data` tests (2094 rows, 41 nodeids) |
| `corpus/amsdal_models.jsonl` | Real traffic from `amsdal_models` tests (108 rows, 18 nodeids) |
