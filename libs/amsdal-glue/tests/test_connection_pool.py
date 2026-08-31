"""Regression tests for the connection pool capacity, leak GC and reuse rules."""

import asyncio
import threading
import time
from typing import Any
from typing import cast
from typing import ClassVar

import pytest

from amsdal_glue.connections.connection_pool import DefaultAsyncConnectionPool
from amsdal_glue.connections.connection_pool import DefaultConnectionPool


class FakeConnection:
    """Minimal sync connection recording its lifecycle."""

    instances: ClassVar[list['FakeConnection']] = []

    def __init__(self) -> None:
        self.connected = False
        self.rollbacks: list[Any] = []
        self.rollback_error: Exception | None = None
        FakeConnection.instances.append(self)

    def connect(self, **kwargs: Any) -> None:  # noqa: ARG002
        time.sleep(0.01)
        self.connected = True

    @property
    def is_connected(self) -> bool:
        return self.connected

    @property
    def is_alive(self) -> bool:
        return self.connected

    def disconnect(self) -> None:
        self.connected = False

    def rollback_transaction(self, transaction: Any) -> Any:
        if self.rollback_error:
            raise self.rollback_error
        self.rollbacks.append(transaction)
        return True


class FakeAsyncConnection:
    """Minimal async connection recording its lifecycle."""

    instances: ClassVar[list['FakeAsyncConnection']] = []

    def __init__(self) -> None:
        self.connected = False
        self.rollbacks: list[Any] = []
        self.rollback_error: Exception | None = None
        FakeAsyncConnection.instances.append(self)

    async def connect(self, **kwargs: Any) -> None:  # noqa: ARG002
        await asyncio.sleep(0.01)
        self.connected = True

    @property
    async def is_connected(self) -> bool:
        return self.connected

    @property
    async def is_alive(self) -> bool:
        return self.connected

    async def disconnect(self) -> None:
        self.connected = False

    async def rollback_transaction(self, transaction: Any) -> Any:
        if self.rollback_error:
            raise self.rollback_error
        self.rollbacks.append(transaction)
        return True


@pytest.fixture(autouse=True)
def _reset_instances() -> None:
    FakeConnection.instances = []
    FakeAsyncConnection.instances = []


def _pool(**kwargs: Any) -> DefaultConnectionPool:
    return DefaultConnectionPool(FakeConnection, **kwargs)  # type: ignore[arg-type]


def _async_pool(**kwargs: Any) -> DefaultAsyncConnectionPool:
    return DefaultAsyncConnectionPool(FakeAsyncConnection, **kwargs)  # type: ignore[arg-type]


def _get(pool: DefaultConnectionPool, transaction_id: str) -> FakeConnection:
    """``get_connection`` is typed to ``ConnectionBase``; the assertions need the fake's own state."""
    return cast('FakeConnection', pool.get_connection(transaction_id=transaction_id))


async def _aget(pool: DefaultAsyncConnectionPool, transaction_id: str) -> FakeAsyncConnection:
    """Async counterpart of ``_get``."""
    return cast('FakeAsyncConnection', await pool.get_connection(transaction_id=transaction_id))


async def test_concurrent_acquisitions_never_exceed_max_connections() -> None:
    pool = _async_pool(max_connections=10, expiration_time=60, acquisition_timeout=0.1)

    async def acquire(index: int) -> str | None:
        try:
            await pool.get_connection(transaction_id=f'tx-{index}')
        except RuntimeError as exc:
            return str(exc)
        return None

    results = await asyncio.gather(*[acquire(i) for i in range(30)])

    assert len(pool.connections) == 10
    assert len(FakeAsyncConnection.instances) == 10
    assert sum(1 for result in results if result) == 20


async def test_waits_for_a_released_slot_instead_of_failing_immediately() -> None:
    pool = _async_pool(max_connections=1, expiration_time=60, acquisition_timeout=5)
    await _aget(pool, 'tx-1')

    async def release_later() -> None:
        await asyncio.sleep(0.05)
        await pool.disconnect_connection(transaction_id='tx-1')

    release_task = asyncio.ensure_future(release_later())
    connection = await _aget(pool, 'tx-2')
    await release_task

    assert connection is not None
    assert list(pool.connections) == ['tx-2']


async def test_idle_transaction_connection_is_not_recycled_by_another_transaction() -> None:
    pool = _async_pool(
        max_connections=1,
        expiration_time=0.05,
        transaction_expiration_time=30,
        acquisition_timeout=0.2,
    )
    running = await _aget(pool, 'slow-tx')

    await asyncio.sleep(0.15)

    with pytest.raises(RuntimeError, match='Max connections reached'):
        await _aget(pool, 'other-tx')

    assert running.rollbacks == []
    assert await _aget(pool, 'slow-tx') is running


