from __future__ import annotations

from amsdal_glue_connections.sql.parsers.default.ast import Between
from amsdal_glue_connections.sql.parsers.default.ast import BinaryOp
from amsdal_glue_connections.sql.parsers.default.ast import BoolKeyword
from amsdal_glue_connections.sql.parsers.default.ast import ColumnRef
from amsdal_glue_connections.sql.parsers.default.ast import FuncCall
from amsdal_glue_connections.sql.parsers.default.ast import InList
from amsdal_glue_connections.sql.parsers.default.ast import Literal
from amsdal_glue_connections.sql.parsers.default.ast import Node
from amsdal_glue_connections.sql.parsers.default.ast import SqlKeyword
from amsdal_glue_connections.sql.parsers.default.ast import TypeCast
from amsdal_glue_connections.sql.parsers.default.ast import UnaryOp

_SQL_KEYWORDS = frozenset({
    'CURRENT_TIMESTAMP',
    'CURRENT_DATE',
    'CURRENT_TIME',
})

# Operator precedence (higher = tighter binding)
_PRECEDENCE: dict[str, int] = {
    'OR': 1,
    'AND': 2,
    '=': 3,
    '<>': 3,
    '!=': 3,
    '<': 3,
    '>': 3,
    '<=': 3,
    '>=': 3,
    '||': 4,
    '+': 5,
    '-': 5,
    '*': 6,
    '/': 6,
    '%': 6,
}

_KEYWORD_OPERATORS = ('AND', 'OR')

# Keyword comparison predicates (``IS [NOT] NULL``, ``IN``, ``NOT IN``, ``LIKE``/``ILIKE``,
# ``NOT LIKE``/``NOT ILIKE``, ``BETWEEN``/``NOT BETWEEN``). They bind at the same level as the
# symbolic comparison operators (``=``, ``<`` ...): tighter than ``AND``/``OR``, looser than
# arithmetic.
_PREDICATE_PRECEDENCE = 3
_PREDICATE_START = frozenset({'IS', 'IN', 'LIKE', 'ILIKE', 'BETWEEN'})
_NOT_PREDICATES = frozenset({'IN', 'LIKE', 'ILIKE', 'BETWEEN'})


