from dataclasses import dataclass
from typing import Union

from amsdal_glue_core.common.data_models.field_reference import FieldReference
from amsdal_glue_core.common.enums import FieldLookup
from amsdal_glue_core.common.enums import FilterConnector
from amsdal_glue_core.common.expressions.value import Value

_SKIP_FLATTEN = object()


@dataclass(kw_only=True)
class Condition:
    field: FieldReference
    lookup: FieldLookup
    value: Value | FieldReference
    negate: bool = False


class Conditions:
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
            self.__flatten_reduce_nesting()
            self.__flatten_by_connector()
            self.__split_by_or()

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

        if len(self.children) == 1:
            self.connector = FilterConnector.AND

    def __flatten_by_connector(self) -> None:
        i = 0

        while i < len(self.children):
            child = self.children[i]
            if isinstance(child, Conditions) and child.connector == self.connector:
                self.children[i : i + 1] = child.children
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
        right = other.children[0] if len(other.children) == 1 else other

        # Combine the left and right Conditions objects with the specified connector.
        return self.__class__(left, right, connector=connector)

    def _negate(self) -> None:
        if self.connector == FilterConnector.AND:
            self.connector = FilterConnector.OR
        else:
            self.connector = FilterConnector.AND

        for child in self.children:
            child._negate()  # type: ignore[union-attr] # noqa: SLF001

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
            *self.children,
            connector=self.connector,
        )

    def __repr__(self) -> str:
        connector = f' {self.connector.value.lower()} '
        children: list[str] = []

        for child in self.children:
            if isinstance(child, Conditions):
                children.append(f'({child!r})')
            else:
                children.append(repr(child))

        return connector.join(children)

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, Conditions):
            return False

        return self.children == __value.children and self.connector == __value.connector
