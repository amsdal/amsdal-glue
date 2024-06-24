from dataclasses import dataclass

from amsdal_glue_core.common.data_models.conditions import Conditions
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.enums import LockAction
from amsdal_glue_core.common.enums import LockMode
from amsdal_glue_core.common.enums import LockParameter
from amsdal_glue_core.common.enums import TransactionAction
from amsdal_glue_core.common.operations.base import Operation
from amsdal_glue_core.common.operations.mutations.data import DataMutation
from amsdal_glue_core.common.operations.mutations.schema import SchemaMutation


@dataclass(kw_only=True)
class SchemaCommand(Operation):
    mutations: list[SchemaMutation]


@dataclass(kw_only=True)
class DataCommand(Operation):
    mutations: list[DataMutation]

    def __post_init__(self):
        if not self.mutations:
            msg = 'The "mutations" list cannot be empty'
            raise ValueError(msg)


@dataclass(kw_only=True)
class TransactionCommand(Operation):
    schema: SchemaReference
    action: TransactionAction
    parent_transaction_id: str | None = None


@dataclass(kw_only=True)
class LockSchemaReference:
    schema: SchemaReference
    query: Conditions | None = None


@dataclass(kw_only=True)
class LockCommand(Operation):
    action: LockAction
    mode: LockMode
    parameter: LockParameter
    locked_objects: list[LockSchemaReference]
