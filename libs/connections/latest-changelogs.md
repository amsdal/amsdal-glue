## [v0.2.0rc2](https://pypi.org/project/amsdal-glue-connections/0.2.0rc2/) - 2026-08-18

### Fixed

- Text-match lookups (`CONTAINS`, `ICONTAINS`, `STARTSWITH`, `ISTARTSWITH`, `ENDSWITH`, `IENDSWITH`) on a bare column reference now cast the column to text in the generated SQL (`col::text LIKE ...` on Postgres, `CAST(col AS text)` on SQLite). Postgres stores JSON columns as `jsonb`, which has no `LIKE`/`ILIKE` operator, so any substring filter on an array or dictionary column failed with `operator does not exist: jsonb ~~ unknown`. The cast is a no-op on text columns and does not change SQLite behaviour, where JSON is already stored as text.
- Regex lookups (`REGEX`, `IREGEX`) get the same text cast -- `~`/`~*` have no `jsonb` operator either, so they failed identically on Postgres.
- A NESTED field reference in any text-match or regex lookup now renders as the `->>` text extraction instead of a cast over the `->` chain. `(payload->'name')::text` is the quoted JSON serialization (`"Emil"`), so `STARTSWITH`/`ENDSWITH` on nested fields could never match the first or last character on Postgres while matching on SQLite; `->>` yields the unquoted text on both engines.
