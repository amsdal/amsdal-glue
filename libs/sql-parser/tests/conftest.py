# mypy: disable-error-code="type-abstract"
from collections.abc import Callable
from typing import Any

import pytest
from amsdal_glue_core.containers import Container

from amsdal_glue_sql_parser.parsers.base import SqlParserBase
from amsdal_glue_sql_parser.parsers.sqloxide_parser import SqlOxideParser


@pytest.fixture(autouse=True)
def _set_up_parser() -> None:
    Container.services.register(SqlParserBase, SqlOxideParser)


@pytest.fixture()
def benchmark() -> Callable[[Callable[[], Any]], Any]:
    """Passthrough fixture used when pytest-benchmark is not installed."""

    def _run(func: Callable[[], Any]) -> Any:
        return func()

    return _run
