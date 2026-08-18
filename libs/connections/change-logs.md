## [v0.2.0rc2](https://pypi.org/project/amsdal-glue-connections/0.2.0rc2/) - 2026-08-18

### Fixed

- Text-match lookups (`CONTAINS`, `ICONTAINS`, `STARTSWITH`, `ISTARTSWITH`, `ENDSWITH`, `IENDSWITH`) on a bare column reference now cast the column to text in the generated SQL (`col::text LIKE ...` on Postgres, `CAST(col AS text)` on SQLite). Postgres stores JSON columns as `jsonb`, which has no `LIKE`/`ILIKE` operator, so any substring filter on an array or dictionary column failed with `operator does not exist: jsonb ~~ unknown`. The cast is a no-op on text columns and does not change SQLite behaviour, where JSON is already stored as text.
- Regex lookups (`REGEX`, `IREGEX`) get the same text cast -- `~`/`~*` have no `jsonb` operator either, so they failed identically on Postgres.
- A NESTED field reference in any text-match or regex lookup now renders as the `->>` text extraction instead of a cast over the `->` chain. `(payload->'name')::text` is the quoted JSON serialization (`"Emil"`), so `STARTSWITH`/`ENDSWITH` on nested fields could never match the first or last character on Postgres while matching on SQLite; `->>` yields the unquoted text on both engines.

## [v0.2.0rc1](https://pypi.org/project/amsdal-glue-connections/0.2.0rc1/) - 2026-07-22

### Added

- SQL generation for SQLite and PostgreSQL is now backed by a native Rust engine, distributed as prebuilt binary wheels (Linux x86_64/aarch64, macOS arm64/x86_64, Windows x64); installation no longer requires a Rust toolchain.

### Changed

- Decimal values preserve full precision and integer values support arbitrary size in generated SQL.
- Schema introspection is now view-based.

### Fixed

- Elasticsearch index creation no longer blocks on single-node clusters.

## [v0.1.27](https://pypi.org/project/amsdal-glue-connections/0.1.27/) - 2026-07-03

### Added

- Postgres and SQLite connections (sync and async) now translate backend foreign key constraint failures into the typed `ForeignKeyViolationError`.

## [v0.1.26](https://pypi.org/project/amsdal-glue-connections/0.1.26/) - 2026-06-15

### Added

- Fixed-precision decimal support via `DecimalSchemaModel`: Postgres maps to `NUMERIC(precision, scale)` and SQLite to `DECIMAL_TEXT(precision, scale)`.
- `Decimal` value type transform for Postgres (`NUMERIC`) and SQLite (`DECIMAL_TEXT`), with SQLite storing decimals as text to preserve precision.

### Changed

- Postgres and SQLite type introspection now reconstructs `DecimalSchemaModel` (with `precision`/`scale`) when reading back `NUMERIC` / `DECIMAL_TEXT` columns instead of coercing them to `float`.

## [v0.1.25](https://pypi.org/project/amsdal-glue-connections/0.1.25/) - 2026-05-20

### Added

- `Exists` subquery support across SQL, CSV, and Elasticsearch connections.
- JSONB array expression support for Postgres.
- Polars final query executor with negation-aware in-memory join and filter.
- Default projection handling in query builder.
- Nested subquery support in query builder.

### Changed

- Improved query builder for subqueries and conditions.

### Fixed

- CSV and Elasticsearch conditions safety (proper negation handling).
- Postgres value transform edge cases.

## [v0.1.24](https://pypi.org/project/amsdal-glue-connections/0.1.24/) - 2026-05-06

### Changed

- Postgres and SQLite (sync + async) connections now raise `UniqueViolationError` on unique constraint violations.

### Fixed

- Postgres `regex` / `iregex` lookups now use the correct `~` / `~*` operators instead of the unsupported `REGEXP` syntax.

## [v0.1.23](https://pypi.org/project/amsdal-glue-connections/0.1.23/) - 2026-01-13

### Fixed

- Fix for creating index in postgres

## [v0.1.22](https://pypi.org/project/amsdal-glue-connections/0.1.22/) - 2025-12-21

### Changed

- Libs update

## [v0.1.21](https://pypi.org/project/amsdal-glue-connections/0.1.21/) - 2025-11-03

### Fixed

- Fix for vector async operations

## [v0.1.20](https://pypi.org/project/amsdal-glue-connections/0.1.20/) - 2025-09-21

### Fixed

- Fix for nested transactions in SQLite connection during schema migration

## [v0.1.19](https://pypi.org/project/amsdal-glue-connections/0.1.19/) - 2025-09-20

### Changed

- Recreate table in sqlite on constraint changes

## [v0.1.18](https://pypi.org/project/amsdal-glue-connections/0.1.18/) - 2025-09-04

### Fixed

- Fixed drop null in the postgres connection

## [v0.1.17](https://pypi.org/project/amsdal-glue-connections/0.1.17/) - 2025-09-03

### Fixed

- Fix for foreign key regexp in SQLite

## [v0.1.16](https://pypi.org/project/amsdal-glue-connections/0.1.16/) - 2025-08-06

