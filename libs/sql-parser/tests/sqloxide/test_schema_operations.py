from datetime import datetime

from amsdal_glue_core.common.data_models.conditions import Condition
from amsdal_glue_core.common.data_models.conditions import Conditions
from amsdal_glue_core.common.data_models.constraints import CheckConstraint
from amsdal_glue_core.common.data_models.constraints import ForeignKeySchema
from amsdal_glue_core.common.data_models.constraints import PrimaryKeyConstraint
from amsdal_glue_core.common.data_models.constraints import UniqueConstraint
from amsdal_glue_core.common.data_models.field_reference import Field
from amsdal_glue_core.common.data_models.field_reference import FieldReference
from amsdal_glue_core.common.data_models.indexes import IndexSchema
from amsdal_glue_core.common.data_models.schema import PropertySchema
from amsdal_glue_core.common.data_models.schema import Schema
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.enums import FieldLookup
from amsdal_glue_core.common.enums import Version
from amsdal_glue_core.common.expressions.value import Value
from amsdal_glue_core.common.operations.mutations.schema import AddConstraint
from amsdal_glue_core.common.operations.mutations.schema import AddIndex
from amsdal_glue_core.common.operations.mutations.schema import AddProperty
from amsdal_glue_core.common.operations.mutations.schema import DeleteConstraint
from amsdal_glue_core.common.operations.mutations.schema import DeleteProperty
from amsdal_glue_core.common.operations.mutations.schema import DeleteSchema
from amsdal_glue_core.common.operations.mutations.schema import RegisterSchema
from amsdal_glue_core.common.operations.mutations.schema import RenameProperty
from amsdal_glue_core.common.operations.mutations.schema import RenameSchema
from amsdal_glue_core.common.operations.queries import SchemaQueryOperation
from amsdal_glue_core.containers import Container
from amsdal_glue_sql_parser.parsers.base import SqlParserBase


def test_simple_create_table_command() -> None:
    parser = Container.services.get(SqlParserBase)
    assert parser.parse_sql(
        'CREATE TABLE users '
        '(id INTEGER, name TEXT, age INT, created_at TIMESTAMP, '
        '"_metadata" JSON, is_active BOOLEAN, height REAL)'
    ) == [
        RegisterSchema(
            schema=Schema(
                name='users',
                version=Version.LATEST,
                properties=[
                    PropertySchema(name='id', type=int, required=False, description=None, default=None),
                    PropertySchema(name='name', type=str, required=False, description=None, default=None),
                    PropertySchema(name='age', type=int, required=False, description=None, default=None),
                    PropertySchema(name='created_at', type=datetime, required=False, description=None, default=None),
                    PropertySchema(name='_metadata', type=dict, required=False, description=None, default=None),
                    PropertySchema(name='is_active', type=bool, required=False, description=None, default=None),
                    PropertySchema(name='height', type=float, required=False, description=None, default=None),
                ],
            ),
        )
    ]


def test_simple_create_table_primary_key() -> None:
    parser = Container.services.get(SqlParserBase)
    assert parser.parse_sql(
        'CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT UNIQUE NOT NULL, full_name VARCHAR(123) NOT NULL)'
    ) == [
        RegisterSchema(
            schema=Schema(
                name='users',
                version=Version.LATEST,
                properties=[
                    PropertySchema(name='id', type=int, required=True, description=None, default=None),
                    PropertySchema(name='username', type=str, required=True, description=None, default=None),
                    PropertySchema(name='full_name', type=str, required=True, description=None, default=None),
                ],
                constraints=[
                    PrimaryKeyConstraint(name='id', fields=['id']),
                    UniqueConstraint(name='username', fields=['username']),
                ],
            ),
        )
    ]


def test_simple_create_table_explicit_constraints() -> None:
    parser = Container.services.get(SqlParserBase)
    assert parser.parse_sql(
        'CREATE TABLE users ('
        'id INTEGER, '
        'username TEXT, '
        'full_name VARCHAR(123), '
        'PRIMARY KEY (id), '
        'UNIQUE (username), '
        'CHECK (id > 0), '
        'FOREIGN KEY (username) REFERENCES other_table (other_field)'
        ')'
    ) == [
        RegisterSchema(
            schema=Schema(
                name='users',
                version=Version.LATEST,
                properties=[
                    PropertySchema(name='id', type=int, required=False, description=None, default=None),
                    PropertySchema(name='username', type=str, required=False, description=None, default=None),
                    PropertySchema(name='full_name', type=str, required=False, description=None, default=None),
                ],
                constraints=[
                    PrimaryKeyConstraint(name='', fields=['id']),
                    UniqueConstraint(name='', fields=['username']),
                    CheckConstraint(
                        name='',
                        condition=Conditions(
                            Condition(
                                field=FieldReference(field=Field(name='id'), table_name='users'),
                                lookup=FieldLookup.GT,
                                value=Value('0'),
                            )
                        ),
                    ),
                    ForeignKeySchema(
                        name='',
                        fields=['username'],
                        reference_schema=SchemaReference(name='other_table', version=Version.LATEST),
                        reference_fields=['other_field'],
                    ),
                ],
            ),
        )
    ]


