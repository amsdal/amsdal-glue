## [v0.2.0rc1](https://pypi.org/project/amsdal-glue-connections/0.2.0rc1/) - 2026-07-22

### Added

- SQL generation for SQLite and PostgreSQL is now backed by a native Rust engine, distributed as prebuilt binary wheels (Linux x86_64/aarch64, macOS arm64/x86_64, Windows x64); installation no longer requires a Rust toolchain.

### Changed

- Decimal values preserve full precision and integer values support arbitrary size in generated SQL.
- Schema introspection is now view-based.

### Fixed

- Elasticsearch index creation no longer blocks on single-node clusters.
