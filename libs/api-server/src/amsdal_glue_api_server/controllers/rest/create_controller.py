# mypy: disable-error-code="type-abstract"
from amsdal_glue_core.common.data_models.data import Data
from amsdal_glue_core.common.data_models.schema import Schema
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.enums import Version
from amsdal_glue_core.common.operations.commands import DataCommand
from amsdal_glue_core.common.operations.mutations.data import InsertData
from amsdal_glue_core.common.services.commands import DataCommandService
from amsdal_glue_core.containers import Container
from fastapi import HTTPException
from pydantic import BaseModel


def generate_create_controller(schema: Schema, schema_model: type[BaseModel]):
    async def _create_object_controller(obj: schema_model) -> schema_model:  # type: ignore[valid-type]
        service = Container.services.get(DataCommandService)
        result = service.execute(
            command=DataCommand(
                mutations=[
                    InsertData(
                        schema=SchemaReference(name=schema.name, version=Version.LATEST),
                        data=[
                            Data(data=obj.model_dump()),  # type: ignore[attr-defined]
                        ],
                    ),
                ],
            ),
        )
        if not result.success:
            raise HTTPException(status_code=400, detail=result.message)

        return obj

    return _create_object_controller
