"""``DefaultConnectionPool`` must recycle a released connection.

A connection was previously returned to the pool only after sitting idle for longer
than ``expiration_time`` (60 s by default) - a window that never opens in a busy
process - and ``disconnect_connection`` physically closed it. Every transaction
therefore paid a fresh connect plus whatever per-connection setup the driver does.
"""

from typing import Any
from typing import cast

import pytest

from amsdal_glue.connections.connection_pool import DefaultConnectionPool


class FakeConnection:
    """Minimal stand-in for a ``ConnectionBase``, counting its physical lifecycle."""

    instances: int = 0

    def __init__(self) -> None:
        type(self).instances += 1
        self.connect_calls = 0
        self.disconnect_calls = 0
        self._connected = False

    @property
    def is_connected(self) -> bool:
        return self._connected

    @property
    def is_alive(self) -> bool:
        return self._connected

    def connect(self, *_args: Any, **_kwargs: Any) -> None:
        self.connect_calls += 1
        self._connected = True

    def disconnect(self) -> None:
        self.disconnect_calls += 1
        self._connected = False

    def rollback_transaction(self, _transaction_id: Any = None) -> None:
        pass


@pytest.fixture(autouse=True)
def _reset_counter() -> None:
    FakeConnection.instances = 0


def _pool(**kwargs: Any) -> DefaultConnectionPool:
    return DefaultConnectionPool(FakeConnection, **kwargs)  # type: ignore[arg-type]


def _get(pool: DefaultConnectionPool, transaction_id: str) -> FakeConnection:
    """``get_connection`` is typed to ``ConnectionBase``; the assertions need the fake's counters."""
    return cast('FakeConnection', pool.get_connection(transaction_id=transaction_id))


def test_released_connection_is_reused() -> None:
    pool = _pool()

    first = _get(pool, 'txn-1')
    pool.disconnect_connection(transaction_id='txn-1')
    second = _get(pool, 'txn-2')

    assert second is first, 'a released connection must be handed back out, not replaced'
    assert FakeConnection.instances == 1
    assert first.connect_calls == 1, 'reuse must not reconnect'
    assert first.disconnect_calls == 0, 'reuse must not close the connection'


def test_concurrent_transactions_get_distinct_connections() -> None:
    pool = _pool()

    first = _get(pool, 'txn-1')
    second = _get(pool, 'txn-2')

    assert first is not second, 'two live transactions must not share a connection'
    assert FakeConnection.instances == 2


def test_same_transaction_id_returns_same_connection() -> None:
    pool = _pool()

    assert _get(pool, 'txn-1') is _get(pool, 'txn-1')
    assert FakeConnection.instances == 1


def test_disconnect_closes_idle_and_live_connections() -> None:
    """Teardown must leave nothing open - callers drop databases and delete files after it."""
    pool = _pool()

    idle = _get(pool, 'txn-1')
    pool.disconnect_connection(transaction_id='txn-1')
    live = _get(pool, 'txn-2')
    other = _get(pool, 'txn-3')

    pool.disconnect()

    for connection in {id(c): c for c in (idle, live, other)}.values():
        assert not connection.is_connected, 'no connection may survive pool.disconnect()'
    assert not pool.connections


def test_expired_idle_connection_is_closed_not_reused() -> None:
    pool = _pool(expiration_time=0)

    first = _get(pool, 'txn-1')
    pool.disconnect_connection(transaction_id='txn-1')
    second = _get(pool, 'txn-2')

    assert second is not first, 'an expired idle connection must not be handed out'
    assert first.disconnect_calls == 1, 'an expired idle connection must be closed'


def test_max_connections_counts_idle_connections() -> None:
    pool = _pool(max_connections=2)

    _get(pool, 'txn-1')
    _get(pool, 'txn-2')

    with pytest.raises(RuntimeError, match='Max connections reached'):
        _get(pool, 'txn-3')


def test_idle_connections_are_reused_before_new_ones_are_made() -> None:
    pool = _pool(max_connections=2)

    _get(pool, 'txn-1')
    _get(pool, 'txn-2')
    pool.disconnect_connection(transaction_id='txn-1')

    # The freed slot must come back from the idle list rather than trip the cap.
    _get(pool, 'txn-3')

    assert FakeConnection.instances == 2


def test_reuse_can_be_disabled() -> None:
    """Opt-out for callers that need a release to close the underlying handle."""
    pool = _pool(reuse_connections=False)

    first = _get(pool, 'txn-1')
    pool.disconnect_connection(transaction_id='txn-1')
    second = _get(pool, 'txn-2')

    assert first.disconnect_calls == 1
    assert second is not first
