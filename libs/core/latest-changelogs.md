## [v0.2.0](https://pypi.org/project/amsdal-glue-core/0.2.0/) - 2026-08-25

### Changed

- `InsertData.data` and `UpdateData.data` now carry `DataInput` write rows (expression-valued) instead of plain `Data`.
- `IndexSchema.fields` is now a list of structured `IndexField` (name, direction, operator class) instead of plain field names.
