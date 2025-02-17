from typing import Protocol

from amsdal_glue_core.common.data_models.field_reference import FieldReference
from amsdal_glue_core.common.data_models.field_reference import FieldReferenceAliased

from amsdal_glue_connections.sql.sql_builders.build_field import build_field
from amsdal_glue_connections.sql.sql_builders.exceptions import DistinctOnNotSupportedError
from amsdal_glue_connections.sql.sql_builders.transform import Transform


class BuildOnlyConstructor(Protocol):
    def __call__(
        self,
        only: list[FieldReference | FieldReferenceAliased] | None,
        transform: Transform,
        *,
        distinct: bool | list[FieldReference | FieldReferenceAliased] = False,
    ) -> str | None: ...


def default_build_only(
    only: list[FieldReference | FieldReferenceAliased] | None,
    transform: Transform,
    *,
    distinct: bool | list[FieldReference | FieldReferenceAliased] = False,
) -> str | None:
    if not only:
        return None

    items = [
        build_field(
            _only,
            transform=transform,
        )
        for _only in only
    ]

    fields = ', '.join(items)

    if distinct:
        if isinstance(distinct, list):
            raise DistinctOnNotSupportedError

        return f'DISTINCT {fields}'

    return fields


def pg_build_only(
    only: list[FieldReference | FieldReferenceAliased] | None,
    transform: Transform,
    *,
    distinct: bool | list[FieldReference | FieldReferenceAliased] = False,
) -> str | None:
    if not only:
        return None

    items = [
        build_field(
            _only,
            transform=transform,
        )
        for _only in only
    ]

    fields = ', '.join(items)

    if distinct:
        if isinstance(distinct, list):
            distinct_fields = ', '.join([
                build_field(
                    _distinct,
                    transform=transform,
                )
                for _distinct in distinct
            ])

            return f'DISTINCT ON ({distinct_fields}) {fields}'

        return f'DISTINCT {fields}'

    return fields
