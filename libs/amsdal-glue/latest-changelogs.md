## [v0.2.1](https://pypi.org/project/amsdal-glue/0.2.1/) - 2026-08-31

### Fixed

- Connection pools no longer hand out more connections than `max_connections` when several transactions start at the same time, and two concurrent callers of the same transaction now share one connection instead of opening two. A transaction-bound connection that is never released - a crashed or cancelled request - is reclaimed after `transaction_expiration_time` seconds (900 by default) and logged as a warning, instead of holding its slot until the process restarts; a reclaimed connection that fails to roll back is discarded rather than handed to the next transaction. Pass `acquisition_timeout` to make a caller wait for a free slot instead of failing as soon as the pool is full.
