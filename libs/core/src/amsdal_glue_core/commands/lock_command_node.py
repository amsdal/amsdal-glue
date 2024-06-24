from dataclasses import dataclass
from typing import Any

from amsdal_glue_core.common.enums import LockAction
from amsdal_glue_core.common.enums import LockMode
from amsdal_glue_core.common.enums import LockParameter
from amsdal_glue_core.common.operations.base import Operation
from amsdal_glue_core.common.operations.commands import LockSchemaReference


@dataclass(kw_only=True)
class ExecutionLockCommand(Operation):
    action: LockAction
    mode: LockMode
    parameter: LockParameter
    locked_object: LockSchemaReference
    result: Any = None
