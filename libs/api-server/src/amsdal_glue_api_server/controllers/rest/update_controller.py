# mypy: disable-error-code="type-abstract"
from typing import Annotated

from amsdal_glue_core.common.data_models.conditions import Condition
from amsdal_glue_core.common.data_models.conditions import Conditions
from amsdal_glue_core.common.data_models.data import Data
from amsdal_glue_core.common.data_models.field_reference import Field
from amsdal_glue_core.common.data_models.field_reference import FieldReference
from amsdal_glue_core.common.data_models.schema import Schema
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.enums import FieldLookup
from amsdal_glue_core.common.enums import Version
from amsdal_glue_core.common.expressions.value import Value
from amsdal_glue_core.common.operations.commands import DataCommand
from amsdal_glue_core.common.operations.mutations.data import UpdateData
from amsdal_glue_core.common.services.commands import DataCommandService
from amsdal_glue_core.containers import Container
from fastapi import Depends
from fastapi import HTTPException
from pydantic import BaseModel


def generate_update_controller(schema: Schema, schema_model: type[BaseModel], pk_parameters: type[BaseModel]):
    async def _update_object_controller(
        pk_key_parameter: Annotated[BaseModel, Depends(pk_parameters)],
        obj: schema_model,  # type: ignore[valid-type]
    ) -> schema_model:  # type: ignore[valid-type]
        service = Container.services.get(DataCommandService)
        result = service.execute(
            command=DataCommand(
                mutations=[
                    UpdateData(
                        schema=SchemaReference(name=schema.name, version=Version.LATEST),
                        data=Data(data=obj.model_dump()),  # type: ignore[attr-defined]
                        query=Conditions(
                            *(
                                Condition(
                                    field=FieldReference(field=Field(name=pk_field), table_name=schema.name),
                                    lookup=FieldLookup.EQ,
                                    value=Value(pk_value),
                                )
                                for pk_field, pk_value in pk_key_parameter.model_dump().items()
                            )
                        ),
                    ),
                ],
            ),
        )

        if not result.success:
            raise HTTPException(status_code=400, detail=result.message)

        return obj

    return _update_object_controller
