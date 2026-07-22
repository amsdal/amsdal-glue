## [v0.2.0rc1](https://pypi.org/project/amsdal-glue-core/0.2.0rc1/) - 2026-07-22

### Changed

- `InsertData.data` and `UpdateData.data` now carry `DataInput` write rows (expression-valued) instead of plain `Data`.
- `IndexSchema.fields` is now a list of structured `IndexField` (name, direction, operator class) instead of plain field names.

## [v0.1.13](https://pypi.org/project/amsdal-glue-core/0.1.13/) - 2026-07-03

### Added

- Added `ForeignKeyViolationError` exception for foreign key constraint violations.

## [v0.1.12](https://pypi.org/project/amsdal-glue-core/0.1.12/) - 2026-06-15

### Added

- New `DecimalSchemaModel` field type for fixed-precision decimal values with optional `precision` and `scale`.

## [v0.1.11](https://pypi.org/project/amsdal-glue-core/0.1.11/) - 2026-05-20

### Added

- New `Exists` expression for `EXISTS` / `NOT EXISTS` subquery support.
- `negated` flag on conditions for SQL negation handling.
- New connection interface hooks to support subquery execution.

## [v0.1.10](https://pypi.org/project/amsdal-glue-core/0.1.10/) - 2026-05-06

### Added

- Raw expressions, conditions improvements.
- Added `UniqueViolationError` exception for unique constraint violations.

### Fixed

- Fix to have `Container.switch` to be thread-safe.

## [v0.1.9](https://pypi.org/project/amsdal-glue-core/0.1.9/) - 2026-04-09

### Added

- Added optional `metadata` field to `DataMutation` for passing additional context through the pipeline.

## [v0.1.8](https://pypi.org/project/amsdal-glue-core/0.1.8/) - 2025-12-21

### Changed

- Update libs

## [v0.1.7](https://pypi.org/project/amsdal-glue-core/0.1.7/) - 2025-06-26

### Added

- Vector models

## [v0.1.6](https://pypi.org/project/amsdal-glue-core/0.1.6/) - 2025-06-17

### Changed

- Update package manager to `uv` for better performance and compatibility.

## [v0.1.5](https://pypi.org/project/amsdal-glue-core/0.1.5/) - 2025-05-19

### Fixed

- Fixed copy of DeleteSchema mutation

## [v0.1.4](https://pypi.org/project/amsdal-glue-core/0.1.4/) - 2025-05-14

### Changed

- Changes for Schema comparison

## [v0.1.3](https://pypi.org/project/amsdal-glue-core/0.1.3/) - 2025-04-16

### Changed

- Changes for polars

## [v0.1.2](https://pypi.org/project/amsdal-glue-core/0.1.2/) - 2025-04-11

### Changed

- Updates for `Combinable`

## [v0.1.1](https://pypi.org/project/amsdal-glue-core/0.1.1/) - 2025-03-06

### Changed

- `LATEST` as default version for the `SchemaReference`

## [v0.1.0](https://pypi.org/project/amsdal-glue-core/0.1.0/) - 2025-02-24

### Changed

- Builder helpers
- Conditions


## [v0.0.14](https://pypi.org/project/amsdal-glue-core/0.0.14/) - 2024-12-18

### Added

- Async safe descriptor.

## [v0.0.10](https://pypi.org/project/amsdal-glue-core/0.0.10/) - 2024-09-16

### Added

- Extended Container by adding 'serialize_state' and 'deserialize_state' to pass into sub-processes. (container-state-serialization)
- Extended Container to manage sub-containers. (sub-containers)
## [v0.0.9](https://pypi.org/project/amsdal-glue-core/0.0.9/) - 2024-08-06

### Added

- Documentation via docstrings (documentation)
## [v0.0.8](https://pypi.org/project/amsdal-glue-core/0.0.8/) - 2024-08-02


### Added

- Typing added (typing-added)
