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
