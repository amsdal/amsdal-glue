import pytest
from amsdal_glue_connections._sql_core import SqlGenerator
from amsdal_glue_connections._sql_core import SqlGenError
from amsdal_glue_connections._sql_core import UnsupportedDialectError


def test_postgresql_dialect() -> None:
    gen = SqlGenerator('postgresql')
    assert gen.dialect == 'postgresql'


def test_postgres_alias() -> None:
    gen = SqlGenerator('postgres')
    assert gen.dialect == 'postgresql'


def test_sqlite_dialect() -> None:
    gen = SqlGenerator('sqlite')
    assert gen.dialect == 'sqlite'


def test_invalid_dialect_raises() -> None:
    with pytest.raises(UnsupportedDialectError, match='Unsupported dialect'):
        SqlGenerator('mysql')


def test_unsupported_dialect_error_is_subclass_of_sql_gen_error() -> None:
    assert issubclass(UnsupportedDialectError, SqlGenError)


def test_sql_gen_error_is_subclass_of_exception() -> None:
    assert issubclass(SqlGenError, Exception)


def test_invalid_dialect_caught_by_base_sql_gen_error() -> None:
    with pytest.raises(SqlGenError):
        SqlGenerator('mysql')
