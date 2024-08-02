# mypy: disable-error-code="type-abstract"
from datetime import datetime

from amsdal_glue_core.common.data_models.conditions import Condition
from amsdal_glue_core.common.data_models.conditions import Conditions
from amsdal_glue_core.common.data_models.constraints import CheckConstraint
from amsdal_glue_core.common.data_models.constraints import ForeignKeyConstraint
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
from amsdal_glue_core.common.operations.base import Operation
from amsdal_glue_core.common.operations.commands import SchemaCommand
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


def test_simple_create_table_command(benchmark) -> None:
    parser = Container.services.get(SqlParserBase)

    def parse_sql() -> list[Operation]:
        return parser.parse_sql(
            'CREATE TABLE users '
            '(id INTEGER, name TEXT, age INT, created_at TIMESTAMP, '
            '"_metadata" JSON, is_active BOOLEAN, height REAL)'
        )

    result = benchmark(parse_sql)

    assert result == [
        SchemaCommand(
            mutations=[
                RegisterSchema(
                    schema=Schema(
                        name='users',
                        version=Version.LATEST,
                        properties=[
                            PropertySchema(name='id', type=int, required=False, description=None, default=None),
                            PropertySchema(name='name', type=str, required=False, description=None, default=None),
                            PropertySchema(name='age', type=int, required=False, description=None, default=None),
                            PropertySchema(
                                name='created_at', type=datetime, required=False, description=None, default=None
                            ),
                            PropertySchema(name='_metadata', type=dict, required=False, description=None, default=None),
                            PropertySchema(name='is_active', type=bool, required=False, description=None, default=None),
                            PropertySchema(name='height', type=float, required=False, description=None, default=None),
                        ],
                    ),
                )
            ]
        )
    ]


def test_simple_create_table_primary_key(benchmark) -> None:
    parser = Container.services.get(SqlParserBase)

    def parse_sql() -> list[Operation]:
        return parser.parse_sql(
            'CREATE TABLE users '
            '(id INTEGER PRIMARY KEY, username TEXT UNIQUE NOT NULL, full_name VARCHAR(123) NOT NULL)'
        )

    result = benchmark(parse_sql)

    assert result == [
        SchemaCommand(
            mutations=[
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
        )
    ]


def test_simple_create_table_explicit_constraints(benchmark) -> None:
    parser = Container.services.get(SqlParserBase)

    def parse_sql() -> list[Operation]:
        return parser.parse_sql(
            'CREATE TABLE users ('
            'id INTEGER, '
            'username TEXT, '
            'full_name VARCHAR(123), '
            'PRIMARY KEY (id), '
            'UNIQUE (username), '
            'CHECK (id > 0), '
            'FOREIGN KEY (username) REFERENCES other_table (other_field)'
            ')'
        )

    result = benchmark(parse_sql)

    assert result == [
        SchemaCommand(
            mutations=[
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
                            ForeignKeyConstraint(
                                name='',
                                fields=['username'],
                                reference_schema=SchemaReference(name='other_table', version=Version.LATEST),
                                reference_fields=['other_field'],
                            ),
                        ],
                    ),
                )
            ]
        )
    ]


def test_simple_create_table_explicit_named_constraints(benchmark) -> None:
    parser = Container.services.get(SqlParserBase)

    def parse_sql() -> list[Operation]:
        return parser.parse_sql(
            'CREATE TABLE users ('
            'id INTEGER, '
            'username TEXT, '
            'full_name VARCHAR(123), '
            'CONSTRAINT id_pk PRIMARY KEY (id), '
            'CONSTRAINT username_unique UNIQUE (username), '
            'CONSTRAINT check_id CHECK (id > 0), '
            'CONSTRAINT username_fk FOREIGN KEY (username) REFERENCES other_table (other_field)'
            ')'
        )

    result = benchmark(parse_sql)

    assert result == [
        SchemaCommand(
            mutations=[
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
                            ForeignKeyConstraint(
                                name='username_fk',
                                fields=['username'],
                                reference_schema=SchemaReference(name='other_table', version=Version.LATEST),
                                reference_fields=['other_field'],
                            ),
                        ],
                    ),
                )
            ]
        )
    ]


def test_create_index(benchmark) -> None:
    parser = Container.services.get(SqlParserBase)

    def parse_sql() -> list[Operation]:
        return parser.parse_sql('CREATE INDEX idx_name ON users (name)')

    result = benchmark(parse_sql)

    assert result == [
        SchemaCommand(
            mutations=[
                AddIndex(
                    schema_reference=SchemaReference(name='users', version=Version.LATEST),
                    index=IndexSchema(name='idx_name', fields=['name']),
                )
            ]
        )
    ]


