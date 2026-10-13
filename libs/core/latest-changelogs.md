## [v0.2.4](https://pypi.org/project/amsdal-glue-core/0.2.4/) - 2026-10-13

### Added

- SQLite and Elasticsearch schema commands now refuse an index type other than btree before any DDL runs. `UnsupportedIndexTypeError` names the index, the field, the type, and the backend, and says to declare the index on PostgreSQL or omit the type to use btree.

### Fixed

- Datetime coercion for `TIMESTAMP` and `TIMESTAMPTZ` now requires an offset or a `Z` suffix, converts aware values to UTC, and rejects naive datetimes and bare dates. Naive values are not treated as UTC.
