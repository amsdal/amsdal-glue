## [v0.2.5](https://pypi.org/project/amsdal-glue-core/0.2.5/) - 2026-11-11

### Added

- `IndexField` has two new optional attributes, `json_path` and `output_type`. Together they declare an expression index over a path inside a JSON column, for example `IndexField(name="evidence", json_path=["ref", "object_id"], output_type=ScalarType.TEXT)`. `output_type` selects `->>` (`TEXT`) or `->` (`JSONB`) for the last step. Both are compared by `IndexSchema` equality. `IndexField` rejects an `output_type` without a `json_path`, and a `json_path` whose `output_type` is not `TEXT` or `JSONB`; an empty `json_path` means a plain column. (json-path-index-field)
