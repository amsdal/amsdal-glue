## [v0.2.0rc2](https://pypi.org/project/amsdal-glue-connections/0.2.0rc2/) - 2026-08-18

### Fixed

- Text-match lookups (`CONTAINS`, `ICONTAINS`, `STARTSWITH`, `ISTARTSWITH`, `ENDSWITH`, `IENDSWITH`) on a bare column reference now cast the column to text in the generated SQL (`col::text LIKE ...` on Postgres, `CAST(col AS text)` on SQLite). Postgres stores JSON columns as `jsonb`, which has no `LIKE`/`ILIKE` operator, so any substring filter on an array or dictionary column failed with `operator does not exist: jsonb ~~ unknown`. The cast is a no-op on text columns and does not change SQLite behaviour, where JSON is already stored as text.
