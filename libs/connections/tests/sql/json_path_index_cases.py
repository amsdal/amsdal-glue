"""Shared declarations for the JSON-path index suites (PostgreSQL / SQLite, sync / async).

An index field with ``json_path`` is an expression index over a path inside a JSON column. Every
suite creates the same indexes on the same table and asserts that introspection reads each one back
equal to what was declared.
"""

from amsdal_glue_core.common.data_models.indexes import IndexField
from amsdal_glue_core.common.data_models.indexes import IndexSchema
from amsdal_glue_core.common.data_models.schema import PropertySchema
from amsdal_glue_core.common.data_models.schema import Schema
from amsdal_glue_core.common.enums import OrderDirection
from amsdal_glue_core.common.enums import ScalarType
from amsdal_glue_core.common.enums import Version

TABLE = 'passage'


def json_field(
    column: str = 'evidence',
    output_type: ScalarType = ScalarType.TEXT,
    direction: OrderDirection = OrderDirection.ASC,
) -> IndexField:
    return IndexField(name=column, json_path=['ref', 'object_id'], output_type=output_type, direction=direction)


INDEXES: dict[str, IndexSchema] = {
    'text_alone': IndexSchema(name='idx_text_alone', fields=[json_field()]),
    'jsonb_alone': IndexSchema(name='idx_jsonb_alone', fields=[json_field(output_type=ScalarType.JSONB)]),
    'text_desc': IndexSchema(name='idx_text_desc', fields=[json_field(direction=OrderDirection.DESC)]),
    'jsonb_desc': IndexSchema(
        name='idx_jsonb_desc', fields=[json_field(output_type=ScalarType.JSONB, direction=OrderDirection.DESC)]
    ),
    'json_then_column': IndexSchema(name='idx_json_then_column', fields=[json_field(), IndexField(name='label')]),
    'column_then_json': IndexSchema(
        name='idx_column_then_json',
        fields=[IndexField(name='label', direction=OrderDirection.DESC), json_field()],
    ),
    'unique': IndexSchema(name='idx_unique', fields=[json_field()], unique=True),
    'plain_column': IndexSchema(name='idx_plain_column', fields=[IndexField(name='label')]),
}


def table_schema(indexes: list[IndexSchema] | None = None) -> Schema:
    return Schema(
        name=TABLE,
        version=Version.LATEST,
        properties=[
            PropertySchema(name='id', type=ScalarType.INTEGER, required=True),
            PropertySchema(name='evidence', type=ScalarType.JSONB, required=False),
            PropertySchema(name='label', type=ScalarType.TEXT, required=False),
        ],
        indexes=indexes,
    )
