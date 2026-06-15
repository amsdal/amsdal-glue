## [v0.1.26](https://pypi.org/project/amsdal-glue-connections/0.1.26/) - 2026-06-15

### Added

- Fixed-precision decimal support via `DecimalSchemaModel`: Postgres maps to `NUMERIC(precision, scale)` and SQLite to `DECIMAL_TEXT(precision, scale)`.
- `Decimal` value type transform for Postgres (`NUMERIC`) and SQLite (`DECIMAL_TEXT`), with SQLite storing decimals as text to preserve precision.

### Changed

- Postgres and SQLite type introspection now reconstructs `DecimalSchemaModel` (with `precision`/`scale`) when reading back `NUMERIC` / `DECIMAL_TEXT` columns instead of coercing them to `float`.
