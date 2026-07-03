# libs/connections/tests/golden/test_fts.py
"""Golden-master tests for PostgreSQL full-text search SQL paths.

Covers: tsvector/tsquery column types, SearchQuery search_type variants,
and FTS_MATCH WHERE clauses using phrase and websearch queries.
"""

import pytest
from amsdal_glue_connections._sql_core import UnsupportedFeatureError
from amsdal_glue_core.common.data_models.conditions import Condition
from amsdal_glue_core.common.data_models.conditions import Conditions
from amsdal_glue_core.common.data_models.field_reference import Field
from amsdal_glue_core.common.data_models.field_reference import FieldReference
from amsdal_glue_core.common.data_models.query import QueryStatement
from amsdal_glue_core.common.data_models.schema import PropertySchema
from amsdal_glue_core.common.data_models.schema import Schema
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.enums import FieldLookup
from amsdal_glue_core.common.enums import ScalarType
from amsdal_glue_core.common.enums import Version
from amsdal_glue_core.common.expressions.field_reference import FieldReferenceExpression
from amsdal_glue_core.common.expressions.search import SearchQuery
from amsdal_glue_core.common.expressions.value import Value
from amsdal_glue_core.common.operations.mutations.schema import RegisterSchema

from ._harness import lite
from ._harness import pg
from ._harness import pg_ddl

SCHEMA_REF = SchemaReference(name='articles', version=Version.LATEST)


def _field(name: str, table: str = 'articles') -> FieldReferenceExpression:
    return FieldReferenceExpression(
        field_reference=FieldReference(field=Field(name=name), table_name=table),
    )


# ---------------------------------------------------------------------------
# tsvector / tsquery column types
# ---------------------------------------------------------------------------


def test_tsvector_column_pg() -> None:
    mutation = RegisterSchema(
        schema_ref=SCHEMA_REF,
        schema=Schema(
            name='articles',
            version=Version.LATEST,
            properties=[
                PropertySchema(name='id', type=ScalarType.INTEGER, required=True),
                PropertySchema(name='title', type=ScalarType.TEXT, required=True),
                PropertySchema(name='search_vector', type=ScalarType.TSVECTOR, required=False),
            ],
        ),
    )
    [(sql, _params)] = pg_ddl(mutation)
    assert sql == (
        'CREATE TABLE "articles" ('
        '"id" integer NOT NULL, '
        '"title" text NOT NULL, '
        '"search_vector" tsvector'
        ')'
    )
    assert 'tsvector' in sql


def test_tsquery_column_pg() -> None:
    mutation = RegisterSchema(
        schema_ref=SCHEMA_REF,
        schema=Schema(
            name='articles',
            version=Version.LATEST,
            properties=[
                PropertySchema(name='id', type=ScalarType.INTEGER, required=True),
                PropertySchema(name='saved_query', type=ScalarType.TSQUERY, required=False),
            ],
        ),
    )
    [(sql, _params)] = pg_ddl(mutation)
    assert sql == (
        'CREATE TABLE "articles" ('
        '"id" integer NOT NULL, '
        '"saved_query" tsquery'
        ')'
    )
    assert 'tsquery' in sql


# ---------------------------------------------------------------------------
# SearchQuery search_type variants
# ---------------------------------------------------------------------------


def test_search_query_plain() -> None:
    sq = SearchQuery(args=[Value(value='english'), Value(value='test')], search_type='plain')
    assert sq.name == 'plainto_tsquery'


def test_search_query_phrase() -> None:
    sq = SearchQuery(args=[Value(value='english'), Value(value='test')], search_type='phrase')
    assert sq.name == 'phraseto_tsquery'


def test_search_query_raw() -> None:
    sq = SearchQuery(args=[Value(value='english'), Value(value='test')], search_type='raw')
    assert sq.name == 'to_tsquery'


def test_search_query_websearch() -> None:
    sq = SearchQuery(args=[Value(value='english'), Value(value='test')], search_type='websearch')
    assert sq.name == 'websearch_to_tsquery'


# ---------------------------------------------------------------------------
# FTS-specific WHERE queries (PostgreSQL only)
# ---------------------------------------------------------------------------


def test_phrase_query_in_where() -> None:
    query = QueryStatement(
        table=SchemaReference(name='articles', version=Version.LATEST),
        where=Conditions(
            Condition(
                left=_field('search_vector'),
                lookup=FieldLookup.FTS_MATCH,
                right=SearchQuery(
                    args=[Value(value='english'), Value(value='quick brown fox')],
                    search_type='phrase',
                ),
            ),
        ),
    )
    sql, params = pg(query)
    assert sql == (
        'SELECT * FROM "articles" WHERE "articles"."search_vector" @@ phraseto_tsquery(%s, %s)'
    )
    assert params == ['english', 'quick brown fox']
    assert '@@' in sql
    assert 'phraseto_tsquery' in sql


def test_phrase_query_in_where_sqlite_unsupported() -> None:
    query = QueryStatement(
        table=SchemaReference(name='articles', version=Version.LATEST),
        where=Conditions(
            Condition(
                left=_field('search_vector'),
                lookup=FieldLookup.FTS_MATCH,
                right=SearchQuery(
                    args=[Value(value='english'), Value(value='quick brown fox')],
                    search_type='phrase',
                ),
            ),
        ),
    )
    with pytest.raises(UnsupportedFeatureError):
        lite(query)


def test_websearch_query_in_where() -> None:
    query = QueryStatement(
        table=SchemaReference(name='articles', version=Version.LATEST),
        where=Conditions(
            Condition(
                left=_field('search_vector'),
                lookup=FieldLookup.FTS_MATCH,
                right=SearchQuery(
                    args=[Value(value='english'), Value(value='"exact phrase" -excluded')],
                    search_type='websearch',
                ),
            ),
        ),
    )
    sql, params = pg(query)
    assert sql == (
        'SELECT * FROM "articles" WHERE "articles"."search_vector" @@ websearch_to_tsquery(%s, %s)'
    )
    assert params == ['english', '"exact phrase" -excluded']
    assert '@@' in sql
    assert 'websearch_to_tsquery' in sql
