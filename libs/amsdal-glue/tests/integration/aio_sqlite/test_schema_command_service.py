# mypy: disable-error-code="type-abstract"
import tempfile
from collections.abc import AsyncGenerator
from pathlib import Path

import pytest
from amsdal_glue_connections.sql.connections.sqlite_connection import AsyncSqliteConnection
from amsdal_glue_core.common.data_models.conditions import Condition
from amsdal_glue_core.common.data_models.conditions import Conditions
from amsdal_glue_core.common.data_models.constraints import CheckConstraint
from amsdal_glue_core.common.data_models.constraints import PrimaryKeyConstraint
from amsdal_glue_core.common.data_models.constraints import UniqueConstraint
from amsdal_glue_core.common.data_models.field_reference import Field
from amsdal_glue_core.common.data_models.field_reference import FieldReference
from amsdal_glue_core.common.data_models.indexes import IndexSchema
from amsdal_glue_core.common.data_models.schema import PropertySchema
from amsdal_glue_core.common.data_models.schema import Schema
from amsdal_glue_core.common.enums import FieldLookup
from amsdal_glue_core.common.enums import Version
from amsdal_glue_core.common.expressions.field_reference import FieldReferenceExpression
from amsdal_glue_core.common.expressions.value import Value
from amsdal_glue_core.common.interfaces.connection_manager import AsyncConnectionManager
from amsdal_glue_core.common.operations.commands import SchemaCommand
from amsdal_glue_core.common.operations.mutations.schema import RegisterSchema
from amsdal_glue_core.common.services.commands import AsyncSchemaCommandService
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
async def test_schema_command_service(register_default_connection: AsyncGenerator[None, None]) -> None:
    async for _ in register_default_connection:
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
                PrimaryKeyConstraint(name='pk_user', fields=['id']),
                UniqueConstraint(name='uk_user_email', fields=['email'], condition=None),
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
        service = Container.services.get(AsyncSchemaCommandService)
        result = await service.execute(
            SchemaCommand(
                mutations=[
                    RegisterSchema(schema=schema),
                ],
            ),
        )

        assert result.success is True
        assert result.schemas == [None]
