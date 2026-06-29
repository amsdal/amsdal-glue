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
_PROBE = textwrap.dedent('''
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
''')


def test_capture_then_assert_roundtrips(tmp_path: Path) -> None:
    """Capture a real connection's execute() traffic, then assert against it on the SAME code → 0 mismatches."""
    probe = tmp_path / 'test_probe.py'
    probe.write_text(_PROBE)
    corpus = tmp_path / 'corpus.jsonl'

    env = os.environ.copy()
    env['PYTHONPATH'] = str(_CONNECTIONS_DIR) + os.pathsep + env.get('PYTHONPATH', '')

    base = ['-p', 'tests.golden.capture_plugin', '-n0', str(probe), '-p', 'no:cacheprovider']
    cap = subprocess.run(
        [sys.executable, '-m', 'pytest', *base, f'--capture-sql={corpus}'],
        capture_output=True,
        cwd=str(_CONNECTIONS_DIR),
        env=env,
    )
    assert cap.returncode == 0, cap.stdout + cap.stderr
    assert corpus.exists() and corpus.read_text().strip(), 'corpus should be non-empty'
    rows = [json.loads(line) for line in corpus.read_text().splitlines()]
    assert any('users' in r['sql'] for r in rows), 'expected captured SQL referencing users'
    asrt = subprocess.run(
        [sys.executable, '-m', 'pytest', *base, f'--assert-sql={corpus}'],
        capture_output=True,
        cwd=str(_CONNECTIONS_DIR),
        env=env,
    )
    assert asrt.returncode == 0, asrt.stdout + asrt.stderr


def test_assert_is_two_sided(tmp_path: Path) -> None:
    """Two-sided assert: a deliberately modified corpus must fail the assert run.

    Case A — delete a corpus entry: the re-run still emits that SQL (extra key, not
    in corpus), so the assert run must fail.

    Case B — append a bogus corpus entry: the re-run never emits the bogus key
    (missing entry, expected but not seen), so the assert run must fail.
    """
    probe = tmp_path / 'test_probe.py'
    probe.write_text(_PROBE)
    corpus = tmp_path / 'corpus.jsonl'

    env = os.environ.copy()
    env['PYTHONPATH'] = str(_CONNECTIONS_DIR) + os.pathsep + env.get('PYTHONPATH', '')

    base = ['-p', 'tests.golden.capture_plugin', '-n0', str(probe), '-p', 'no:cacheprovider']

    # Step 1: capture a clean corpus.
    cap = subprocess.run(
        [sys.executable, '-m', 'pytest', *base, f'--capture-sql={corpus}'],
        capture_output=True,
        cwd=str(_CONNECTIONS_DIR),
        env=env,
    )
    assert cap.returncode == 0, cap.stdout + cap.stderr
    lines = corpus.read_text().splitlines()
    assert len(lines) >= 2, 'probe must emit at least two execute() calls for this test to be meaningful'

    # Case A: remove the last corpus line → that execute() call is "extra" in the re-run.
    truncated = tmp_path / 'corpus_truncated.jsonl'
    truncated.write_text('\n'.join(lines[:-1]) + '\n')

    result_a = subprocess.run(
        [sys.executable, '-m', 'pytest', *base, f'--assert-sql={truncated}'],
        capture_output=True,
        cwd=str(_CONNECTIONS_DIR),
        env=env,
    )
    output_a = (result_a.stdout + result_a.stderr).decode()
    assert result_a.returncode != 0, (
        f'expected assert run to FAIL on truncated corpus (extra-key detection), got exit 0.\n{output_a}'
    )
    assert 'mismatch' in output_a.lower(), (
        f'expected "mismatch" in output for extra-key case, got:\n{output_a}'
    )

    # Case B: append a bogus entry → the re-run never emits it (missing-key detection).
    bogus = json.dumps({
        'fn': 'sqlite',
        'sql': 'SELECT BOGUS_SENTINEL FROM nowhere',
        'params': [],
        'nodeid': 'bogus::test_nonexistent',
        'seq': 9999,
    })
    extended = tmp_path / 'corpus_extended.jsonl'
    extended.write_text(corpus.read_text() + bogus + '\n')

    result_b = subprocess.run(
        [sys.executable, '-m', 'pytest', *base, f'--assert-sql={extended}'],
        capture_output=True,
        cwd=str(_CONNECTIONS_DIR),
        env=env,
    )
    output_b = (result_b.stdout + result_b.stderr).decode()
    assert result_b.returncode != 0, (
        f'expected assert run to FAIL on corpus with bogus entry (missing-key detection), got exit 0.\n{output_b}'
    )
    assert 'mismatch' in output_b.lower(), (
        f'expected "mismatch" in output for missing-key case, got:\n{output_b}'
    )
