import json
import os
import subprocess
import sys
import textwrap
from pathlib import Path

# Root of the connections library — needed so the subprocess can import
# tests.golden.capture_plugin regardless of which directory pytest is invoked from.
_CONNECTIONS_DIR = Path(__file__).parent.parent.parent

# A throwaway test module the plugin can instrument: open an in-memory SQLite
# connection and run one query so execute() fires at least once.
_PROBE = textwrap.dedent("""
    from amsdal_glue_connections.sql.connections.sqlite_connection.sync_connection import SqliteConnection
    from amsdal_glue_core.common.data_models.query import QueryStatement
    from amsdal_glue_core.common.data_models.schema import SchemaReference
    from amsdal_glue_core.common.enums import Version

    def test_probe_executes():
        conn = SqliteConnection()
        conn.connect(db_path=':memory:', check_same_thread=False)
        conn.execute('CREATE TABLE users (id INTEGER)')
        conn.execute('INSERT INTO users (id) VALUES (1)')
        # a real query through the builder->execute path
        conn.query(QueryStatement(table=SchemaReference(name='users', version=Version.LATEST)))
        conn.disconnect()
""")


def _base_args(probe: Path) -> list:
    return ['-p', 'tests.golden.capture_plugin', '-n0', str(probe), '-p', 'no:cacheprovider']


def _env() -> dict:
    env = os.environ.copy()
    env['PYTHONPATH'] = str(_CONNECTIONS_DIR) + os.pathsep + env.get('PYTHONPATH', '')
    return env


def test_capture_then_assert_roundtrips(tmp_path: Path) -> None:
    """Capture a real connection's execute() traffic, then assert against it on the SAME code → 0 mismatches."""
    probe = tmp_path / 'test_probe.py'
    probe.write_text(_PROBE)
    corpus = tmp_path / 'corpus.jsonl'

    base = _base_args(probe)
    env = _env()

    cap = subprocess.run(  # noqa: S603, PLW1510
        [sys.executable, '-m', 'pytest', *base, f'--capture-sql={corpus}'],
        capture_output=True,
        cwd=str(_CONNECTIONS_DIR),
        env=env,
    )
    assert cap.returncode == 0, cap.stdout + cap.stderr
    assert corpus.exists() and corpus.read_text().strip(), 'corpus should be non-empty'
    rows = [json.loads(line) for line in corpus.read_text().splitlines()]
    assert any('users' in r['sql'] for r in rows), 'expected captured SQL referencing users'
    asrt = subprocess.run(  # noqa: S603, PLW1510
        [sys.executable, '-m', 'pytest', *base, f'--assert-sql={corpus}'],
        capture_output=True,
        cwd=str(_CONNECTIONS_DIR),
        env=env,
    )
    assert asrt.returncode == 0, asrt.stdout + asrt.stderr


def test_assert_is_order_independent(tmp_path: Path) -> None:
    """Swapping the row order within a (nodeid, dialect) group must still PASS assert.

    The probe emits CREATE, INSERT, SELECT in that order.  We write a corpus
    file with the first two rows swapped — same multiset, different sequence.
    The assert run must exit 0 because multiset comparison is order-independent.
    """
    probe = tmp_path / 'test_probe.py'
    probe.write_text(_PROBE)
    corpus = tmp_path / 'corpus.jsonl'

    base = _base_args(probe)
    env = _env()

    cap = subprocess.run(  # noqa: S603, PLW1510
        [sys.executable, '-m', 'pytest', *base, f'--capture-sql={corpus}'],
        capture_output=True,
        cwd=str(_CONNECTIONS_DIR),
        env=env,
    )
    assert cap.returncode == 0, cap.stdout + cap.stderr
    lines = corpus.read_text().splitlines()
    assert len(lines) >= 2, 'probe must emit at least two execute() calls for this test to be meaningful'

    # Swap the first two rows — same multiset, different order in the corpus file.
    swapped = [lines[1], lines[0], *lines[2:]]
    reordered = tmp_path / 'corpus_reordered.jsonl'
    reordered.write_text('\n'.join(swapped) + '\n')

    result = subprocess.run(  # noqa: S603, PLW1510
        [sys.executable, '-m', 'pytest', *base, f'--assert-sql={reordered}'],
        capture_output=True,
        cwd=str(_CONNECTIONS_DIR),
        env=env,
    )
    output = (result.stdout + result.stderr).decode()
    assert result.returncode == 0, (
        f'expected assert run to PASS on reordered corpus (order-independent), got non-zero.\n{output}'
    )


