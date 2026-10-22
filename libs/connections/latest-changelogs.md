## [v0.2.4](https://pypi.org/project/amsdal-glue-connections/0.2.4/) - 2026-10-22

### Fixed

- Query results no longer decode a string as JSON just because it starts with `{` or `[` and ends with `}` or `]`. On Postgres, values of `text`, `varchar`, `char` and `name` columns come back exactly as stored. Before, source code such as `{ x: 1 }` failed the whole query with `JSONDecodeError`, and text that happened to be valid JSON came back as a dict or list. On every SQL backend, a value that looks like JSON but does not parse now stays a string instead of failing the query. (text-columns-not-json-decoded)
