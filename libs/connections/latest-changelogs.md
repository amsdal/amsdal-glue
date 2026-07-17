## [v0.1.27](https://pypi.org/project/amsdal-glue-connections/0.1.27/) - 2026-07-03

### Added

- Postgres and SQLite connections (sync and async) now translate backend foreign key constraint failures into the typed `ForeignKeyViolationError`.
