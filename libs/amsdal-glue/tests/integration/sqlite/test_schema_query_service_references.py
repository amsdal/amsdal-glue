# mypy: disable-error-code="type-abstract"
from collections.abc import Generator
from dataclasses import asdict
from pathlib import Path

import pytest
from amsdal_glue_connections.sql.connections.sqlite_connection import SqliteConnection
from amsdal_glue_connections.sql.schema_registry import TABLE_REGISTRY
from amsdal_glue_core.common.data_models.query import QueryStatement
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.enums import ReferentialAction
from amsdal_glue_core.common.enums import ScalarType
from amsdal_glue_core.common.enums import Version
from amsdal_glue_core.common.interfaces.connection_manager import ConnectionManager
from amsdal_glue_core.common.operations.queries import SchemaQueryOperation
from amsdal_glue_core.common.services.queries import SchemaQueryService
from amsdal_glue_core.containers import Container

import amsdal_glue as glue
from amsdal_glue.connections.connection_pool import DefaultConnectionPool
from amsdal_glue.initialize import init_default_containers

FIXTURES_PATH = Path(__file__).parent / 'fixtures'


@pytest.fixture(autouse=True)
def _register_default_connection() -> Generator[None, None, None]:
    init_default_containers()
    connection_mng = Container.managers.get(ConnectionManager)

    connection_mng.register_connection_pool(
        DefaultConnectionPool(SqliteConnection, db_path=FIXTURES_PATH / 'references.sqlite', check_same_thread=False)
    )

    try:
        yield
    finally:
        connection_mng.disconnect_all()


def test_schema_query_service_references() -> None:
    query_service = Container.services.get(SchemaQueryService)
    result = query_service.execute(
        SchemaQueryOperation(query=QueryStatement(table=SchemaReference(name=TABLE_REGISTRY, version=Version.LATEST))),
    )
    assert result.success is True
    assert result.schemas
    assert len(result.schemas or []) == 4

    _prop = lambda name, type_, required=False: {  # noqa: E731
        'name': name,
        'type': type_,
        'required': required,
        'description': None,
        'default': None,
        'generated': None,
        'db_collation': None,
        'identity': None,
    }
    _fk = lambda name, fields, ref_name, ref_fields: {  # noqa: E731
        'name': name,
        'fields': fields,
        'reference_schema': {
            'name': ref_name,
            'version': glue.Version.LATEST,
            'alias': None,
            'namespace': None,
            'metadata': None,
        },
        'reference_fields': ref_fields,
        'on_delete': ReferentialAction.NO_ACTION,
        'on_update': ReferentialAction.NO_ACTION,
    }

    assert list(map(asdict, sorted((result.schemas or []), key=lambda schema: schema.name if schema else None))) == [  # type: ignore[arg-type,return-value]
        {
            'name': 'courses',
            'version': glue.Version.LATEST,
            'namespace': None,
            'properties': [
                _prop('course_id', ScalarType.INTEGER),
                _prop('title', ScalarType.TEXT, required=True),
            ],
            'constraints': [{'name': 'pk_courses', 'fields': ['course_id']}],
            'indexes': None,
            'metadata': None,
        },
        {
            'name': 'student_courses',
            'version': glue.Version.LATEST,
            'namespace': None,
            'properties': [
                _prop('student_id', ScalarType.INTEGER),
                _prop('course_id', ScalarType.INTEGER),
            ],
            'constraints': [
                {'name': 'pk_student_courses', 'fields': ['student_id', 'course_id']},
                _fk('fk_course_id', ['course_id'], 'courses', ['course_id']),
                _fk('fk_student_id', ['student_id'], 'students', ['student_id']),
            ],
            'indexes': None,
            'metadata': None,
        },
        {
            'name': 'students',
            'version': glue.Version.LATEST,
            'namespace': None,
            'properties': [
                _prop('student_id', ScalarType.INTEGER),
                _prop('name', ScalarType.TEXT, required=True),
                _prop('user_id', ScalarType.INTEGER),
            ],
            'constraints': [
                {'name': 'pk_students', 'fields': ['student_id']},
                _fk('fk_students_0', ['user_id'], 'users', ['user_id']),
            ],
            'indexes': None,
            'metadata': None,
        },
        {
            'name': 'users',
            'version': glue.Version.LATEST,
            'namespace': None,
            'properties': [
                _prop('user_id', ScalarType.INTEGER),
                _prop('username', ScalarType.TEXT, required=True),
            ],
            'constraints': [{'name': 'pk_users', 'fields': ['user_id']}],
            'indexes': None,
            'metadata': None,
        },
    ]
