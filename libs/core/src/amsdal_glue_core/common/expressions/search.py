from dataclasses import dataclass

from amsdal_glue_core.common.expressions.func import Func

_SEARCH_TYPE_MAP = {
    'plain': 'plainto_tsquery',
    'phrase': 'phraseto_tsquery',
    'raw': 'to_tsquery',
    'websearch': 'websearch_to_tsquery',
}


@dataclass(kw_only=True)
class SearchVector(Func):
    name: str = 'to_tsvector'


@dataclass(kw_only=True)
class SearchQuery(Func):
    name: str = 'plainto_tsquery'
    search_type: str = 'plain'

    def __post_init__(self) -> None:
        self.name = _SEARCH_TYPE_MAP.get(self.search_type, self.name)


@dataclass(kw_only=True)
class SearchRank(Func):
    name: str = 'ts_rank'


@dataclass(kw_only=True)
class SearchHeadline(Func):
    name: str = 'ts_headline'
