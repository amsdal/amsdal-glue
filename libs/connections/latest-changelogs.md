## [v0.2.0](https://pypi.org/project/amsdal-glue-connections/0.2.0/) - 2026-08-25

### Added

- SQL generation for SQLite and PostgreSQL is now backed by a native Rust engine, distributed as prebuilt binary wheels (Linux x86_64/aarch64, macOS arm64/x86_64, Windows x64); installation no longer requires a Rust toolchain.

### Changed

- Decimal values preserve full precision and integer values support arbitrary size in generated SQL.
- Schema introspection is now view-based.
- The text cast is unconditional, so a `bytea` column in a text-match lookup is now matched as its hex representation (`\x68656c6c6f`) instead of its raw bytes: `bytea_col__contains='abc'` used to resolve to `bytea ~~ bytea` and match the bytes, and now returns no rows. Substring search over binary columns is out of contract; this matches Django's behaviour, which casts to text the same way.

### Fixed

- Text-match lookups (`CONTAINS`, `ICONTAINS`, `STARTSWITH`, `ISTARTSWITH`, `ENDSWITH`, `IENDSWITH`) on a bare column reference now cast the column to text in the generated SQL (`col::text LIKE ...` on Postgres, `CAST(col AS text)` on SQLite). Postgres stores JSON columns as `jsonb`, which has no `LIKE`/`ILIKE` operator, so any substring filter on an array or dictionary column failed with `operator does not exist: jsonb ~~ unknown`. The cast is a no-op on text columns and does not change SQLite behaviour, where JSON is already stored as text.
- Regex lookups (`REGEX`, `IREGEX`) get the same text cast -- `~`/`~*` have no `jsonb` operator either, so they failed identically on Postgres.
- A NESTED field reference in any text-match or regex lookup now renders as the `->>` text extraction instead of a cast over the `->` chain. `(payload->'name')::text` is the quoted JSON serialization (`"Emil"`), so `STARTSWITH`/`ENDSWITH` on nested fields could never match the first or last character on Postgres while matching on SQLite; `->>` yields the unquoted text on both engines.
- Elasticsearch index creation no longer blocks on single-node clusters.
- Known limitation: on SQLite a text match over a WHOLE JSON column compares against the stored serialization, which escapes non-ASCII characters (`["alpha","\u0431..."]`), so `payload__contains='бета'` matches on Postgres and finds nothing on SQLite. Nested lookups (`payload__name__contains=...`) are unaffected -- extraction unescapes on both engines.

### Performance

- The SQLite registry views are created once per connection instead of on every `query_schema` call. The view DDL is idempotent, so re-issuing it was harmless, but `query_schema` is on the hot path of every query and each call paid the round trips. The views are `TEMPORARY` and therefore belong to the connection that made them, so the flag guarding them is cleared in both `connect` and `disconnect` — a reconnect recreates them, exactly as before.
