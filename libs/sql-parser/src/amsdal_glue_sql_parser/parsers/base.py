from abc import ABC
from abc import abstractmethod

from amsdal_glue_core.common.operations.base import Operation


class SqlParserBase(ABC):
    @abstractmethod
    def parse_sql(self, sql: str, dialect: str | None = None) -> list[Operation]:
        pass
