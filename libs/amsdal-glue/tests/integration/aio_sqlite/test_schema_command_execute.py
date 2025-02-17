# mypy: disable-error-code="type-abstract"
import tempfile
from collections.abc import AsyncGenerator
from pathlib import Path

import pytest
from amsdal_glue_connections.sql.connections.sqlite_connection import AsyncSqliteConnection
from amsdal_glue_core.commands.planner.schema_command_planner import AsyncSchemaCommandPlanner
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
from amsdal_glue_core.common.enums import FieldLookup
from amsdal_glue_core.common.enums import Version
from amsdal_glue_core.common.expressions.field_reference import FieldReferenceExpression
from amsdal_glue_core.common.expressions.value import Value
from amsdal_glue_core.common.interfaces.connection_manager import AsyncConnectionManager
from amsdal_glue_core.common.operations.commands import SchemaCommand
from amsdal_glue_core.common.operations.mutations.schema import RegisterSchema
from amsdal_glue_core.common.operations.queries import SchemaQueryOperation
from amsdal_glue_core.common.services.queries import AsyncSchemaQueryService
from amsdal_glue_core.containers import Container

from amsdal_glue.connections.connection_pool import DefaultAsyncConnectionPool
from amsdal_glue.initialize import init_default_containers


@pytest.fixture(autouse=True)
async def register_default_connection() -> AsyncGenerator[None, None]:
    init_default_containers()
    connection_mng = Container.managers.get(AsyncConnectionManager)

    with tempfile.TemporaryDirectory() as temp_dir:
        db_path = f'{temp_dir}/data.sqlite'
        connection_mng.register_connection_pool(
            DefaultAsyncConnectionPool(AsyncSqliteConnection, db_path=Path(db_path), check_same_thread=False),
        )

        try:
            yield
        finally:
            await connection_mng.disconnect_all()


@pytest.mark.asyncio
async def test_create_schema(register_default_connection: AsyncGenerator[None, None]) -> None:
    async for _ in register_default_connection:
        connection_mng = Container.managers.get(AsyncConnectionManager)
        schema = Schema(
            name='user',
            version=Version.LATEST,
            properties=[
                PropertySchema(
                    name='id',
                    type=int,
                    required=True,
                ),
                PropertySchema(
                    name='email',
                    type=str,
                    required=True,
                ),
                PropertySchema(
                    name='age',
                    type=int,
                    required=True,
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

        planner = Container.planners.get(AsyncSchemaCommandPlanner)
        plan = planner.plan_schema_command(
            SchemaCommand(
                mutations=[
                    RegisterSchema(schema=schema),
                ],
            ),
        )
        await plan.execute(transaction_id=None, lock_id=None)

        conn = await connection_mng.get_connection_pool('user').get_connection()
        result = await conn.query_schema(filters=None)
        assert len(result) == 1
        _schema = result[0]
        assert _schema.name == 'user'
        assert {prop.name: prop.type for prop in _schema.properties} == {
            'id': int,
            'email': str,
            'age': int,
            'first_name': str,
            'last_name': str,
        }
        query_service = Container.services.get(AsyncSchemaQueryService)
        schema_result = await query_service.execute(
            SchemaQueryOperation(filters=None),
        )

        assert schema_result.schemas == [
            Schema(
                name='user',
                version=Version.LATEST,
                properties=[
                    PropertySchema(
                        name='id',
                        type=int,
                        required=True,
                    ),
                    PropertySchema(
                        name='email',
                        type=str,
                        required=True,
                    ),
                    PropertySchema(
                        name='age',
                        type=int,
                        required=True,
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
                ],
                indexes=[
                    IndexSchema(name='idx_user_email', fields=['first_name', 'last_name']),
                ],
            )
        ]


@pytest.mark.asyncio
async def test_create_schema_complex_types(register_default_connection: AsyncGenerator[None, None]) -> None:
    async for _ in register_default_connection:
        connection_mng = Container.managers.get(AsyncConnectionManager)
        schema = Schema(
            name='user',
            version=Version.LATEST,
            properties=[
                PropertySchema(
                    name='dictionary',
                    type=DictSchemaModel(key_type=str, value_type=int),
                    required=True,
                ),
                PropertySchema(
                    name='array',
                    type=ArraySchemaModel(item_type=str),
                    required=True,
                ),
                PropertySchema(
                    name='nested_schema',
                    type=NestedSchemaModel(properties={'string': str, 'integer': int, 'float': float}),
                    required=True,
                ),
            ],
        )

        planner = Container.planners.get(AsyncSchemaCommandPlanner)
        plan = planner.plan_schema_command(
            SchemaCommand(
                mutations=[
                    RegisterSchema(schema=schema),
                ],
            ),
        )
        await plan.execute(transaction_id=None, lock_id=None)

        conn = await connection_mng.get_connection_pool('user').get_connection()
        result = await conn.query_schema(filters=None)
        assert len(result) == 1
        _schema = result[0]
        assert _schema.name == 'user'
        assert {prop.name: prop.type for prop in _schema.properties} == {
            'dictionary': dict,
            'array': dict,
            'nested_schema': dict,
        }