async def test_leaked_transaction_connection_is_reclaimed_after_transaction_expiration() -> None:
    pool = _async_pool(
        max_connections=1,
        expiration_time=30,
        transaction_expiration_time=0.05,
        acquisition_timeout=0.2,
    )
    leaked = await _aget(pool, 'leaked-tx')

    await asyncio.sleep(0.15)
    reused = await _aget(pool, 'new-tx')

    assert reused is leaked
    assert leaked.rollbacks == ['leaked-tx']
    assert list(pool.connections) == ['new-tx']


async def test_reclaimed_connection_that_fails_to_roll_back_is_discarded() -> None:
    pool = _async_pool(
        max_connections=1,
        expiration_time=30,
        transaction_expiration_time=0.05,
        acquisition_timeout=0.2,
    )
    broken = await _aget(pool, 'leaked-tx')
    broken.rollback_error = ConnectionError('server closed the connection unexpectedly')

    await asyncio.sleep(0.15)
    replacement = await _aget(pool, 'new-tx')

    assert replacement is not broken
    assert broken.connected is False


async def test_concurrent_acquisitions_for_the_same_transaction_share_one_connection() -> None:
    pool = _async_pool(max_connections=10, expiration_time=60, acquisition_timeout=1)

    connections = await asyncio.gather(*[_aget(pool, 'tx-1') for _ in range(5)])

    assert len({id(connection) for connection in connections}) == 1
    assert list(pool.connections) == ['tx-1']
    assert [connection.connected for connection in FakeAsyncConnection.instances].count(True) == 1


async def test_second_caller_of_the_same_transaction_waits_even_without_an_acquisition_timeout() -> None:
    """A caller joining a transaction is not competing for a slot, so the pool must not fail it fast."""
    pool = _async_pool(max_connections=10, expiration_time=60)

    connections = await asyncio.gather(*[_aget(pool, 'tx-1') for _ in range(3)])

    assert len({id(connection) for connection in connections}) == 1
    assert [connection.connected for connection in FakeAsyncConnection.instances].count(True) == 1


def test_sync_concurrent_acquisitions_never_exceed_max_connections() -> None:
    pool = _pool(max_connections=10, expiration_time=60, acquisition_timeout=0.1)
    errors: list[str] = []

    def acquire(index: int) -> None:
        try:
            pool.get_connection(transaction_id=f'tx-{index}')
        except RuntimeError as exc:
            errors.append(str(exc))

    threads = [threading.Thread(target=acquire, args=(i,)) for i in range(30)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    assert len(pool.connections) == 10
    assert len(FakeConnection.instances) == 10
    assert len(errors) == 20


def test_sync_idle_transaction_connection_is_not_recycled_by_another_transaction() -> None:
    pool = _pool(
        max_connections=1,
        expiration_time=0.05,
        transaction_expiration_time=30,
        acquisition_timeout=0.2,
    )
    running = _get(pool, 'slow-tx')

    time.sleep(0.15)

    with pytest.raises(RuntimeError, match='Max connections reached'):
        _get(pool, 'other-tx')

    assert running.rollbacks == []
    assert _get(pool, 'slow-tx') is running


def test_sync_leaked_transaction_connection_is_reclaimed_after_transaction_expiration() -> None:
    pool = _pool(
        max_connections=1,
        expiration_time=30,
        transaction_expiration_time=0.05,
        acquisition_timeout=0.2,
    )
    leaked = _get(pool, 'leaked-tx')

    time.sleep(0.15)
    reused = _get(pool, 'new-tx')

    assert reused is leaked
    assert leaked.rollbacks == ['leaked-tx']
    assert list(pool.connections) == ['new-tx']


def test_sync_concurrent_acquisitions_for_the_same_transaction_share_one_connection() -> None:
    pool = _pool(max_connections=10, expiration_time=60, acquisition_timeout=1)
    acquired: list[FakeConnection] = []
    lock = threading.Lock()

    def acquire() -> None:
        connection = _get(pool, 'tx-1')

        with lock:
            acquired.append(connection)

    threads = [threading.Thread(target=acquire) for _ in range(5)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    assert len({id(connection) for connection in acquired}) == 1
    assert list(pool.connections) == ['tx-1']
    assert [connection.connected for connection in FakeConnection.instances].count(True) == 1
