## [v0.2.2](https://pypi.org/project/amsdal-glue-connections/0.2.2/) - 2026-09-30

### Fixed

- Fixed Postgres index introspection reporting custom access methods (e.g. pgvector's `hnsw` / `ivfflat`) as `BuiltinIndexType.BTREE` instead of the real access method. Added golden and pgvector/pg17 integration test coverage for `hnsw`/`ivfflat` indexes with operator classes and `WITH (...)` parameters, and documented the related pgvector limits (2000-dimension cap, `lists` scaling, no `CONCURRENTLY` on inline-declared indexes) in code comments.

  Also fixed, from review of the above:

  - `TABLE_INDEX_REGISTRY` now selects `ic.reloptions`, parsed back into `IndexSchema.parameters` -- previously the registry view never selected it at all, so every index declared with `WITH (...)` (pgvector's `m` / `ef_construction` / `lists`, or any other storage parameter) compared unequal to its own introspection.
  - `TABLE_INDEX_REGISTRY` now also selects the unconditional `opc.opcname` as `default_op_class`; `IndexSchema._fields_equal` uses it to resolve a declared `op_class` that names the access method's default (e.g. btree's `text_ops` on a `TEXT` column) against the introspected row, where it is nulled by the existing `opc.opcdefault` check.
  - `_resolve_index_type` casefolds the catalog access-method name before building a `CustomIndexType`, so a declaration using a different case (e.g. `CustomIndexType(name='HNSW')`) still equals its always-lowercase introspection.
  - A declared `IndexSchema.include` now raises `UnsupportedFeatureError` when building DDL for SQLite instead of being silently dropped -- the SQLite renderer has no `INCLUDE` support and SQLite's catalog has no `is_included` row to introspect back, so the previous behaviour was a permanent, silent round-trip failure.
  - `CustomIndexType.name`, `IndexField.op_class`, and index-parameter keys/values are now validated (bare identifier / safe-literal allow-list) before reaching the DDL renderer. They were previously spliced verbatim into the generated statement with no quoting and no bind parameters, so a crafted value could run as a second SQL statement; the doc comments describing this as "surfacing as Postgres' own error" were corrected to say so.

  Added integration test coverage for all of the above (sync and async Postgres), plus golden-test coverage for the identifier/value validation.
