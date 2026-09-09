## [v0.2.1](https://pypi.org/project/amsdal-glue-sql-parser/0.2.1/) - 2026-09-09

### Added

- Added Python 3.13 and 3.14 to the supported/tested versions. Bumped the `sqloxide` extra from 0.1.47 to 0.61.1 (the first release with cp313/cp314 wheels) and updated `SqlOxideParser` for the underlying `sqlparser-rs` AST changes that shipped between those versions (object names, values, joins, `ORDER BY`/`LIMIT`/`GROUP BY`, and index/constraint column lists are now wrapped differently).

## [v0.2.0](https://pypi.org/project/amsdal-glue-sql-parser/0.2.0/) - 2026-08-25

### Changed

- Parsed insert and update statements now produce `DataInput`-based mutations.

## [v0.2.0rc1](https://pypi.org/project/amsdal-glue-sql-parser/0.2.0rc1/) - 2026-07-22

### Changed

- Parsed insert and update statements now produce `DataInput`-based mutations.

## [v0.1.4](https://pypi.org/project/amsdal-glue-sql-parser/0.1.4/) - 2025-12-21

### Changed

- Libs updated

## [v0.1.3](https://pypi.org/project/amsdal-glue-sql-parser/0.1.3/) - 2025-06-17

### Changed

- Update package manager to `uv` for better performance and compatibility.

## [v0.1.2](https://pypi.org/project/amsdal-glue-sql-parser/0.1.2/) - 2025-04-11

### Added

- Added support for for more complex operations

## [v0.1.1](https://pypi.org/project/amsdal-glue-sql-parser/0.1.1/) - 2025-03-18

### Added

- Support for different joins


## [v0.1.0](https://pypi.org/project/amsdal-glue-sql-parser/0.1.0/) - 2025-02-24

### Changed

- Builder helpers
- Conditions

## [v0.0.5](https://pypi.org/project/amsdal-glue-sql-parser/0.0.5/) - 2024-08-02


### Added

- Typing added (typing-added)
