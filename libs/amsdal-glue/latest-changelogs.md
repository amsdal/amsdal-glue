## [v0.2.0rc2](https://pypi.org/project/amsdal-glue/0.2.0rc2/) - 2026-08-24

### Added

- Connection pool live check (live-check)

### Changed

- `DefaultConnectionPool.disconnect_connection` now releases a connection back to the pool instead of closing it, and `_get_available_connection` hands an idle one straight back out. Previously a connection was only ever reconsidered after sitting idle for longer than `expiration_time` (60 s by default) — a window that never opens in a busy process — so every transaction built and connected a brand new connection and closed it at commit. On the historical connections that also meant a full schema introspection per transaction; on a networked backend it means a TCP connect and authentication per transaction. An idle connection that does go past `expiration_time` is closed rather than reused, `disconnect()` closes idle and in-use connections alike (so callers that drop a database or delete a file straight after teardown still find nothing holding it open), and `max_connections` now counts idle connections too. Pass `reuse_connections=False` to restore closing on release. Measured on the `amsdal` framework test suite: physical connections per run fell by 82% and the suite got 21% faster. (connection-pool-reuse)
