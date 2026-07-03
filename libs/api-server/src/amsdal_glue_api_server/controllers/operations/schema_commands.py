# mypy: disable-error-code="type-abstract"
from typing import Any
from typing import Union

from amsdal_glue_core.common.data_models.constraints import BaseConstraint
from amsdal_glue_core.common.data_models.constraints import CheckConstraint
from amsdal_glue_core.common.data_models.constraints import ForeignKeyConstraint
from amsdal_glue_core.common.data_models.constraints import PrimaryKeyConstraint
from amsdal_glue_core.common.data_models.constraints import UniqueConstraint
from amsdal_glue_core.common.data_models.indexes import IndexField
from amsdal_glue_core.common.data_models.indexes import IndexSchema
from amsdal_glue_core.common.data_models.schema import PropertySchema
from amsdal_glue_core.common.data_models.schema import Schema
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.data_models.types import FieldType  # noqa: F401 (needed for pydantic model_rebuild)
from amsdal_glue_core.common.enums import ScalarType
from amsdal_glue_core.common.enums import Version
from amsdal_glue_core.common.operations.commands import SchemaCommand
from amsdal_glue_core.common.operations.mutations.schema import AddConstraint
from amsdal_glue_core.common.operations.mutations.schema import AddIndex
from amsdal_glue_core.common.operations.mutations.schema import AddProperty
from amsdal_glue_core.common.operations.mutations.schema import DeleteConstraint
from amsdal_glue_core.common.operations.mutations.schema import DeleteIndex
from amsdal_glue_core.common.operations.mutations.schema import DeleteProperty
from amsdal_glue_core.common.operations.mutations.schema import DeleteSchema
from amsdal_glue_core.common.operations.mutations.schema import RegisterSchema
from amsdal_glue_core.common.operations.mutations.schema import RenameProperty
from amsdal_glue_core.common.operations.mutations.schema import RenameSchema
from amsdal_glue_core.common.operations.mutations.schema import SchemaMutation
from amsdal_glue_core.common.operations.mutations.schema import UpdateProperty
from amsdal_glue_core.common.services.commands import SchemaCommandService
from amsdal_glue_core.containers import Container
from fastapi import HTTPException
from fastapi import Response
from pydantic import BaseModel

from amsdal_glue_api_server.controllers.operations.models import Conditions
from amsdal_glue_api_server.controllers.operations.models import conditions_to_core_conditions
from amsdal_glue_api_server.controllers.operations.models import conditions_to_core_conditions_required


def constraint_to_core_constraint(
    constraint: Union[
        'PrimaryKeyConstraintBody',
        'ForeignKeySchemaBody',
        'UniqueConstraintBody',
        'CheckConstraintBody',
    ],
) -> BaseConstraint:
    if isinstance(constraint, PrimaryKeyConstraintBody):
        return PrimaryKeyConstraint(
            name=constraint.name,
            fields=constraint.fields,
        )

    if isinstance(constraint, ForeignKeySchemaBody):
        return ForeignKeyConstraint(
            name=constraint.name,
            fields=constraint.fields,
            reference_schema=constraint.reference_schema,
            reference_fields=constraint.reference_fields,
        )

    if isinstance(constraint, UniqueConstraintBody):
        return UniqueConstraint(
            name=constraint.name,
            fields=constraint.fields,
            condition=conditions_to_core_conditions(constraint.condition),
        )

    if isinstance(constraint, CheckConstraintBody):
        return CheckConstraint(
            name=constraint.name,
            condition=conditions_to_core_conditions_required(constraint.condition),
        )

    msg = f'Unknown constraint type: {constraint}'
    raise ValueError(msg)


def property_type_to_core_property_type(
    prop_type: Union['SchemaBody', 'SchemaReference', str],
) -> Schema | SchemaReference | ScalarType:
    if isinstance(prop_type, SchemaBody):
        return schema_to_core_schema(prop_type)  # type: ignore[return-value]

    if isinstance(prop_type, SchemaReference):
        return prop_type  # type: ignore[return-value]

    return {
        'int': ScalarType.INTEGER,
        'str': ScalarType.TEXT,
        'float': ScalarType.FLOAT,
        'bool': ScalarType.BOOLEAN,
        'list': ScalarType.JSON,
        'dict': ScalarType.JSONB,
    }.get(prop_type, ScalarType.TEXT)


def property_to_core_property(prop: 'PropertySchemaBody') -> PropertySchema:
    return PropertySchema(
        name=prop.name,
        type=property_type_to_core_property_type(prop.type),  # type: ignore[arg-type]
        required=prop.required,
        description=prop.description,
        default=prop.default,
    )


