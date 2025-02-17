from typing import Any

from amsdal_glue_core.common.data_models.field_reference import FieldReference
from amsdal_glue_core.common.data_models.field_reference import FieldReferenceAliased

from amsdal_glue_connections.sql.sql_builders.transform import Transform
from amsdal_glue_connections.sql.sql_builders.transform import TransformTypes


def build_field(
    field: FieldReference | FieldReferenceAliased,
    transform: Transform,
    output_type: Any = None,
) -> str:
    _item = []
    _field = field.field
    _namespace = transform.apply(TransformTypes.TABLE_QUOTE, field.namespace)

    while _field:
        _item.append(_field.name)
        _field = _field.child  # type: ignore[assignment]

    if len(_item) == 1:
        _field_stm = _item[0]
        _is_asterisk = _field_stm == '*'

        if field.table_name:
            _table = transform.apply(TransformTypes.TABLE_QUOTE, field.table_name)
            _stmt = _field_stm if _is_asterisk else transform.apply(TransformTypes.FIELD_QUOTE, _field_stm)
            _field_stm = transform.apply(TransformTypes.TABLE_SEPARATOR, _namespace, _table, _stmt)
        else:
            _field_stm = f'{_field_stm}'

        if not _is_asterisk and output_type is not None:
            _field_stm = transform.apply(TransformTypes.CAST, _field_stm, output_type)
    else:
        _field_stm = transform.apply(
            TransformTypes.NESTED_FIELD,
            table_alias=field.table_name,
            namespace=field.namespace,
            field=_item[0],
            fields=_item[1:],
            transform=transform,
            output_type=output_type,
        )

    if isinstance(field, FieldReferenceAliased) and field.alias:
        _alias = transform.apply(TransformTypes.FIELD_QUOTE, field.alias)
        _field_stm = f'{_field_stm} AS {_alias}'

    return _field_stm
