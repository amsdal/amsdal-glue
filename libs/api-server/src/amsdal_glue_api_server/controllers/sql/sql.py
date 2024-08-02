# mypy: disable-error-code="type-abstract"
from typing import Any

from amsdal_glue_core.common.operations.commands import DataCommand
from amsdal_glue_core.common.operations.commands import SchemaCommand
from amsdal_glue_core.common.operations.queries import DataQueryOperation
from amsdal_glue_core.common.services.commands import DataCommandService
from amsdal_glue_core.common.services.commands import SchemaCommandService
from amsdal_glue_core.common.services.queries import DataQueryService
from amsdal_glue_core.containers import Container
from amsdal_glue_sql_parser.parsers.base import SqlParserBase
from pydantic import BaseModel


class SqlCommandBody(BaseModel):
    sql: str


def process_operation(
    operation,
    lock_id: str | None = None,
    root_transaction_id: str | None = None,
    transaction_id: str | None = None,
):
    if isinstance(operation, DataCommand):
        data_service = Container.services.get(DataCommandService)

        operation.lock_id = lock_id
        operation.root_transaction_id = root_transaction_id
        operation.transaction_id = transaction_id

        return data_service.execute(command=operation)

    if isinstance(operation, SchemaCommand):
        schema_service = Container.services.get(SchemaCommandService)

        operation.lock_id = lock_id
        operation.root_transaction_id = root_transaction_id
        operation.transaction_id = transaction_id

        return schema_service.execute(command=operation)

    if isinstance(operation, DataQueryOperation):
        query_service = Container.services.get(DataQueryService)

        operation.lock_id = lock_id
        operation.root_transaction_id = root_transaction_id
        operation.transaction_id = transaction_id

        return query_service.execute(operation)

    return None


async def sql_command(
    sql_body: SqlCommandBody,
    lock_id: str | None = None,
    root_transaction_id: str | None = None,
    transaction_id: str | None = None,
) -> list[Any]:
    parser = Container.services.get(SqlParserBase)
    operations = parser.parse_sql(sql_body.sql)

    return [
        process_operation(
            operation=operation,
            lock_id=lock_id,
            root_transaction_id=root_transaction_id,
            transaction_id=transaction_id,
        )
        for operation in operations
    ]