def test_assert_is_two_sided(tmp_path: Path) -> None:
    """Assert mode is two-sided: removed, extra, and changed SQL each trigger failure.

    Case A — removed sql: delete a corpus row so the re-run emits one SQL that
    is no longer in the expected multiset → the observed count exceeds expected → fail.

    Case B — extra sql: append a bogus corpus row that the re-run never emits →
    expected count 1, observed count 0 → fail.

    Case C — changed sql: modify the sql text of an existing corpus row → the
    expected multiset no longer matches observed (wrong sql expected, right sql
    is a surprise) → fail.
    """
    probe = tmp_path / 'test_probe.py'
    probe.write_text(_PROBE)
    corpus = tmp_path / 'corpus.jsonl'

    base = _base_args(probe)
    env = _env()

    # Step 1: capture a clean corpus.
    cap = subprocess.run(  # noqa: S603, PLW1510
        [sys.executable, '-m', 'pytest', *base, f'--capture-sql={corpus}'],
        capture_output=True,
        cwd=str(_CONNECTIONS_DIR),
        env=env,
    )
    assert cap.returncode == 0, cap.stdout + cap.stderr
    lines = corpus.read_text().splitlines()
    assert len(lines) >= 2, 'probe must emit at least two execute() calls for this test to be meaningful'

    # ------------------------------------------------------------------ Case A
    # Remove the last corpus line → the re-run still emits that SQL, giving an
    # observed count of 1 where expected is 0 → mismatch.
    truncated = tmp_path / 'corpus_truncated.jsonl'
    truncated.write_text('\n'.join(lines[:-1]) + '\n')

    result_a = subprocess.run(  # noqa: S603, PLW1510
        [sys.executable, '-m', 'pytest', *base, f'--assert-sql={truncated}'],
        capture_output=True,
        cwd=str(_CONNECTIONS_DIR),
        env=env,
    )
    output_a = (result_a.stdout + result_a.stderr).decode()
    assert result_a.returncode != 0, (
        f'expected assert run to FAIL on truncated corpus (removed-sql detection), got exit 0.\n{output_a}'
    )
    assert 'mismatch' in output_a.lower(), f'expected "mismatch" in output for removed-sql case, got:\n{output_a}'

    # ------------------------------------------------------------------ Case B
    # Append a bogus entry for a nodeid that never runs → expected count 1,
    # observed count 0 → mismatch.
    bogus = json.dumps({
        'fn': 'sqlite',
        'sql': 'SELECT BOGUS_SENTINEL FROM nowhere',
        'params': [],
        'nodeid': 'bogus::test_nonexistent',
        'seq': 9999,
    })
    extended = tmp_path / 'corpus_extended.jsonl'
    extended.write_text(corpus.read_text() + bogus + '\n')

    result_b = subprocess.run(  # noqa: S603, PLW1510
        [sys.executable, '-m', 'pytest', *base, f'--assert-sql={extended}'],
        capture_output=True,
        cwd=str(_CONNECTIONS_DIR),
        env=env,
    )
    output_b = (result_b.stdout + result_b.stderr).decode()
    assert result_b.returncode != 0, (
        f'expected assert run to FAIL on corpus with bogus entry (extra-sql detection), got exit 0.\n{output_b}'
    )
    assert 'mismatch' in output_b.lower(), f'expected "mismatch" in output for extra-sql case, got:\n{output_b}'

    # ------------------------------------------------------------------ Case C
    # Modify the sql field of the first corpus row → the expected multiset has
    # the altered sql (count 1) but not the original; the re-run emits the
    # original (count 1) but not the altered → two-entry mismatch.
    first_row = json.loads(lines[0])
    first_row['sql'] = 'SELECT CHANGED_SENTINEL FROM nowhere'
    changed_lines = [json.dumps(first_row), *lines[1:]]
    changed = tmp_path / 'corpus_changed.jsonl'
    changed.write_text('\n'.join(changed_lines) + '\n')

    result_c = subprocess.run(  # noqa: S603, PLW1510
        [sys.executable, '-m', 'pytest', *base, f'--assert-sql={changed}'],
        capture_output=True,
        cwd=str(_CONNECTIONS_DIR),
        env=env,
    )
    output_c = (result_c.stdout + result_c.stderr).decode()
    assert result_c.returncode != 0, f'expected assert run to FAIL on corpus with changed sql, got exit 0.\n{output_c}'
    assert 'mismatch' in output_c.lower(), f'expected "mismatch" in output for changed-sql case, got:\n{output_c}'
