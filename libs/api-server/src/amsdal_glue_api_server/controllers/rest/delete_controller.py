# mypy: disable-error-code="type-abstract"
from typing import Annotated

from amsdal_glue_core.common.data_models.conditions import Condition
from amsdal_glue_core.common.data_models.conditions import Conditions
from amsdal_glue_core.common.data_models.field_reference import Field
from amsdal_glue_core.common.data_models.field_reference import FieldReference
from amsdal_glue_core.common.data_models.schema import Schema
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.enums import FieldLookup
from amsdal_glue_core.common.enums import Version
from amsdal_glue_core.common.expressions.value import Value
from amsdal_glue_core.common.operations.commands import DataCommand
from amsdal_glue_core.common.operations.mutations.data import DeleteData
from amsdal_glue_core.common.services.commands import DataCommandService
from amsdal_glue_core.containers import Container
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Response
from pydantic import BaseModel


def generate_delete_controller(schema: Schema, pk_parameters: type[BaseModel]):
    async def _delete_object_controller(pk_key_parameter: Annotated[BaseModel, Depends(pk_parameters)]) -> Response:
        service = Container.services.get(DataCommandService)
        result = service.execute(
            command=DataCommand(
                mutations=[
                    DeleteData(
                        schema=SchemaReference(name=schema.name, version=Version.LATEST),
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

        return Response(status_code=204)

    return _delete_object_controller
