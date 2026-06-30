from copy import copy
from dataclasses import dataclass

from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.enums import LockAction
from amsdal_glue_core.common.enums import LockMode
from amsdal_glue_core.common.enums import LockParameter
from amsdal_glue_core.common.enums import LockScope
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


@dataclass(kw_only=True, frozen=True, slots=True)
class LockIdentifier:
    """Opaque application-level key for non-row locks.

    Used as a ``LockReference.reference`` target when the lock is not a
    table or row lock but an application-defined rendezvous
    (``pg_advisory_lock`` in PostgreSQL, ``GET_LOCK`` in MySQL,
    ``sp_getapplock`` in SQL Server, ``DBMS_LOCK.REQUEST`` in Oracle).

    ``pool`` names the logical connection pool that owns the lock.
    Required because advisory locks are connection-scoped — there is no
    table to route by, so the caller must address a pool explicitly.
    """

    key: str
    pool: str


@dataclass(kw_only=True)
class LockReference:
    """Lock target — discriminated by the type of ``reference``.

    - ``SchemaReference`` → table-level lock (``LOCK TABLE …``).
    - ``LockIdentifier``  → session advisory lock (``pg_advisory_lock(key)``).

    Row-level ``SELECT … FOR UPDATE`` is not expressed here; it lives on
    ``QueryStatement.lock`` and is handled inside ``query()``.
    """

    reference: SchemaReference | LockIdentifier

    def __copy__(self):
        return LockReference(reference=copy(self.reference))


@dataclass(kw_only=True)
class LockCommand(Operation):
    """Represents a lock command operation.

    Attributes:
        action (LockAction): The action to be performed for the lock.
        mode (LockMode): The mode of the lock.
        parameter (LockParameter): The parameter for the lock.
        locked_objects (list[LockReference]): The list of lock references to be locked.

    Note: inherits ``transaction_id``, ``lock_id``, ``root_transaction_id`` from
    ``Operation`` (prod divergence from pure-source ``@dataclass``; see spec §3).
    """

    action: LockAction
    mode: LockMode
    parameter: LockParameter
    locked_objects: list[LockReference]
    timeout: float | None = None
    """Maximum seconds to wait for the lock.  ``None`` → block indefinitely
    unless ``parameter=NOWAIT``.  Support is driver-specific: MySQL, Oracle
    and SQL Server accept per-call timeouts natively; PG advisory locks
    ignore it (use ``parameter=NOWAIT`` for non-blocking); table-level
    ``LOCK TABLE`` uses ``SET LOCAL lock_timeout``."""
    scope: LockScope = LockScope.TRANSACTION
    """Lifetime of the lock.  ``TRANSACTION`` (default) — auto-released at
    the end of the current transaction; ``SESSION`` — held until explicit
    release or connection death.  Public ``Engine`` API requires an active
    transaction and always uses ``TRANSACTION``; ``SESSION`` is reserved
    for infrastructure (e.g. WAL ownership)."""

    def __copy__(self):
        return LockCommand(
            action=self.action,
            mode=self.mode,
            parameter=self.parameter,
            locked_objects=[copy(o) for o in self.locked_objects],
            timeout=self.timeout,
            scope=self.scope,
        )
