# mypy: disable-error-code="type-abstract"
from amsdal_glue_core.common.data_models.data import Data
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.operations.commands import DataCommand
from amsdal_glue_core.common.operations.mutations.data import DataMutation
from amsdal_glue_core.common.operations.mutations.data import DeleteData
from amsdal_glue_core.common.operations.mutations.data import InsertData
from amsdal_glue_core.common.operations.mutations.data import UpdateData
from amsdal_glue_core.common.services.commands import DataCommandService
from amsdal_glue_core.containers import Container
from fastapi import HTTPException
from fastapi import Response
from pydantic import BaseModel

from amsdal_glue_api_server.controllers.operations.models import Conditions
from amsdal_glue_api_server.controllers.operations.models import conditions_to_core_conditions


class InsertDataBody(BaseModel):
    schema: SchemaReference  # type: ignore[assignment]
    data: list[Data]


class UpdateDataBody(BaseModel):
    schema: SchemaReference  # type: ignore[assignment]
    data: Data
    query: Conditions | None = None


class DeleteDataBody(BaseModel):
    schema: SchemaReference  # type: ignore[assignment]
    query: Conditions | None = None


async def _data_command(
    mutation_command: DataMutation,
    lock_id: str | None = None,
    root_transaction_id: str | None = None,
    transaction_id: str | None = None,
) -> Response:
    service = Container.services.get(DataCommandService)
    result = service.execute(
        command=DataCommand(
            lock_id=lock_id,
            root_transaction_id=root_transaction_id,
            transaction_id=transaction_id,
            mutations=[mutation_command],
        ),
    )

    if not result.success:
        raise HTTPException(status_code=400, detail=result.message)

    return Response(status_code=200)


async def insert_command(
    insert_data: InsertDataBody,
    lock_id: str | None = None,
    root_transaction_id: str | None = None,
    transaction_id: str | None = None,
) -> Response:
    return await _data_command(
        mutation_command=InsertData(schema=insert_data.schema, data=insert_data.data),
        lock_id=lock_id,
        root_transaction_id=root_transaction_id,
        transaction_id=transaction_id,
    )


async def update_command(
    update_data: UpdateDataBody,
    lock_id: str | None = None,
    root_transaction_id: str | None = None,
    transaction_id: str | None = None,
) -> Response:
    return await _data_command(
        mutation_command=UpdateData(
            schema=update_data.schema, data=update_data.data, query=conditions_to_core_conditions(update_data.query)
        ),
        lock_id=lock_id,
        root_transaction_id=root_transaction_id,
        transaction_id=transaction_id,
    )


async def delete_command(
    delete_data: DeleteDataBody,
    lock_id: str | None = None,
    root_transaction_id: str | None = None,
    transaction_id: str | None = None,
) -> Response:
    return await _data_command(
        mutation_command=DeleteData(schema=delete_data.schema, query=conditions_to_core_conditions(delete_data.query)),
        lock_id=lock_id,
        root_transaction_id=root_transaction_id,
        transaction_id=transaction_id,
    )
