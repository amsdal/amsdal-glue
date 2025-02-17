from typing import Protocol

from amsdal_glue_core.common.data_models.output_type import OutputType

from amsdal_glue_connections.sql.sql_builders.transform import Transform
from amsdal_glue_connections.sql.sql_builders.transform import TransformTypes


class NestedFieldTransform(Protocol):
    def __call__(
        self,
        table_alias: str,
        namespace: str,
        field: str,
        fields: list[str],
        transform: Transform,
        output_type: type | OutputType | None = None,
    ) -> str: ...


def default_nested_field_transform(
    table_alias: str,
    namespace: str,
    field: str,
    fields: list[str],
    transform: Transform,
    output_type: type | OutputType | None = None,  # noqa: ARG001
) -> str:
    stmt = '__'.join([field, *fields])

    if table_alias:
        _namespace = transform.apply(TransformTypes.TABLE_QUOTE, namespace)
        _table = transform.apply(TransformTypes.TABLE_QUOTE, table_alias)
        _stmt = transform.apply(TransformTypes.FIELD_QUOTE, stmt)

        stmt = transform.apply(TransformTypes.TABLE_SEPARATOR, _namespace, _table, _stmt)

    return stmt
