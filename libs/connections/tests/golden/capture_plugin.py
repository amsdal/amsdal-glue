"""Capture or assert the SQL each connection actually sends to execute().

Wraps `execute` on the sync and async SQL connection classes. execute() is the
TRUE oracle: it sees queries, DML, DDL, lock, and transaction SQL uniformly —
including the inline DDL/lock/transaction paths that never go through build_*.
Patching the class methods in pytest_configure is enough: callers always reach
them via `self.execute(...)`, and instances are created during the tests (after
configure), so no early-import gymnastics are needed.

Assert mode is ORDER-INDEPENDENT: SQL emissions within a (nodeid, dialect) pair
are compared as multisets (collections.Counter).  Tests that emit the same set
of SQL statements in a different order pass; only genuinely added, removed, or
changed SQL triggers a failure.  The ``seq`` field is still written in capture
mode for reference/debugging but is not used during assertion.
"""
import inspect
import json
from collections import Counter, defaultdict
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
    # assert mode: observed[(nodeid, dialect)] -> Counter of sql strings
    'observed': defaultdict(Counter),
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
        _STATE['observed'][(nodeid, dialect)][sql] += 1


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
        # expected[(nodeid, dialect)] -> Counter of sql strings (multiset)
        _STATE['observed'] = defaultdict(Counter)
        _STATE['expected'] = defaultdict(Counter)
        with open(asrt) as fh:  # noqa: PTH123
            for line in fh:
                row = json.loads(line)
                _STATE['expected'][(row['nodeid'], row['fn'])][row['sql']] += 1


def pytest_runtest_setup(item: Any) -> None:
    _STATE['nodeid'] = item.nodeid


def pytest_sessionfinish(session: Any, exitstatus: int) -> None:  # noqa: ARG001
    if _STATE['fh']:
        _STATE['fh'].close()
    if _STATE['mode'] == 'assert':
        mismatches = []
        all_keys = sorted(set(_STATE['expected']) | set(_STATE['observed']))
        for key in all_keys:
            nodeid, dialect = key
            exp: Counter = _STATE['expected'].get(key, Counter())
            obs: Counter = _STATE['observed'].get(key, Counter())
            if exp == obs:
                continue
            for sql in sorted(set(exp) | set(obs)):
                exp_count = exp.get(sql, 0)
                obs_count = obs.get(sql, 0)
                if exp_count != obs_count:
                    mismatches.append(
                        {
                            'nodeid': nodeid,
                            'dialect': dialect,
                            'sql': sql,
                            'expected_count': exp_count,
                            'observed_count': obs_count,
                        }
                    )
        if mismatches:
            lines = []
            for m in mismatches:
                lines.append(
                    f"nodeid={m['nodeid']} dialect={m['dialect']}\n"
                    f"  sql: {m['sql']}\n"
                    f"  expected count: {m['expected_count']}, observed count: {m['observed_count']}"
                )
            msg = f"{len(mismatches)} SQL parity mismatch(es):\n" + '\n'.join(lines)
            raise AssertionError(msg)
