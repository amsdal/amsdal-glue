# mypy: disable-error-code="type-abstract"
from amsdal_glue_core.common.data_models.data import Data
from amsdal_glue_core.common.operations.queries import DataQueryOperation
from amsdal_glue_core.common.services.queries import DataQueryService
from amsdal_glue_core.containers import Container
from fastapi import HTTPException

from amsdal_glue_api_server.controllers.operations.models import query_statement_to_core_query_statement
from amsdal_glue_api_server.controllers.operations.models import QueryStatementBody

__all__ = [
    'QueryStatementBody',
    'data_query_command',
    'query_statement_to_core_query_statement',
]


async def data_query_command(
    query: QueryStatementBody,
    lock_id: str | None = None,
    root_transaction_id: str | None = None,
    transaction_id: str | None = None,
) -> list[Data]:
    query_service = Container.services.get(DataQueryService)
    result = query_service.execute(
        DataQueryOperation(
            query=query_statement_to_core_query_statement(query),
            lock_id=lock_id,
            root_transaction_id=root_transaction_id,
            transaction_id=transaction_id,
        )
    )

    if not result.success:
        raise HTTPException(status_code=400, detail=result.message)

    return result.data or []
