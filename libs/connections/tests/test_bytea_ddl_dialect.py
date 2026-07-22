"""BYTEA renders as SQLite's native ``BLOB`` in DDL, and as ``bytea`` on Postgres.

The canonical glue type for binary data is ``ScalarType.BYTEA`` (a Postgres-oriented name). qcraft
renders that name verbatim, so on SQLite it would emit a ``bytea`` column (NUMERIC affinity, and a
type name no SQLite tool expects). Binary columns use ``BLOB`` on SQLite, so the
SQLite dialect must lower ``bytea`` -> ``BLOB`` in DDL. This keeps new tables byte-for-byte
schema-compatible with existing ones and round-trips through introspection (``BLOB`` -> BYTEA).
"""

from amsdal_glue_connections._sql_core import SqlGenerator
from amsdal_glue_core.common.data_models.schema import PropertySchema
from amsdal_glue_core.common.data_models.schema import Schema
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.enums import ScalarType
from amsdal_glue_core.common.enums import Version
from amsdal_glue_core.common.operations.mutations.schema import AddProperty
from amsdal_glue_core.common.operations.mutations.schema import RegisterSchema

_lite = SqlGenerator('sqlite', param_style='qmark')
_pg = SqlGenerator('postgresql', param_style='format')
_TABLE = SchemaReference(name='t', version=Version.LATEST)


def _register(gen: SqlGenerator) -> str:
    schema = Schema(
        name='t',
        version=Version.LATEST,
        properties=[PropertySchema(name='secret', type=ScalarType.BYTEA, required=True)],
    )
    [(ddl, _)] = gen.compile_schema_mutation(RegisterSchema(schema_ref=_TABLE, schema=schema))
    return ddl


def test_sqlite_register_schema_bytea_renders_blob() -> None:
    ddl = _register(_lite)

    assert 'BLOB' in ddl
    assert 'bytea' not in ddl.lower()


def test_postgres_register_schema_bytea_stays_bytea() -> None:
    ddl = _register(_pg)

    assert 'bytea' in ddl.lower()
    assert 'BLOB' not in ddl.upper()


def test_sqlite_add_property_bytea_renders_blob() -> None:
    prop = PropertySchema(name='secret', type=ScalarType.BYTEA, required=False)
    [(ddl, _)] = _lite.compile_schema_mutation(AddProperty(schema_ref=_TABLE, property=prop))

    assert 'BLOB' in ddl
    assert 'bytea' not in ddl.lower()
