## [v0.2.5](https://pypi.org/project/amsdal-glue-connections/0.2.5/) - 2026-11-11

### Added

- An index field with `json_path` is created as an expression index on PostgreSQL and SQLite. The expression is rendered by the same code as a filter on that path with the same `output_type`, so the planner uses the index for such filters. `name` and each `json_path` element are validated as bare identifiers. Expression indexes are now read back by introspection (PostgreSQL `pg_get_indexdef`, SQLite `CREATE INDEX` DDL) as the same `IndexField`, so a declared index equals its introspection and a table rebuilt from the introspected indexes keeps it. Other expression columns are still not reported. (json-path-index-field)
