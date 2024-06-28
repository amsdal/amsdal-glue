# AMSDAL Glue examples

## Querying data

The initiation of data querying is predicated on the definition of a query using the
[QueryStatement](../libs/core/src/amsdal_glue_core/common/data_models/query.py#L17).

Then you need to build [DataQueryOperation](../libs/core/src/amsdal_glue_core/common/operations/queries.py#L19) and put
it to corresponding service:

```python
from amsdal_glue_core.common.data_models.query import QueryStatement
from amsdal_glue_core.common.operations.queries import DataQueryOperation
from amsdal_glue_core.common.services.queries import DataQueryService
from amsdal_glue_core.containers import Container

query = QueryStatement(...)
operation = DataQueryOperation(
    query=query,
)
service = Container.services.get(DataQueryService)
data_result = service.execute(query_op=operation)
```

The simplest `SELECT * FROM table` query can be defined as follows:

```python
from amsdal_glue_core.common.data_models.query import QueryStatement
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.enums import Version

query = QueryStatement(
    table=SchemaReference(name='table', version=Version.LATEST),
)
```

The next SQL query is a bit more complex, as it includes a `WHERE` clause:

`SELECT name, 2024 AS year FROM table WHERE age > 18`

```python
from amsdal_glue_core.common.data_models.annotation import AnnotationQuery
from amsdal_glue_core.common.data_models.annotation import ValueAnnotation
from amsdal_glue_core.common.data_models.conditions import Condition
from amsdal_glue_core.common.data_models.conditions import Conditions
from amsdal_glue_core.common.data_models.field_reference import Field
from amsdal_glue_core.common.data_models.field_reference import FieldReference
from amsdal_glue_core.common.data_models.query import QueryStatement
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.enums import FieldLookup
from amsdal_glue_core.common.enums import Version
from amsdal_glue_core.common.expressions.value import Value

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
from amsdal_glue_core.common.data_models.conditions import Condition
from amsdal_glue_core.common.data_models.conditions import Conditions
from amsdal_glue_core.common.data_models.field_reference import Field
from amsdal_glue_core.common.data_models.field_reference import FieldReference
from amsdal_glue_core.common.data_models.join import JoinQuery
from amsdal_glue_core.common.data_models.query import QueryStatement
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.enums import FieldLookup
from amsdal_glue_core.common.enums import Version

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
from amsdal_glue_core.common.data_models.aggregation import AggregationQuery
from amsdal_glue_core.common.data_models.annotation import AnnotationQuery
from amsdal_glue_core.common.data_models.field_reference import Field
from amsdal_glue_core.common.data_models.field_reference import FieldReference
from amsdal_glue_core.common.data_models.query import QueryStatement
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.data_models.sub_query import SubQueryStatement
from amsdal_glue_core.common.enums import Version
from amsdal_glue_core.common.expressions.aggregation import Count

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

## Query schemas

In order to fetch available schemas, you need to define a schema query operation using the
[SchemaQueryOperation](../libs/core/src/amsdal_glue_core/common/operations/queries.py#L14)
and put it to the corresponding service:

```python
from amsdal_glue_core.common.operations.queries import SchemaQueryOperation
from amsdal_glue_core.common.services.queries import SchemaQueryService
from amsdal_glue_core.containers import Container

operation = SchemaQueryOperation(filters=None)
service = Container.services.get(SchemaQueryService)
schemas_result = service.execute(query_op=operation)
```

You can specify filters to filter schemas by name:

```python
from amsdal_glue_core.common.data_models.conditions import Condition
from amsdal_glue_core.common.data_models.conditions import Conditions
from amsdal_glue_core.common.data_models.field_reference import Field
from amsdal_glue_core.common.data_models.field_reference import FieldReference
from amsdal_glue_core.common.enums import FieldLookup
from amsdal_glue_core.common.expressions.value import Value
from amsdal_glue_core.common.operations.queries import SchemaQueryOperation

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

```python
from amsdal_glue_core.common.data_models.results.schema import SchemaResult
from amsdal_glue_core.common.operations.commands import SchemaCommand
from amsdal_glue_core.common.operations.mutations.schema import SchemaMutation
from amsdal_glue_core.common.services.commands import SchemaCommandService
from amsdal_glue_core.containers import Container

mutation = SchemaMutation(
    # Fill in the necessary parameters here
)

command = SchemaCommand(
    mutations=[mutation]  # You can pass in multiple mutations in this list
)
service = Container.services.get(SchemaCommandService)
schema_result: SchemaResult = service.execute(command=command)
```

