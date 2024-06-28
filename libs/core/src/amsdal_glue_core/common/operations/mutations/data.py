from dataclasses import dataclass

from amsdal_glue_core.common.data_models.conditions import Conditions
from amsdal_glue_core.common.data_models.data import Data
from amsdal_glue_core.common.data_models.schema import SchemaReference


@dataclass(kw_only=True)
class DataMutation:
    schema: SchemaReference


@dataclass(kw_only=True)
class InsertData(DataMutation):
    data: list[Data]


@dataclass(kw_only=True)
class UpdateData(DataMutation):
    data: Data
    query: Conditions | None = None


@dataclass(kw_only=True)
class DeleteData(DataMutation):
    query: Conditions | None = None
