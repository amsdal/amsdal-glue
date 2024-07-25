# mypy: disable-error-code="type-abstract"
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.enums import TransactionAction
from amsdal_glue_core.common.enums import Version
from amsdal_glue_core.common.operations.base import Operation
from amsdal_glue_core.common.operations.commands import TransactionCommand
from amsdal_glue_core.containers import Container
from amsdal_glue_sql_parser.parsers.base import SqlParserBase


def test_begin_command(benchmark) -> None:
    parser = Container.services.get(SqlParserBase)
    expected_result = [
        TransactionCommand(
            transaction_id=None,
            schema=SchemaReference(name='', version=Version.LATEST),
            action=TransactionAction.BEGIN,
        )
    ]

    def parse_sql() -> list[Operation]:
        return parser.parse_sql('BEGIN')

    result = benchmark(parse_sql)

    assert result == expected_result
    assert parser.parse_sql('BEGIN TRANSACTION') == expected_result
    assert parser.parse_sql('BEGIN WORK') == expected_result


def test_begin_nested_transaction_command(benchmark) -> None:
    parser = Container.services.get(SqlParserBase)

    def parse_sql() -> list[Operation]:
        return parser.parse_sql('SAVEPOINT test_savepoint')

    result = benchmark(parse_sql)

    assert result == [
        TransactionCommand(
            transaction_id='test_savepoint',
            schema=SchemaReference(name='', version=Version.LATEST),
            action=TransactionAction.BEGIN,
        )
    ]


def test_rollback_transaction_command(benchmark) -> None:
    parser = Container.services.get(SqlParserBase)

    def parse_sql() -> list[Operation]:
        return parser.parse_sql('ROLLBACK')

    result = benchmark(parse_sql)

    assert result == [
        TransactionCommand(
            transaction_id=None,
            schema=SchemaReference(name='', version=Version.LATEST),
            action=TransactionAction.ROLLBACK,
        )
    ]


def test_rollback_nested_transaction_command(benchmark) -> None:
    parser = Container.services.get(SqlParserBase)
    expected_result = [
        TransactionCommand(
            transaction_id='test_savepoint',
            schema=SchemaReference(name='', version=Version.LATEST),
            action=TransactionAction.ROLLBACK,
        )
    ]

    def parse_sql() -> list[Operation]:
        return parser.parse_sql('ROLLBACK TO SAVEPOINT test_savepoint')

    result = benchmark(parse_sql)

    assert result == expected_result
    assert parser.parse_sql('ROLLBACK TO test_savepoint') == expected_result
    assert parser.parse_sql('ROLLBACK TRANSACTION TO test_savepoint') == expected_result
    assert parser.parse_sql('ROLLBACK WORK TO test_savepoint') == expected_result


def test_commit_transaction(benchmark) -> None:
    parser = Container.services.get(SqlParserBase)
    expected_result = [
        TransactionCommand(
            transaction_id=None,
            schema=SchemaReference(name='', version=Version.LATEST),
            action=TransactionAction.COMMIT,
        )
    ]

    def parse_sql() -> list[Operation]:
        return parser.parse_sql('COMMIT')

    result = benchmark(parse_sql)

    assert result == expected_result
    assert parser.parse_sql('COMMIT TRANSACTION') == expected_result
    assert parser.parse_sql('COMMIT WORK') == expected_result
