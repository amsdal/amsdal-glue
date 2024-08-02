# mypy: disable-error-code="type-abstract"
from typing import Any

from amsdal_glue_core.common.data_models.constraints import PrimaryKeyConstraint
from amsdal_glue_core.common.data_models.schema import Schema
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.operations.queries import SchemaQueryOperation
from amsdal_glue_core.common.services.queries import SchemaQueryService
from amsdal_glue_core.containers import Container
from fastapi import FastAPI
from pydantic import BaseModel
from pydantic import create_model

from amsdal_glue_api_server.controllers.operations.data_commands import delete_command
from amsdal_glue_api_server.controllers.operations.data_commands import insert_command
from amsdal_glue_api_server.controllers.operations.data_commands import update_command
from amsdal_glue_api_server.controllers.operations.query_commands import data_query_command
from amsdal_glue_api_server.controllers.operations.schema_commands import add_constraint
from amsdal_glue_api_server.controllers.operations.schema_commands import add_index
from amsdal_glue_api_server.controllers.operations.schema_commands import add_property
from amsdal_glue_api_server.controllers.operations.schema_commands import delete_constraint
from amsdal_glue_api_server.controllers.operations.schema_commands import delete_index
from amsdal_glue_api_server.controllers.operations.schema_commands import delete_property
from amsdal_glue_api_server.controllers.operations.schema_commands import delete_schema
from amsdal_glue_api_server.controllers.operations.schema_commands import register_schema
from amsdal_glue_api_server.controllers.operations.schema_commands import rename_property
from amsdal_glue_api_server.controllers.operations.schema_commands import rename_schema
from amsdal_glue_api_server.controllers.operations.schema_commands import update_property
from amsdal_glue_api_server.controllers.operations.transaction_commands import transaction_command
from amsdal_glue_api_server.controllers.rest.create_controller import generate_create_controller
from amsdal_glue_api_server.controllers.rest.delete_controller import generate_delete_controller
from amsdal_glue_api_server.controllers.rest.list_controller import generate_list_controller
from amsdal_glue_api_server.controllers.rest.update_controller import generate_update_controller
from amsdal_glue_api_server.controllers.sql.sql import sql_command


def _fetch_schemas() -> list[Schema | None]:
    query_service = Container.services.get(SchemaQueryService)
    result = query_service.execute(
        SchemaQueryOperation(filters=None),
    )

    if not result.success:
        raise ValueError(result.message)

    if result.schemas is None:
        msg = 'No schemas found'
        raise ValueError(msg)

    return result.schemas or []


def model_from_schema(schema: Schema) -> type[BaseModel]:
    properties = {}
    _type: type[BaseModel | Any] | None
    for prop in schema.properties:
        if isinstance(prop.type, Schema):
            _type = model_from_schema(prop.type)
        elif isinstance(prop.type, SchemaReference):
            _type = int
        else:
            _type = prop.type

        if not prop.required:
            _type = _type | None  # type: ignore[assignment,operator]

        properties[prop.name] = (_type, prop.default)

    return create_model(schema.name.capitalize(), **properties)  # type: ignore[call-overload]


def _get_primary_key_constraint(schema: Schema) -> PrimaryKeyConstraint | None:
    for constraint in schema.constraints or []:
        if isinstance(constraint, PrimaryKeyConstraint):
            return constraint

    return None


def _create_pk_parameter(pk_constraint: PrimaryKeyConstraint) -> type[BaseModel]:
    pk_parameters = {field: (str, None) for field in pk_constraint.fields}

    return create_model('PathParameters', **pk_parameters)  # type: ignore[call-overload]


def register_model_routes(app: FastAPI, schema: Schema) -> None:
    schema_model: type[BaseModel] = model_from_schema(schema)
    pk_constraint = _get_primary_key_constraint(schema)

    app.add_api_route(
        f'/api/v1/schemas/{schema.name}/',
        generate_list_controller(schema, schema_model),
        methods=['GET'],
        summary=f"List all objects in the '{schema.name}' schema",
        status_code=200,
        tags=['REST'],
    )
    app.add_api_route(
        f'/api/v1/schemas/{schema.name}/',
        generate_create_controller(schema, schema_model),
        methods=['POST'],
        summary=f"Create a new object in the '{schema.name}' schema",
        status_code=201,
        tags=['REST'],
    )

    if pk_constraint is not None:
        path_parts = '/'.join([f'{{{field}}}' for field in sorted(pk_constraint.fields)])
        pk_parameters = _create_pk_parameter(pk_constraint)
        app.add_api_route(
            f'/api/v1/schemas/{schema.name}/{path_parts}/',
            generate_update_controller(schema, schema_model, pk_parameters),
            methods=['PUT'],
            summary=f"Update an object in the '{schema.name}' schema",
            status_code=200,
            tags=['REST'],
        )
        app.add_api_route(
            f'/api/v1/schemas/{schema.name}/{path_parts}/',
            generate_delete_controller(schema, pk_parameters),
            methods=['DELETE'],
            summary=f"Delete an object in the '{schema.name}' schema",
            status_code=204,
            tags=['REST'],
        )


