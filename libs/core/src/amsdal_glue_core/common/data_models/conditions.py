from copy import copy
from dataclasses import dataclass
from typing import Union

from amsdal_glue_core.common.enums import FieldLookup
from amsdal_glue_core.common.enums import FilterConnector
from amsdal_glue_core.common.expressions.expression import Expression

_SKIP_FLATTEN = object()


@dataclass(kw_only=True)
class Condition:
    """Represents a condition in a query.

    Attributes:
        left (Expression): The left expression to which the condition applies.
        lookup (FieldLookup): The lookup type for the condition.
        right (left): The right expression for the condition.
        negate (bool): Whether the condition is negated. Defaults to False.
    """

    left: Expression
    lookup: FieldLookup
    right: Expression
    negate: bool = False

    def __copy__(self) -> 'Condition':
        return Condition(
            left=copy(self.left),
            lookup=self.lookup,
            right=copy(self.right),
            negate=self.negate,
        )

    def __invert__(self) -> 'Condition':
        self.negate = not self.negate

        return self

    def __eq__(self, __value: object) -> bool:  # noqa: PYI063
        if not isinstance(__value, Condition):
            if isinstance(__value, Conditions) and len(__value.children) == 1 and not __value.negated:
                return self == __value.children[0]

            return False

        return (
            self.left == __value.left
            and self.lookup == __value.lookup
            and self.right == __value.right
            and self.negate == __value.negate
        )


class Conditions:
    """Represents a collection of conditions in a query.

    Attributes:
        children (list[Union[Conditions, Condition]]): The list of child conditions.
        connector (FilterConnector): The connector type (AND/OR) for the conditions.
        negated (bool): Whether the conditions are negated. Defaults to False.
    """

    def __init__(
        self,
        *args: Union['Conditions', Condition, object],
        connector: FilterConnector = FilterConnector.AND,
        negated: bool = False,
    ) -> None:
        _skip_flatten, _args = self._parse_args(args)  # type: ignore
        self.negated = negated
        self.connector = connector
        self.children = _args

        if not _skip_flatten:
            self._flatten_reduce_nesting_many()
            self.__flatten_reduce_nesting()
            self.__flatten_by_connector()
            self.__split_by_or()
            self._flatten_reduce_nesting_many()

    @staticmethod
    def _parse_args(
        args: tuple[Union['Conditions', Condition, object]],
    ) -> tuple[bool, list[Union['Conditions', Condition]]]:
        if _SKIP_FLATTEN in args:
            return True, [arg for arg in args if arg is not _SKIP_FLATTEN]  # type: ignore[misc]

        return False, list(args)  # type: ignore[arg-type]

    def copy(self) -> 'Conditions':
        return self.__copy__()

    def __flatten_reduce_nesting(self) -> None:
        while len(self.children) == 1 and isinstance(self.children[0], Conditions):
            child = self.children[0]
            self.children = child.children
            self.connector = child.connector

            if self.negated:
                self.negated = not child.negated
            else:
                self.negated = child.negated

        if len(self.children) == 1:
            self.connector = FilterConnector.AND

    def _flatten_reduce_nesting_many(self) -> None:
        for child in self.children:
            if isinstance(child, Conditions):
                child._flatten_reduce_nesting_many()  # noqa: SLF001

        if self.negated:
            return

        all_positive = True
        same_connector = True
        all_conditions = True

        for child in self.children:
            if not isinstance(child, Conditions):
                all_conditions = False
                break

            if child.negated:
                all_positive = False

            if child.connector != self.connector:
                same_connector = False

        if not all_conditions or not all_positive or not same_connector:
            return

        new_children: list[Conditions | Condition] = []
        for child in self.children:
            new_children.extend(child.children)  # type: ignore[union-attr]

        self.children = new_children

    def __flatten_by_connector(self) -> None:
        i = 0

        while i < len(self.children):
            child = self.children[i]
            if (
                isinstance(child, Conditions)
                and child.connector == self.connector
                and not child.negated
                and not self.negated
            ):
                self.children[slice(i, i + 1)] = child.children
            else:
                i += 1

        for child in self.children:
            if isinstance(child, Conditions):
                child.__flatten_by_connector()  # noqa: SLF001

    def __split_by_or(self) -> None:
        if self.connector == FilterConnector.AND:
            or_children = [
                child
                for child in self.children
                if isinstance(child, Conditions) and child.connector == FilterConnector.OR
            ]

            if or_children:
                or_child = or_children[0]
                self.children.remove(or_child)

                new_children = []
                for grandchild in or_child.children:
                    new_child = self.__class__(*self.children, grandchild, connector=FilterConnector.AND)
                    new_child.__split_by_or()  # noqa: SLF001
                    new_children.append(new_child)

                self.children = new_children  # type: ignore[assignment]
                self.connector = FilterConnector.OR

        for child in self.children:
            if isinstance(child, Conditions):
                child.__split_by_or()  # noqa: SLF001

    def _combine(self, other: 'Conditions', connector: FilterConnector) -> 'Conditions':
        if not isinstance(other, Conditions):
            raise TypeError(other)

        # If the current Conditions object has no children, return the other Conditions object.
        if len(self.children) == 0:
            return other

        # If the other Conditions object has no children, return the current Conditions object.
        if len(other.children) == 0:
            return self

        # If the current Conditions object has only one child, use the child directly.
        # Otherwise, use the current Conditions object.
        left = self.children[0] if len(self.children) == 1 else self

        # If the other Conditions object has only one child, use the child directly.
        # Otherwise, use the other Conditions object.
        right = (other.children[0] if len(other.children) == 1 else other) if self.negated == other.negated else other

        # Combine the left and right Conditions objects with the specified connector.
        return self.__class__(left, right, connector=connector, negated=self.negated)

    def _negate(self) -> None:
        if self.connector == FilterConnector.AND:
            self.connector = FilterConnector.OR
        else:
            self.connector = FilterConnector.AND

        for child in self.children:
            if isinstance(child, Conditions):
                child._negate()  # noqa: SLF001
            else:
                child.negate = not child.negate

        self.__split_by_or()

    def __and__(self, other: 'Conditions') -> 'Conditions':
        return self._combine(other, FilterConnector.AND)

    def __or__(self, other: 'Conditions') -> 'Conditions':
        return self._combine(other, FilterConnector.OR)

    def __invert__(self) -> 'Conditions':
        q_obj = self.__copy__()
        q_obj._negate()  # noqa: SLF001

        return q_obj

    def __copy__(self) -> 'Conditions':
        return self.__class__(
            _SKIP_FLATTEN,
            *[child.__copy__() for child in self.children],
            connector=self.connector,
            negated=self.negated,
        )

    def __repr__(self) -> str:
        connector = f' {self.connector.value.lower()} '
        children: list[str] = [repr(child) for child in self.children]

        r = f'({connector.join(children)})'

        if self.negated:
            r = f'~{r}'

        return r

    def __eq__(self, __value: object) -> bool:  # noqa: PYI063
        if not isinstance(__value, Conditions):
            if isinstance(__value, Condition) and len(self.children) == 1 and not self.negated:
                return self.children[0] == __value

            return False

        return (
            self.children == __value.children
            and self.connector == __value.connector
            and self.negated == __value.negated
        )
