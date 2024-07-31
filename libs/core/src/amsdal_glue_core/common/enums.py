from enum import Enum


class Version(str, Enum):
    """Represents the version of a schema.

    Attributes:
        LATEST (str): The latest version.
        ALL (str): All versions.
    """

    LATEST = 'LATEST'
    ALL = 'ALL'


class ConnectionAlias(str, Enum):
    """Represents the alias for a connection.

    Attributes:
        DEFAULT (str): The default connection alias.
        LAKEHOUSE (str): The lakehouse connection alias.
    """

    DEFAULT = 'DEFAULT'
    LAKEHOUSE = 'LAKEHOUSE'


class JoinType(str, Enum):
    """Represents the type of join in a query.

    Attributes:
        INNER (str): Inner join.
        LEFT (str): Left join.
        RIGHT (str): Right join.
        FULL (str): Full join.
    """

    INNER = 'INNER'
    LEFT = 'LEFT'
    RIGHT = 'RIGHT'
    FULL = 'FULL'


class FilterConnector(str, Enum):
    """Represents the connector for filters in a query.

    Attributes:
        AND (str): Logical AND connector.
        OR (str): Logical OR connector.
    """

    AND = 'AND'
    OR = 'OR'


class FieldLookup(str, Enum):
    """Represents the lookup type for a field in a query.

    Attributes:
        EXACT (str): Exact match.
        EQ (str): Equal to.
        NEQ (str): Not equal to.
        GT (str): Greater than.
        GTE (str): Greater than or equal to.
        LT (str): Less than.
        LTE (str): Less than or equal to.
        IN (str): In a list.
        CONTAINS (str): Contains a value.
        ICONTAINS (str): Case-insensitive contains.
        STARTSWITH (str): Starts with a value.
        ISTARTSWITH (str): Case-insensitive starts with.
        ENDSWITH (str): Ends with a value.
        IENDSWITH (str): Case-insensitive ends with.
        ISNULL (str): Is null.
        REGEX (str): Matches a regular expression.
        IREGEX (str): Case-insensitive matches a regular expression.
    """

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
    """Represents the direction of ordering in a query.

    Attributes:
        ASC (str): Ascending order.
        DESC (str): Descending order.
    """

    ASC = 'ASC'
    DESC = 'DESC'


class TransactionAction(str, Enum):
    """Represents the action of a transaction.

    Attributes:
        BEGIN (str): Begin a transaction.
        COMMIT (str): Commit a transaction.
        ROLLBACK (str): Rollback a transaction.
        REVERT (str): Revert a transaction.
    """

    BEGIN = 'BEGIN'
    COMMIT = 'COMMIT'
    ROLLBACK = 'ROLLBACK'
    REVERT = 'REVERT'


class LockAction(str, Enum):
    """Represents the action of a lock.

    Attributes:
        ACQUIRE (str): Acquire a lock.
        RELEASE (str): Release a lock.
    """

    ACQUIRE = 'ACQUIRE'
    RELEASE = 'RELEASE'


class LockMode(str, Enum):
    """Represents the mode of a lock.

    Attributes:
        EXCLUSIVE (str): Exclusive lock.
        SHARED (str): Shared lock.
    """

    EXCLUSIVE = 'EXCLUSIVE'
    SHARED = 'SHARED'


class LockParameter(str, Enum):
    """Represents the parameter of a lock.

    Attributes:
        NOWAIT (str): Do not wait for the lock.
        SKIP_LOCKED (str): Skip locked rows.
        WAIT (str): Wait for the lock.
    """

    NOWAIT = 'NOWAIT'
    SKIP_LOCKED = 'SKIP_LOCKED'
    WAIT = 'WAIT'
