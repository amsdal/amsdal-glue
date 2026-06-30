from __future__ import annotations

from copy import copy
from dataclasses import dataclass
from typing import Any
from typing import Protocol
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from amsdal_glue_core.common.data_models.conditions import Conditions
    from amsdal_glue_core.common.data_models.cte import CommonTableExpression
    from amsdal_glue_core.common.data_models.data import Data
    from amsdal_glue_core.common.data_models.field_reference import FieldReference
    from amsdal_glue_core.common.data_models.from_values import FromValues
    from amsdal_glue_core.common.data_models.query import QueryStatement
    from amsdal_glue_core.common.data_models.schema import SchemaReference
    from amsdal_glue_core.common.data_models.select_expression import SelectExpression
    from amsdal_glue_core.common.data_models.sub_query import SubQueryStatement
    from amsdal_glue_core.common.enums import ConflictAction
    from amsdal_glue_core.common.expressions.expression import Expression

    ReturningItem = FieldReference | SelectExpression


class MutationCompiler(Protocol):
    def compile_mutation(self, mutation: DataMutation) -> tuple[str, list[Any]]: ...


@dataclass(kw_only=True)
class OnConflict:
    fields: list[FieldReference]
    action: ConflictAction
    update_fields: list[FieldReference] | None = None
    where: Conditions | None = None


@dataclass(kw_only=True)
class DataMutation:
    schema: SchemaReference
    metadata: dict[str, Any] | None = None


@dataclass(kw_only=True)
class InsertData(DataMutation):
    data: list[Data]
    on_conflict: OnConflict | None = None
    returning: list[ReturningItem] | None = None
    ctes: list[CommonTableExpression] | None = None

    def __copy__(self):
        return InsertData(
            schema=copy(self.schema),
            data=[copy(data) for data in self.data],
            returning=copy(self.returning) if self.returning else None,
            on_conflict=self.on_conflict,
            metadata=copy(self.metadata) if self.metadata else None,
            ctes=[copy(cte) for cte in self.ctes] if self.ctes else None,
        )


@dataclass(kw_only=True)
class InsertFromSelect(DataMutation):
    query: QueryStatement
    columns: list[FieldReference] | None = None
    returning: list[ReturningItem] | None = None

    def __copy__(self):
        return InsertFromSelect(
            schema=copy(self.schema),
            query=copy(self.query),
            columns=copy(self.columns) if self.columns else None,
            returning=copy(self.returning) if self.returning else None,
            metadata=copy(self.metadata) if self.metadata else None,
        )


@dataclass(kw_only=True)
class UpdateData(DataMutation):
    data: dict[str, Expression]
    query: Conditions | None = None
    from_tables: list[SchemaReference | SubQueryStatement | FromValues] | None = None
    returning: list[ReturningItem] | None = None
    ctes: list[CommonTableExpression] | None = None

    def __copy__(self):
        return UpdateData(
            schema=copy(self.schema),
            data=self.data.copy(),
            query=copy(self.query) if self.query else None,
            from_tables=copy(self.from_tables) if self.from_tables else None,
            returning=copy(self.returning) if self.returning else None,
            metadata=copy(self.metadata) if self.metadata else None,
            ctes=[copy(cte) for cte in self.ctes] if self.ctes else None,
        )


@dataclass(kw_only=True)
class DeleteData(DataMutation):
    query: Conditions | None = None
    returning: list[ReturningItem] | None = None
    ctes: list[CommonTableExpression] | None = None

    def __copy__(self):
        return DeleteData(
            schema=copy(self.schema),
            query=copy(self.query) if self.query else None,
            returning=copy(self.returning) if self.returning else None,
            metadata=copy(self.metadata) if self.metadata else None,
            ctes=[copy(cte) for cte in self.ctes] if self.ctes else None,
        )


@dataclass(kw_only=True)
class UpdateItem:
    data: dict[str, Expression]
    query: Conditions | None = None

    def __copy__(self):
        return UpdateItem(
            data=self.data.copy(),
            query=copy(self.query) if self.query else None,
        )


@dataclass(kw_only=True)
class UpdateManyData(DataMutation):
    items: list[UpdateItem]

    def __copy__(self):
        return UpdateManyData(
            schema=copy(self.schema),
            items=[copy(item) for item in self.items],
            metadata=copy(self.metadata) if self.metadata else None,
        )

    def compile_grouped(
        self,
        compiler: MutationCompiler,
    ) -> list[tuple[str, list[list[Any]]]]:
        """Group items by compiled SQL template, return (sql, param_sets) pairs.

        Compiles each item to determine its SQL shape, then groups items
        that produce identical SQL. Returns a list of ``(sql, param_sets)``
        tuples suitable for ``executemany``.
        """
        groups: dict[str, list[list[Any]]] = {}
        order: list[str] = []

        for item in self.items:
            mutation = UpdateData(
                schema=copy(self.schema),
                data=item.data,
                query=item.query,
            )
            sql, params = compiler.compile_mutation(mutation)

            if sql not in groups:
                groups[sql] = []
                order.append(sql)
            groups[sql].append(params)

        return [(sql, groups[sql]) for sql in order]
