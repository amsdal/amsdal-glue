"""CSV connection: behavior on unsupported Expression children and on negated Conditions."""

from pathlib import Path

import pandas as pd
import pytest
from amsdal_glue_core.common.data_models.conditions import Condition
from amsdal_glue_core.common.data_models.conditions import Conditions
from amsdal_glue_core.common.data_models.field_reference import Field
from amsdal_glue_core.common.data_models.field_reference import FieldReference
from amsdal_glue_core.common.data_models.query import QueryStatement
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.enums import FieldLookup
from amsdal_glue_core.common.expressions.exists import Exists
from amsdal_glue_core.common.expressions.field_reference import FieldReferenceExpression
from amsdal_glue_core.common.expressions.value import Value

from amsdal_glue_connections.sql.connections.csv_connection.sync_connection import CsvConnection


def _make_connection(tmp_path: Path) -> CsvConnection:
    conn = CsvConnection()
    conn.connect(db_path=tmp_path)
    return conn


def _df() -> pd.DataFrame:
    return pd.DataFrame({'id': [1, 2, 3], 'name': ['a', 'b', 'c']})


def _exists_child() -> Exists:
    from amsdal_glue_core.common.data_models.sub_query import SubQueryStatement

    sub = SubQueryStatement(
        query=QueryStatement(
            only=[FieldReference(field=Field(name='1'), table_name='')],
            table=SchemaReference(name='Other'),
        ),
        alias='_exists_subquery',
    )
    return Exists(subquery=sub)


def _eq_id_1() -> Condition:
    return Condition(
        left=FieldReferenceExpression(field_reference=FieldReference(field=Field(name='id'), table_name='t')),
        lookup=FieldLookup.EQ,
        right=Value(value=1),
    )


def test_csv_get_conditions_raises_for_exists_expression_child(tmp_path: Path) -> None:
    """CSV cannot evaluate `Exists`; must raise NotImplementedError (not AttributeError)."""
    conn = _make_connection(tmp_path)
    df = _df()
    conditions = Conditions(_exists_child())

    with pytest.raises(NotImplementedError, match='Expression'):
        conn._get_conditions(conditions, df)  # noqa: SLF001


def test_csv_get_conditions_honors_outer_negated(tmp_path: Path) -> None:
    """`Conditions.negated=True` must invert the mask at the outer level."""
    conn = _make_connection(tmp_path)
    df = _df()
    conditions = Conditions(_eq_id_1(), negated=True)

    mask = conn._get_conditions(conditions, df)  # noqa: SLF001

    # Without the fix, `negated` is ignored and rows with id==1 remain True.
    assert mask.tolist() == [False, True, True]


def test_csv_process_on_raises_for_exists_child(tmp_path: Path) -> None:
    """`_process_on` (JOIN ON evaluation) must reject Expression children explicitly.

    Without the guard, `condition.left` access on an Exists child raises
    AttributeError at runtime and mypy also flags the union-attr unsafety.
    """
    conn = _make_connection(tmp_path)
    conditions = Conditions(_exists_child())

    with pytest.raises(NotImplementedError, match='Expression'):
        conn._process_on(conditions, left_on=True)  # noqa: SLF001


def test_csv_update_conditions_with_row_values_skips_non_condition_children(tmp_path: Path) -> None:
    """`_update_conditions_with_row_values` must not AttributeError on Expression children."""
    conn = _make_connection(tmp_path)
    row = pd.Series({'id': 1, 'name': 'a'})
    conditions = Conditions(_exists_child())

    # Must not raise. Walks the tree and leaves the Expression child alone.
    conn._update_conditions_with_row_values(conditions, row)  # noqa: SLF001
