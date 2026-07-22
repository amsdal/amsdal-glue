import pytest
from amsdal_glue_core.common.data_models.data import DataInput
from amsdal_glue_core.common.data_models.query import QueryStatement
from amsdal_glue_core.common.data_models.schema import PropertySchema
from amsdal_glue_core.common.data_models.schema import Schema
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.enums import ScalarType
from amsdal_glue_core.common.enums import Version
from amsdal_glue_core.common.expressions.value import Value
from amsdal_glue_core.common.operations.commands import SchemaCommand
from amsdal_glue_core.common.operations.mutations.data import InsertData
from amsdal_glue_core.common.operations.mutations.schema import RegisterSchema
from amsdal_glue_core.common.operations.mutations.schema import UpdateProperty

from amsdal_glue_connections.sql.connections.sqlite_connection import SqliteConnection
from amsdal_glue_connections.sql.schema_registry import TABLE_REGISTRY


def test_update_int_to_str_not_required(database_connection: SqliteConnection) -> None:
    schema: Schema = database_connection.run_schema_command(  # type: ignore[assignment]
        SchemaCommand(
            mutations=[
                RegisterSchema(
                    schema_ref=SchemaReference(name='TestTable', version=Version.LATEST),
                    schema=Schema(
                        name='TestTable',
                        version=Version.LATEST,
                        properties=[
                            PropertySchema(
                                name='field_a',
                                type=ScalarType.TEXT,
                                required=False,
                            ),
                            PropertySchema(
                                name='field_b',
                                type=ScalarType.INTEGER,
                                required=False,
                            ),
                        ],
                    ),
                ),
            ],
        ),
    )[0]
    database_connection.run_mutations([
        InsertData(
            schema=SchemaReference(name=schema.name, version=schema.version),
            data=[
                DataInput(data={'field_a': 'value1', 'field_b': 1}),
                DataInput(data={'field_a': 'value2', 'field_b': 2}),
                DataInput(data={'field_a': 'value3', 'field_b': 3}),
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
                    schema_ref=SchemaReference(name=schema.name, version=schema.version),
                    property=PropertySchema(name='field_b', type=ScalarType.TEXT, required=False),
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

    assert database_connection.query_schema(
        query=QueryStatement(table=SchemaReference(name=TABLE_REGISTRY, version=Version.LATEST))
    ) == [
        Schema(
            name='TestTable',
            version=Version.LATEST,
            properties=[
                PropertySchema(
                    name='field_a',
                    type=ScalarType.TEXT,
                    required=False,
                ),
                PropertySchema(
                    name='field_b',
                    type=ScalarType.TEXT,
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
                    schema_ref=SchemaReference(name='TestTable', version=Version.LATEST),
                    schema=Schema(
                        name='TestTable',
                        version=Version.LATEST,
                        properties=[
                            PropertySchema(
                                name='field_a',
                                type=ScalarType.TEXT,
                                required=True,
                            ),
                            PropertySchema(
                                name='field_b',
                                type=ScalarType.INTEGER,
                                required=True,
                            ),
                        ],
                    ),
                ),
            ],
        ),
    )[0]
    database_connection.run_mutations([
        InsertData(
            schema=SchemaReference(name=schema.name, version=schema.version),
            data=[
                DataInput(data={'field_a': 'value1', 'field_b': 1}),
                DataInput(data={'field_a': 'value2', 'field_b': 2}),
                DataInput(data={'field_a': 'value3', 'field_b': 3}),
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

    with pytest.raises(
        ValueError,
        match=(
            r"Cannot update field_b column. SQLite doesn't support "
            'ALTER COLUMN with required=True and no default value.'
        ),
    ):
        database_connection.run_schema_command(
            SchemaCommand(
                mutations=[
                    UpdateProperty(
                        schema_ref=SchemaReference(name=schema.name, version=schema.version),
                        property=PropertySchema(name='field_b', type=ScalarType.TEXT, required=True),
                    ),
                ],
            ),
        )[0]


def test_change_required_str(database_connection: SqliteConnection) -> None:
    schema: Schema = database_connection.run_schema_command(  # type: ignore[assignment]
        SchemaCommand(
            mutations=[
                RegisterSchema(
                    schema_ref=SchemaReference(name='TestTable', version=Version.LATEST),
                    schema=Schema(
                        name='TestTable',
                        version=Version.LATEST,
                        properties=[
                            PropertySchema(
                                name='field_a',
                                type=ScalarType.TEXT,
                                required=True,
                                default=Value(value=''),
                            ),
                            PropertySchema(
                                name='field_b',
                                type=ScalarType.TEXT,
                                required=False,
                                default=Value(value=''),
                            ),
                        ],
                    ),
                ),
            ],
        ),
    )[0]
    database_connection.run_mutations([
        InsertData(
            schema=SchemaReference(name=schema.name, version=schema.version),
            data=[
                DataInput(data={'field_a': 'value1', 'field_b': '1'}),
                DataInput(data={'field_a': 'value2', 'field_b': None}),
                DataInput(data={'field_a': 'value3', 'field_b': '3'}),
            ],
        ),
    ])

    query = QueryStatement(table=SchemaReference(name=schema.name, version=schema.version))
    result = database_connection.query(query)
    stored_data = [data.data for data in result]
    assert stored_data == [
        {'field_a': 'value1', 'field_b': '1'},
        {'field_a': 'value2', 'field_b': None},
        {'field_a': 'value3', 'field_b': '3'},
    ]

    with pytest.raises(ConnectionError) as excinfo:
        database_connection.run_schema_command(
            SchemaCommand(
                mutations=[
                    UpdateProperty(
                        schema_ref=SchemaReference(name=schema.name, version=schema.version),
                        property=PropertySchema(
                            name='field_b', type=ScalarType.TEXT, required=True, default=Value(value='')
                        ),
                    ),
                ],
            ),
        )[0]

    assert 'NOT NULL constraint failed' in str(excinfo.value)


def test_update_int_to_str(database_connection: SqliteConnection) -> None:
    schema: Schema = database_connection.run_schema_command(  # type: ignore[assignment]
        SchemaCommand(
            mutations=[
                RegisterSchema(
                    schema_ref=SchemaReference(name='TestTable', version=Version.LATEST),
                    schema=Schema(
                        name='TestTable',
                        version=Version.LATEST,
                        properties=[
                            PropertySchema(
                                name='field_a',
                                type=ScalarType.TEXT,
                                required=False,
                            ),
                            PropertySchema(
                                name='field_b',
                                type=ScalarType.TEXT,
                                required=False,
                            ),
                        ],
                    ),
                ),
            ],
        ),
    )[0]
    database_connection.run_mutations([
        InsertData(
            schema=SchemaReference(name=schema.name, version=schema.version),
            data=[
                DataInput(data={'field_a': 'value1', 'field_b': 1}),
                DataInput(data={'field_a': 'value2', 'field_b': 2}),
                DataInput(data={'field_a': 'value3', 'field_b': 3}),
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
                    schema_ref=SchemaReference(name=schema.name, version=schema.version),
                    property=PropertySchema(name='field_b', type=ScalarType.INTEGER, required=False),
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

    assert database_connection.query_schema(
        query=QueryStatement(table=SchemaReference(name=TABLE_REGISTRY, version=Version.LATEST))
    ) == [
        Schema(
            name='TestTable',
            version=Version.LATEST,
            properties=[
                PropertySchema(
                    name='field_a',
                    type=ScalarType.TEXT,
                    required=False,
                ),
                PropertySchema(
                    name='field_b',
                    type=ScalarType.INTEGER,
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
                    schema_ref=SchemaReference(name='TestTable', version=Version.LATEST),
                    schema=Schema(
                        name='TestTable',
                        version=Version.LATEST,
                        properties=[
                            PropertySchema(
                                name='field_a',
                                type=ScalarType.TEXT,
                                required=False,
                            ),
                            PropertySchema(
                                name='field_b',
                                type=ScalarType.TEXT,
                                required=False,
                            ),
                        ],
                    ),
                ),
            ],
        ),
    )[0]
    database_connection.run_mutations([
        InsertData(
            schema=SchemaReference(name=schema.name, version=schema.version),
            data=[
                DataInput(data={'field_a': 'value1', 'field_b': 'a1'}),
                DataInput(data={'field_a': 'value2', 'field_b': 'b2'}),
                DataInput(data={'field_a': 'value3', 'field_b': 'c3'}),
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
                    schema_ref=SchemaReference(name=schema.name, version=schema.version),
                    property=PropertySchema(name='field_b', type=ScalarType.INTEGER, required=False),
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

    assert database_connection.query_schema(
        query=QueryStatement(table=SchemaReference(name=TABLE_REGISTRY, version=Version.LATEST))
    ) == [
        Schema(
            name='TestTable',
            version=Version.LATEST,
            properties=[
                PropertySchema(
                    name='field_a',
                    type=ScalarType.TEXT,
                    required=False,
                ),
                PropertySchema(
                    name='field_b',
                    type=ScalarType.INTEGER,
                    required=False,
                ),
            ],
            constraints=[],
            indexes=[],
        )
    ]
