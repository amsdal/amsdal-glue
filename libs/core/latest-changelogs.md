## [v0.2.1](https://pypi.org/project/amsdal-glue-core/0.2.1/) - 2026-08-31

### Fixed

- The connection of a root transaction is now released back to the pool even when its COMMIT, ROLLBACK or REVERT raises, instead of staying checked out until the pool reclaims it.
