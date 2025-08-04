import os
from collections.abc import Generator
from dataclasses import dataclass
from typing import Any

import pytest
from elasticsearch import Elasticsearch

from amsdal_glue_connections.elasticsearch_connection.sync_connection import ElasticsearchConnection


@dataclass
class ConnectionInfo:
    host: str
    port: int
    user: str
    password: str
    connection: Any
    scheme: str = 'http'


@pytest.fixture(scope='session')
def test_prefix() -> str:
    """
    Provides a unique prefix for test indices based on the worker ID.
    This allows parallel test execution without index conflicts.
    """
    worker_id = os.getenv('PYTEST_XDIST_WORKER', 'main')
    return f'test-{worker_id}-'


def get_elasticsearch_credentials() -> tuple[str, int, str, str, str]:
    es_host = os.getenv('ELASTICSEARCH_HOST', 'localhost')
    es_port = int(os.getenv('ELASTICSEARCH_PORT', '9200'))
    es_user = os.getenv('ELASTICSEARCH_USER', 'elastic')
    es_password = os.getenv('ELASTICSEARCH_PASSWORD', 'changeme')
    es_scheme = os.getenv('ELASTICSEARCH_SCHEME', 'http')

    return es_host, es_port, es_user, es_password, es_scheme


@pytest.fixture(scope='function')
def database_connection(test_prefix: str) -> Generator[ElasticsearchConnection, None, None]:
    """
    Provides an ElasticsearchConnection scoped to a unique test token. All indices containing the
    token are cleaned up at teardown to ensure nothing is left behind.
    """

    # Raw ES client used for cleanup and initial index creation
    es_host, es_port, es_user, es_password, es_scheme = get_elasticsearch_credentials()
    raw_es = Elasticsearch(
        hosts=[{'host': es_host, 'port': es_port, 'scheme': es_scheme}],
        basic_auth=(es_user, es_password),
        request_timeout=60,
    )

    # Create connection with same prefix so any indices it creates include the token
    conn = ElasticsearchConnection()
    conn.connect(
        [{'host': es_host, 'port': es_port, 'scheme': es_scheme}],  # type: ignore[list-item]
        basic_auth=(es_user, es_password),
        index_prefix=test_prefix,
        instant_refresh=True,
        request_timeout=60,
    )

    try:
        yield conn
    finally:
        try:
            # List all indices and filter locally; avoid wildcard delete.
            indices_info = raw_es.cat.indices(format='json')  # returns list of dicts with 'index' key
            for info in indices_info:
                name = info.get('index') if isinstance(info, dict) else None  # type: ignore[union-attr]
                if name and name.startswith(test_prefix):  # Only delete indices created by this worker
                    try:
                        raw_es.indices.delete(index=name, ignore_unavailable=True)
                    except Exception as exc:  # noqa: BLE001
                        print(f'Warning: failed to delete index {name}: {exc}')  # noqa: T201
        except Exception as exc:  # noqa: BLE001
            print(f'Warning: failed to list indices for cleanup: {exc}')  # noqa: T201
        finally:
            raw_es.close()
