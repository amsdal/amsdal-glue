# mypy: disable-error-code="type-abstract"
from collections.abc import AsyncGenerator
from dataclasses import asdict
from pathlib import Path

import pytest
from amsdal_glue_connections.sql.connections.sqlite_connection import AsyncSqliteConnection
from amsdal_glue_core.common.interfaces.connection_manager import AsyncConnectionManager
from amsdal_glue_core.common.operations.queries import SchemaQueryOperation
from amsdal_glue_core.common.services.queries import AsyncSchemaQueryService
from amsdal_glue_core.containers import Container

import amsdal_glue as glue
from amsdal_glue.connections.connection_pool import DefaultAsyncConnectionPool
from amsdal_glue.initialize import init_default_containers

FIXTURES_PATH = Path(__file__).parent / 'fixtures'


@pytest.fixture(autouse=True)
async def register_default_connection() -> AsyncGenerator[None, None]:
    init_default_containers()
    connection_mng = Container.managers.get(AsyncConnectionManager)

    connection_mng.register_connection_pool(
        DefaultAsyncConnectionPool(
            AsyncSqliteConnection, db_path=FIXTURES_PATH / 'references.sqlite', check_same_thread=False
        )
    )

    try:
        yield
    finally:
        await connection_mng.disconnect_all()


@pytest.mark.asyncio
async def test_schema_query_service_references() -> None:
    query_service = Container.services.get(AsyncSchemaQueryService)
    result = await query_service.execute(
        SchemaQueryOperation(filters=None),
    )
    assert result.success is True
    assert len(result.schemas or []) == 4

    assert list(map(asdict, sorted(result.schemas, key=lambda schema: schema.name if schema else None))) == [  # type: ignore[arg-type,return-value]
        {
            'constraints': [{'fields': ['course_id'], 'name': 'pk_courses'}],
            'extends': None,
            'indexes': [],
            'metadata': None,
            'name': 'courses',
            'namespace': '',
            'properties': [
                {'default': None, 'description': None, 'name': 'course_id', 'required': False, 'type': int},
                {'default': None, 'description': None, 'name': 'title', 'required': True, 'type': str},
            ],
            'version': glue.Version.LATEST,
        },
        {
            'constraints': [
                {'fields': ['student_id', 'course_id'], 'name': 'pk_student_courses'},
                {
                    'fields': ['course_id'],
                    'name': 'fk_course_id',
                    'reference_fields': ['course_id'],
                    'reference_schema': {
                        'alias': None,
                        'metadata': None,
                        'name': 'courses',
                        'namespace': None,
                        'version': glue.Version.LATEST,
                    },
                },
                {
                    'fields': ['student_id'],
                    'name': 'fk_student_id',
                    'reference_fields': ['student_id'],
                    'reference_schema': {
                        'alias': None,
                        'metadata': None,
                        'name': 'students',
                        'namespace': None,
                        'version': glue.Version.LATEST,
                    },
                },
            ],
            'extends': None,
            'indexes': [],
            'metadata': None,
            'name': 'student_courses',
            'namespace': '',
            'properties': [
                {'default': None, 'description': None, 'name': 'student_id', 'required': False, 'type': int},
                {'default': None, 'description': None, 'name': 'course_id', 'required': False, 'type': int},
            ],
            'version': glue.Version.LATEST,
        },
        {
            'constraints': [
                {'fields': ['student_id'], 'name': 'pk_students'},
                {
                    'fields': ['user_id'],
                    'name': 'fk_user_id',
                    'reference_fields': ['user_id'],
                    'reference_schema': {
                        'alias': None,
                        'metadata': None,
                        'name': 'users',
                        'namespace': None,
                        'version': glue.Version.LATEST,
                    },
                },
            ],
            'extends': None,
            'indexes': [],
            'metadata': None,
            'name': 'students',
            'namespace': '',
            'properties': [
                {'default': None, 'description': None, 'name': 'student_id', 'required': False, 'type': int},
                {'default': None, 'description': None, 'name': 'name', 'required': True, 'type': str},
                {'default': None, 'description': None, 'name': 'user_id', 'required': False, 'type': int},
            ],
            'version': glue.Version.LATEST,
        },
        {
            'constraints': [{'fields': ['user_id'], 'name': 'pk_users'}],
            'extends': None,
            'indexes': [],
            'metadata': None,
            'name': 'users',
            'namespace': '',
            'properties': [
                {'default': None, 'description': None, 'name': 'user_id', 'required': False, 'type': int},
                {'default': None, 'description': None, 'name': 'username', 'required': True, 'type': str},
            ],
            'version': glue.Version.LATEST,
        },
    ]
