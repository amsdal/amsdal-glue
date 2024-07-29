# AMSDAL Glue project

AMSDAL Glue is a flexible, lightweight, yet powerful, Python ETL interface designed to separate your analytics, application, or ORM from its data, allowing you to operate on multiple databases or other data stores simultaneously through a common interface, using SQL, Python objects, or custom parser, query and command planners.

[![PyPI - Version](https://img.shields.io/pypi/v/amsdal-glue.svg)](https://pypi.org/project/amsdal-glue)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/amsdal-glue.svg)](https://pypi.org/project/amsdal-glue)

-----

## Table of Contents

- [Introduction](#introduction)
- [Installation](#installation)
- [Usage](#usage)
- [Performance](#performance)
- [Performance](#performance)
- [Roadmap](#roadmap)
- [Contributing](docs/contributing.md)
- [License](#license)

## Introduction

AMSDAL Glue is a simple yet critical data technology that can be utilized in almost all data applications.

In it's most basic sense, AMSDAL Glue provides users a low-level abstraction for their data commands and queries, without limiting the feature-set and funcionality of the underlying database itself. 

This unified, flexible, all-important ETL technology serves as a powerful tool to simplify the development and maintenance process of database-related tasks in Python applications, reducing cost and increasing scalability.
AMSDAL Glue is a simple yet critical data technology that can be utilized in almost all data applications.

In it's most basic sense, AMSDAL Glue provides users a low-level abstraction for their data commands and queries, without limiting the feature-set and funcionality of the underlying database itself. 

This unified, flexible, all-important ETL technology serves as a powerful tool to simplify the development and maintenance process of database-related tasks in Python applications, reducing cost and increasing scalability.

The project aims to solve several challenges:

1. **Data Interactions**: It provides a unified way to interact with all data (SQL, NoSQL, unstructured, integrations, etc) abstracting the
1. **Data Interactions**: It provides a unified way to interact with all data (SQL, NoSQL, unstructured, integrations, etc) abstracting the
   specifics of each database type and allowing developers to focus on their application logic.

2. **Simultaneous Connections**: It enables applications to connect with or integrate to multiple data sources simultaneously, critical in all but the most basic applications, allowing your analytics or application to be agnostic to where it's data is physically located (now or in the future).

3. **Performance**: At it's core [amsdal-glue-core](libs/core/) simply provides you a common interface to interact with data, allowing you to delegate as much of the workload to the underlying database technology as possible. 

In essensce, by detaching your applicaiton from its data, AMSDAL Glue simplifies the process of writing and maintaining database-related code with a minimal sacrifice of flexibility or perfmance. 
2. **Simultaneous Connections**: It enables applications to connect with or integrate to multiple data sources simultaneously, critical in all but the most basic applications, allowing your analytics or application to be agnostic to where it's data is physically located (now or in the future).

3. **Performance**: At it's core [amsdal-glue-core](libs/core/) simply provides you a common interface to interact with data, allowing you to delegate as much of the workload to the underlying database technology as possible. 

In essensce, by detaching your applicaiton from its data, AMSDAL Glue simplifies the process of writing and maintaining database-related code with a minimal sacrifice of flexibility or perfmance. 

For more information, please refer to the [Overview](docs/overview.md).

## Installation

The AMSDAL Glue project consists of three main packages: `amsdal-glue-core`, `amsdal-glue-connections`,
and `amsdal-glue`. You can install each package separately or install the `amsdal-glue` package, which includes all the
dependencies.

You can install the AMSDAL Glue project using `pip`:

```bash
pip install amsdal-glue
```

This command automatically installs `amsdal-glue-core` and `amsdal-glue-connections` packages as dependencies.
Note, the `amsdal-glue-connections` will be installed without extra dependencies.
If you want to use `PostgresConnection` in order to connect to postgres database, you need explicitly install the
`amsdal-glue-connections` with the `postgres` extra dependency:

```bash
pip install amsdal-glue-connections[postgres]
```

## Usage

Here is a simple example of how to use the `amsdal-glue` package to connect to a SQLite database and execute a query:

```python
from amsdal_glue.connections.connection_pool import DefaultConnectionPool
from amsdal_glue.initialize import init_default_containers
from amsdal_glue_connections.sql.connections.sqlite_connection import SqliteConnection
from amsdal_glue_core.common.data_models.field_reference import Field
from amsdal_glue_core.common.data_models.field_reference import FieldReference
from amsdal_glue_core.common.data_models.order_by import OrderByQuery
from amsdal_glue_core.common.data_models.query import QueryStatement
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.enums import OrderDirection
from amsdal_glue_core.common.enums import Version
from amsdal_glue_core.common.operations.queries import DataQueryOperation
from amsdal_glue_core.common.services.managers.connection import ConnectionManager
from amsdal_glue_core.common.services.queries import DataQueryService
from amsdal_glue_core.containers import Container


def main() -> None:
    init_default_containers()

    # Register a connection to a SQLite database
    connection_mng = Container.managers.get(ConnectionManager)
    connection_mng.register_connection_pool(
        DefaultConnectionPool(
            SqliteConnection,
            db_path='customers.sqlite',
            check_same_thread=False,  # The default parallel executor works on top of threads
        ),
    )

    # Build a query
    query = QueryStatement(
        only=[
            FieldReference(field=Field(name='id'), table_name='c'),
            FieldReference(field=Field(name='first_name'), table_name='c'),
        ],
        table=SchemaReference(name='customers', alias='c', version=Version.LATEST),
        order_by=[
            OrderByQuery(
                field=FieldReference(field=Field(name='id'), table_name='c'),
                direction=OrderDirection.ASC,
            ),
        ],
    )

    # Execute the query
    service = Container.services.get(DataQueryService)
    data_result = service.execute(
        query_op=DataQueryOperation(
            query=query,
        ),
    )

    assert data_result.success is True
    assert [item.data for item in data_result.data] == [
        {'id': 1, 'first_name': 'John'},
        {'id': 2, 'first_name': 'Robert'},
        {'id': 3, 'first_name': 'David'},
        {'id': 4, 'first_name': 'John'},
        {'id': 5, 'first_name': 'Betty'},
    ]
```

This example demonstrates how to connect to a SQLite database, build a query, and execute it using the AMSDAL Glue.
For more examples and detailed documentation, please see the [Examples](docs/examples.md) and [Templates](templates/) sections.

## Performance

AMSDAL Glue is designed to be highly performant. At it's core [amsdal-glue-core](libs/core/) is simply an interface, allowing you to delegate as much of the workload to the underlying database technology as possible. 

In practice, AMSDAL Glue comes at relatively little cost as seen in our benchmarking [results](https://amsdal.github.io/amsdal-glue/connections_benchmark/index.html)

You can find more benchmarking results [here](docs/benchmarking.md) 

## Performance

AMSDAL Glue is designed to be highly performant. At it's core [amsdal-glue-core](libs/core/) is simply an interface, allowing you to delegate as much of the workload to the underlying database technology as possible. 

In practice, AMSDAL Glue comes at relatively little cost as seen in our benchmarking [results](https://amsdal.github.io/amsdal-glue/connections_benchmark/index.html)

You can find more benchmarking results [here](docs/benchmarking.md) 

## Roadmap

The AMSDAL Glue project is under active development, and we have plans to add more features and improvements in the
future. Some of the planned features include:

- Support for data transformation/hooks (coming soon)
- Support for more database types:
    - ✅SQLite
    - ✅PostgreSQL
    - ⬜MySQL
    - ⬜MongoDB
    - ⬜Iceberg support
- ✅ SQL to AMSDAL Glue query & command translator to have an ability to integrate with any existing SQL ORM
  library ([sql-parser-usage](templates/sql-parser-usage/README.md))
  library ([sql-parser-usage](templates/sql-parser-usage/README.md))
- Add support for more complex queries and commands

## License

This project is licensed under the Apache License, Version 2.0 - see the [LICENSE](LICENSE.txt) file for details.

