from collections import defaultdict
from typing import TYPE_CHECKING

from amsdal_glue_core.commands.planner.lock_command_planner import AsyncLockCommandPlanner
from amsdal_glue_core.commands.planner.lock_command_planner import LockCommandPlanner
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.enums import LockScope
from amsdal_glue_core.common.operations.commands import LockCommand
from amsdal_glue_core.common.operations.commands import LockIdentifier
from amsdal_glue_core.common.operations.commands import LockReference
from amsdal_glue_core.common.workflows.chain import AsyncChainTask
from amsdal_glue_core.common.workflows.chain import ChainTask

if TYPE_CHECKING:
    from amsdal_glue_core.common.workflows.task import AsyncTask
    from amsdal_glue_core.common.workflows.task import Task

from amsdal_glue.commands.tasks.lock_tasks import AsyncLockCommandTask
from amsdal_glue.commands.tasks.lock_tasks import LockCommandTask


class DefaultLockCommandPlanner(LockCommandPlanner):
    """
    DefaultLockCommandPlanner groups ``locked_objects`` by resolved connection and emits one
    ``LockCommandTask`` per group (Approach A — one task per homogeneous connection group).

    Grouping key: ``(pool_key, routing_key)`` where
    - ``pool_key``    = ``ref.reference.name`` for ``SchemaReference``; ``ref.reference.pool`` for
                        ``LockIdentifier``.
    - ``routing_key`` = ``command.root_transaction_id`` (``TRANSACTION`` scope only in first cut).

    ``SESSION``-scope is deferred: raises ``NotImplementedError`` (TODO spec §8.7).
    """

    def plan_lock(self, command: LockCommand) -> ChainTask:
        """
        Plans the execution of a lock command by grouping locked_objects by connection.

        Args:
            command (LockCommand): The lock command containing lock operations to be executed.

        Returns:
            ChainTask: A chain of tasks that execute the lock operations, one per connection group.

        Raises:
            NotImplementedError: If ``command.scope == LockScope.SESSION`` (deferred, TODO §8.7).
            ValueError: If a group is mixed (both SchemaReference and LockIdentifier).
        """
        if command.scope == LockScope.SESSION:
            msg = (
                'SESSION-scope advisory locks are not supported in the first cut. '
                'Use scope=LockScope.TRANSACTION instead. (TODO spec §8.7)'
            )
            raise NotImplementedError(msg)

        groups: dict[tuple[str | None, str | None], list[LockReference]] = defaultdict(list)
        for ref in command.locked_objects:
            if isinstance(ref.reference, SchemaReference):
                pool_key: str | None = ref.reference.name
            else:
                # ref.reference is narrowed to LockIdentifier here (the only non-SchemaReference variant).
                pool_key = ref.reference.pool
            routing_key = command.root_transaction_id
            groups[(pool_key, routing_key)].append(ref)

        tasks: list[Task] = []
        for (pool_key, _routing_key), refs in groups.items():
            has_schema = any(isinstance(r.reference, SchemaReference) for r in refs)
            has_ident = any(isinstance(r.reference, LockIdentifier) for r in refs)
            if has_schema and has_ident:
                msg = (
                    f'Lock group for pool_key={pool_key!r} is mixed (SchemaReference and LockIdentifier). '
                    'Each group must be homogeneous (all table refs OR all advisory keys). '
                    'Rust rejects mixed groups in one compile_lock_command call.'
                )
                raise ValueError(msg)

            grouped_command = LockCommand(
                lock_id=command.lock_id,
                root_transaction_id=command.root_transaction_id,
                transaction_id=command.transaction_id,
                action=command.action,
                mode=command.mode,
                parameter=command.parameter,
                locked_objects=refs,
                timeout=command.timeout,
                scope=command.scope,
            )
            tasks.append(LockCommandTask(lock_command=grouped_command))

        return ChainTask(tasks=tasks)


class DefaultAsyncLockCommandPlanner(AsyncLockCommandPlanner):
    """
    Async version of DefaultLockCommandPlanner.

    Groups ``locked_objects`` by connection and emits one ``AsyncLockCommandTask`` per group.
    ``SESSION``-scope is deferred: raises ``NotImplementedError`` (TODO spec §8.7).
    """

    def plan_lock(self, command: LockCommand) -> AsyncChainTask:
        """
        Plans the execution of a lock command by grouping locked_objects by connection.

        Args:
            command (LockCommand): The lock command containing lock operations to be executed.

        Returns:
            AsyncChainTask: A chain of tasks that execute the lock operations, one per connection group.

        Raises:
            NotImplementedError: If ``command.scope == LockScope.SESSION`` (deferred, TODO §8.7).
            ValueError: If a group is mixed (both SchemaReference and LockIdentifier).
        """
        if command.scope == LockScope.SESSION:
            msg = (
                'SESSION-scope advisory locks are not supported in the first cut. '
                'Use scope=LockScope.TRANSACTION instead. (TODO spec §8.7)'
            )
            raise NotImplementedError(msg)

        groups: dict[tuple[str | None, str | None], list[LockReference]] = defaultdict(list)
        for ref in command.locked_objects:
            if isinstance(ref.reference, SchemaReference):
                pool_key: str | None = ref.reference.name
            else:
                # ref.reference is narrowed to LockIdentifier here (the only non-SchemaReference variant).
                pool_key = ref.reference.pool
            routing_key = command.root_transaction_id
            groups[(pool_key, routing_key)].append(ref)

        tasks: list[AsyncTask] = []
        for (pool_key, _routing_key), refs in groups.items():
            has_schema = any(isinstance(r.reference, SchemaReference) for r in refs)
            has_ident = any(isinstance(r.reference, LockIdentifier) for r in refs)
            if has_schema and has_ident:
                msg = (
                    f'Lock group for pool_key={pool_key!r} is mixed (SchemaReference and LockIdentifier). '
                    'Each group must be homogeneous (all table refs OR all advisory keys). '
                    'Rust rejects mixed groups in one compile_lock_command call.'
                )
                raise ValueError(msg)

            grouped_command = LockCommand(
                lock_id=command.lock_id,
                root_transaction_id=command.root_transaction_id,
                transaction_id=command.transaction_id,
                action=command.action,
                mode=command.mode,
                parameter=command.parameter,
                locked_objects=refs,
                timeout=command.timeout,
                scope=command.scope,
            )
            tasks.append(AsyncLockCommandTask(lock_command=grouped_command))

        return AsyncChainTask(tasks=tasks)
