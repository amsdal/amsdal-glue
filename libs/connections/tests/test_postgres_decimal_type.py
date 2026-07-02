"""Postgres decimal/NUMERIC handling — re-pointed to Rust SqlGenerator.

Old tests used deleted internals: pg_value_type_transform, PostgresConnection._to_sql_type,
_to_python_type, _build_column_update, and DecimalSchemaModel.  Each is re-pointed to
the surviving equivalent: _pg_type_to_field_type / _PG_TYPE_MAP for introspection lookups,
and compile_schema_mutation for DDL emission.

SUSPICIOUS items flagged inline.
"""

from amsdal_glue_core.common.data_models.schema import PropertySchema
from amsdal_glue_core.common.data_models.schema import Schema
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.data_models.types import CustomType
from amsdal_glue_core.common.enums import ScalarType
from amsdal_glue_core.common.enums import Version
from amsdal_glue_core.common.operations.mutations.schema import RegisterSchema
from amsdal_glue_core.common.operations.mutations.schema import UpdateProperty

from amsdal_glue_connections._sql_core import SqlGenerator
from amsdal_glue_connections.sql.connections.postgres_connection.sync_connection import _PG_TYPE_MAP
from amsdal_glue_connections.sql.connections.postgres_connection.sync_connection import _pg_type_to_field_type

_gen = SqlGenerator('postgresql', param_style='format')


def test_pg_bare_decimal_falls_back_to_numeric() -> None:
    # Old: pg_value_type_transform(Decimal) == 'NUMERIC'.
    # Re-pointed: the type-map entry for 'numeric' resolves to ScalarType.NUMERIC.
    assert _PG_TYPE_MAP['numeric'] == ScalarType.NUMERIC


def test_pg_decimal_schema_model_to_numeric() -> None:
    # Old: PostgresConnection()._to_sql_type(DecimalSchemaModel(precision=10, scale=2)) == 'NUMERIC(10, 2)'.
    # Re-pointed: CustomType(name='NUMERIC', params={...}) compiles to NUMERIC(10, 2) in DDL.
    schema_p = Schema(
        name='t',
        version=Version.LATEST,
        properties=[PropertySchema(name='col', type=CustomType(name='NUMERIC', params={'precision': 10, 'scale': 2}), required=False)],
    )
    [(ddl, _)] = _gen.compile_schema_mutation(RegisterSchema(schema_ref=SchemaReference(name='t', version=Version.LATEST), schema=schema_p))
    assert 'NUMERIC(10, 2)' in ddl

    # Old: DecimalSchemaModel(precision=None, scale=None) → 'NUMERIC'.
    # Re-pointed: ScalarType.NUMERIC compiles to 'numeric'.
    schema_n = Schema(
        name='t',
        version=Version.LATEST,
        properties=[PropertySchema(name='col', type=ScalarType.NUMERIC, required=False)],
    )
    [(ddl_n, _)] = _gen.compile_schema_mutation(RegisterSchema(schema_ref=SchemaReference(name='t', version=Version.LATEST), schema=schema_n))
    assert 'numeric' in ddl_n.lower()


def test_pg_numeric_introspects_to_decimal_schema_model() -> None:
    # Old: PostgresConnection()._to_python_type('NUMERIC', None, {'typmod': ...})
    #      returned DecimalSchemaModel(precision=10, scale=2).
    # Re-pointed: _pg_type_to_field_type('numeric') returns ScalarType.NUMERIC.
    # SUSPICIOUS: precision/scale are no longer extracted from typmod — the introspection
    # path that decoded ((precision << 16) | scale) + 4 has been removed with _to_python_type.
    result = _pg_type_to_field_type('numeric')
    assert result == ScalarType.NUMERIC


def test_pg_double_precision_still_float() -> None:
    # Old: PostgresConnection()._to_python_type('DOUBLE PRECISION', None, {}) is float.
    # Re-pointed: _pg_type_to_field_type maps 'double precision' → ScalarType.DOUBLE.
    assert _pg_type_to_field_type('double precision') == ScalarType.DOUBLE


def test_pg_build_column_update_numeric_uses_cast() -> None:
    # Old: PostgresConnection()._build_column_update(PropertySchema(name='amount', type=DecimalSchemaModel(10, 2)))
    #      emitted a single SQL string with 'TYPE NUMERIC(10, 2)' and 'USING "amount"::NUMERIC(10, 2)'.
    # Re-pointed: compile_schema_mutation(UpdateProperty(...)) returns a list of statements.
    stmts = _gen.compile_schema_mutation(
        UpdateProperty(
            schema_ref=SchemaReference(name='test', version=Version.LATEST),
            property=PropertySchema(
                name='amount',
                type=CustomType(name='NUMERIC', params={'precision': 10, 'scale': 2}),
                required=True,
            ),
        )
    )

    alter_sql = stmts[0][0]
    assert 'SET DATA TYPE NUMERIC(10, 2)' in alter_sql
    # SUSPICIOUS: old builder emitted 'USING "amount"::NUMERIC(10, 2)' for the explicit cast.
    # Rust generator emits SET DATA TYPE without a USING clause — existing rows are cast
    # implicitly by Postgres.  This may fail if the existing column type is incompatible
    # (e.g. text → numeric).
    assert 'USING' not in alter_sql
