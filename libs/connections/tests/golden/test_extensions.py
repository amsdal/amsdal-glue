# libs/connections/tests/golden/test_extensions.py
"""Tests for CREATE/DROP EXTENSION and CREATE/DROP COLLATION DDL paths.

Covers: CREATE EXTENSION with IF NOT EXISTS, schema, version, cascade;
DROP EXTENSION with IF EXISTS and cascade; CREATE COLLATION with locale,
provider, deterministic; DROP COLLATION; UnsupportedFeatureError on SQLite;
InvalidValueError for invalid provider values; SQL-injection escaping.
"""

import pytest
from amsdal_glue_connections._sql_core import InvalidValueError
from amsdal_glue_connections._sql_core import UnsupportedFeatureError
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.enums import Version
from amsdal_glue_core.common.operations.mutations.schema import CreateCollation
from amsdal_glue_core.common.operations.mutations.schema import CreateExtension
from amsdal_glue_core.common.operations.mutations.schema import DropExtension
from amsdal_glue_core.common.operations.mutations.schema import RemoveCollation

from ._harness import lite_ddl
from ._harness import pg_ddl

SCHEMA_REF = SchemaReference(name='_default', version=Version.LATEST)


# ---------------------------------------------------------------------------
# CREATE EXTENSION
# ---------------------------------------------------------------------------


def test_create_extension_pg() -> None:
    mutation = CreateExtension(
        schema_ref=SCHEMA_REF,
        extension_name='pgvector',
    )
    [(sql, params)] = pg_ddl(mutation)
    assert sql == 'CREATE EXTENSION IF NOT EXISTS "pgvector"'
    assert params == []


def test_create_extension_no_if_not_exists() -> None:
    mutation = CreateExtension(
        schema_ref=SCHEMA_REF,
        extension_name='pgvector',
        if_not_exists=False,
    )
    [(sql, _params)] = pg_ddl(mutation)
    assert sql == 'CREATE EXTENSION "pgvector"'


def test_create_extension_with_schema() -> None:
    mutation = CreateExtension(
        schema_ref=SCHEMA_REF,
        extension_name='postgis',
        schema_name='public',
    )
    [(sql, _params)] = pg_ddl(mutation)
    assert sql == 'CREATE EXTENSION IF NOT EXISTS "postgis" SCHEMA "public"'
    assert 'CREATE EXTENSION IF NOT EXISTS "postgis"' in sql
    assert 'SCHEMA' in sql
    assert 'public' in sql


def test_create_extension_with_version() -> None:
    mutation = CreateExtension(
        schema_ref=SCHEMA_REF,
        extension_name='pgvector',
        version='0.7.0',
    )
    [(sql, _params)] = pg_ddl(mutation)
    assert sql == 'CREATE EXTENSION IF NOT EXISTS "pgvector" VERSION \'0.7.0\''
    assert 'CREATE EXTENSION IF NOT EXISTS "pgvector"' in sql
    assert "'0.7.0'" in sql


def test_create_extension_with_cascade() -> None:
    mutation = CreateExtension(
        schema_ref=SCHEMA_REF,
        extension_name='postgis',
        cascade=True,
    )
    [(sql, _params)] = pg_ddl(mutation)
    assert sql == 'CREATE EXTENSION IF NOT EXISTS "postgis" CASCADE'
    assert 'CREATE EXTENSION IF NOT EXISTS "postgis"' in sql
    assert 'CASCADE' in sql


def test_create_extension_full() -> None:
    mutation = CreateExtension(
        schema_ref=SCHEMA_REF,
        extension_name='postgis',
        schema_name='public',
        version='3.4.0',
        cascade=True,
    )
    [(sql, _params)] = pg_ddl(mutation)
    assert sql == 'CREATE EXTENSION IF NOT EXISTS "postgis" SCHEMA "public" VERSION \'3.4.0\' CASCADE'
    assert 'CREATE EXTENSION IF NOT EXISTS "postgis"' in sql
    assert 'public' in sql
    assert "'3.4.0'" in sql
    assert 'CASCADE' in sql


def test_create_extension_sqlite_unsupported() -> None:
    mutation = CreateExtension(
        schema_ref=SCHEMA_REF,
        extension_name='pgvector',
    )
    with pytest.raises(UnsupportedFeatureError):
        lite_ddl(mutation)


# ---------------------------------------------------------------------------
# DROP EXTENSION
# ---------------------------------------------------------------------------


def test_drop_extension_pg() -> None:
    mutation = DropExtension(
        schema_ref=SCHEMA_REF,
        extension_name='pgvector',
    )
    [(sql, params)] = pg_ddl(mutation)
    assert sql == 'DROP EXTENSION IF EXISTS "pgvector"'
    assert params == []


