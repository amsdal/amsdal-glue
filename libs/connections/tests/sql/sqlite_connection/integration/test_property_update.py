from amsdal_glue_core.common.data_models.data import Data
from amsdal_glue_core.common.data_models.query import QueryStatement
from amsdal_glue_core.common.data_models.schema import PropertySchema
from amsdal_glue_core.common.data_models.schema import Schema
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.enums import Version
from amsdal_glue_core.common.operations.commands import SchemaCommand
from amsdal_glue_core.common.operations.mutations.data import InsertData
from amsdal_glue_core.common.operations.mutations.schema import RegisterSchema
from amsdal_glue_core.common.operations.mutations.schema import UpdateProperty

from amsdal_glue_connections.sql.connections.sqlite_connection import SqliteConnection


def test_update_int_to_str_not_required(database_connection: SqliteConnection) -> None:
    schema: Schema = database_connection.run_schema_command(  # type: ignore[assignment]
        SchemaCommand(
            mutations=[
                RegisterSchema(
                    schema=Schema(
                        name='TestTable',
                        version=Version.LATEST,
                        properties=[
                            PropertySchema(
                                name='field_a',
                                type=str,
                                required=False,
                            ),
                            PropertySchema(
                                name='field_b',
                                type=int,
                                required=False,
                            ),
                        ],
                    )
                ),
            ],
        ),
    )[0]
    database_connection.run_mutations([
        InsertData(
            schema=SchemaReference(name=schema.name, version=schema.version),
            data=[
                Data(data={'field_a': 'value1', 'field_b': 1}),
                Data(data={'field_a': 'value2', 'field_b': 2}),
                Data(data={'field_a': 'value3', 'field_b': 3}),
            ],
        ),
    ])

    query = QueryStatement(table=SchemaReference(name=schema.name, version=schema.version))
    result = database_connection.query(query)
    stored_data = [data.data for data in result]
    assert stored_data == [
        {'field_a': 'value1', 'field_b': 1},
        {'field_a': 'value2', 'field_b': 2},
        {'field_a': 'value3', 'field_b': 3},
    ]

    database_connection.run_schema_command(
        SchemaCommand(
            mutations=[
                UpdateProperty(
                    schema_reference=SchemaReference(name=schema.name, version=schema.version),
                    property=PropertySchema(name='field_b', type=str, required=False),
                ),
            ],
        ),
    )[0]

    query = QueryStatement(table=SchemaReference(name=schema.name, version=schema.version))
    result = database_connection.query(query)
    stored_data = [data.data for data in result]
    assert stored_data == [
        {'field_a': 'value1', 'field_b': '1'},
        {'field_a': 'value2', 'field_b': '2'},
        {'field_a': 'value3', 'field_b': '3'},
    ]

    assert database_connection.query_schema() == [
        Schema(
            name='TestTable',
            version=Version.LATEST,
            properties=[
                PropertySchema(
                    name='field_a',
                    type=str,
                    required=False,
                ),
                PropertySchema(
                    name='field_b',
                    type=str,
                    required=False,
                ),
            ],
            constraints=[],
            indexes=[],
        )
    ]


def test_update_int_to_str_required(database_connection: SqliteConnection) -> None:
    schema: Schema = database_connection.run_schema_command(  # type: ignore[assignment]
        SchemaCommand(
            mutations=[
                RegisterSchema(
                    schema=Schema(
                        name='TestTable',
                        version=Version.LATEST,
                        properties=[
                            PropertySchema(
                                name='field_a',
                                type=str,
                                required=True,
                            ),
                            PropertySchema(
                                name='field_b',
                                type=int,
                                required=True,
                            ),
                        ],
                    )
                ),
            ],
        ),
    )[0]
    database_connection.run_mutations([
        InsertData(
            schema=SchemaReference(name=schema.name, version=schema.version),
            data=[
                Data(data={'field_a': 'value1', 'field_b': 1}),
                Data(data={'field_a': 'value2', 'field_b': 2}),
                Data(data={'field_a': 'value3', 'field_b': 3}),
            ],
        ),
    ])

    query = QueryStatement(table=SchemaReference(name=schema.name, version=schema.version))
    result = database_connection.query(query)
    stored_data = [data.data for data in result]
    assert stored_data == [
        {'field_a': 'value1', 'field_b': 1},
        {'field_a': 'value2', 'field_b': 2},
        {'field_a': 'value3', 'field_b': 3},
    ]

    database_connection.run_schema_command(
        SchemaCommand(
            mutations=[
                UpdateProperty(
                    schema_reference=SchemaReference(name=schema.name, version=schema.version),
                    property=PropertySchema(name='field_b', type=str, required=True),
                ),
            ],
        ),
    )[0]

    query = QueryStatement(table=SchemaReference(name=schema.name, version=schema.version))
    result = database_connection.query(query)
    stored_data = [data.data for data in result]
    assert stored_data == [
        {'field_a': 'value1', 'field_b': '1'},
        {'field_a': 'value2', 'field_b': '2'},
        {'field_a': 'value3', 'field_b': '3'},
    ]

    assert database_connection.query_schema() == [
        Schema(
            name='TestTable',
            version=Version.LATEST,
            properties=[
                PropertySchema(
                    name='field_a',
                    type=str,
                    required=True,
                ),
                PropertySchema(
                    name='field_b',
                    type=str,
                    required=False,
                ),
            ],
            constraints=[],
            indexes=[],
        )
    ]


