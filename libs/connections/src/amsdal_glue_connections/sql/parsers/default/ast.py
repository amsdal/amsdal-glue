from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Literal:
    value: str | int | float | None


@dataclass
class BoolKeyword:
    value: bool


@dataclass
class SqlKeyword:
    name: str


@dataclass
class FuncCall:
    name: str
    args: list[Node]


@dataclass
class TypeCast:
    expr: Node
    type_name: str


@dataclass
class UnaryOp:
    operator: str
    operand: Node


@dataclass
class ColumnRef:
    name: str
    table: str | None = None


@dataclass
class BinaryOp:
    left: Node
    operator: str
    right: Node


Node = Literal | BoolKeyword | SqlKeyword | FuncCall | TypeCast | UnaryOp | ColumnRef | BinaryOp