def schema_to_core_schema(schema: 'SchemaBody') -> Schema:
    return Schema(
        name=schema.name,
        version=schema.version,
        properties=[property_to_core_property(prop) for prop in schema.properties],
        constraints=None,
        namespace=schema.namespace or None,
        indexes=[index_to_core_index(index) for index in schema.indexes or []] or None,
    )


def index_to_core_index(index: 'IndexSchemaBody') -> IndexSchema:
    return IndexSchema(
        name=index.name,
        fields=[IndexField(name=f) for f in index.fields],
        condition=conditions_to_core_conditions(index.condition),
    )


class CheckConstraintBody(BaseModel):
    name: str
    condition: Conditions
    constraint_type: str = 'check'


class ForeignKeySchemaBody(BaseModel):
    name: str
    fields: list[str]
    reference_schema: SchemaReference
    reference_fields: list[str]
    constraint_type: str = 'foreign_key'


class PrimaryKeyConstraintBody(BaseModel):
    name: str
    fields: list[str]
    constraint_type: str = 'primary_key'


class UniqueConstraintBody(BaseModel):
    name: str
    fields: list[str]
    condition: Conditions | None = None
    constraint_type: str = 'unique'


class IndexSchemaBody(BaseModel):
    name: str
    fields: list[str]
    condition: Conditions | None = None


class PropertySchemaBody(BaseModel):
    type: Union['SchemaBody', 'SchemaReference', str]
    name: str
    required: bool
    description: str | None = None
    default: Any | None = None


class SchemaBody(BaseModel):
    properties: list[PropertySchemaBody]
    indexes: list[IndexSchemaBody] | None = None
    namespace: str = ''
    name: str
    version: str | Version


PropertySchemaBody.model_rebuild()
SchemaBody.model_rebuild()


class RegisterSchemaBody(BaseModel):
    schema: SchemaBody  # type: ignore[assignment]


class DeleteSchemaBody(BaseModel):
    schema_reference: SchemaReference


class RenameSchemaBody(BaseModel):
    schema_reference: SchemaReference
    new_schema_name: str


class AddPropertyBody(BaseModel):
    schema_reference: SchemaReference
    property: PropertySchemaBody


class DeletePropertyBody(BaseModel):
    schema_reference: SchemaReference
    property_name: str


class RenamePropertyBody(BaseModel):
    schema_reference: SchemaReference
    old_name: str
    new_name: str


class UpdatePropertyBody(BaseModel):
    schema_reference: SchemaReference
    property: PropertySchemaBody


class AddConstraintBody(BaseModel):
    schema_reference: SchemaReference
    constraint: PrimaryKeyConstraintBody | ForeignKeySchemaBody | UniqueConstraintBody | CheckConstraintBody


class DeleteConstraintBody(BaseModel):
    schema_reference: SchemaReference
    constraint_name: str


class AddIndexBody(BaseModel):
    schema_reference: SchemaReference
    index: IndexSchemaBody


class DeleteIndexBody(BaseModel):
    schema_reference: SchemaReference
    index_name: str


async def _execute_schema_command(
    schema_mutation: SchemaMutation,
    lock_id: str | None = None,
    root_transaction_id: str | None = None,
    transaction_id: str | None = None,
) -> Response:
    service = Container.services.get(SchemaCommandService)
    result = service.execute(
        command=SchemaCommand(
            lock_id=lock_id,
            root_transaction_id=root_transaction_id,
            transaction_id=transaction_id,
            mutations=[schema_mutation],
        ),
    )
    if not result.success:
        raise HTTPException(status_code=400, detail=result.message)
    return Response(status_code=200)


async def register_schema(
    register_schema_body: RegisterSchemaBody,
    lock_id: str | None = None,
    root_transaction_id: str | None = None,
    transaction_id: str | None = None,
) -> Response:
    _schema = schema_to_core_schema(register_schema_body.schema)
    return await _execute_schema_command(
        schema_mutation=RegisterSchema(
            schema_ref=SchemaReference(name=_schema.name, version=_schema.version, namespace=_schema.namespace),
            schema=_schema,
        ),
        lock_id=lock_id,
        root_transaction_id=root_transaction_id,
        transaction_id=transaction_id,
    )


async def delete_schema(
    delete_schema_body: DeleteSchemaBody,
    lock_id: str | None = None,
    root_transaction_id: str | None = None,
    transaction_id: str | None = None,
) -> Response:
    return await _execute_schema_command(
        schema_mutation=DeleteSchema(schema_ref=delete_schema_body.schema_reference),
        lock_id=lock_id,
        root_transaction_id=root_transaction_id,
        transaction_id=transaction_id,
    )


