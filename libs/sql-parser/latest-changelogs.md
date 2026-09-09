## [v0.2.1](https://pypi.org/project/amsdal-glue-sql-parser/0.2.1/) - 2026-09-09

### Added

- Added Python 3.13 and 3.14 to the supported/tested versions. Bumped the `sqloxide` extra from 0.1.47 to 0.61.1 (the first release with cp313/cp314 wheels) and updated `SqlOxideParser` for the underlying `sqlparser-rs` AST changes that shipped between those versions (object names, values, joins, `ORDER BY`/`LIMIT`/`GROUP BY`, and index/constraint column lists are now wrapped differently).
