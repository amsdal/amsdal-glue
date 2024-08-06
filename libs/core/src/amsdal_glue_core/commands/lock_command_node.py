from dataclasses import dataclass
from typing import Any

from amsdal_glue_core.common.enums import LockAction
from amsdal_glue_core.common.enums import LockMode
from amsdal_glue_core.common.enums import LockParameter
from amsdal_glue_core.common.operations.base import Operation
from amsdal_glue_core.common.operations.commands import LockSchemaReference


@dataclass(kw_only=True)
class ExecutionLockCommand(Operation):
    """
    Represents a node in the lock command tree.

    Attributes:
        action (LockAction): The lock action to be executed.
        mode (LockMode): The lock mode to be used.
        parameter (LockParameter): The lock parameter to be used.
        locked_object (LockSchemaReference): The object to be locked.
        result (Any | None): The result of the lock command execution.
    """

    action: LockAction
    mode: LockMode
    parameter: LockParameter
    locked_object: LockSchemaReference
    result: Any = None