async def rename_schema(
    rename_schema_body: RenameSchemaBody,
    lock_id: str | None = None,
    root_transaction_id: str | None = None,
    transaction_id: str | None = None,
) -> Response:
    return await _execute_schema_command(
        schema_mutation=RenameSchema(
            schema_ref=rename_schema_body.schema_reference,
            new_name=rename_schema_body.new_schema_name,
        ),
        lock_id=lock_id,
        root_transaction_id=root_transaction_id,
        transaction_id=transaction_id,
    )


async def add_property(
    add_property_body: AddPropertyBody,
    lock_id: str | None = None,
    root_transaction_id: str | None = None,
    transaction_id: str | None = None,
) -> Response:
    return await _execute_schema_command(
        schema_mutation=AddProperty(
            schema_ref=add_property_body.schema_reference,
            property=property_to_core_property(add_property_body.property),
        ),
        lock_id=lock_id,
        root_transaction_id=root_transaction_id,
        transaction_id=transaction_id,
    )


async def delete_property(
    delete_property_body: DeletePropertyBody,
    lock_id: str | None = None,
    root_transaction_id: str | None = None,
    transaction_id: str | None = None,
) -> Response:
    return await _execute_schema_command(
        schema_mutation=DeleteProperty(
            schema_ref=delete_property_body.schema_reference,
            property_name=delete_property_body.property_name,
        ),
        lock_id=lock_id,
        root_transaction_id=root_transaction_id,
        transaction_id=transaction_id,
    )


async def rename_property(
    rename_property_body: RenamePropertyBody,
    lock_id: str | None = None,
    root_transaction_id: str | None = None,
    transaction_id: str | None = None,
) -> Response:
    return await _execute_schema_command(
        schema_mutation=RenameProperty(
            schema_ref=rename_property_body.schema_reference,
            old_name=rename_property_body.old_name,
            new_name=rename_property_body.new_name,
        ),
        lock_id=lock_id,
        root_transaction_id=root_transaction_id,
        transaction_id=transaction_id,
    )


async def update_property(
    update_property_body: UpdatePropertyBody,
    lock_id: str | None = None,
    root_transaction_id: str | None = None,
    transaction_id: str | None = None,
) -> Response:
    return await _execute_schema_command(
        schema_mutation=UpdateProperty(
            schema_ref=update_property_body.schema_reference,
            property=property_to_core_property(update_property_body.property),
        ),
        lock_id=lock_id,
        root_transaction_id=root_transaction_id,
        transaction_id=transaction_id,
    )


async def add_constraint(
    add_constraint_body: AddConstraintBody,
    lock_id: str | None = None,
    root_transaction_id: str | None = None,
    transaction_id: str | None = None,
) -> Response:
    return await _execute_schema_command(
        schema_mutation=AddConstraint(
            schema_ref=add_constraint_body.schema_reference,
            constraint=constraint_to_core_constraint(add_constraint_body.constraint),
        ),
        lock_id=lock_id,
        root_transaction_id=root_transaction_id,
        transaction_id=transaction_id,
    )


async def delete_constraint(
    delete_constraint_body: DeleteConstraintBody,
    lock_id: str | None = None,
    root_transaction_id: str | None = None,
    transaction_id: str | None = None,
) -> Response:
    return await _execute_schema_command(
        schema_mutation=DeleteConstraint(
            schema_ref=delete_constraint_body.schema_reference,
            constraint_name=delete_constraint_body.constraint_name,
        ),
        lock_id=lock_id,
        root_transaction_id=root_transaction_id,
        transaction_id=transaction_id,
    )


async def add_index(
    add_index_body: AddIndexBody,
    lock_id: str | None = None,
    root_transaction_id: str | None = None,
    transaction_id: str | None = None,
) -> Response:
    return await _execute_schema_command(
        schema_mutation=AddIndex(
            schema_ref=add_index_body.schema_reference,
            index=index_to_core_index(add_index_body.index),
        ),
        lock_id=lock_id,
        root_transaction_id=root_transaction_id,
        transaction_id=transaction_id,
    )


async def delete_index(
    delete_index_body: DeleteIndexBody,
    lock_id: str | None = None,
    root_transaction_id: str | None = None,
    transaction_id: str | None = None,
) -> Response:
    return await _execute_schema_command(
        schema_mutation=DeleteIndex(
            schema_ref=delete_index_body.schema_reference,
            index_name=delete_index_body.index_name,
        ),
        lock_id=lock_id,
        root_transaction_id=root_transaction_id,
        transaction_id=transaction_id,
    )