def register_routes(
    app: FastAPI,
    *,
    enable_rest_api: bool = True,
    enable_general_api: bool = True,
    enable_sql_api: bool = True,
) -> None:
    if enable_rest_api:
        for schema in _fetch_schemas():
            if schema is None:
                continue

            register_model_routes(app, schema)

    if enable_general_api:
        app.add_api_route(
            '/api/v1/operations/update-command/',
            update_command,
            methods=['POST'],
            summary='Update data command',
            status_code=200,
            tags=['Operations'],
        )

        app.add_api_route(
            '/api/v1/operations/insert-command/',
            insert_command,
            methods=['POST'],
            summary='Insert data command',
            status_code=200,
            tags=['Operations'],
        )
        app.add_api_route(
            '/api/v1/operations/delete-command/',
            delete_command,
            methods=['POST'],
            summary='Delete data command',
            status_code=200,
            tags=['Operations'],
        )

        app.add_api_route(
            '/api/v1/operations/register-schema/',
            register_schema,
            methods=['POST'],
            summary='Register schema',
            status_code=200,
            tags=['Operations'],
        )
        app.add_api_route(
            '/api/v1/operations/delete-schema/',
            delete_schema,
            methods=['POST'],
            summary='Delete schema',
            status_code=200,
            tags=['Operations'],
        )
        app.add_api_route(
            '/api/v1/operations/rename-schema/',
            rename_schema,
            methods=['POST'],
            summary='Rename schema',
            status_code=200,
            tags=['Operations'],
        )
        app.add_api_route(
            '/api/v1/operations/add-property/',
            add_property,
            methods=['POST'],
            summary='Add property',
            status_code=200,
            tags=['Operations'],
        )
        app.add_api_route(
            '/api/v1/operations/delete-property/',
            delete_property,
            methods=['POST'],
            summary='Delete property',
            status_code=200,
            tags=['Operations'],
        )
        app.add_api_route(
            '/api/v1/operations/rename-property/',
            rename_property,
            methods=['POST'],
            summary='Rename property',
            status_code=200,
            tags=['Operations'],
        )
        app.add_api_route(
            '/api/v1/operations/update-property/',
            update_property,
            methods=['POST'],
            summary='Update property',
            status_code=200,
            tags=['Operations'],
        )
        app.add_api_route(
            '/api/v1/operations/add-constraint/',
            add_constraint,
            methods=['POST'],
            summary='Add constraint',
            status_code=200,
            tags=['Operations'],
        )
        app.add_api_route(
            '/api/v1/operations/delete-constraint/',
            delete_constraint,
            methods=['POST'],
            summary='Delete constraint',
            status_code=200,
            tags=['Operations'],
        )
        app.add_api_route(
            '/api/v1/operations/add-index/',
            add_index,
            methods=['POST'],
            summary='Add index',
            status_code=200,
            tags=['Operations'],
        )
        app.add_api_route(
            '/api/v1/operations/delete-index/',
            delete_index,
            methods=['POST'],
            summary='Delete index',
            status_code=200,
            tags=['Operations'],
        )
        app.add_api_route(
            '/api/v1/operations/transaction-command/',
            transaction_command,
            methods=['POST'],
            summary='Transaction command',
            status_code=200,
            tags=['Operations'],
        )
        app.add_api_route(
            '/api/v1/operations/data-query/',
            data_query_command,  # type: ignore[arg-type]
            methods=['POST'],
            summary='Data query',
            status_code=200,
            tags=['Operations'],
        )

    if enable_sql_api:
        app.add_api_route(
            '/api/v1/sql/command/',
            sql_command,  # type: ignore[arg-type]
            methods=['POST'],
            summary='SQL command',
            status_code=200,
            tags=['SQL'],
        )
