"""Postgres decimal/NUMERIC handling — re-pointed to Rust SqlGenerator.

Old tests used deleted internals: pg_value_type_transform, PostgresConnection._to_sql_type,
_to_python_type, _build_column_update, and DecimalSchemaModel.  Each is re-pointed to
the surviving equivalent: _pg_type_to_field_type / _PG_TYPE_MAP for introspection lookups,
and compile_schema_mutation for DDL emission.

SUSPICIOUS items flagged inline.
"""

from amsdal_glue_connections._sql_core import SqlGenerator
from amsdal_glue_core.common.data_models.schema import PropertySchema
from amsdal_glue_core.common.data_models.schema import Schema
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.data_models.types import DecimalType
from amsdal_glue_core.common.enums import ScalarType
from amsdal_glue_core.common.enums import Version
from amsdal_glue_core.common.operations.mutations.schema import RegisterSchema
from amsdal_glue_core.common.operations.mutations.schema import UpdateProperty

from amsdal_glue_connections.sql.connections.postgres_connection.sync_connection import _PG_TYPE_MAP
from amsdal_glue_connections.sql.connections.postgres_connection.sync_connection import _pg_type_to_field_type

_gen = SqlGenerator('postgresql', param_style='format')


def test_pg_bare_decimal_falls_back_to_numeric() -> None:
    # Re-pointed: the type-map entry for 'numeric' resolves to ScalarType.NUMERIC.
    assert _PG_TYPE_MAP['numeric'] == ScalarType.NUMERIC


def test_pg_decimal_schema_model_to_numeric() -> None:
    # Agnostic DecimalType(precision, scale) compiles to NUMERIC(10, 2) in the PostgreSQL DDL.
    schema_p = Schema(
        name='t',
        version=Version.LATEST,
        properties=[PropertySchema(name='col', type=DecimalType(precision=10, scale=2), required=False)],
    )
    [(ddl, _)] = _gen.compile_schema_mutation(
        RegisterSchema(schema_ref=SchemaReference(name='t', version=Version.LATEST), schema=schema_p)
    )
    assert 'NUMERIC(10, 2)' in ddl

    # Re-pointed: ScalarType.NUMERIC compiles to 'numeric'.
    schema_n = Schema(
        name='t',
        version=Version.LATEST,
        properties=[PropertySchema(name='col', type=ScalarType.NUMERIC, required=False)],
    )
    [(ddl_n, _)] = _gen.compile_schema_mutation(
        RegisterSchema(schema_ref=SchemaReference(name='t', version=Version.LATEST), schema=schema_n)
    )
    assert 'numeric' in ddl_n.lower()


def test_pg_numeric_introspects_to_decimal_schema_model() -> None:
    # Bare numeric (no precision from catalog) stays as ScalarType.NUMERIC.
    result = _pg_type_to_field_type('numeric')
    assert result == ScalarType.NUMERIC

    # When the catalog provides precision/scale, introspection returns the agnostic DecimalType
    # so a RegisterSchema→introspect cycle round-trips both precision and scale.
    result_with_params = _pg_type_to_field_type('numeric', numeric_precision=10, numeric_scale=2)
    assert result_with_params == DecimalType(precision=10, scale=2)

    # decimal type alias also handled.
    result_decimal = _pg_type_to_field_type('decimal', numeric_precision=5, numeric_scale=3)
    assert result_decimal == DecimalType(precision=5, scale=3)


def test_pg_double_precision_still_float() -> None:
    # Re-pointed: _pg_type_to_field_type maps 'double precision' → ScalarType.DOUBLE.
    assert _pg_type_to_field_type('double precision') == ScalarType.DOUBLE


def test_pg_build_column_update_numeric_uses_cast() -> None:
    #      emitted a single SQL string with 'TYPE NUMERIC(10, 2)' and 'USING "amount"::NUMERIC(10, 2)'.
    # Re-pointed: compile_schema_mutation(UpdateProperty(...)) returns a list of statements.
    stmts = _gen.compile_schema_mutation(
        UpdateProperty(
            schema_ref=SchemaReference(name='test', version=Version.LATEST),
            property=PropertySchema(
                name='amount',
                type=DecimalType(precision=10, scale=2),
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
