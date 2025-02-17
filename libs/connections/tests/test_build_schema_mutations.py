from amsdal_glue_core.common.data_models.constraints import PrimaryKeyConstraint
from amsdal_glue_core.common.data_models.indexes import IndexSchema
from amsdal_glue_core.common.data_models.schema import PropertySchema
from amsdal_glue_core.common.data_models.schema import Schema
from amsdal_glue_core.common.enums import Version
from amsdal_glue_core.common.operations.mutations.schema import RegisterSchema

from amsdal_glue_connections.sql.connections.sqlite_connection import get_sqlite_transform
from amsdal_glue_connections.sql.connections.sqlite_connection import SqliteConnection
from amsdal_glue_connections.sql.sql_builders.schema_builder import build_schema_mutation


def test_build_schema_mutation__register_schema() -> None:
    stmts = build_schema_mutation(
        RegisterSchema(
            schema=Schema(
                name='Person',
                version=Version.LATEST,
                properties=[
                    PropertySchema(name='id', type=int, required=True),
                    PropertySchema(name='name', type=str, required=True),
                    PropertySchema(name='age', type=int, required=False, default=18),
                ],
                constraints=[
                    PrimaryKeyConstraint(name='pk_person', fields=['id']),
                ],
                indexes=[
                    IndexSchema(name='idx_person_name', fields=['name']),
                ],
            ),
        ),
        type_transform=SqliteConnection.to_sql_type,
        transform=get_sqlite_transform(),
    )

    assert stmts == [
        (
            "CREATE TABLE 'Person' ("
            "'id' INTEGER NOT NULL, "
            "'name' TEXT NOT NULL, "
            "'age' INTEGER, "
            "CONSTRAINT 'pk_person' PRIMARY KEY ('id')"
            ')',
            [],
        ),
        ("CREATE INDEX 'idx_person_name' ON 'Person' ('name')", []),
    ]


def test_build_schema_mutation_with_namespace__register_schema() -> None:
    stmts = build_schema_mutation(
        RegisterSchema(
            schema=Schema(
                name='Person',
                namespace='ns1',
                version=Version.LATEST,
                properties=[
                    PropertySchema(name='id', type=int, required=True),
                    PropertySchema(name='name', type=str, required=True),
                    PropertySchema(name='age', type=int, required=False, default=18),
                ],
                constraints=[
                    PrimaryKeyConstraint(name='pk_person', fields=['id']),
                ],
                indexes=[
                    IndexSchema(name='idx_person_name', fields=['name']),
                ],
            ),
        ),
        type_transform=SqliteConnection.to_sql_type,
        transform=get_sqlite_transform(),
    )

    assert stmts == [
        (
            "CREATE TABLE 'ns1'.'Person' ("
            "'id' INTEGER NOT NULL, "
            "'name' TEXT NOT NULL, "
            "'age' INTEGER, "
            "CONSTRAINT 'pk_person' PRIMARY KEY ('id')"
            ')',
            [],
        ),
        ("CREATE INDEX 'ns1'.'idx_person_name' ON 'ns1'.'Person' ('name')", []),
    ]
