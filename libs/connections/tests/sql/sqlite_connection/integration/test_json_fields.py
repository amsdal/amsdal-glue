from amsdal_glue_core.common.data_models.annotation import AnnotationQuery
from amsdal_glue_core.common.data_models.annotation import ExpressionAnnotation
from amsdal_glue_core.common.data_models.data import Data
from amsdal_glue_core.common.data_models.query import QueryStatement
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.expressions.raw import RawExpression
from amsdal_glue_core.common.operations.mutations.data import InsertData

from amsdal_glue_connections.sql.connections.sqlite_connection import SqliteConnection

from ..testcases.schema_mutations import create_json_fields


def test_insert_and_read_json_data(database_connection: SqliteConnection) -> None:
    schema = create_json_fields(database_connection)

    data = Data(
        data={
            'field_dict': {'key': 'value'},
            'field_list': ['item1', 'item2'],
        },
    )

    database_connection.run_mutations([
        InsertData(
            schema=SchemaReference(name=schema.name, version=schema.version),
            data=[data],
        ),
    ])
    query = QueryStatement(
        table=SchemaReference(name=schema.name, version=schema.version),
    )

    result = database_connection.query(query)
    stored_data = [data.data for data in result]
    assert stored_data == [
        {
            'field_dict': {'key': 'value'},
            'field_list': ['item1', 'item2'],
        }
    ]


def test_annotate_json_object(database_connection: SqliteConnection) -> None:
    schema = create_json_fields(database_connection)
    data = Data(
        data={
            'field_dict': {'key': 'value'},
            'field_list': ['item1', 'item2'],
        },
    )

    database_connection.run_mutations([
        InsertData(
            schema=SchemaReference(name=schema.name, version=schema.version),
            data=[data],
        ),
    ])

    METADATA_SELECT_EXPRESSION = """
    json_object(
        'field_1', 10,
        'field_2', 'value',
        'field_3', json_object('nested_field', 'nested_value')
    )
    """  # noqa: N806
    query = QueryStatement(
        annotations=[
            AnnotationQuery(
                value=ExpressionAnnotation(
                    expression=RawExpression(METADATA_SELECT_EXPRESSION),
                    alias='_metadata',
                ),
            ),
        ],
        table=SchemaReference(name=schema.name, version=schema.version),
    )

    result = database_connection.query(query)
    stored_data = [data.data for data in result]
    assert stored_data == [
        {
            '_metadata': {
                'field_1': 10,
                'field_2': 'value',
                'field_3': {'nested_field': 'nested_value'},
            },
        }
    ]