### Added

- Elasticsearch connection

## [v0.1.15](https://pypi.org/project/amsdal-glue-connections/0.1.15/) - 2025-06-26

### Added

- Added support for vector operations

## [v0.1.14](https://pypi.org/project/amsdal-glue-connections/0.1.14/) - 2025-06-17

### Changed

- Update package manager to `uv` for better performance and compatibility.

## [v0.1.13](https://pypi.org/project/amsdal-glue-connections/0.1.13/) - 2025-06-10

### Fixed

- Fixes for JSON in connections

## [v0.1.12](https://pypi.org/project/amsdal-glue-connections/0.1.12/) - 2025-06-09

### Fixed

- Fix for SQLite table info retrieval

## [v0.1.11](https://pypi.org/project/amsdal-glue-connections/0.1.11/) - 2025-05-22

### Fixed

- Fixed locking for async sqlite

## [v0.1.10](https://pypi.org/project/amsdal-glue-connections/0.1.10/) - 2025-05-19

### Added

- Raise NOT NULL constraint failed for SQLite update column
- Added DEFAULT for column in sql builder

## [v0.1.9](https://pypi.org/project/amsdal-glue-connections/0.1.9/) - 2025-05-14

### Changed

- Changes for tables retrieval

## [v0.1.8](https://pypi.org/project/amsdal-glue-connections/0.1.8/) - 2025-05-06

### Fixed

- Fixed 'references' SQL

## [v0.1.7](https://pypi.org/project/amsdal-glue-connections/0.1.7/) - 2025-04-01

### Fixed

- FK names in SQLite

## [v0.1.6](https://pypi.org/project/amsdal-glue-connections/0.1.6/) - 2025-03-18

### Added

- Add `csv` as an optional dependency.

## [v0.1.5](https://pypi.org/project/amsdal-glue-connections/0.1.5/) - 2025-03-17

### Added

- Support inline unique definition in SQLite

## [v0.1.4](https://pypi.org/project/amsdal-glue-connections/0.1.4/) - 2025-03-14

### Changed

- Remove `exception` logs from connections

## [v0.1.3](https://pypi.org/project/amsdal-glue-connections/0.1.3/) - 2025-03-13

### Fixed

- Adjustments for limit in CSV Connection

## [v0.1.2](https://pypi.org/project/amsdal-glue-connections/0.1.2/) - 2025-03-02

### Added

- CSV Connection

## [v0.1.1](https://pypi.org/project/amsdal-glue-connections/0.1.1/) - 2025-02-25

### Fixed

- Fixed ANY in postgresql


## [v0.1.0](https://pypi.org/project/amsdal-glue-connections/0.1.0/) - 2025-02-24

### Changed

- Builder helpers
- Conditions


## [v0.0.21](https://pypi.org/project/amsdal-glue-connections/0.0.21/) - 2024-02-13

### Fixes

- Disable locking in SQLite connection.

## [v0.0.20](https://pypi.org/project/amsdal-glue-connections/0.0.20/) - 2025-02-06

### Added

- Postgres locking with `SELECT FOR UPDATE`.

## [v0.0.19](https://pypi.org/project/amsdal-glue-connections/0.0.19/) - 2024-12-18

### Fixes

- Postgres is_alive check.

## [v0.0.18](https://pypi.org/project/amsdal-glue-connections/0.0.18/) - 2024-12-05

### Added

- Postgres async connection.

## [v0.0.17](https://pypi.org/project/amsdal-glue-connections/0.0.17/) - 2024-11-14

### Added

- Async connections support.

## [v0.0.16](https://pypi.org/project/amsdal-glue-connections/0.0.16/) - 2024-10-18

### Changed

- Use 'JSONB' instead of 'JSON' in Postgres connections.

## [v0.0.15](https://pypi.org/project/amsdal-glue-connections/0.0.15/) - 2024-10-18

### Fixed

- Error messages (error-messages)
- Postgres connection index retrieval (postgres-connection-index-retrieval)


## [v0.0.14](https://pypi.org/project/amsdal-glue-connections/0.0.14/) - 2024-10-15

### Fixed

- Fixed postgres field update to DOUBLE PRECISION and BIGINT (postgres-field-update)

## [v0.0.13](https://pypi.org/project/amsdal-glue-connections/0.0.13/) - 2024-10-14

### Added

- Nested types (nested-types)

## [v0.0.12](https://pypi.org/project/amsdal-glue-connections/0.0.12/) - 2024-09-16

### Added

- Added ability to use math expressions in annotations. (math-expressions)
## [v0.0.11](https://pypi.org/project/amsdal-glue-connections/0.0.11/) - 2024-08-06

### Added

- Documentation via docstrings (documentation)

### Changed

- PostgresConnection: autocommit=True by default (autocommit-true)
## [v0.0.10](https://pypi.org/project/amsdal-glue-connections/0.0.10/) - 2024-08-02


### Fixed

- Fixed dependencies (fixed-dependencies)



## [v0.0.9](https://pypi.org/project/amsdal-glue-connections/0.0.9/) - 2024-08-02


### Added

- Typing added (typing-added)
