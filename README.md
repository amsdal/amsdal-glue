# AMSDAL Glue project

This repository contains the AMSDAL Glue project's python packages, a Python interface providing high-level abstraction
for interacting with multiple databases simultaneously, simplifying the development and maintenance process.

[![PyPI - Version](https://img.shields.io/pypi/v/amsdal-glue.svg)](https://pypi.org/project/amsdal-glue)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/amsdal-glue.svg)](https://pypi.org/project/amsdal-glue)

-----

## Table of Contents

- [Introduction](#introduction)
- [Installation](#installation)
- [Usage](#usage)
- [Roadmap](#roadmap)
- [Contributing](docs/contributing.md)
- [License](#license)

## Introduction

The AMSDAL Glue project is a Python interface that provides a high-level abstraction for interacting with multiple
databases or any other data sources simultaneously. It is designed to simplify the development and maintenance process
of database-related tasks in Python applications.

The project aims to solve several challenges:

1. **Database Interactions**: It provides a unified way to interact with different types of databases, abstracting the
   specifics of each database type and allowing developers to focus on their application logic.

2. **Simultaneous Connections**: It enables applications to connect to multiple databases simultaneously, which can be
   crucial for applications that need to work with data stored in different databases.

3. **Simplified Development**: By providing a high-level interface, it simplifies the process of writing and maintaining
   database-related code. This can lead to increased productivity and reduced chances of errors.

4. **Maintenance**: It simplifies the maintenance process by providing a consistent interface for database interactions,
   making it easier to update or replace database systems without significant changes to the application code.

In summary, the AMSDAL Glue project is a tool designed to make working with databases in Python applications easier and
more efficient. It is particularly useful for applications that need to interact with multiple databases or those that
require a high level of abstraction for their database interactions.

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

The AMSDAL Glue project provides a high-level interface for interacting with databases in Python applications. Here is a
simple example of how to use the `amsdal-glue` package to connect to a SQLite database and execute a query:

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
For more examples and detailed documentation, please refer to the [Examples](docs/examples.md) section.

## Roadmap

The AMSDAL Glue project is under active development, and we have plans to add more features and improvements in the
future. Some of the planned features include:

- Support for more database types:
    - ✅SQLite
    - ✅PostgreSQL
    - ⬜MySQL
    - ⬜MongoDB
    - ⬜Iceberg support
- Implement SQL to AMSDAL Glue query & command translator to have an ability to integrate with any existing SQL ORM
  library
- Add support for more complex queries and commands

## License

This project is licensed under the Apache License, Version 2.0 - see the [LICENSE](LICENSE.txt) file for details.

