# Task 13 Report – ALTER/DROP/RENAME DDL Golden Tests

## Status
COMPLETE

## Commit SHA
47cf8a7e32f5ffb4c39805805efedfdc83846a13

## Test summary
18 passed, 2 xfailed (20 tests total)

## File created
`libs/connections/tests/golden/test_alter_table.py`

## Introspection-bound / xfailed mutations
- **SQLite AddConstraint** (`test_add_constraint_sqlite`): xfail(strict=True)  
  `_recreate_table_with_constraints` calls `self.connection.execute('BEGIN')` on the raw `sqlite3.Connection` (not through the overridable `execute()` hook).  The recording harness never establishes a DB connection → `ConnectionError('Connection not established')`.
- **SQLite DeleteConstraint** (`test_delete_constraint_sqlite`): xfail(strict=True)  
  Same path as AddConstraint.

## Non-deterministic mutation handled structurally
- **SQLite UpdateProperty** (`test_update_property_sqlite`): NOT xfailed — runs cleanly via recording harness.  
  The 4-step workaround (ADD temp UUID column → UPDATE/copy → DROP original → RENAME temp→original) embeds a `uuid.uuid4().hex` temp column name that is non-deterministic.  Test asserts structural shape (len=4, prefix/suffix patterns) instead of exact byte-for-byte SQL.

## Class-name corrections
None — all class names in `schema.py` matched the brief exactly: `AddProperty`, `DeleteProperty`, `RenameProperty`, `UpdateProperty`, `AddConstraint`, `DeleteConstraint`, `AddIndex`, `DeleteIndex`, `DeleteSchema`, `RenameSchema`.

## KNOWN-DIVERGENCE markers applied
1. **`test_update_property_pg`**: PG UpdateProperty emits `ALTER COLUMN TYPE … , ALTER COLUMN DROP NOT NULL` as a comma-separated sequence in one `ALTER TABLE` statement.
2. **`test_add_constraint_pg`** (UniqueConstraint): PG `_build_constraint` does NOT quote the constraint name — `CONSTRAINT uq_person_email UNIQUE ("email")` instead of `CONSTRAINT "uq_person_email" UNIQUE ("email")`. Same inconsistency documented in `test_create_table.py`; FK names ARE quoted.

## Both dialects covered
- AddProperty: SQLite ✓ PG ✓
- DeleteProperty: SQLite ✓ PG ✓
- RenameProperty: SQLite ✓ PG ✓
- UpdateProperty: SQLite ✓ (structural) PG ✓
- AddConstraint: SQLite xfail PG ✓
- DeleteConstraint: SQLite xfail PG ✓
- AddIndex: SQLite ✓ PG ✓
- DeleteIndex: SQLite ✓ PG ✓
- DeleteSchema (DROP TABLE): SQLite ✓ PG ✓
- RenameSchema (RENAME TABLE): SQLite ✓ PG ✓
