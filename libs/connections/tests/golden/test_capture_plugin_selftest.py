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
