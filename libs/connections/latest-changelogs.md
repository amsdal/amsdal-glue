## [v0.2.0rc3](https://pypi.org/project/amsdal-glue-connections/0.2.0rc3/) - 2026-08-24

### Performance

- The SQLite registry views are created once per connection instead of on every `query_schema` call. The view DDL is idempotent, so re-issuing it was harmless, but `query_schema` is on the hot path of every query and each call paid the round trips. The views are `TEMPORARY` and therefore belong to the connection that made them, so the flag guarding them is cleared in both `connect` and `disconnect` — a reconnect recreates them, exactly as before. (sqlite-registry-views)
