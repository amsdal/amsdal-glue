"""Capture or assert the SQL each connection actually sends to execute().

Wraps `execute` on the sync and async SQL connection classes. execute() is the
TRUE oracle: it sees queries, DML, DDL, lock, and transaction SQL uniformly —
including the inline DDL/lock/transaction paths that never go through build_*.
Patching the class methods in pytest_configure is enough: callers always reach
them via `self.execute(...)`, and instances are created during the tests (after
configure), so no early-import gymnastics are needed.
"""
import inspect
import json
from collections import defaultdict
from typing import Any

import pytest

from amsdal_glue_connections.sql.connections.postgres_connection.async_connection import AsyncPostgresConnection
from amsdal_glue_connections.sql.connections.postgres_connection.sync_connection import PostgresConnection
from amsdal_glue_connections.sql.connections.sqlite_connection.async_connection import AsyncSqliteConnection
from amsdal_glue_connections.sql.connections.sqlite_connection.sync_connection import SqliteConnection

# dialect-key -> connection class.
_TARGETS = {
    'pg': PostgresConnection,
    'pg_async': AsyncPostgresConnection,
    'sqlite': SqliteConnection,
    'sqlite_async': AsyncSqliteConnection,
}
_STATE: dict[str, Any] = {
    'mode': None,
    'nodeid': '',
    'seq': defaultdict(int),
    'fh': None,
    'mismatches': [],
    'seen': set(),
}


def _safe(params: list) -> list:
    out = []
    for p in params:
        try:
            json.dumps(p)
            out.append(p)
        except TypeError:
            out.append(repr(p))
    return out


def _record(dialect: str, sql: str, params: list) -> None:
    nodeid = _STATE['nodeid']
    seq = _STATE['seq'][nodeid]
    _STATE['seq'][nodeid] += 1
    if _STATE['mode'] == 'capture':
        _STATE['fh'].write(
            json.dumps({'fn': dialect, 'sql': sql, 'params': _safe(params), 'nodeid': nodeid, 'seq': seq}) + '\n'
        )
    elif _STATE['mode'] == 'assert':
        key = (nodeid, seq, dialect)
        _STATE['seen'].add(key)
        expected = _STATE['expected'].get(key)
        if expected is None:
            _STATE['mismatches'].append({'type': 'extra', 'key': key, 'actual': sql})
        elif expected['sql'] != sql:
            _STATE['mismatches'].append({'type': 'diff', 'key': key, 'expected': expected['sql'], 'actual': sql})


def _wrap_sync(dialect: str, orig: Any) -> Any:
    def inner(self: Any, query: str, *args: Any) -> Any:
        if _STATE['mode']:
            _record(dialect, query, list(args))
        return orig(self, query, *args)

    return inner


def _wrap_async(dialect: str, orig: Any) -> Any:
    async def inner(self: Any, query: str, *args: Any) -> Any:
        if _STATE['mode']:
            _record(dialect, query, list(args))
        return await orig(self, query, *args)

    return inner


def pytest_addoption(parser: Any) -> None:
    parser.addoption('--capture-sql', default=None)
    parser.addoption('--assert-sql', default=None)


def pytest_configure(config: Any) -> None:
    if getattr(config, 'workerinput', None) is not None:
        raise pytest.UsageError('capture_plugin requires serial run; use -n0')
    cap = config.getoption('--capture-sql')
    asrt = config.getoption('--assert-sql')
    if not cap and not asrt:
        return
    if cap and asrt:
        raise pytest.UsageError('--capture-sql and --assert-sql are mutually exclusive')
    for dialect, cls in _TARGETS.items():
        orig = cls.execute
        wrapper = _wrap_async(dialect, orig) if inspect.iscoroutinefunction(orig) else _wrap_sync(dialect, orig)
        cls.execute = wrapper  # type: ignore[method-assign]
    if cap:
        _STATE['mode'] = 'capture'
        _STATE['fh'] = open(cap, 'w')  # noqa: SIM115, PTH123
    else:
        _STATE['mode'] = 'assert'
        _STATE['seen'] = set()
        _STATE['expected'] = {}
        with open(asrt) as fh:  # noqa: PTH123
            for line in fh:
                row = json.loads(line)
                _STATE['expected'][(row['nodeid'], row['seq'], row['fn'])] = row


def pytest_runtest_setup(item: Any) -> None:
    _STATE['nodeid'] = item.nodeid


def pytest_sessionfinish(session: Any, exitstatus: int) -> None:  # noqa: ARG001
    if _STATE['fh']:
        _STATE['fh'].close()
    if _STATE['mode'] == 'assert':
        mismatches = list(_STATE['mismatches'])
        # Missing: corpus entries that were never re-emitted
        seen_keys = _STATE['seen']
        for key in sorted(set(_STATE['expected'].keys()) - seen_keys):
            expected_sql = _STATE['expected'][key]['sql']
            mismatches.append({'type': 'missing', 'key': key, 'expected': expected_sql})
        if mismatches:
            lines = []
            for m in mismatches:
                if m.get('type') == 'extra':
                    lines.append(f"{m['key']}\n  unexpected SQL not in corpus: {m['actual']}")
                elif m.get('type') == 'missing':
                    lines.append(f"{m['key']}\n  expected SQL not emitted: {m['expected']}")
                else:
                    lines.append(f"{m['key']}\n  expected: {m['expected']}\n  actual:   {m['actual']}")
            msg = f"{len(mismatches)} SQL parity mismatch(es):\n" + '\n'.join(lines)
            raise AssertionError(msg)