def test_update_int_to_str(database_connection: SqliteConnection) -> None:
    schema: Schema = database_connection.run_schema_command(  # type: ignore[assignment]
        SchemaCommand(
            mutations=[
                RegisterSchema(
                    schema=Schema(
                        name='TestTable',
                        version=Version.LATEST,
                        properties=[
                            PropertySchema(
                                name='field_a',
                                type=str,
                                required=False,
                            ),
                            PropertySchema(
                                name='field_b',
                                type=str,
                                required=False,
                            ),
                        ],
                    )
                ),
            ],
        ),
    )[0]
    database_connection.run_mutations([
        InsertData(
            schema=SchemaReference(name=schema.name, version=schema.version),
            data=[
                Data(data={'field_a': 'value1', 'field_b': 1}),
                Data(data={'field_a': 'value2', 'field_b': 2}),
                Data(data={'field_a': 'value3', 'field_b': 3}),
            ],
        ),
    ])

    query = QueryStatement(table=SchemaReference(name=schema.name, version=schema.version))
    result = database_connection.query(query)
    stored_data = [data.data for data in result]
    assert stored_data == [
        {'field_a': 'value1', 'field_b': '1'},
        {'field_a': 'value2', 'field_b': '2'},
        {'field_a': 'value3', 'field_b': '3'},
    ]

    database_connection.run_schema_command(
        SchemaCommand(
            mutations=[
                UpdateProperty(
                    schema_reference=SchemaReference(name=schema.name, version=schema.version),
                    property=PropertySchema(name='field_b', type=int, required=False),
                ),
            ],
        ),
    )[0]

    query = QueryStatement(table=SchemaReference(name=schema.name, version=schema.version))
    result = database_connection.query(query)
    stored_data = [data.data for data in result]
    assert stored_data == [
        {'field_a': 'value1', 'field_b': 1},
        {'field_a': 'value2', 'field_b': 2},
        {'field_a': 'value3', 'field_b': 3},
    ]

    assert database_connection.query_schema() == [
        Schema(
            name='TestTable',
            version=Version.LATEST,
            properties=[
                PropertySchema(
                    name='field_a',
                    type=str,
                    required=False,
                ),
                PropertySchema(
                    name='field_b',
                    type=int,
                    required=False,
                ),
            ],
            constraints=[],
            indexes=[],
        )
    ]


def test_update_int_to_str_invalid(database_connection: SqliteConnection) -> None:
    schema: Schema = database_connection.run_schema_command(  # type: ignore[assignment]
        SchemaCommand(
            mutations=[
                RegisterSchema(
                    schema=Schema(
                        name='TestTable',
                        version=Version.LATEST,
                        properties=[
                            PropertySchema(
                                name='field_a',
                                type=str,
                                required=False,
                            ),
                            PropertySchema(
                                name='field_b',
                                type=str,
                                required=False,
                            ),
                        ],
                    )
                ),
            ],
        ),
    )[0]
    database_connection.run_mutations([
        InsertData(
            schema=SchemaReference(name=schema.name, version=schema.version),
            data=[
                Data(data={'field_a': 'value1', 'field_b': 'a1'}),
                Data(data={'field_a': 'value2', 'field_b': 'b2'}),
                Data(data={'field_a': 'value3', 'field_b': 'c3'}),
            ],
        ),
    ])

    query = QueryStatement(table=SchemaReference(name=schema.name, version=schema.version))
    result = database_connection.query(query)
    stored_data = [data.data for data in result]
    assert stored_data == [
        {'field_a': 'value1', 'field_b': 'a1'},
        {'field_a': 'value2', 'field_b': 'b2'},
        {'field_a': 'value3', 'field_b': 'c3'},
    ]

    database_connection.run_schema_command(
        SchemaCommand(
            mutations=[
                UpdateProperty(
                    schema_reference=SchemaReference(name=schema.name, version=schema.version),
                    property=PropertySchema(name='field_b', type=int, required=False),
                ),
            ],
        ),
    )

    query = QueryStatement(table=SchemaReference(name=schema.name, version=schema.version))
    result = database_connection.query(query)
    stored_data = [data.data for data in result]
    assert stored_data == [
        {'field_a': 'value1', 'field_b': 'a1'},
        {'field_a': 'value2', 'field_b': 'b2'},
        {'field_a': 'value3', 'field_b': 'c3'},
    ]

    assert database_connection.query_schema() == [
        Schema(
            name='TestTable',
            version=Version.LATEST,
            properties=[
                PropertySchema(
                    name='field_a',
                    type=str,
                    required=False,
                ),
                PropertySchema(
                    name='field_b',
                    type=int,
                    required=False,
                ),
            ],
            constraints=[],
            indexes=[],
        )
    ]
