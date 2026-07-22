"""Raw ``dict``/``list`` values bound to JSONB columns must be serialised by the connection.

``_coerce`` passes JSON/JSONB values through unchanged (a native ``dict``/``list``) and delegates
serialisation to the binding layer. The connection must therefore accept a raw ``dict``/``list`` param
and store it as JSON -- callers should not have to pre-``json.dumps`` their JSONB values.
"""

from amsdal_glue_core.common.data_models.data import DataInput
from amsdal_glue_core.common.data_models.query import QueryStatement
from amsdal_glue_core.common.data_models.schema import PropertySchema
from amsdal_glue_core.common.data_models.schema import Schema
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.enums import ScalarType
from amsdal_glue_core.common.enums import Version
from amsdal_glue_core.common.operations.commands import SchemaCommand
from amsdal_glue_core.common.operations.mutations.data import InsertData
from amsdal_glue_core.common.operations.mutations.schema import RegisterSchema


def _register_json_schema(database_connection, name: str = 'JsonRawBinding') -> Schema:
    schema = Schema(
        name=name,
        version=Version.LATEST,
        properties=[
            PropertySchema(name='field_dict', type=ScalarType.JSONB, required=True),
            PropertySchema(name='field_list', type=ScalarType.JSONB, required=True),
        ],
    )
    database_connection.run_schema_command(
        SchemaCommand(
            mutations=[
                RegisterSchema(
                    schema_ref=SchemaReference(name=schema.name, version=Version.LATEST),
                    schema=schema,
                ),
            ],
        ),
    )
    return schema


def test_insert_raw_dict_and_list_into_jsonb(database_connection) -> None:
    schema = _register_json_schema(database_connection)

    # RAW dict/list -- NOT pre-serialised. This is what `_coerce` hands the binding layer for JSONB.
    data = DataInput(data={'field_dict': {'key': 'value', 'n': 1}, 'field_list': ['a', 'b', 3]})

    database_connection.run_mutations([
        InsertData(schema=SchemaReference(name=schema.name, version=Version.LATEST), data=[data]),
    ])

    result = database_connection.query(QueryStatement(table=SchemaReference(name=schema.name, version=Version.LATEST)))

    assert [row.data for row in result] == [{'field_dict': {'key': 'value', 'n': 1}, 'field_list': ['a', 'b', 3]}]


def test_insert_list_of_objects_into_jsonb(database_connection) -> None:
    """A JSONB column holding a list of OBJECTS -- the nested-container case.

    Each object round-trips through the generator as a JSON element inside a SQL array. The array is
    bound as one JSON parameter, so its elements must be plain Python objects, not per-element JSON
    markers -- otherwise the whole-array ``json.dumps`` chokes on the marker.
    """
    schema = _register_json_schema(database_connection, name='JsonListOfObjects')

    data = DataInput(
        data={
            'field_dict': {'k': 1},
            'field_list': [{'ref': {'id': 'a'}}, {'ref': {'id': 'b'}}],
        },
    )

    database_connection.run_mutations([
        InsertData(schema=SchemaReference(name=schema.name, version=Version.LATEST), data=[data]),
    ])

    result = database_connection.query(QueryStatement(table=SchemaReference(name=schema.name, version=Version.LATEST)))

    assert [row.data for row in result] == [
        {'field_dict': {'k': 1}, 'field_list': [{'ref': {'id': 'a'}}, {'ref': {'id': 'b'}}]},
    ]