def test_create_index_multi_column(benchmark) -> None:
    parser = Container.services.get(SqlParserBase)

    def parse_sql() -> list[Operation]:
        return parser.parse_sql('CREATE UNIQUE INDEX idx_name ON users (name, username)')

    result = benchmark(parse_sql)

    assert result == [
        SchemaCommand(
            mutations=[
                AddIndex(
                    schema_reference=SchemaReference(name='users', version=Version.LATEST),
                    index=IndexSchema(name='idx_name', fields=['name', 'username']),
                )
            ]
        )
    ]


def test_update_schema_add_property(benchmark) -> None:
    parser = Container.services.get(SqlParserBase)

    def parse_sql() -> list[Operation]:
        return parser.parse_sql('ALTER TABLE users ADD COLUMN age INT')

    result = benchmark(parse_sql)

    assert result == [
        SchemaCommand(
            mutations=[
                AddProperty(
                    schema_reference=SchemaReference(name='users', version=Version.LATEST),
                    property=PropertySchema(name='age', type=int, required=False, description=None, default=None),
                )
            ]
        )
    ]


def test_update_schema_drop_property(benchmark) -> None:
    parser = Container.services.get(SqlParserBase)

    def parse_sql() -> list[Operation]:
        return parser.parse_sql('ALTER TABLE users DROP COLUMN age')

    result = benchmark(parse_sql)

    assert result == [
        SchemaCommand(
            mutations=[
                DeleteProperty(
                    schema_reference=SchemaReference(name='users', version=Version.LATEST),
                    property_name='age',
                )
            ]
        )
    ]


def test_update_schema_rename_property(benchmark) -> None:
    parser = Container.services.get(SqlParserBase)

    def parse_sql() -> list[Operation]:
        return parser.parse_sql('ALTER TABLE users RENAME COLUMN age TO years')

    result = benchmark(parse_sql)

    assert result == [
        SchemaCommand(
            mutations=[
                RenameProperty(
                    schema_reference=SchemaReference(name='users', version=Version.LATEST),
                    old_name='age',
                    new_name='years',
                )
            ]
        )
    ]


def test_update_schema_rename_table(benchmark) -> None:
    parser = Container.services.get(SqlParserBase)

    def parse_sql() -> list[Operation]:
        return parser.parse_sql('ALTER TABLE users RENAME TO people')

    result = benchmark(parse_sql)

    assert result == [
        SchemaCommand(
            mutations=[
                RenameSchema(
                    schema_reference=SchemaReference(name='users', version=Version.LATEST),
                    new_schema_name='people',
                )
            ]
        )
    ]


def test_delete_schema(benchmark) -> None:
    parser = Container.services.get(SqlParserBase)

    def parse_sql() -> list[Operation]:
        return parser.parse_sql('DROP TABLE users')

    result = benchmark(parse_sql)

    assert result == [
        SchemaCommand(
            mutations=[
                DeleteSchema(
                    schema_reference=SchemaReference(name='users', version=Version.LATEST),
                )
            ]
        )
    ]


def test_add_pk_constraint(benchmark) -> None:
    parser = Container.services.get(SqlParserBase)

    def parse_sql() -> list[Operation]:
        return parser.parse_sql('ALTER TABLE users ADD CONSTRAINT id_pk PRIMARY KEY (id)')

    result = benchmark(parse_sql)

    assert result == [
        SchemaCommand(
            mutations=[
                AddConstraint(
                    schema_reference=SchemaReference(name='users', version=Version.LATEST),
                    constraint=PrimaryKeyConstraint(name='id_pk', fields=['id']),
                )
            ]
        )
    ]

    assert parser.parse_sql('ALTER TABLE users ADD PRIMARY KEY (id)') == [
        SchemaCommand(
            mutations=[
                AddConstraint(
                    schema_reference=SchemaReference(name='users', version=Version.LATEST),
                    constraint=PrimaryKeyConstraint(name='', fields=['id']),
                )
            ]
        )
    ]


def test_delete_constraint(benchmark) -> None:
    parser = Container.services.get(SqlParserBase)

    def parse_sql() -> list[Operation]:
        return parser.parse_sql('ALTER TABLE users DROP CONSTRAINT id_pk')

    result = benchmark(parse_sql)

    assert result == [
        SchemaCommand(
            mutations=[
                DeleteConstraint(
                    schema_reference=SchemaReference(name='users', version=Version.LATEST),
                    constraint_name='id_pk',
                )
            ]
        )
    ]


def test_fetch_schemas(benchmark) -> None:
    parser = Container.services.get(SqlParserBase)

    def parse_sql() -> list[Operation]:
        return parser.parse_sql('SELECT * FROM amsdal_schema_registry')

    result = benchmark(parse_sql)

    assert result == [SchemaQueryOperation(filters=None)]


def test_fetch_schemas_conditions(benchmark) -> None:
    parser = Container.services.get(SqlParserBase)

    def parse_sql() -> list[Operation]:
        return parser.parse_sql("SELECT * FROM amsdal_schema_registry WHERE name = 'users'")

    result = benchmark(parse_sql)

    assert result == [
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
