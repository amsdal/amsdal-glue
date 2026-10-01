"""Shared assertions for the UTC datetime storage contract.

The ISO strings of these three instants sort differently from instant order
(``22:00+04`` is the earliest instant and the middle string). A backend that
stores the original offset text fails ``ORDER BY`` and a ``>=`` bound.
"""

from datetime import datetime
from datetime import timedelta
from datetime import timezone
from typing import Any

import pytest
from amsdal_glue_core.common.data_models.conditions import Condition
from amsdal_glue_core.common.data_models.conditions import Conditions
from amsdal_glue_core.common.data_models.data import DataInput
from amsdal_glue_core.common.data_models.field_reference import Field
from amsdal_glue_core.common.data_models.field_reference import FieldReference
from amsdal_glue_core.common.data_models.order_by import OrderByQuery
from amsdal_glue_core.common.data_models.query import QueryStatement
from amsdal_glue_core.common.data_models.schema import PropertySchema
from amsdal_glue_core.common.data_models.schema import Schema
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.enums import FieldLookup
from amsdal_glue_core.common.enums import OrderDirection
from amsdal_glue_core.common.enums import ScalarType
from amsdal_glue_core.common.enums import Version
from amsdal_glue_core.common.expressions.field_reference import FieldReferenceExpression
from amsdal_glue_core.common.expressions.value import Value
from amsdal_glue_core.common.operations.commands import SchemaCommand
from amsdal_glue_core.common.operations.mutations.data import InsertData
from amsdal_glue_core.common.operations.mutations.schema import RegisterSchema

_PLUS_4 = timezone(timedelta(hours=4))
_PLUS_3 = timezone(timedelta(hours=3))

# Instant order is 1, 2, 3. Lexicographic order of the original ISO strings is 3, 1, 2.
_ROWS = (
    (1, datetime(2026, 9, 22, 22, 0, tzinfo=_PLUS_4)),  # 18:00 UTC
    (2, datetime(2026, 9, 22, 23, 0, tzinfo=_PLUS_3)),  # 20:00 UTC
    (3, datetime(2026, 9, 22, 21, 0, tzinfo=timezone.utc)),  # 21:00 UTC
)
_UTC = (
    datetime(2026, 9, 22, 18, 0, tzinfo=timezone.utc),
    datetime(2026, 9, 22, 20, 0, tzinfo=timezone.utc),
    datetime(2026, 9, 22, 21, 0, tzinfo=timezone.utc),
)


def _register(connection: Any, name: str) -> SchemaReference:
    connection.run_schema_command(
        SchemaCommand(
            mutations=[
                RegisterSchema(
                    schema_ref=SchemaReference(name=name, version=Version.LATEST),
                    schema=Schema(
                        name=name,
                        version=Version.LATEST,
                        properties=[
                            PropertySchema(name='id', type=ScalarType.INTEGER, required=True),
                            PropertySchema(name='happened_at', type=ScalarType.TIMESTAMPTZ, required=True),
                        ],
                    ),
                ),
            ],
        ),
    )
    return SchemaReference(name=name, version=Version.LATEST)


def _happened_at(table: str) -> FieldReferenceExpression:
    return FieldReferenceExpression(
        field_reference=FieldReference(field=Field(name='happened_at'), table_name=table),
    )


def _ids(connection: Any, query: QueryStatement) -> list[int]:
    return [row.data['id'] for row in connection.query(query)]


def assert_offset_datetimes_order_by_instant(connection: Any) -> None:
    schema_ref = _register(connection, 'event')
    connection.run_mutations([
        InsertData(
            schema=schema_ref,
            data=[DataInput(data={'id': row_id, 'happened_at': moment}) for row_id, moment in _ROWS],
        ),
    ])

    ordered = connection.query(
        QueryStatement(
            table=schema_ref,
            order_by=[OrderByQuery(expression=_happened_at('event'), direction=OrderDirection.ASC)],
        ),
    )
    assert [row.data['id'] for row in ordered] == [1, 2, 3]
    for row, expected in zip(ordered, _UTC, strict=True):
        moment = row.data['happened_at']
        assert isinstance(moment, datetime)
        assert moment.tzinfo is not None
        assert moment == expected

    # 23:00+03 is 20:00 UTC. The original ISO string sorts after 21:00+00.
    lower = datetime(2026, 9, 22, 23, 0, tzinfo=_PLUS_3)
    gte = QueryStatement(
        table=schema_ref,
        where=Conditions(
            Condition(left=_happened_at('event'), lookup=FieldLookup.GTE, right=Value(lower)),
        ),
        order_by=[OrderByQuery(expression=_happened_at('event'), direction=OrderDirection.ASC)],
    )
    assert _ids(connection, gte) == [2, 3]

    # The same bound as a query-string (``Z``), coerced with the field type.
    gte_text = QueryStatement(
        table=schema_ref,
        where=Conditions(
            Condition(
                left=_happened_at('event'),
                lookup=FieldLookup.GTE,
                right=Value('2026-09-22T20:00:00Z', output_type=ScalarType.TIMESTAMPTZ),
            ),
        ),
        order_by=[OrderByQuery(expression=_happened_at('event'), direction=OrderDirection.ASC)],
    )
    assert _ids(connection, gte_text) == [2, 3]


def assert_naive_datetime_insert_rejected(connection: Any) -> None:
    schema_ref = _register(connection, 'naive_event')
    with pytest.raises(ValueError, match='naive values are not treated as UTC'):
        connection.run_mutations([
            InsertData(
                schema=schema_ref,
                data=[DataInput(data={'id': 1, 'happened_at': datetime(2026, 9, 22, 21, 0)})],  # noqa: DTZ001
            ),
        ])
