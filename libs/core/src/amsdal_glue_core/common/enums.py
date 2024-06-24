from enum import Enum


class Version(str, Enum):
    LATEST = 'LATEST'
    ALL = 'ALL'


class ConnectionAlias(str, Enum):
    DEFAULT = 'DEFAULT'
    LAKEHOUSE = 'LAKEHOUSE'


class JoinType(str, Enum):
    INNER = 'INNER'
    LEFT = 'LEFT'
    RIGHT = 'RIGHT'
    FULL = 'FULL'


class FilterConnector(str, Enum):
    AND = 'AND'
    OR = 'OR'


class FieldLookup(str, Enum):
    EXACT = 'EXACT'
    EQ = 'EQ'
    NEQ = 'NEQ'
    GT = 'GT'
    GTE = 'GTE'
    LT = 'LT'
    LTE = 'LTE'
    IN = 'IN'
    CONTAINS = 'CONTAINS'
    ICONTAINS = 'ICONTAINS'
    STARTSWITH = 'STARTSWITH'
    ISTARTSWITH = 'ISTARTSWITH'
    ENDSWITH = 'ENDSWITH'
    IENDSWITH = 'IENDSWITH'
    ISNULL = 'ISNULL'
    REGEX = 'REGEX'
    IREGEX = 'IREGEX'

    def __repr__(self) -> str:  # noqa: PLR0911, PLR0912, C901
        match self:
            case FieldLookup.EXACT:
                return 'is'
            case FieldLookup.EQ:
                return '=='
            case FieldLookup.NEQ:
                return '!='
            case FieldLookup.GT:
                return '>'
            case FieldLookup.GTE:
                return '>='
            case FieldLookup.LT:
                return '<'
            case FieldLookup.LTE:
                return '<='
            case FieldLookup.IN:
                return 'in'
            case FieldLookup.CONTAINS:
                return 'contains'
            case FieldLookup.ICONTAINS:
                return 'icontains'
            case FieldLookup.STARTSWITH:
                return 'startswith'
            case FieldLookup.ISTARTSWITH:
                return 'istartswith'
            case FieldLookup.ENDSWITH:
                return 'endswith'
            case FieldLookup.IENDSWITH:
                return 'iendswith'
            case FieldLookup.ISNULL:
                return 'isnull'
            case FieldLookup.REGEX:
                return 'regex'
            case FieldLookup.IREGEX:
                return 'iregex'
            case _:
                msg = f'{self} not supported'
                raise ValueError(msg)


class OrderDirection(str, Enum):
    ASC = 'ASC'
    DESC = 'DESC'


class TransactionAction(str, Enum):
    BEGIN = 'BEGIN'
    COMMIT = 'COMMIT'
    ROLLBACK = 'ROLLBACK'
    REVERT = 'REVERT'


class LockAction(str, Enum):
    ACQUIRE = 'ACQUIRE'
    RELEASE = 'RELEASE'


class LockMode(str, Enum):
    EXCLUSIVE = 'EXCLUSIVE'
    SHARED = 'SHARED'


class LockParameter(str, Enum):
    NOWAIT = 'NOWAIT'
    SKIP_LOCKED = 'SKIP_LOCKED'
    WAIT = 'WAIT'