def test_simple_create_table_explicit_named_constraints() -> None:
    parser = Container.services.get(SqlParserBase)
    assert parser.parse_sql(
        'CREATE TABLE users ('
        'id INTEGER, '
        'username TEXT, '
        'full_name VARCHAR(123), '
        'CONSTRAINT id_pk PRIMARY KEY (id), '
        'CONSTRAINT username_unique UNIQUE (username), '
        'CONSTRAINT check_id CHECK (id > 0), '
        'CONSTRAINT username_fk FOREIGN KEY (username) REFERENCES other_table (other_field)'
        ')'
    ) == [
        RegisterSchema(
            schema=Schema(
                name='users',
                version=Version.LATEST,
                properties=[
                    PropertySchema(name='id', type=int, required=False, description=None, default=None),
                    PropertySchema(name='username', type=str, required=False, description=None, default=None),
                    PropertySchema(name='full_name', type=str, required=False, description=None, default=None),
                ],
                constraints=[
                    PrimaryKeyConstraint(name='id_pk', fields=['id']),
                    UniqueConstraint(name='username_unique', fields=['username']),
                    CheckConstraint(
                        name='check_id',
                        condition=Conditions(
                            Condition(
                                field=FieldReference(field=Field(name='id'), table_name='users'),
                                lookup=FieldLookup.GT,
                                value=Value('0'),
                            )
                        ),
                    ),
                    ForeignKeySchema(
                        name='username_fk',
                        fields=['username'],
                        reference_schema=SchemaReference(name='other_table', version=Version.LATEST),
                        reference_fields=['other_field'],
                    ),
                ],
            ),
        )
    ]


def test_create_index() -> None:
    parser = Container.services.get(SqlParserBase)
    assert parser.parse_sql('CREATE INDEX idx_name ON users (name)') == [
        AddIndex(
            schema_reference=SchemaReference(name='users', version=Version.LATEST),
            index=IndexSchema(name='idx_name', fields=['name']),
        )
    ]


def test_create_index_multi_column() -> None:
    parser = Container.services.get(SqlParserBase)
    assert parser.parse_sql('CREATE UNIQUE INDEX idx_name ON users (name, username)') == [
        AddIndex(
            schema_reference=SchemaReference(name='users', version=Version.LATEST),
            index=IndexSchema(name='idx_name', fields=['name', 'username']),
        )
    ]


def test_update_schema_add_property() -> None:
    parser = Container.services.get(SqlParserBase)
    assert parser.parse_sql('ALTER TABLE users ADD COLUMN age INT') == [
        AddProperty(
            schema_reference=SchemaReference(name='users', version=Version.LATEST),
            property=PropertySchema(name='age', type=int, required=False, description=None, default=None),
        )
    ]


def test_update_schema_drop_property() -> None:
    parser = Container.services.get(SqlParserBase)
    assert parser.parse_sql('ALTER TABLE users DROP COLUMN age') == [
        DeleteProperty(
            schema_reference=SchemaReference(name='users', version=Version.LATEST),
            property_name='age',
        )
    ]


def test_update_schema_rename_property() -> None:
    parser = Container.services.get(SqlParserBase)
    assert parser.parse_sql('ALTER TABLE users RENAME COLUMN age TO years') == [
        RenameProperty(
            schema_reference=SchemaReference(name='users', version=Version.LATEST),
            old_name='age',
            new_name='years',
        )
    ]


def test_update_schema_rename_table() -> None:
    parser = Container.services.get(SqlParserBase)
    assert parser.parse_sql('ALTER TABLE users RENAME TO people') == [
        RenameSchema(
            schema_reference=SchemaReference(name='users', version=Version.LATEST),
            new_schema_name='people',
        )
    ]


def test_delete_schema() -> None:
    parser = Container.services.get(SqlParserBase)
    assert parser.parse_sql('DROP TABLE users') == [
        DeleteSchema(
            schema_reference=SchemaReference(name='users', version=Version.LATEST),
        )
    ]


def test_add_pk_constraint() -> None:
    parser = Container.services.get(SqlParserBase)
    assert parser.parse_sql('ALTER TABLE users ADD CONSTRAINT id_pk PRIMARY KEY (id)') == [
        AddConstraint(
            schema_reference=SchemaReference(name='users', version=Version.LATEST),
            constraint=PrimaryKeyConstraint(name='id_pk', fields=['id']),
        ),
    ]

    assert parser.parse_sql('ALTER TABLE users ADD PRIMARY KEY (id)') == [
        AddConstraint(
            schema_reference=SchemaReference(name='users', version=Version.LATEST),
            constraint=PrimaryKeyConstraint(name='', fields=['id']),
        ),
    ]


def test_delete_constraint() -> None:
    parser = Container.services.get(SqlParserBase)
    assert parser.parse_sql('ALTER TABLE users DROP CONSTRAINT id_pk') == [
        DeleteConstraint(
            schema_reference=SchemaReference(name='users', version=Version.LATEST),
            constraint_name='id_pk',
        ),
    ]


def test_fetch_schemas() -> None:
    parser = Container.services.get(SqlParserBase)
    assert parser.parse_sql('SELECT * FROM amsdal_schema_registry') == [SchemaQueryOperation(filters=None)]
    assert parser.parse_sql("SELECT * FROM amsdal_schema_registry WHERE name = 'users'") == [
        SchemaQueryOperation(
            filters=Conditions(
                Condition(
                    field=FieldReference(field=Field(name='name'), table_name='amsdal_schema_registry'),
                    lookup=FieldLookup.EQ,
                    value=Value('users'),
                )
            ),
        )
    ]
