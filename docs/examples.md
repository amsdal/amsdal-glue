---
title: Examples - AMSDAL Glue
description: AMSDAL Glue example code for for querying data and schemas as well as running data and schema commands
amsdal_docs:
  target: glue/examples.md
  nav_title: Queries & Commands
  nav_section: Glue (ETL)
  nav_order: 3
---

# AMSDAL Glue examples

## Querying data

The initiation of data querying is predicated on the definition of a query using the
[QueryStatement](https://github.com/amsdal/amsdal-glue/blob/main/libs/core/src/amsdal_glue_core/common/data_models/query.py#L17).

Then you need to build [DataQueryOperation](https://github.com/amsdal/amsdal-glue/blob/main/libs/core/src/amsdal_glue_core/common/operations/queries.py#L19) and put
it to corresponding service:

=== "Sync"

    ```python
    from amsdal_glue import Container
    from amsdal_glue import QueryStatement, DataQueryOperation
    from amsdal_glue.interfaces import DataQueryService

    query = QueryStatement(...)
    operation = DataQueryOperation(
        query=query,
    )
    service = Container.services.get(DataQueryService)
    data_result = service.execute(query_op=operation)
    ```

=== "Async"

    ```python
    from amsdal_glue import Container
    from amsdal_glue import QueryStatement, DataQueryOperation
    from amsdal_glue.interfaces import AsyncDataQueryService

    query = QueryStatement(...)
    operation = DataQueryOperation(
        query=query,
    )
    service = Container.services.get(AsyncDataQueryService)
    data_result = await service.execute(query_op=operation)
    ```

The simplest `SELECT * FROM table` query can be defined as follows:

```python
from amsdal_glue import QueryStatement, SchemaReference, Version

query = QueryStatement(
    table=SchemaReference(name='table', version=Version.LATEST),
)
```

The next SQL query is a bit more complex, as it includes a `WHERE` clause:

`SELECT name, 2024 AS year FROM table WHERE age > 18`

```python
from amsdal_glue import QueryStatement, SchemaReference, Version
from amsdal_glue import AnnotationQuery, ValueAnnotation, FieldReference, Field
from amsdal_glue import Conditions, Condition, FieldLookup, Value

query = QueryStatement(
    only=[FieldReference(field=Field(name='name'), table_name='table')],
    table=SchemaReference(name='table', version=Version.LATEST),
    annotations=[
        AnnotationQuery(value=ValueAnnotation(value=Value(2024), alias='year')),
    ],
    where=Conditions(
        Condition(
            field=FieldReference(field=Field(name='age'), table_name='table'),
            lookup=FieldLookup.GT,
            value=Value(18),
        ),
    ),
)
```

Here is an example of a query that includes a `JOIN` clause:

`SELECT t1.name, t2.age FROM table1 t1 JOIN table2 t2 ON t1.id = t2.id`

```python
from amsdal_glue import QueryStatement, SchemaReference, Version
from amsdal_glue import JoinQuery, FieldReference, Field
from amsdal_glue import Conditions, Condition, FieldLookup


query = QueryStatement(
    only=[
        FieldReference(field=Field(name='name'), table_name='t1'),
        FieldReference(field=Field(name='age'), table_name='t2'),
    ],
    table=SchemaReference(name='table', version=Version.LATEST, alias='t1'),
    joins=[
        JoinQuery(
            table=SchemaReference(name='table2', version=Version.LATEST, alias='t2'),
            on=Conditions(
                Condition(
                    field=FieldReference(field=Field(name='id'), table_name='t1'),
                    lookup=FieldLookup.EQ,
                    value=FieldReference(field=Field(name='id'), table_name='t2'),
                ),
            ),
        ),
    ],
)
```

The subquery can be defined as follows:

`SELECT t1.name, (SELECT COUNT(id) FROM books) as books_num FROM (SELECT * FROM table) AS t1`

```python
from amsdal_glue import QueryStatement, SchemaReference, SubQueryStatement, Version
from amsdal_glue import AnnotationQuery, AggregationQuery, FieldReference, Field, Count


query = QueryStatement(
    only=[
        FieldReference(field=Field(name='name'), table_name='t1'),
    ],
    table=SubQueryStatement(
        query=QueryStatement(
            table=SchemaReference(name='table', version=Version.LATEST),
        ),
        alias='t1'
    ),
    annotations=[
        AnnotationQuery(
            value=SubQueryStatement(
                query=QueryStatement(
                    aggregations=[
                        AggregationQuery(
                            expression=Count(
                                field=FieldReference(field=Field(name='id'), table_name='books'),
                            ),
                            alias='books_num',
                        ),
                    ],
                    table=SchemaReference(name='books', version=Version.LATEST),
                ),
                alias='books_num',
            ),
        ),
    ],
)
```

## Running Data Mutation Commands

The DataCommand class is used to execute data mutation operations in the AMSDAL Glue project, such as inserting,
updating, and deleting data.

In order to run a data mutation command, you need to define a mutation operation using one of
[DataMutation](https://github.com/amsdal/amsdal-glue/blob/main/libs/core/src/amsdal_glue_core/common/operations/mutations/data.py#L14) subclasses and put it to the
corresponding service:

=== "Sync"

    ```python
    from amsdal_glue import Container
    from amsdal_glue import DataCommand, DataResult
    from amsdal_glue.interfaces import DataCommandService


    data_mutation = ...  # Initialize the mutation object
    command = DataCommand(
        mutations=[
            data_mutation,
            ...  # You can pass in multiple mutations in this list
        ],
    )
    service = Container.services.get(DataCommandService)
    data_result: DataResult = service.execute(command=command)
    ```

=== "Async"

    ```python
    from amsdal_glue import Container
    from amsdal_glue import DataCommand, DataResult
    from amsdal_glue.interfaces import AsyncDataCommandService


    data_mutation = ...  # Initialize the mutation object
    command = DataCommand(
        mutations=[
            data_mutation,
            ...  # You can pass in multiple mutations in this list
        ],
    )
    service = Container.services.get(AsyncDataCommandService)
    data_result: DataResult = await service.execute(command=command)
    ```

Here is an example of inserting data into a table:

```python
from amsdal_glue import SchemaReference, Version
from amsdal_glue import InsertData, Data

mutation = InsertData(
    schema=SchemaReference(name='table', version=Version.LATEST),
    data=[
        Data(
            data={
                'name': 'John Doe',
                'age': 30,
            },
        ),
        Data(
            data={
                'name': 'Jane Doe',
                'age': 25,
            },
        ),
    ],
)
```

The SQL equivalent of the above command can be represented as:

```sql
INSERT INTO table (name, age)
VALUES ('John Doe', 30),
       ('Jane Doe', 25);
```

Here is an example of updating data in a table:

```python
from amsdal_glue import SchemaReference, Version
from amsdal_glue import Conditions, Condition, FieldReference, Field, FieldLookup, Value
from amsdal_glue import UpdateData, Data

mutation = UpdateData(
    schema=SchemaReference(name='table', version=Version.LATEST),
    data=Data(
        data={
            'age': 35,
        },
    ),
    query=Conditions(
        Condition(
            field=FieldReference(field=Field(name='name'), table_name='table'),
            lookup=FieldLookup.EQ,
            value=Value('John Doe'),
        ),
    ),
)
```

The SQL equivalent of the above command can be represented as:

```sql
UPDATE table
SET age = 35
WHERE name = 'John Doe';
```

Here is an example of deleting data from a table:

```python
from amsdal_glue import SchemaReference, Version
from amsdal_glue import Conditions, Condition, FieldReference, Field, FieldLookup, Value
from amsdal_glue import DeleteData


mutation = DeleteData(
    schema=SchemaReference(name='table', version=Version.LATEST),
    query=Conditions(
        Condition(
            field=FieldReference(field=Field(name='name'), table_name='table'),
            lookup=FieldLookup.EQ,
            value=Value('John Doe'),
        ),
    ),
)
```

The SQL equivalent of the above command can be represented as:

```sql
DELETE
FROM table
WHERE name = 'John Doe';
```

## Query schemas

In order to fetch available schemas, you need to define a schema query operation using the
[SchemaQueryOperation](https://github.com/amsdal/amsdal-glue/blob/main/libs/core/src/amsdal_glue_core/common/operations/queries.py#L14)
and put it to the corresponding service:

```python
from amsdal_glue import Container, SchemaQueryOperation
from amsdal_glue.interfaces import SchemaQueryService

operation = SchemaQueryOperation(filters=None)
service = Container.services.get(SchemaQueryService)
schemas_result = service.execute(query_op=operation)
```

You can specify filters to filter schemas by name:

```python
from amsdal_glue import SchemaQueryOperation
from amsdal_glue import Conditions, Condition, FieldReference, Field, FieldLookup, Value


# the operation to get all schemas that start with 'user'
operation = SchemaQueryOperation(
    filters=Conditions(
        Condition(
            field=FieldReference(field=Field(name='name'), table_name=''),
            lookup=FieldLookup.STARTSWITH,
            value=Value('user'),
        )
    ),
)
```

## Running Schema Mutation Commands

The SchemaCommand class is used to execute schema mutation operations in the AMSDAL Glue project. It is a part of the
command pattern used in the project, where each command represents an operation to be performed.

Here's an example of how to use SchemaCommand to run schema mutation commands:

=== "Sync"

    ```python
    from amsdal_glue import Container, SchemaCommand
    from amsdal_glue import SchemaResult, SchemaMutation
    from amsdal_glue.interfaces import SchemaCommandService


    mutation: SchemaMutation = ...  # Initialize the mutation object

    command = SchemaCommand(
        mutations=[mutation]  # You can pass in multiple mutations in this list
    )
    service = Container.services.get(SchemaCommandService)
    schema_result: SchemaResult = service.execute(command=command)
    ```

=== "Async"

    ```python
    from amsdal_glue import Container, SchemaCommand
    from amsdal_glue import SchemaResult, SchemaMutation
    from amsdal_glue.interfaces import AsyncSchemaCommandService


    mutation: SchemaMutation = ...  # Initialize the mutation object

    command = SchemaCommand(
        mutations=[mutation]  # You can pass in multiple mutations in this list
    )
    service = Container.services.get(AsyncSchemaCommandService)
    schema_result: SchemaResult = await service.execute(command=command)
    ```

Here is an example of creating a new schema:

```python
from amsdal_glue import RegisterSchema
from amsdal_glue import PrimaryKeyConstraint, IndexSchema, Schema, PropertySchema, Version


mutation = RegisterSchema(
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
)
```

The SQL equivalent of the above command can be represented as:

```sql
CREATE TABLE Person
(
    id    INT,
    name  VARCHAR(255) NOT NULL,
    age   INT DEFAULT 18,
    PRIMARY KEY (id),
    INDEX idx_person_name (name)
);
```

Here is an example of renaming an existing schema:

```python
from amsdal_glue import RenameSchema, SchemaReference, Version

mutation = RenameSchema(
    schema_reference=SchemaReference(name='OldUser', version=Version.LATEST),
    new_schema_name='User',
)
```

The SQL equivalent of the above command can be represented as:

```sql
ALTER TABLE OldUser RENAME TO User;
```

Here is an example of adding a new property to an existing schema:

```python
from amsdal_glue import AddProperty, SchemaReference, PropertySchema, Version


mutation = AddProperty(
    schema_reference=SchemaReference(name='User', version=Version.LATEST),
    property=PropertySchema(name='email', type=str, required=True),
)
```

The SQL equivalent of the above command can be represented as:

```sql
ALTER TABLE User
    ADD COLUMN email VARCHAR(255) NOT NULL;
```

Here is an example of renaming an existing property in a schema:

```python
from amsdal_glue import RenameProperty, SchemaReference, Version


mutation = RenameProperty(
    schema_reference=SchemaReference(name='User', version=Version.LATEST),
    old_name='email',
    new_name='email_address',
)
```

The SQL equivalent of the above command can be represented as:

```sql
ALTER TABLE User
    RENAME COLUMN email TO email_address;
```

Here is an example of removing an existing property from a schema:

```python
from amsdal_glue import DeleteProperty, SchemaReference, Version


mutation = DeleteProperty(
    schema_reference=SchemaReference(name='User', version=Version.LATEST),
    property_name='email_address',
)
```

The SQL equivalent of the above command can be represented as:

```sql
ALTER TABLE User
DROP
COLUMN email_address;
```

Here is an example of adding a new constraint to an existing schema:

```python
from amsdal_glue import AddConstraint, SchemaReference, Version, UniqueConstraint


mutation = AddConstraint(
    schema_reference=SchemaReference(name='User', version=Version.LATEST),
    constraint=UniqueConstraint(name='uk_user_email', fields=['email']),
)
```

The SQL equivalent of the above command can be represented as:

```sql
ALTER TABLE User
    ADD CONSTRAINT uk_user_email UNIQUE (email);
```

Here is an example of removing an existing constraint from a schema:

```python
from amsdal_glue import DeleteConstraint, SchemaReference, Version


mutation = DeleteConstraint(
    schema_reference=SchemaReference(name='User', version=Version.LATEST),
    constraint_name='uk_user_email',
)
```

The SQL equivalent of the above command can be represented as:

```sql
ALTER TABLE User
DROP
CONSTRAINT uk_user_email;
```

Here is an example of adding a new index to an existing schema:

```python
from amsdal_glue import AddIndex, SchemaReference, Version, IndexSchema


mutation = AddIndex(
    schema_reference=SchemaReference(name='User', version=Version.LATEST),
    index=IndexSchema(name='idx_user_email', fields=['email']),
)
```

The SQL equivalent of the above command can be represented as:

```sql
CREATE INDEX idx_user_email
    ON User (email);
```

Here is an example of removing an existing index from a schema:

```python
from amsdal_glue import DeleteIndex, SchemaReference, Version

mutation = DeleteIndex(
    schema_reference=SchemaReference(name='User', version=Version.LATEST),
    index_name='idx_user_email',
)
```

The SQL equivalent of the above command can be represented as:

```sql
DROP INDEX idx_user_email;
```