## [v0.2.2](https://pypi.org/project/amsdal-glue/0.2.2/) - 2026-09-09

### Added

- Added Python 3.13 and 3.14 to the supported/tested versions (pure Python, no code changes required).

## [v0.2.1](https://pypi.org/project/amsdal-glue/0.2.1/) - 2026-08-31

### Fixed

- Connection pools no longer hand out more connections than `max_connections` when several transactions start at the same time, and two concurrent callers of the same transaction now share one connection instead of opening two. A transaction-bound connection that is never released - a crashed or cancelled request - is reclaimed after `transaction_expiration_time` seconds (900 by default) and logged as a warning, instead of holding its slot until the process restarts; a reclaimed connection that fails to roll back is discarded rather than handed to the next transaction. Pass `acquisition_timeout` to make a caller wait for a free slot instead of failing as soon as the pool is full.

## [v0.2.0](https://pypi.org/project/amsdal-glue/0.2.0/) - 2026-08-25

### Added

- Connection pool live check.

### Changed

- Data mutation operations align with the `DataInput` input model and the structured `IndexField` schema.
- `DefaultConnectionPool.disconnect_connection` now releases a connection back to the pool instead of closing it, and `_get_available_connection` hands an idle one straight back out. Previously a connection was only ever reconsidered after sitting idle for longer than `expiration_time` (60 s by default) — a window that never opens in a busy process — so every transaction built and connected a brand new connection and closed it at commit. On the historical connections that also meant a full schema introspection per transaction; on a networked backend it means a TCP connect and authentication per transaction. An idle connection that does go past `expiration_time` is closed rather than reused, `disconnect()` closes idle and in-use connections alike (so callers that drop a database or delete a file straight after teardown still find nothing holding it open), and `max_connections` now counts idle connections too. Pass `reuse_connections=False` to restore closing on release. Measured on the `amsdal` framework test suite: physical connections per run fell by 82% and the suite got 21% faster.

## [v0.2.0rc2](https://pypi.org/project/amsdal-glue/0.2.0rc2/) - 2026-08-24

### Added

- Connection pool live check (live-check)

### Changed

- `DefaultConnectionPool.disconnect_connection` now releases a connection back to the pool instead of closing it, and `_get_available_connection` hands an idle one straight back out. Previously a connection was only ever reconsidered after sitting idle for longer than `expiration_time` (60 s by default) — a window that never opens in a busy process — so every transaction built and connected a brand new connection and closed it at commit. On the historical connections that also meant a full schema introspection per transaction; on a networked backend it means a TCP connect and authentication per transaction. An idle connection that does go past `expiration_time` is closed rather than reused, `disconnect()` closes idle and in-use connections alike (so callers that drop a database or delete a file straight after teardown still find nothing holding it open), and `max_connections` now counts idle connections too. Pass `reuse_connections=False` to restore closing on release. Measured on the `amsdal` framework test suite: physical connections per run fell by 82% and the suite got 21% faster. (connection-pool-reuse)
## [v0.2.0rc1](https://pypi.org/project/amsdal-glue/0.2.0rc1/) - 2026-07-22

### Changed

- Data mutation operations align with the `DataInput` input model and the structured `IndexField` schema.

## [v0.1.7](https://pypi.org/project/amsdal-glue/0.1.7/) - 2026-05-20

### Added

- Public exports for `Exists` expression.
- Polars final query executor exposed in the public API.
- Connection pool live check.

## [v0.1.6](https://pypi.org/project/amsdal-glue/0.1.6/) - 2025-12-21

### Changed

- Libs updated

## [v0.1.5](https://pypi.org/project/amsdal-glue/0.1.5/) - 2025-08-25

### Changed

- Ignore `KeyError` when popping from connections in `ConnectionPool`.

## [v0.1.4](https://pypi.org/project/amsdal-glue/0.1.4/) - 2025-06-17

### Changed

- Update package manager to `uv` for better performance and compatibility.

## [v0.1.3](https://pypi.org/project/amsdal-glue/0.1.3/) - 2025-04-11

### Added

- SCHEMA_REGISTRY_TABLE added to imports

## [v0.1.2](https://pypi.org/project/amsdal-glue/0.1.2/) - 2025-03-18

### Added

- Add `csv` as an optional dependency.

## [v0.1.1](https://pypi.org/project/amsdal-glue/0.1.1/) - 2025-03-06

### Changed

- Improved error catching for pipelines

## [v0.1.0](https://pypi.org/project/amsdal-glue/0.1.0/) - 2025-02-24

### Changed

- Builder helpers
- Conditions

## [v0.0.16](https://pypi.org/project/amsdal-glue/0.0.16/) - 2024-10-18

### Fixed

- Error messages (error-messages)

## [v0.0.15](https://pypi.org/project/amsdal-glue/0.0.15/) - 2024-10-14

### Added

- is_connected and is_alive methods added to the Connection pool (is_connected-is_alive) 

## [v0.0.14](https://pypi.org/project/amsdal-glue/0.0.14/) - 2024-09-16

### Added

- CQRSApplcation - predefined pipeline to build the CQRS pattern. (cqrs)
- LakehouseApplcation - predefined pipeline to build Lakehouse application. (lakehouse)
- Added Pipeline service to build complex pipelines of AMSDAL Glue containers (pipelines)

## [v0.0.13](https://pypi.org/project/amsdal-glue/0.0.13/) - 2024-08-06

### Added

- Documentation via docstrings (documentation)
- Optimization for imports: common classes, interfaces, planners, executors, services, tasks (imports-optimization)
## [v0.0.12](https://pypi.org/project/amsdal-glue/0.0.12/) - 2024-08-02


### Fixed

- Fixed dependencies (fixed-dependencies)


## [v0.0.11](https://pypi.org/project/amsdal-glue/0.0.11/) - 2024-08-02


### Added

- Typing added (typing-added)
