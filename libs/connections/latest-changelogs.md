## [v0.1.24](https://pypi.org/project/amsdal-glue-connections/0.1.24/) - 2026-05-06

### Changed

- Postgres and SQLite (sync + async) connections now raise `UniqueViolationError` on unique constraint violations.

### Fixed

- Postgres `regex` / `iregex` lookups now use the correct `~` / `~*` operators instead of the unsupported `REGEXP` syntax.
