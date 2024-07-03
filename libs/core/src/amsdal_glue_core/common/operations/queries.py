from dataclasses import dataclass

from amsdal_glue_core.common.data_models.conditions import Conditions
from amsdal_glue_core.common.data_models.query import QueryStatement
from amsdal_glue_core.common.operations.base import Operation


@dataclass(kw_only=True)
class QueryOperationBase(Operation): ...


@dataclass(kw_only=True)
class SchemaQueryOperation(QueryOperationBase):
    filters: Conditions | None


@dataclass(kw_only=True)
class DataQueryOperation(QueryOperationBase):
    query: QueryStatement


@dataclass(kw_only=True)
class ReferencedByQueryOperation(QueryOperationBase):
    filters: Conditions | None


@dataclass(kw_only=True)
class ReferencedToQueryOperation(QueryOperationBase):
    filters: Conditions | None
