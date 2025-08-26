# mypy: disable-error-code="type-abstract"
import os
import uuid
from collections.abc import Generator
from contextlib import contextmanager
from contextlib import suppress

import pytest
from amsdal_glue_connections.elasticsearch_connection.sync_connection import ElasticsearchConnection
from amsdal_glue_core.commands.planner.schema_command_planner import SchemaCommandPlanner
from amsdal_glue_core.common.data_models.conditions import Condition
from amsdal_glue_core.common.data_models.conditions import Conditions
from amsdal_glue_core.common.data_models.constraints import CheckConstraint
from amsdal_glue_core.common.data_models.constraints import PrimaryKeyConstraint
from amsdal_glue_core.common.data_models.constraints import UniqueConstraint
from amsdal_glue_core.common.data_models.field_reference import Field
from amsdal_glue_core.common.data_models.field_reference import FieldReference
from amsdal_glue_core.common.data_models.indexes import IndexSchema
from amsdal_glue_core.common.data_models.schema import ArraySchemaModel
from amsdal_glue_core.common.data_models.schema import DictSchemaModel
from amsdal_glue_core.common.data_models.schema import NestedSchemaModel
from amsdal_glue_core.common.data_models.schema import PropertySchema
from amsdal_glue_core.common.data_models.schema import Schema
from amsdal_glue_core.common.data_models.schema import VectorSchemaModel
from amsdal_glue_core.common.enums import FieldLookup
from amsdal_glue_core.common.enums import Version
from amsdal_glue_core.common.expressions.field_reference import FieldReferenceExpression
from amsdal_glue_core.common.expressions.value import Value
from amsdal_glue_core.common.interfaces.connection_manager import ConnectionManager
from amsdal_glue_core.common.operations.commands import SchemaCommand
from amsdal_glue_core.common.operations.mutations.schema import RegisterSchema
from amsdal_glue_core.common.operations.queries import SchemaQueryOperation
from amsdal_glue_core.common.services.queries import SchemaQueryService
from amsdal_glue_core.containers import Container
from elasticsearch import Elasticsearch

from amsdal_glue.connections.connection_pool import DefaultConnectionPool
from amsdal_glue.initialize import init_default_containers


@contextmanager
def cleanup_elasticsearch_indices(es_client: Elasticsearch, prefix: str) -> Generator[None, None, None]:
    try:
        yield
    finally:
        try:
            indices_info = es_client.cat.indices(format='json')
            for info in indices_info:
                name = info.get('index') if isinstance(info, dict) else None
                if name and name.startswith(prefix):
                    with suppress(Exception):
                        es_client.indices.delete(index=name, ignore_unavailable=True)
        except Exception:  # noqa: S110, BLE001
            pass


@pytest.fixture(autouse=True)
def _register_default_connection() -> Generator[None, None, None]:
    init_default_containers()
    connection_mng = Container.managers.get(ConnectionManager)

    # Elasticsearch connection setup
    es_host = os.getenv('ELASTICSEARCH_HOST', 'localhost')
    es_port = int(os.getenv('ELASTICSEARCH_PORT', '9200'))
    es_user = os.getenv('ELASTICSEARCH_USER', 'elastic')
    es_password = os.getenv('ELASTICSEARCH_PASSWORD', 'changeme')
    es_scheme = os.getenv('ELASTICSEARCH_SCHEME', 'http')

    # Generate unique prefix for test indices
    test_prefix = f'test-{uuid.uuid4().hex}-'

    # Create raw ES client for cleanup
    raw_es = Elasticsearch(
        hosts=[{'host': es_host, 'port': es_port, 'scheme': es_scheme}],
        basic_auth=(es_user, es_password),
        request_timeout=60,
    )

    with cleanup_elasticsearch_indices(raw_es, test_prefix):
        connection_mng.register_connection_pool(
            DefaultConnectionPool(
                ElasticsearchConnection,
                [{'host': es_host, 'port': es_port, 'scheme': es_scheme}],  # hosts positional arg for connect()
                index_prefix=test_prefix,  # kwargs for connect()
                basic_auth=(es_user, es_password),
                instant_refresh=True,
                request_timeout=60,
            ),
        )

        try:
            yield
        finally:
            connection_mng.disconnect_all()
            raw_es.close()


