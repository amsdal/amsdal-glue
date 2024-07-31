from dataclasses import dataclass

from amsdal_glue_core.common.data_models.conditions import Conditions
from amsdal_glue_core.common.data_models.data import Data
from amsdal_glue_core.common.data_models.schema import SchemaReference


@dataclass(kw_only=True)
class DataMutation:
    """Represents a data mutation operation.

    Attributes:
        schema (SchemaReference): The schema reference associated with the data mutation.
    """

    schema: SchemaReference


@dataclass(kw_only=True)
class InsertData(DataMutation):
    """Represents an insert data mutation.

    Attributes:
        data (list[Data]): The list of data to be inserted.
    """

    data: list[Data]


@dataclass(kw_only=True)
class UpdateData(DataMutation):
    """Represents an update data mutation.

    Attributes:
        data (Data): The data to be updated.
        query (Conditions | None): The conditions to filter the data to be updated. Defaults to None.
    """

    data: Data
    query: Conditions | None = None


@dataclass(kw_only=True)
class DeleteData(DataMutation):
    """Represents a delete data mutation.

    Attributes:
        query (Conditions | None): The conditions to filter the data to be deleted. Defaults to None.
    """

    query: Conditions | None = None
