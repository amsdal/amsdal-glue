"""Property-type conversion in the schema-command controller.

A nested-object property maps to ``NestedType``; scalars map to ``ScalarType``.
A relation is NOT a property type — relations are expressed via ``ForeignKeyConstraint``,
so a ``SchemaReference`` is rejected as a property ``type``.
"""

import pytest
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.data_models.types import NestedType
from amsdal_glue_core.common.enums import ScalarType
from pydantic import ValidationError

from amsdal_glue_api_server.controllers.operations.schema_commands import PropertySchemaBody
from amsdal_glue_api_server.controllers.operations.schema_commands import SchemaBody
from amsdal_glue_api_server.controllers.operations.schema_commands import property_type_to_core_property_type


@pytest.mark.parametrize(
    ('name', 'expected'),
    [
        ('int', ScalarType.INTEGER),
        ('str', ScalarType.TEXT),
        ('float', ScalarType.FLOAT),
        ('bool', ScalarType.BOOLEAN),
        ('list', ScalarType.JSON),
        ('dict', ScalarType.JSONB),
        ('unknown', ScalarType.TEXT),  # fallback
    ],
)
def test_scalar_property_type(name: str, expected: ScalarType) -> None:
    assert property_type_to_core_property_type(name) == expected


def test_nested_object_property_maps_to_nested_type() -> None:
    nested = SchemaBody(
        name='address',
        version='LATEST',
        properties=[
            PropertySchemaBody(name='street', type='str', required=True),
            PropertySchemaBody(name='zip', type='int', required=False),
        ],
    )

    result = property_type_to_core_property_type(nested)

    assert result == NestedType(properties={'street': ScalarType.TEXT, 'zip': ScalarType.INTEGER})


def test_deeply_nested_object_recurses() -> None:
    nested = SchemaBody(
        name='profile',
        version='LATEST',
        properties=[
            PropertySchemaBody(
                name='address',
                type=SchemaBody(
                    name='address',
                    version='LATEST',
                    properties=[PropertySchemaBody(name='city', type='str', required=True)],
                ),
                required=True,
            ),
        ],
    )

    result = property_type_to_core_property_type(nested)

    assert result == NestedType(properties={'address': NestedType(properties={'city': ScalarType.TEXT})})


def test_schema_reference_is_rejected_as_property_type() -> None:
    # Relations are ForeignKeyConstraints, not property types — a SchemaReference must not
    # be accepted where a property type is expected.
    with pytest.raises(ValidationError):
        PropertySchemaBody(
            name='customer',
            type=SchemaReference(name='customers', version='LATEST'),
            required=True,
        )
