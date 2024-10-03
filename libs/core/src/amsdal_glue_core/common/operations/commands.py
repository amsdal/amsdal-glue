from copy import copy
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
    """Represents a schema command operation.

    Attributes:
        mutations (list[SchemaMutation]): The list of schema mutations to be applied.
    """

    mutations: list[SchemaMutation]

    def __copy__(self):
        return SchemaCommand(
            mutations=[copy(mutation) for mutation in self.mutations],
        )


@dataclass(kw_only=True)
class DataCommand(Operation):
    """Represents a data command operation.

    Attributes:
        mutations (list[DataMutation]): The list of data mutations to be applied.
    """

    mutations: list[DataMutation]

    def __post_init__(self):
        if not self.mutations:
            msg = 'The "mutations" list cannot be empty'
            raise ValueError(msg)

    def __copy__(self):
        return DataCommand(
            mutations=[copy(mutation) for mutation in self.mutations],
        )


@dataclass(kw_only=True)
class TransactionCommand(Operation):
    """Represents a transaction command operation.

    Attributes:
        action (TransactionAction): The action to be performed in the transaction.
        schema (SchemaReference | None): The schema reference associated with the transaction. Defaults to None.
        parent_transaction_id (str | None): The ID of the parent transaction, if any. Defaults to None.
    """

    action: TransactionAction
    schema: SchemaReference | None = None
    parent_transaction_id: str | None = None

    def __copy__(self):
        return TransactionCommand(
            action=self.action,
            schema=copy(self.schema) if self.schema is not None else None,
            parent_transaction_id=self.parent_transaction_id,
        )


@dataclass(kw_only=True)
class LockSchemaReference:
    """Represents a reference to a schema for locking purposes.

    Attributes:
        schema (SchemaReference): The schema reference to be locked.
        query (Conditions | None): The conditions for the lock. Defaults to None.
    """

    schema: SchemaReference
    query: Conditions | None = None

    def __copy__(self):
        return LockSchemaReference(
            schema=copy(self.schema),
            query=copy(self.query) if self.query is not None else None,
        )


@dataclass(kw_only=True)
class LockCommand(Operation):
    """Represents a lock command operation.

    Attributes:
        action (LockAction): The action to be performed for the lock.
        mode (LockMode): The mode of the lock.
        parameter (LockParameter): The parameter for the lock.
        locked_objects (list[LockSchemaReference]): The list of schema references to be locked.
    """

    action: LockAction
    mode: LockMode
    parameter: LockParameter
    locked_objects: list[LockSchemaReference]

    def __copy__(self):
        return LockCommand(
            action=self.action,
            mode=self.mode,
            parameter=self.parameter,
            locked_objects=[copy(locked_object) for locked_object in self.locked_objects],
        )