class DefaultParser:
    """Recursive-descent parser for SQL DEFAULT / GENERATED expressions."""

    def __init__(self, raw: str) -> None:
        self._raw = raw
        self._pos = 0

    def parse(self) -> Node:
        node = self._parse_expr()
        self._skip_ws()
        if self._pos < len(self._raw):
            msg = f'Unexpected trailing input at position {self._pos}: {self._raw[self._pos :]!r}'
            raise ValueError(msg)
        return node

    def _parse_expr(self, min_prec: int = 0) -> Node:
        self._skip_ws()

        # NOT as prefix operator with precedence between OR and AND
        if self._pos < len(self._raw):
            not_candidate = self._raw[self._pos : self._pos + 3].upper()
            if not_candidate == 'NOT':
                after = self._pos + 3
                if after >= len(self._raw) or not (self._raw[after].isalnum() or self._raw[after] == '_'):
                    not_prec = 2  # between OR(1) and AND(2), binds looser than AND
                    if not_prec >= min_prec:
                        self._pos = after
                        self._skip_ws()
                        operand = self._parse_expr(min_prec=not_prec)
                        return UnaryOp(operator='NOT', operand=operand)

        node = self._parse_unary()
        self._skip_ws()

        # PostgreSQL typecast: expr::type
        while self._peek(2) == '::':
            self._pos += 2
            type_name = self._parse_type_name()
            node = TypeCast(expr=node, type_name=type_name)
            self._skip_ws()

        # Binary operators with precedence climbing
        while True:
            self._skip_ws()

            # Keyword comparison predicates (IS [NOT] NULL, IN, LIKE, BETWEEN, ...)
            predicate = self._peek_predicate_keyword()
            if predicate is not None and min_prec <= _PREDICATE_PRECEDENCE:
                node = self._parse_predicate(node, predicate)
                continue

            op = self._peek_operator()
            if op is None or _PRECEDENCE.get(op, 0) < min_prec:
                break
            self._pos += len(op)
            # Left-associative: right side parses at prec + 1
            right = self._parse_expr(min_prec=_PRECEDENCE[op] + 1)
            node = BinaryOp(left=node, operator=op, right=right)

        return node

    def _peek_predicate_keyword(self) -> str | None:
        """Return the canonical keyword-predicate operator at the cursor, or ``None``.

        Recognises ``IS``, ``IN``, ``LIKE``, ``ILIKE``, ``BETWEEN`` and their ``NOT``-prefixed
        forms (``NOT IN``/``NOT LIKE``/``NOT ILIKE``/``NOT BETWEEN``). The cursor is not advanced.
        """
        word, after = self._read_word_at(self._pos)
        if word is None:
            return None
        if word in _PREDICATE_START:
            return word
        if word == 'NOT':
            word2, _ = self._read_word_at(after)
            if word2 in _NOT_PREDICATES:
                return f'NOT {word2}'
        return None

    def _parse_predicate(self, left: Node, predicate: str) -> Node:
        negated = predicate.startswith('NOT ')
        if negated:
            self._consume_word()  # NOT
            keyword = predicate[len('NOT ') :]
        else:
            keyword = predicate
        self._consume_word()  # IS / IN / LIKE / ILIKE / BETWEEN

        if keyword == 'IS':
            return self._parse_is_predicate(left)
        if keyword == 'IN':
            return BinaryOp(left=left, operator='NOT IN' if negated else 'IN', right=self._parse_paren_list())
        if keyword in ('LIKE', 'ILIKE'):
            operator = f'NOT {keyword}' if negated else keyword
            pattern = self._parse_expr(min_prec=_PRECEDENCE['='] + 1)
            return BinaryOp(left=left, operator=operator, right=pattern)
        # BETWEEN low AND high
        low = self._parse_expr(min_prec=_PRECEDENCE['AND'] + 1)
        and_word = self._consume_word()
        if and_word != 'AND':
            msg = f'Expected AND in BETWEEN at position {self._pos} in: {self._raw!r}'
            raise ValueError(msg)
        high = self._parse_expr(min_prec=_PRECEDENCE['AND'] + 1)
        return Between(expr=left, low=low, high=high, negated=negated)

    def _parse_is_predicate(self, left: Node) -> Node:
        # ``IS`` has already been consumed; expect ``NULL`` or ``NOT NULL``.
        word = self._consume_word()
        if word == 'NOT':
            null_word = self._consume_word()
            if null_word != 'NULL':
                msg = f'Expected NULL after IS NOT at position {self._pos} in: {self._raw!r}'
                raise ValueError(msg)
            return BinaryOp(left=left, operator='IS NOT', right=Literal(value=None))
        if word != 'NULL':
            msg = f'Expected NULL or NOT NULL after IS at position {self._pos} in: {self._raw!r}'
            raise ValueError(msg)
        return BinaryOp(left=left, operator='IS', right=Literal(value=None))

    def _parse_paren_list(self) -> InList:
        self._skip_ws()
        if self._pos >= len(self._raw) or self._current() != '(':
            msg = f'Expected "(" for IN list at position {self._pos} in: {self._raw!r}'
            raise ValueError(msg)
        self._pos += 1

        items: list[Node] = []
        self._skip_ws()
        if self._pos < len(self._raw) and self._current() != ')':
            items.append(self._parse_expr())
            self._skip_ws()
            while self._pos < len(self._raw) and self._current() == ',':
                self._pos += 1
                items.append(self._parse_expr())
                self._skip_ws()

        if self._pos >= len(self._raw) or self._current() != ')':
            msg = f'Expected ")" closing IN list in: {self._raw!r}'
            raise ValueError(msg)
        self._pos += 1
        return InList(items=items)

    def _read_word_at(self, pos: int) -> tuple[str | None, int]:
        """Read an identifier word (upper-cased) starting at ``pos`` (skipping leading spaces).

        Returns ``(word, next_pos)`` without mutating the cursor; ``(None, pos)`` if there is no word.
        """
        while pos < len(self._raw) and self._raw[pos] == ' ':
            pos += 1
        start = pos
        while pos < len(self._raw) and (self._raw[pos].isalnum() or self._raw[pos] == '_'):
            pos += 1
        if pos == start:
            return None, pos
        return self._raw[start:pos].upper(), pos

    def _consume_word(self) -> str:
        word, after = self._read_word_at(self._pos)
        if word is None:
            msg = f'Expected keyword at position {self._pos} in: {self._raw!r}'
            raise ValueError(msg)
        self._pos = after
        return word

    def _peek_operator(self) -> str | None:
        if self._pos >= len(self._raw):
            return None

        # Keyword operators: AND, OR (must be followed by non-alnum to avoid matching column names)
        for kw in _KEYWORD_OPERATORS:
            if self._raw[self._pos : self._pos + len(kw)].upper() == kw:
                after = self._pos + len(kw)
                if after >= len(self._raw) or not (self._raw[after].isalnum() or self._raw[after] == '_'):
                    return kw

        # Two-char symbol operators
        two = self._peek(2)
        if two in ('||', '<>', '!=', '<=', '>='):
            return two

        ch = self._raw[self._pos]
        if ch in ('+', '-', '*', '/', '%', '<', '>', '='):
            return ch
        return None

    def _parse_unary(self) -> Node:
        self._skip_ws()

        ch = self._current()

        # Parenthesized expression
        if ch == '(':
            self._pos += 1
            node = self._parse_expr()
            self._skip_ws()
            if self._pos >= len(self._raw) or self._current() != ')':
                msg = f'Expected closing parenthesis in: {self._raw!r}'
                raise ValueError(msg)
            self._pos += 1
            return node

        # Quoted identifier: "name"
        if ch == '"':
            return self._maybe_member_access(self._parse_quoted_identifier())

        # String literal
        if ch == "'":
            return self._parse_string()

        # Unary minus
        if ch == '-':
            self._pos += 1
            operand = self._parse_unary()
            return UnaryOp(operator='-', operand=operand)

        # Numeric literal
        if ch.isdigit():
            return self._parse_number()

        # Identifier or keyword
        if ch.isalpha() or ch == '_':
            node = self._parse_identifier_or_call()
            return self._maybe_member_access(node) if isinstance(node, ColumnRef) else node

        msg = f'Unexpected character {ch!r} at position {self._pos} in: {self._raw!r}'
        raise ValueError(msg)

    def _maybe_member_access(self, node: ColumnRef) -> ColumnRef:
        # Qualified references: table.column or "table"."column" (deeper qualifiers keep the
        # last segment as the column and the preceding one as the table).
        while self._pos < len(self._raw) and self._raw[self._pos] == '.':
            self._pos += 1
            if self._pos < len(self._raw) and self._current() == '"':
                segment = self._parse_quoted_identifier().name
            else:
                segment = self._parse_identifier()
            node = ColumnRef(name=segment, table=node.name)
        return node

    def _parse_quoted_identifier(self) -> ColumnRef:
        # caller already checked current char is '"'
        self._pos += 1
        start = self._pos
        while self._pos < len(self._raw) and self._raw[self._pos] != '"':
            self._pos += 1
        if self._pos >= len(self._raw):
            msg = f'Unterminated quoted identifier in: {self._raw!r}'
            raise ValueError(msg)
        name = self._raw[start : self._pos]
        self._pos += 1  # skip closing "
        return ColumnRef(name=name)

    def _parse_string(self) -> Literal:
        # caller already checked current char is "'"
        self._pos += 1

        parts: list[str] = []
        while self._pos < len(self._raw):
            ch = self._raw[self._pos]
            if ch == "'":
                # Escaped quote: ''
                if self._pos + 1 < len(self._raw) and self._raw[self._pos + 1] == "'":
                    parts.append("'")
                    self._pos += 2
                else:
                    self._pos += 1
                    return Literal(value=''.join(parts))
            else:
                parts.append(ch)
                self._pos += 1

        msg = f'Unterminated string literal in: {self._raw!r}'
        raise ValueError(msg)

    def _parse_number(self) -> Literal:
        start = self._pos
        while self._pos < len(self._raw) and self._raw[self._pos].isdigit():
            self._pos += 1

        if self._pos < len(self._raw) and self._raw[self._pos] == '.':
            self._pos += 1
            while self._pos < len(self._raw) and self._raw[self._pos].isdigit():
                self._pos += 1
            return Literal(value=float(self._raw[start : self._pos]))

        return Literal(value=int(self._raw[start : self._pos]))

    def _parse_identifier_or_call(self) -> Node:
        name = self._parse_identifier()
        upper = name.upper()

        # SQL keywords
        if upper in _SQL_KEYWORDS:
            return SqlKeyword(name=upper)

        # Boolean keywords
        if upper == 'TRUE':
            return BoolKeyword(value=True)
        if upper == 'FALSE':
            return BoolKeyword(value=False)

        # NULL
        if upper == 'NULL':
            return Literal(value=None)  # type: ignore[arg-type]

        self._skip_ws()

        # Function call: name(...)
        if self._pos < len(self._raw) and self._current() == '(':
            return self._parse_func_call(name)

        # Bare identifier — column reference
        return ColumnRef(name=name)

    def _parse_func_call(self, name: str) -> FuncCall:
        # caller already checked current char is '('
        self._pos += 1

        args: list[Node] = []
        self._skip_ws()

        if self._pos < len(self._raw) and self._current() != ')':
            args.append(self._parse_expr())
            self._skip_ws()

            while self._pos < len(self._raw) and self._current() == ',':
                self._pos += 1
                args.append(self._parse_expr())
                self._skip_ws()

        if self._pos >= len(self._raw) or self._current() != ')':
            msg = f'Expected closing parenthesis in: {self._raw!r}'
            raise ValueError(msg)
        self._pos += 1

        return FuncCall(name=name, args=args)

    def _parse_identifier(self) -> str:
        start = self._pos
        while self._pos < len(self._raw) and (self._raw[self._pos].isalnum() or self._raw[self._pos] == '_'):
            self._pos += 1
        if self._pos == start:
            msg = f'Expected identifier at position {self._pos} in: {self._raw!r}'
            raise ValueError(msg)
        return self._raw[start : self._pos]

    def _parse_type_name(self) -> str:
        self._skip_ws()
        parts: list[str] = []

        # Type name can be multi-word: "character varying", "double precision", "timestamp with time zone"
        while self._pos < len(self._raw):
            ch = self._raw[self._pos]
            if ch.isalpha() or ch == '_':
                parts.append(self._parse_identifier())
                self._skip_ws()
            elif ch == '(' and parts:
                # Parameterized type: varchar(255)
                self._pos += 1
                depth = 1
                param_start = self._pos
                while self._pos < len(self._raw) and depth > 0:
                    if self._raw[self._pos] == '(':
                        depth += 1
                    elif self._raw[self._pos] == ')':
                        depth -= 1
                    self._pos += 1
                parts.append(f'({self._raw[param_start : self._pos - 1]})')
                self._skip_ws()
            else:
                break

        if not parts:
            msg = f'Expected type name at position {self._pos} in: {self._raw!r}'
            raise ValueError(msg)
        return ' '.join(parts)

    def _current(self) -> str:
        return self._raw[self._pos]

    def _peek(self, n: int = 1) -> str:
        return self._raw[self._pos : self._pos + n]

    def _skip_ws(self) -> None:
        while self._pos < len(self._raw) and self._raw[self._pos] == ' ':
            self._pos += 1


def parse(raw: str) -> Node:
    return DefaultParser(raw).parse()
