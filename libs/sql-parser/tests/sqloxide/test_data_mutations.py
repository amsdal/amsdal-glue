from amsdal_glue_core.common.data_models.conditions import Condition
from amsdal_glue_core.common.data_models.conditions import Conditions
from amsdal_glue_core.common.data_models.data import Data
from amsdal_glue_core.common.data_models.field_reference import Field
from amsdal_glue_core.common.data_models.field_reference import FieldReference
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.enums import FieldLookup
from amsdal_glue_core.common.enums import FilterConnector
from amsdal_glue_core.common.enums import Version
from amsdal_glue_core.common.expressions.value import Value
from amsdal_glue_core.common.operations.mutations.data import DeleteData
from amsdal_glue_core.common.operations.mutations.data import InsertData
from amsdal_glue_core.common.operations.mutations.data import UpdateData
from amsdal_glue_core.containers import Container
from amsdal_glue_sql_parser.parsers.base import SqlParserBase


def test_simple_insert_command() -> None:
    parser = Container.services.get(SqlParserBase)
    assert parser.parse_sql("INSERT INTO users (name, age) VALUES ('John', 30)") == [
        InsertData(
            schema=SchemaReference(name='users', version=Version.LATEST),
            data=[
                Data(
                    data={'name': 'John', 'age': '30'},
                    metadata=None,
                )
            ],
        )
    ]


def test_multiple_inserts() -> None:
    parser = Container.services.get(SqlParserBase)
    assert parser.parse_sql("INSERT INTO users (name, age) VALUES ('John', 30), ('Jane', 25)") == [
        InsertData(
            schema=SchemaReference(name='users', version=Version.LATEST),
            data=[
                Data(
                    data={'name': 'John', 'age': '30'},
                    metadata=None,
                ),
                Data(
                    data={'name': 'Jane', 'age': '25'},
                    metadata=None,
                ),
            ],
        )
    ]


def test_simple_update_command() -> None:
    parser = Container.services.get(SqlParserBase)
    assert parser.parse_sql("UPDATE users SET name = 'Jane', age = 25") == [
        UpdateData(
            schema=SchemaReference(name='users', version=Version.LATEST),
            data=[
                Data(
                    data={'name': 'Jane', 'age': '25'},
                    metadata=None,
                )
            ],
        )
    ]


def test_simple_update_command_condition() -> None:
    parser = Container.services.get(SqlParserBase)
    assert parser.parse_sql("UPDATE users SET name = 'Jane', age = 25 WHERE id = 1") == [
        UpdateData(
            schema=SchemaReference(name='users', version=Version.LATEST),
            data=[
                Data(
                    data={'name': 'Jane', 'age': '25'},
                    metadata=None,
                )
            ],
            query=Conditions(
                Condition(
                    field=FieldReference(field=Field(name='id'), table_name='users'),
                    lookup=FieldLookup.EQ,
                    value=Value(value='1'),
                ),
                connector=FilterConnector.AND,
            ),
        )
    ]


def test_simple_delete_command() -> None:
    parser = Container.services.get(SqlParserBase)
    assert parser.parse_sql('DELETE FROM users') == [
        DeleteData(
            schema=SchemaReference(name='users', version=Version.LATEST),
        )
    ]


def test_simple_delete_command_condition() -> None:
    parser = Container.services.get(SqlParserBase)
    assert parser.parse_sql('DELETE FROM users WHERE id = 1') == [
        DeleteData(
            schema=SchemaReference(name='users', version=Version.LATEST),
            query=Conditions(
                Condition(
                    field=FieldReference(field=Field(name='id'), table_name='users'),
                    lookup=FieldLookup.EQ,
                    value=Value(value='1'),
                ),
                connector=FilterConnector.AND,
            ),
        )
    ]
