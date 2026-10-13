## [v0.2.3](https://pypi.org/project/amsdal-glue-connections/0.2.3/) - 2026-10-13

### Added

- SQLite (sync and async) and Elasticsearch refuse `hnsw`, `ivfflat`, and the non-btree builtins (`hash`, `gin`, `gist`, `brin`) at the start of a schema command. The index is not degraded to btree and no statement from that command runs. Native Elasticsearch `knn_vector` mappings are unchanged.

### Fixed

- SQLite datetime values are stored as fixed-width UTC text (`YYYY-MM-DDTHH:MM:SS.ffffff+00:00`) so ordering and range filters follow instant order. Naive datetimes are rejected on write, including values that skip coercion. `TIMESTAMP` and `TIMESTAMPTZ` read back as aware UTC datetimes.
