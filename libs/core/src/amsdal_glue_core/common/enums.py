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
        CROSS (str): Cross join.
        INNER_LATERAL (str): Inner lateral join.
        LEFT_LATERAL (str): Left lateral join.
    """

    INNER = 'INNER'
    LEFT = 'LEFT'
    RIGHT = 'RIGHT'
    FULL = 'FULL'
    CROSS = 'CROSS'
    INNER_LATERAL = 'INNER_LATERAL'
    LEFT_LATERAL = 'LEFT_LATERAL'


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
    BETWEEN = 'BETWEEN'
    JSONB_CONTAINS = 'JSONB_CONTAINS'
    JSONB_CONTAINED_BY = 'JSONB_CONTAINED_BY'
    JSONB_HAS_KEY = 'JSONB_HAS_KEY'
    JSONB_HAS_ANY_KEY = 'JSONB_HAS_ANY_KEY'
    JSONB_HAS_ALL_KEYS = 'JSONB_HAS_ALL_KEYS'
    FTS_MATCH = 'FTS_MATCH'
    TRIGRAM_SIMILAR = 'TRIGRAM_SIMILAR'
    TRIGRAM_WORD_SIMILAR = 'TRIGRAM_WORD_SIMILAR'
    TRIGRAM_STRICT_WORD_SIMILAR = 'TRIGRAM_STRICT_WORD_SIMILAR'
    RANGE_CONTAINS = 'RANGE_CONTAINS'
    RANGE_CONTAINED_BY = 'RANGE_CONTAINED_BY'
    RANGE_OVERLAP = 'RANGE_OVERLAP'
    RANGE_STRICTLY_LEFT = 'RANGE_STRICTLY_LEFT'
    RANGE_STRICTLY_RIGHT = 'RANGE_STRICTLY_RIGHT'
    RANGE_NOT_LEFT = 'RANGE_NOT_LEFT'
    RANGE_NOT_RIGHT = 'RANGE_NOT_RIGHT'
    RANGE_ADJACENT = 'RANGE_ADJACENT'

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
            case FieldLookup.BETWEEN:
                return 'between'
            case FieldLookup.JSONB_CONTAINS:
                return '@>'
            case FieldLookup.JSONB_CONTAINED_BY:
                return '<@'
            case FieldLookup.JSONB_HAS_KEY:
                return '?'
            case FieldLookup.JSONB_HAS_ANY_KEY:
                return '?|'
            case FieldLookup.JSONB_HAS_ALL_KEYS:
                return '?&'
            case FieldLookup.FTS_MATCH:
                return '@@'
            case FieldLookup.TRIGRAM_SIMILAR:
                return '%'
            case FieldLookup.TRIGRAM_WORD_SIMILAR:
                return '<%'
            case FieldLookup.TRIGRAM_STRICT_WORD_SIMILAR:
                return '<<%'
            case FieldLookup.RANGE_CONTAINS:
                return '@>'
            case FieldLookup.RANGE_CONTAINED_BY:
                return '<@'
            case FieldLookup.RANGE_OVERLAP:
                return '&&'
            case FieldLookup.RANGE_STRICTLY_LEFT:
                return '<<'
            case FieldLookup.RANGE_STRICTLY_RIGHT:
                return '>>'
            case FieldLookup.RANGE_NOT_LEFT:
                return '&>'
            case FieldLookup.RANGE_NOT_RIGHT:
                return '&<'
            case FieldLookup.RANGE_ADJACENT:
                return '-|-'
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


class LockScope(str, Enum):
    """Lifetime of a non-row lock.

    - ``TRANSACTION`` — auto-released at end of the current transaction
      (``pg_advisory_xact_lock`` / ``LOCK TABLE`` inside ``BEGIN``).
    - ``SESSION`` — held until explicit release or connection death
      (``pg_advisory_lock``); used by infrastructure (e.g. WAL ownership)
      that must outlive a single transaction.
    """

    TRANSACTION = 'TRANSACTION'
    SESSION = 'SESSION'


class SetOperationType(str, Enum):
    UNION = 'union'
    UNION_ALL = 'union_all'
    INTERSECT = 'intersect'
    EXCEPT = 'except'


class WindowFrameType(str, Enum):
    ROWS = 'rows'
    RANGE = 'range'
    GROUPS = 'groups'


class LockStrength(str, Enum):
    UPDATE = 'for_update'
    NO_KEY_UPDATE = 'for_no_key_update'
    SHARE = 'for_share'
    KEY_SHARE = 'for_key_share'


class ScalarType(str, Enum):
    TEXT = 'text'
    INTEGER = 'integer'
    BIGINT = 'bigint'
    SMALLINT = 'smallint'
    FLOAT = 'float'
    # ANSI ``double precision``: a bare ``double`` is not a valid Postgres type. Rendered verbatim as
    # the column/cast type on both dialects (SQLite accepts it as REAL affinity), and both introspection
    # maps resolve ``double precision`` -> DOUBLE, so a RegisterSchema->introspect cycle round-trips.
    DOUBLE = 'double precision'
    NUMERIC = 'numeric'
    BOOLEAN = 'boolean'
    DATE = 'date'
    TIME = 'time'
    TIMESTAMP = 'timestamp'
    TIMESTAMPTZ = 'timestamptz'
    INTERVAL = 'interval'
    BYTEA = 'bytea'
    JSON = 'json'
    JSONB = 'jsonb'
    UUID = 'uuid'
    SMALLSERIAL = 'smallserial'
    SERIAL = 'serial'
    BIGSERIAL = 'bigserial'
    TSVECTOR = 'tsvector'
    TSQUERY = 'tsquery'
    INT4RANGE = 'int4range'
    INT8RANGE = 'int8range'
    NUMRANGE = 'numrange'
    DATERANGE = 'daterange'
    TSRANGE = 'tsrange'
    TSTZRANGE = 'tstzrange'


class BuiltinIndexType(str, Enum):
    BTREE = 'btree'
    HASH = 'hash'
    GIN = 'gin'
    GIST = 'gist'
    BRIN = 'brin'


class ReferentialAction(str, Enum):
    NO_ACTION = 'no_action'
    RESTRICT = 'restrict'
    CASCADE = 'cascade'
    SET_NULL = 'set_null'
    SET_DEFAULT = 'set_default'


class ConflictAction(str, Enum):
    NOTHING = 'nothing'
    UPDATE = 'update'
