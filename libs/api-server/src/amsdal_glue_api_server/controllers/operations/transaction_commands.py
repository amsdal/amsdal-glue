# mypy: disable-error-code="type-abstract"
from amsdal_glue_core.common.operations.commands import TransactionCommand
from amsdal_glue_core.common.services.commands import TransactionCommandService
from amsdal_glue_core.containers import Container
from fastapi import HTTPException
from fastapi import Response
from pydantic import BaseModel


class TransactionCommandBody(TransactionCommand, BaseModel):  # type: ignore[misc]
    pass


async def transaction_command(transaction_data: TransactionCommandBody) -> Response:
    service = Container.services.get(TransactionCommandService)
    result = service.execute(command=transaction_data)

    if not result.success:
        raise HTTPException(status_code=400, detail=result.message)

    return Response(status_code=200)
