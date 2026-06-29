from dataclasses import dataclass

from amsdal_glue_core.common.expressions.expression import Expression


@dataclass(kw_only=True)
class GroupByQuery:
    expression: Expression

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, GroupByQuery):
            return False

        return self.expression == other.expression

    def __hash__(self) -> int:
        return hash(self.expression)
