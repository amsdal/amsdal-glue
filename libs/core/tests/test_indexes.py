from copy import copy

import pytest

from amsdal_glue_core.common.data_models.indexes import CustomIndexType
from amsdal_glue_core.common.data_models.indexes import IndexField
from amsdal_glue_core.common.data_models.indexes import IndexSchema
from amsdal_glue_core.common.enums import BuiltinIndexType
from amsdal_glue_core.common.enums import OrderDirection
from amsdal_glue_core.common.enums import ScalarType


def test_hash_does_not_raise() -> None:
    """A non-frozen dataclass with default `eq=True` gets `__hash__ = None`; `IndexSchema` overrides
    `__hash__` explicitly, so hashing a schema (including one with a `CustomIndexType`) must not raise.
    """
    schema = IndexSchema(
        name='idx_embedding',
        fields=[IndexField(name='embedding')],
        index_type=CustomIndexType(name='hnsw'),
    )
    assert isinstance(hash(schema), int)


def test_eq_and_hash_agree_for_equal_schemas() -> None:
    schema_a = IndexSchema(name='idx_status', fields=[IndexField(name='status')])
    schema_b = IndexSchema(name='idx_status', fields=[IndexField(name='status')])

    assert schema_a == schema_b
    assert hash(schema_a) == hash(schema_b)


def test_eq_and_hash_tolerate_fields_none() -> None:
    """`fields=None` is tolerated (treated as empty) rather than raising, matching `main`'s original
    None-safe semantics that a stricter `zip(..., strict=True)` had dropped.
    """
    schema_a = IndexSchema(name='idx_empty', fields=None)  # type: ignore[arg-type]
    schema_b = IndexSchema(name='idx_empty', fields=[])

    assert schema_a == schema_b
    assert hash(schema_a) == hash(schema_b)
    assert isinstance(hash(schema_a), int)


def test_include_makes_schemas_with_different_include_unequal() -> None:
    schema_with_include = IndexSchema(
        name='idx_covering',
        fields=[IndexField(name='status')],
        include=['amount'],
    )
    schema_without_include = IndexSchema(
        name='idx_covering',
        fields=[IndexField(name='status')],
    )

    assert schema_with_include != schema_without_include
    assert hash(schema_with_include) != hash(schema_without_include)


def test_include_makes_schemas_with_same_include_equal() -> None:
    schema_a = IndexSchema(name='idx_covering', fields=[IndexField(name='status')], include=['amount'])
    schema_b = IndexSchema(name='idx_covering', fields=[IndexField(name='status')], include=['amount'])

    assert schema_a == schema_b
    assert hash(schema_a) == hash(schema_b)


def test_direction_ignored_for_non_btree_type() -> None:
    """Only `btree` honours per-column ordering; for any other access method, `ASC` vs `DESC` must
    not affect equality (every other access method always reports ascending on introspection).
    """
    asc_schema = IndexSchema(
        name='idx_embedding',
        fields=[IndexField(name='embedding', direction=OrderDirection.ASC)],
        index_type=CustomIndexType(name='hnsw'),
    )
    desc_schema = IndexSchema(
        name='idx_embedding',
        fields=[IndexField(name='embedding', direction=OrderDirection.DESC)],
        index_type=CustomIndexType(name='hnsw'),
    )

    assert asc_schema == desc_schema
    assert hash(asc_schema) == hash(desc_schema)


def test_direction_matters_for_btree_type() -> None:
    asc_schema = IndexSchema(
        name='idx_amount',
        fields=[IndexField(name='amount', direction=OrderDirection.ASC)],
        index_type=BuiltinIndexType.BTREE,
    )
    desc_schema = IndexSchema(
        name='idx_amount',
        fields=[IndexField(name='amount', direction=OrderDirection.DESC)],
        index_type=BuiltinIndexType.BTREE,
    )

    assert asc_schema != desc_schema


def test_custom_index_type_name_case_fold() -> None:
    """`CustomIndexType.__post_init__` casefolds `name` so a declaration of `CustomIndexType(name='HNSW')`
    still equals its (always-lowercase) introspection.
    """
    declared = IndexSchema(
        name='idx_embedding',
        fields=[IndexField(name='embedding')],
        index_type=CustomIndexType(name='HNSW'),
    )
    introspected = IndexSchema(
        name='idx_embedding',
        fields=[IndexField(name='embedding')],
        index_type=CustomIndexType(name='hnsw'),
    )

    assert declared.index_type == introspected.index_type
    assert declared == introspected


def test_custom_index_type_params_does_not_break_equality() -> None:
    """`CustomIndexType.params` is dead weight (never read by the extractor) and is excluded from
    equality/hash so a declaration that sets it still equals the introspected value, which never
    populates it.
    """
    declared = CustomIndexType(name='hnsw', params={'m': 16})
    introspected = CustomIndexType(name='hnsw')

    assert declared == introspected
    assert hash(IndexSchema(name='i', fields=[], index_type=declared)) == hash(
        IndexSchema(name='i', fields=[], index_type=introspected)
    )


