"""ES connection: behavior on unsupported Expression children and on negated Conditions."""

import pytest
from amsdal_glue_core.common.data_models.conditions import Condition
from amsdal_glue_core.common.data_models.conditions import Conditions
from amsdal_glue_core.common.data_models.field_reference import Field
from amsdal_glue_core.common.data_models.field_reference import FieldReference
from amsdal_glue_core.common.data_models.query import QueryStatement
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.enums import FieldLookup
from amsdal_glue_core.common.data_models.sub_query import SubQueryStatement
from amsdal_glue_core.common.expressions.exists import Exists
from amsdal_glue_core.common.expressions.field_reference import FieldReferenceExpression
from amsdal_glue_core.common.expressions.value import Value

from amsdal_glue_connections.elasticsearch_connection.sync_connection import ElasticsearchConnection


def _exists_child() -> Exists:
    sub = QueryStatement(
        only=[FieldReference(field=Field(name='1'), table_name='')],
        table=SchemaReference(name='Other'),
    )
    return Exists(subquery=SubQueryStatement(query=sub, alias='exists_sub'))


def _eq_id_1() -> Condition:
    return Condition(
        left=FieldReferenceExpression(field_reference=FieldReference(field=Field(name='id'), table_name='t')),
        lookup=FieldLookup.EQ,
        right=Value(value=1),
    )


def test_es_conditions_to_es_query_raises_for_exists_child() -> None:
    """ES cannot translate `Exists` to an ES DSL fragment; must raise NotImplementedError."""
    conn = ElasticsearchConnection()
    conditions = Conditions(_exists_child())

    with pytest.raises(NotImplementedError, match='Expression'):
        conn._conditions_to_es_query(conditions)  # noqa: SLF001


def test_es_evaluate_conditions_on_data_raises_for_exists_child() -> None:
    """`_evaluate_conditions_on_data` must reject Expression children explicitly."""
    conn = ElasticsearchConnection()
    conditions = Conditions(_exists_child())

    with pytest.raises(NotImplementedError, match='Expression'):
        conn._evaluate_conditions_on_data({'id': 1}, conditions)  # noqa: SLF001


def test_es_row_matches_conditions_raises_for_exists_child() -> None:
    """`_row_matches_conditions` must reject Expression children explicitly."""
    conn = ElasticsearchConnection()
    conditions = Conditions(_exists_child())

    with pytest.raises(NotImplementedError, match='Expression'):
        conn._row_matches_conditions({'id': 1}, conditions)  # noqa: SLF001


def test_es_evaluate_conditions_on_data_honors_outer_negated() -> None:
    """`Conditions.negated=True` must invert the boolean at the outer level."""
    conn = ElasticsearchConnection()
    conditions = Conditions(_eq_id_1(), negated=True)

    # Row matches the inner condition (id=1) — but outer is negated.
    assert conn._evaluate_conditions_on_data({'id': 1}, conditions) is False  # noqa: SLF001
    # Row does not match the inner condition — outer-negated should be True.
    assert conn._evaluate_conditions_on_data({'id': 2}, conditions) is True  # noqa: SLF001


def test_es_row_matches_conditions_honors_outer_negated() -> None:
    """`Conditions.negated=True` must invert the row-match decision."""
    conn = ElasticsearchConnection()
    conditions = Conditions(_eq_id_1(), negated=True)

    assert conn._row_matches_conditions({'id': 1}, conditions) is False  # noqa: SLF001
    assert conn._row_matches_conditions({'id': 2}, conditions) is True  # noqa: SLF001


def test_es_conditions_to_es_query_with_substitution_raises_for_exists_child() -> None:
    """The substitution variant must also reject Expression children."""
    conn = ElasticsearchConnection()
    conditions = Conditions(_exists_child())

    with pytest.raises(NotImplementedError, match='Expression'):
        conn._conditions_to_es_query_with_substitution(  # noqa: SLF001
            conditions,
            main_result={},
            main_table_alias='t',
        )
