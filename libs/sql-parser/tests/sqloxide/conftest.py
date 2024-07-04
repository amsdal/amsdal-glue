import pytest
from amsdal_glue_core.containers import Container
from amsdal_glue_sql_parser.parsers.base import SqlParserBase
from amsdal_glue_sql_parser.parsers.sqloxide_parser import SqlOxideParser


@pytest.fixture(autouse=True)
def _set_up_parser() -> None:
    Container.services.register(SqlParserBase, SqlOxideParser)