def test_create_schema() -> None:
    connection_mng = Container.managers.get(ConnectionManager)
    schema = Schema(
        name='user',
        version=Version.LATEST,
        properties=[
            PropertySchema(
                name='id',
                type=int,
                required=False,  # Elasticsearch doesn't enforce required fields at schema level
            ),
            PropertySchema(
                name='email',
                type=str,
                required=False,
            ),
            PropertySchema(
                name='age',
                type=int,
                required=False,
            ),
            PropertySchema(
                name='first_name',
                type=str,
                required=False,
            ),
            PropertySchema(
                name='last_name',
                type=str,
                required=False,
            ),
        ],
        constraints=[
            PrimaryKeyConstraint(name='pk_user_custom_name', fields=['id']),
            UniqueConstraint(name='uk_user_email', fields=['email'], condition=None),
            UniqueConstraint(name='uk_user_email_last_name', fields=['email', 'last_name'], condition=None),
            CheckConstraint(
                name='ck_user_age',
                condition=Conditions(
                    Condition(
                        left=FieldReferenceExpression(
                            field_reference=FieldReference(field=Field(name='age'), table_name='user')
                        ),
                        lookup=FieldLookup.GT,
                        right=Value(value=18),
                    ),
                ),
            ),
        ],
        indexes=[
            IndexSchema(name='idx_user_email', fields=['first_name', 'last_name']),
        ],
    )

    planner = Container.planners.get(SchemaCommandPlanner)
    plan = planner.plan_schema_command(
        SchemaCommand(
            mutations=[
                RegisterSchema(schema=schema),
            ],
        ),
    )
    plan.execute(transaction_id=None, lock_id=None)

    conn = connection_mng.get_connection_pool('user').get_connection()
    result = conn.query_schema(filters=None)
    assert len(result) == 1
    _schema = result[0]
    # Schema name includes the index prefix, so just check it ends with 'user'
    assert _schema.name.endswith('user')
    assert {prop.name: prop.type for prop in _schema.properties} == {
        'id': int,
        'email': str,
        'age': int,
        'first_name': str,
        'last_name': str,
    }

    query_service = Container.services.get(SchemaQueryService)
    schema_result = query_service.execute(
        SchemaQueryOperation(filters=None),
    )

    # Elasticsearch preserves constraints and indexes in metadata but properties are simplified
    assert schema_result.schemas is not None and len(schema_result.schemas) > 0
    result_schema = schema_result.schemas[0]
    assert result_schema is not None
    assert result_schema.name.endswith('user')  # Schema name includes index prefix
    assert result_schema.version == Version.LATEST

    # Check properties (order may vary, so convert to dict)
    assert result_schema.properties is not None
    prop_dict = {prop.name: (prop.type, prop.required) for prop in result_schema.properties}
    expected_props = {
        'id': (int, False),
        'age': (int, False),
        'email': (str, False),
        'first_name': (str, False),
        'last_name': (str, False),
    }
    assert prop_dict == expected_props

    # Check that constraints and indexes are preserved
    assert result_schema.constraints is not None
    assert result_schema.indexes is not None
    assert len(result_schema.constraints) == 4
    assert len(result_schema.indexes) == 1

    # Verify index exists
    assert len(result_schema.indexes) > 0
    assert result_schema.indexes[0].name == 'idx_user_email'
    assert result_schema.indexes[0].fields == ['first_name', 'last_name']


def test_create_schema_complex_types() -> None:
    connection_mng = Container.managers.get(ConnectionManager)
    schema = Schema(
        name='user',
        version=Version.LATEST,
        properties=[
            PropertySchema(
                name='dictionary',
                type=DictSchemaModel(key_type=str, value_type=int),
                required=False,  # Elasticsearch doesn't enforce required at schema level
            ),
            PropertySchema(
                name='array',
                type=ArraySchemaModel(item_type=str),
                required=False,
            ),
            PropertySchema(
                name='nested_schema',
                type=NestedSchemaModel(properties={'string': str, 'integer': int, 'float': float}),
                required=False,
            ),
        ],
    )

    planner = Container.planners.get(SchemaCommandPlanner)
    plan = planner.plan_schema_command(
        SchemaCommand(
            mutations=[
                RegisterSchema(schema=schema),
            ],
        ),
    )
    plan.execute(transaction_id=None, lock_id=None)

    conn = connection_mng.get_connection_pool('user').get_connection()
    result = conn.query_schema(filters=None)
    assert len(result) == 1
    _schema = result[0]
    assert _schema.name.endswith('user')
    # In Elasticsearch, complex types are all mapped to object type and returned as DictSchemaModel
    # This is because ES doesn't have the same type system granularity as SQL databases
    prop_types = {prop.name: prop.type for prop in _schema.properties}

    # All complex types are converted to DictSchemaModel when stored/retrieved from ES
    assert isinstance(prop_types['dictionary'], DictSchemaModel)
    assert isinstance(prop_types['array'], DictSchemaModel)
    assert isinstance(prop_types['nested_schema'], DictSchemaModel)

    # They all have default key/value types of str
    for prop_name in ['dictionary', 'array', 'nested_schema']:
        prop_type = prop_types[prop_name]
        assert isinstance(prop_type, DictSchemaModel)
        assert prop_type.key_type is str
        assert prop_type.value_type is str


def test_create_schema_embeddings() -> None:
    connection_mng = Container.managers.get(ConnectionManager)
    schema = Schema(
        name='user',
        version=Version.LATEST,
        properties=[
            PropertySchema(
                name='embedding',
                type=VectorSchemaModel(dimensions=3),
                required=False,  # Elasticsearch doesn't enforce required at schema level
            ),
            PropertySchema(
                name='name',
                type=str,
                required=False,
            ),
        ],
    )

    planner = Container.planners.get(SchemaCommandPlanner)
    plan = planner.plan_schema_command(
        SchemaCommand(
            mutations=[
                RegisterSchema(schema=schema),
            ],
        ),
    )
    plan.execute(transaction_id=None, lock_id=None)

    conn = connection_mng.get_connection_pool('user').get_connection()
    result = conn.query_schema(filters=None)
    assert len(result) == 1
    _schema = result[0]
    assert _schema.name.endswith('user')
    assert {prop.name: prop.type for prop in _schema.properties} == {
        'embedding': VectorSchemaModel(dimensions=3),
        'name': str,
    }
