from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.enums import TransactionAction
from amsdal_glue_core.common.enums import Version
from amsdal_glue_core.common.operations.commands import TransactionCommand
from amsdal_glue_core.containers import Container
from amsdal_glue_sql_parser.parsers.base import SqlParserBase


def test_begin_command() -> None:
    parser = Container.services.get(SqlParserBase)
    expected_result = [
        TransactionCommand(
            transaction_id=None,
            schema=SchemaReference(name='', version=Version.LATEST),
            action=TransactionAction.BEGIN,
        )
    ]
    assert parser.parse_sql('BEGIN') == expected_result
    assert parser.parse_sql('BEGIN TRANSACTION') == expected_result
    assert parser.parse_sql('BEGIN WORK') == expected_result


def test_begin_nested_transaction_command() -> None:
    parser = Container.services.get(SqlParserBase)
    assert parser.parse_sql('SAVEPOINT test_savepoint') == [
        TransactionCommand(
            transaction_id='test_savepoint',
            schema=SchemaReference(name='', version=Version.LATEST),
            action=TransactionAction.BEGIN,
        )
    ]


def test_rollback_transaction_command() -> None:
    parser = Container.services.get(SqlParserBase)
    assert parser.parse_sql('ROLLBACK') == [
        TransactionCommand(
            transaction_id=None,
            schema=SchemaReference(name='', version=Version.LATEST),
            action=TransactionAction.ROLLBACK,
        )
    ]


def test_rollback_nested_transaction_command() -> None:
    parser = Container.services.get(SqlParserBase)
    expected_result = [
        TransactionCommand(
            transaction_id='test_savepoint',
            schema=SchemaReference(name='', version=Version.LATEST),
            action=TransactionAction.ROLLBACK,
        )
    ]
    assert parser.parse_sql('ROLLBACK TO SAVEPOINT test_savepoint') == expected_result
    assert parser.parse_sql('ROLLBACK TO test_savepoint') == expected_result
    assert parser.parse_sql('ROLLBACK TRANSACTION TO test_savepoint') == expected_result
    assert parser.parse_sql('ROLLBACK WORK TO test_savepoint') == expected_result


def test_commit_transaction() -> None:
    parser = Container.services.get(SqlParserBase)
    expected_result = [
        TransactionCommand(
            transaction_id=None,
            schema=SchemaReference(name='', version=Version.LATEST),
            action=TransactionAction.COMMIT,
        )
    ]
    assert parser.parse_sql('COMMIT') == expected_result
    assert parser.parse_sql('COMMIT TRANSACTION') == expected_result
    assert parser.parse_sql('COMMIT WORK') == expected_result
