from __future__ import annotations

from typing import TYPE_CHECKING

from amsdal_glue_core.common.data_models.indexes import CustomIndexType
from amsdal_glue_core.common.enums import BuiltinIndexType
from amsdal_glue_core.common.exceptions import UnsupportedIndexTypeError

if TYPE_CHECKING:
    from amsdal_glue_core.common.data_models.indexes import IndexSchema
    from amsdal_glue_core.common.data_models.indexes import IndexType
    from amsdal_glue_core.common.operations.mutations.schema import SchemaMutation

_ALTERNATIVE = 'Declare this index on PostgreSQL, or omit the index type to use btree.'


def index_type_name(index_type: IndexType) -> str:
    if isinstance(index_type, CustomIndexType):
        return index_type.name
    return index_type.value


def declared_indexes(mutations: list[SchemaMutation]) -> list[IndexSchema]:
    from amsdal_glue_core.common.operations.mutations.schema import AddIndex
    from amsdal_glue_core.common.operations.mutations.schema import RegisterSchema

    indexes: list[IndexSchema] = []
    for mutation in mutations:
        if isinstance(mutation, AddIndex):
            indexes.append(mutation.index)
        elif isinstance(mutation, RegisterSchema):
            indexes.extend(mutation.schema.indexes or [])
    return indexes


def refuse_unsupported_index_types(mutations: list[SchemaMutation], *, backend: str) -> None:
    for index in declared_indexes(mutations):
        type_name = index_type_name(index.index_type)
        if type_name == BuiltinIndexType.BTREE.value:
            continue

        field_names = [field.name for field in index.fields]
        if len(field_names) == 1:
            field_text = f"field '{field_names[0]}'"
        elif field_names:
            quoted = ', '.join(f"'{name}'" for name in field_names)
            field_text = f'fields {quoted}'
        else:
            field_text = "field '<unknown>'"

        msg = (
            f"{backend} cannot build index '{index.name}' on {field_text} with type '{type_name}'. "
            f'{backend} only supports btree. {_ALTERNATIVE}'
        )
        raise UnsupportedIndexTypeError(msg)
