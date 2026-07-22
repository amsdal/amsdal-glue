## [v0.2.0rc1](https://pypi.org/project/amsdal-glue-core/0.2.0rc1/) - 2026-07-22

### Changed

- `InsertData.data` and `UpdateData.data` now carry `DataInput` write rows (expression-valued) instead of plain `Data`.
- `IndexSchema.fields` is now a list of structured `IndexField` (name, direction, operator class) instead of plain field names.
