# mypy: disable-error-code="type-abstract"
import re
from typing import Annotated
from typing import Any

from amsdal_glue_core.common.data_models.conditions import Condition
from amsdal_glue_core.common.data_models.conditions import Conditions
from amsdal_glue_core.common.data_models.field_reference import Field
from amsdal_glue_core.common.data_models.field_reference import FieldReference
from amsdal_glue_core.common.data_models.limit import LimitQuery
from amsdal_glue_core.common.data_models.order_by import OrderByQuery
from amsdal_glue_core.common.data_models.query import QueryStatement
from amsdal_glue_core.common.data_models.schema import Schema
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.enums import FieldLookup
from amsdal_glue_core.common.enums import OrderDirection
from amsdal_glue_core.common.enums import Version
from amsdal_glue_core.common.expressions.value import Value
from amsdal_glue_core.common.operations.queries import DataQueryOperation
from amsdal_glue_core.common.services.queries import DataQueryService
from amsdal_glue_core.containers import Container
from fastapi import Depends
from pydantic import BaseModel
from pydantic import create_model


class _EmptyFilter:
    pass


FILTER_PATTERN = re.compile(
    r'((?P<negated>not\.)?(?P<operator>{})\.)?(?P<value>.+)'.format(
        '|'.join(key.lower() for key in FieldLookup.__members__)
    )
)
ORDER_PATTERN = re.compile(r'(?P<field>\w+)(\.(?P<direction>asc|desc))?')


def _create_filters(schema: Schema) -> type[BaseModel]:
    query_params = {}
    for prop in schema.properties:
        if isinstance(prop.type, Schema):
            continue

        if isinstance(prop.type, SchemaReference):
            query_params[prop.name] = (int | type[_EmptyFilter], _EmptyFilter)
        else:
            query_params[prop.name] = (str | type[_EmptyFilter], _EmptyFilter)

    return create_model('Query', **query_params)  # type: ignore[call-overload]


def _process_filter(schema: Schema, filter_name: str, filter_values: str):
    _match = FILTER_PATTERN.match(filter_values)

    if not _match:
        return None

    negated = False
    if _match.group('negated') is not None:
        negated = True

    lookup = FieldLookup.EQ
    if _match.group('operator') is not None:
        lookup = FieldLookup(_match.group('operator').upper())

    value = _match.group('value')
    return Condition(
        field=FieldReference(field=Field(name=filter_name), table_name=schema.name),
        lookup=lookup,
        value=Value(value),
        negate=negated,
    )


def _process_filters(schema: Schema, filters: dict[str, Any]):
    conditions = []
    for filter_name, filter_value in filters.items():
        if filter_value is _EmptyFilter:
            continue

        if not (_condition := _process_filter(schema, filter_name, filter_value)):
            continue
        conditions.append(_condition)

    if not conditions:
        return None

    return Conditions(*conditions)


def _process_order(schema: Schema, order: str | None = None):
    if not order:
        return None

    orderings = []
    for _match in ORDER_PATTERN.findall(order):
        field_name = _match[0]
        desc = _match[2] == 'desc'
        orderings.append(
            OrderByQuery(
                field=FieldReference(field=Field(name=field_name), table_name=schema.name),
                direction=OrderDirection.DESC if desc else OrderDirection.ASC,
            )
        )

    return orderings


def generate_list_controller(schema: Schema, schema_model: type[BaseModel]):
    async def _list_objects_controller(
        filter_parameters: Annotated[BaseModel, Depends(_create_filters(schema))],
        limit: int | None = None,
        offset: int | None = None,
        order: str | None = None,
    ) -> list[schema_model]:  # type: ignore[valid-type]
        query = QueryStatement(
            table=SchemaReference(name=schema.name, version=Version.LATEST),
            where=_process_filters(schema, filter_parameters.model_dump()),
            limit=LimitQuery(limit=limit, offset=offset or 0) if limit is not None else None,
            order_by=_process_order(schema, order),
        )

        query_service = Container.services.get(DataQueryService)
        result = query_service.execute(
            DataQueryOperation(query=query),
        )

        return [schema_model(**d.data) for d in (result.data or [])]

    return _list_objects_controller
