from dataclasses import dataclass

from amsdal_glue_core.common.data_models.conditions import Conditions
from amsdal_glue_core.common.data_models.query import QueryStatement
from amsdal_glue_core.common.operations.base import Operation


@dataclass(kw_only=True)
class QueryOperationBase(Operation):
    """Base class for query operations."""


@dataclass(kw_only=True)
class SchemaQueryOperation(QueryOperationBase):
    """Represents a schema query operation.

    Attributes:
        filters (Conditions | None): The conditions to filter the schema query. Defaults to None.
    """

    filters: Conditions | None = None


@dataclass(kw_only=True)
class DataQueryOperation(QueryOperationBase):
    """Represents a data query operation.

    Attributes:
        query (QueryStatement): The query statement to be executed.
    """

    query: QueryStatement


@dataclass(kw_only=True)
class ReferencedByQueryOperation(QueryOperationBase):
    """Represents a query operation to find references by a schema.

    Attributes:
        filters (Conditions | None): The conditions to filter the references. Defaults to None.
    """

    filters: Conditions | None = None


@dataclass(kw_only=True)
class ReferencedToQueryOperation(QueryOperationBase):
    """Represents a query operation to find references to a schema.

    Attributes:
        filters (Conditions | None): The conditions to filter the references. Defaults to None.
    """

    filters: Conditions | None = None