def test_drop_extension_no_if_exists() -> None:
    mutation = DropExtension(
        schema_ref=SCHEMA_REF,
        extension_name='pgvector',
        if_exists=False,
    )
    [(sql, _params)] = pg_ddl(mutation)
    assert sql == 'DROP EXTENSION "pgvector"'


def test_drop_extension_cascade() -> None:
    mutation = DropExtension(
        schema_ref=SCHEMA_REF,
        extension_name='postgis',
        cascade=True,
    )
    [(sql, _params)] = pg_ddl(mutation)
    assert sql == 'DROP EXTENSION IF EXISTS "postgis" CASCADE'


# ---------------------------------------------------------------------------
# CREATE COLLATION
# ---------------------------------------------------------------------------


def test_create_collation_pg() -> None:
    mutation = CreateCollation(
        schema_ref=SCHEMA_REF,
        collation_name='case_insensitive',
        provider='icu',
        locale='und-u-ks-level2',
        deterministic=False,
    )
    [(sql, params)] = pg_ddl(mutation)
    assert sql == (
        'CREATE COLLATION IF NOT EXISTS "case_insensitive"'
        " (LOCALE = 'und-u-ks-level2', PROVIDER = icu, DETERMINISTIC = FALSE)"
    )
    assert 'CREATE COLLATION' in sql
    assert '"case_insensitive"' in sql
    assert 'LOCALE' in sql
    assert 'und-u-ks-level2' in sql
    assert 'DETERMINISTIC' in sql
    assert 'FALSE' in sql
    assert params == []


def test_create_collation_deterministic() -> None:
    mutation = CreateCollation(
        schema_ref=SCHEMA_REF,
        collation_name='ukrainian',
        provider='icu',
        locale='uk-UA',
        deterministic=True,
    )
    [(sql, _params)] = pg_ddl(mutation)
    assert sql == (
        'CREATE COLLATION IF NOT EXISTS "ukrainian" (LOCALE = \'uk-UA\', PROVIDER = icu, DETERMINISTIC = TRUE)'
    )
    assert 'CREATE COLLATION' in sql
    assert '"ukrainian"' in sql
    assert 'uk-UA' in sql


def test_create_collation_sqlite_unsupported() -> None:
    mutation = CreateCollation(
        schema_ref=SCHEMA_REF,
        collation_name='test',
        locale='en',
    )
    with pytest.raises(UnsupportedFeatureError):
        lite_ddl(mutation)


# ---------------------------------------------------------------------------
# DROP COLLATION
# ---------------------------------------------------------------------------


def test_remove_collation_pg() -> None:
    mutation = RemoveCollation(
        schema_ref=SCHEMA_REF,
        collation_name='case_insensitive',
    )
    [(sql, params)] = pg_ddl(mutation)
    assert sql == 'DROP COLLATION IF EXISTS "case_insensitive"'
    assert params == []


def test_remove_collation_no_if_exists() -> None:
    mutation = RemoveCollation(
        schema_ref=SCHEMA_REF,
        collation_name='case_insensitive',
        if_exists=False,
    )
    [(sql, _params)] = pg_ddl(mutation)
    assert sql == 'DROP COLLATION "case_insensitive"'


def test_remove_collation_sqlite_unsupported() -> None:
    mutation = RemoveCollation(
        schema_ref=SCHEMA_REF,
        collation_name='test',
    )
    with pytest.raises(UnsupportedFeatureError):
        lite_ddl(mutation)


# ---------------------------------------------------------------------------
# CREATE COLLATION — SQL injection prevention
# ---------------------------------------------------------------------------


def test_create_collation_invalid_provider() -> None:
    mutation = CreateCollation(
        schema_ref=SCHEMA_REF,
        collation_name='evil',
        provider='icu; DROP TABLE users',
        locale='en',
    )
    with pytest.raises(InvalidValueError, match='Invalid collation provider'):
        pg_ddl(mutation)


def test_create_collation_locale_with_quotes() -> None:
    mutation = CreateCollation(
        schema_ref=SCHEMA_REF,
        collation_name='tricky',
        provider='icu',
        locale="en'; DROP TABLE users; --",
        deterministic=True,
    )
    [(sql, _params)] = pg_ddl(mutation)
    # The locale value must be escaped with doubled single-quotes.
    assert "'en''; DROP TABLE users; --'" in sql
    # After collapsing escaped quotes, no raw injection string survives.
    assert "en'; DROP TABLE" not in sql.replace("''", '')