def test_custom_index_type_params_excluded_from_repr() -> None:
    assert 'params' not in repr(CustomIndexType(name='hnsw', params={'m': 16}))


def test_op_class_default_resolves_equal_to_declared_default() -> None:
    """A declared `op_class` naming the access method's default reads back as `None` on
    introspection (see `TABLE_INDEX_REGISTRY`'s `opc.opcdefault` check); `default_op_class` --
    populated only by introspection -- lets `IndexSchema.__eq__` resolve the two as equal.
    """
    declared = IndexSchema(
        name='idx_title',
        fields=[IndexField(name='title', op_class='text_ops')],
        index_type=BuiltinIndexType.BTREE,
    )
    introspected = IndexSchema(
        name='idx_title',
        fields=[IndexField(name='title', op_class=None, default_op_class='text_ops')],
        index_type=BuiltinIndexType.BTREE,
    )

    assert declared == introspected


def test_op_class_non_default_mismatch_stays_unequal() -> None:
    declared = IndexSchema(
        name='idx_title',
        fields=[IndexField(name='title', op_class='text_pattern_ops')],
        index_type=BuiltinIndexType.BTREE,
    )
    introspected = IndexSchema(
        name='idx_title',
        fields=[IndexField(name='title', op_class=None, default_op_class='text_ops')],
        index_type=BuiltinIndexType.BTREE,
    )

    assert declared != introspected


def test_default_op_class_excluded_from_raw_field_equality() -> None:
    """`default_op_class` is introspection-only and must not affect the auto-generated `IndexField`
    equality used when comparing raw field lists directly (not via `IndexSchema._fields_equal`).
    """
    declared = IndexField(name='embedding', op_class='vector_cosine_ops')
    introspected = IndexField(name='embedding', op_class='vector_cosine_ops', default_op_class='vector_l2_ops')

    assert declared == introspected
    assert 'default_op_class' not in repr(introspected)


def test_copy_preserves_equality() -> None:
    schema = IndexSchema(
        name='idx_status',
        fields=[IndexField(name='status')],
        include=['amount'],
        parameters={'m': '16'},
    )
    assert copy(schema) == schema


def _json_path_field(**kwargs) -> IndexField:
    return IndexField(name='evidence', json_path=['ref', 'object_id'], output_type=ScalarType.TEXT, **kwargs)


def test_json_path_defaults_to_a_plain_column() -> None:
    field = IndexField(name='evidence')

    assert field.json_path is None
    assert field.output_type is None


def test_json_path_and_output_type_are_part_of_equality_and_hash() -> None:
    declared = IndexSchema(name='idx', fields=[_json_path_field()])

    assert declared == IndexSchema(name='idx', fields=[_json_path_field()])
    assert hash(declared) == hash(IndexSchema(name='idx', fields=[_json_path_field()]))

    other_output_type = IndexSchema(
        name='idx',
        fields=[IndexField(name='evidence', json_path=['ref', 'object_id'], output_type=ScalarType.JSONB)],
    )
    other_path = IndexSchema(
        name='idx',
        fields=[IndexField(name='evidence', json_path=['ref', 'object_version'], output_type=ScalarType.TEXT)],
    )
    plain_column = IndexSchema(name='idx', fields=[IndexField(name='evidence')])

    assert declared != other_output_type
    assert declared != other_path
    assert declared != plain_column


def test_json_path_is_compared_in_field_order() -> None:
    declared = IndexSchema(name='idx', fields=[_json_path_field(), IndexField(name='label')])

    assert declared == IndexSchema(name='idx', fields=[_json_path_field(), IndexField(name='label')])
    assert declared != IndexSchema(name='idx', fields=[IndexField(name='label'), _json_path_field()])


def test_json_path_direction_is_compared_for_btree() -> None:
    ascending = IndexSchema(name='idx', fields=[_json_path_field()])
    descending = IndexSchema(name='idx', fields=[_json_path_field(direction=OrderDirection.DESC)])

    assert ascending != descending


def test_empty_json_path_is_a_plain_column() -> None:
    assert IndexField(name='evidence', json_path=[]).json_path is None


@pytest.mark.parametrize('output_type', [None, ScalarType.INTEGER])
def test_json_path_requires_text_or_jsonb_output_type(output_type: ScalarType | None) -> None:
    with pytest.raises(ValueError, match='output_type'):
        IndexField(name='evidence', json_path=['ref', 'object_id'], output_type=output_type)


def test_output_type_requires_json_path() -> None:
    with pytest.raises(ValueError, match='json_path'):
        IndexField(name='evidence', output_type=ScalarType.TEXT)
