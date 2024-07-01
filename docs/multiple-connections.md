# Multiple Connections support

The AMSDAL Glue supports multiple connections to the same or different databases. This is useful when you need to
connect to multiple databases in the same application.

## Connection Manager

The AMSDAL Glue uses a connection manager to manage connections. To get the connection manager, you can use the
following code:

```python
from amsdal_glue_core.containers import Container
from amsdal_glue_core.common.services.managers.connection import ConnectionManager

connection_mng = Container.managers.get(ConnectionManager)
```

Using the connection manager, you can register new connections, get existing ones, and close them all.
The connection manager operates with the connection pools.

## Connection pool

The AMSDAL Glue uses a connection pool to manage connections.
Here is an example of how to create a connection pool and register it in the connection manager:

```python
from amsdal_glue.connections.connection_pool import DefaultConnectionPool
from amsdal_glue_connections.sql.connections.sqlite_connection import SqliteConnection
from amsdal_glue_core.containers import Container
from amsdal_glue_core.common.services.managers.connection import ConnectionManager

sql_connection_pool = DefaultConnectionPool(SqliteConnection, db_path='customers.sqlite', check_same_thread=False)

connection_mng = Container.managers.get(ConnectionManager)

# Register the connection pool as default one (not related to any schema)
connection_mng.register_connection_pool(sql_connection_pool)

# Register the connection pool as 'customers' schema
connection_mng.register_connection_pool(sql_connection_pool, 'customers')
```

Now, you can get the connection pool from the connection manager by the schema name:

```python
from amsdal_glue.connections.connection_pool import DefaultConnectionPool
from amsdal_glue_connections.sql.connections.sqlite_connection import SqliteConnection
from amsdal_glue_core.containers import Container
from amsdal_glue_core.common.services.managers.connection import ConnectionManager

sql_connection_pool = DefaultConnectionPool(SqliteConnection, db_path='customers.sqlite', check_same_thread=False)

connection_mng = Container.managers.get(ConnectionManager)

sqlite_connection_pool = connection_mng.get_connection_pool('customers')
```

Note, the ConnectionManager is a singleton, so once you register a connection pool, you can get it from any place in
your application.

## Multiple connections to different databases

You can register multiple connection pools to the same or different databases.
The connection manager will manage them and provide you with the connection pool by the schema name. This is useful when
you need to connect to multiple databases in the same application.

Here is an example of how to register multiple connection pools:

```python
from amsdal_glue.connections.connection_pool import DefaultConnectionPool
from amsdal_glue_connections.sql.connections.sqlite_connection import SqliteConnection
from amsdal_glue_core.containers import Container
from amsdal_glue_core.common.services.managers.connection import ConnectionManager

sql_customers_db = DefaultConnectionPool(SqliteConnection, db_path='customers.sqlite', check_same_thread=False)
sql_orders_db = DefaultConnectionPool(SqliteConnection, db_path='orders.sqlite', check_same_thread=False)

connection_mng = Container.managers.get(ConnectionManager)

# Register the sql_customers_db connection pool as default one (not related to any schema)
connection_mng.register_connection_pool(sql_customers_db)

# Register the sql_orders_db connection pool as 'orders' schema
connection_mng.register_connection_pool(sql_orders_db, 'orders')
```

Now, when you will request the connection pool by the schema name, you will get the corresponding connection pool.

## Querying multiple databases

When you have multiple connections to different databases, you can query them using the complex query contains the
subqueries or joins between tables from different databases.

Here is an example of how to query multiple databases:

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
        FieldReference(field=Field(name='name'), table_name='c'),
        FieldReference(field=Field(name='amount'), table_name='o'),
    ],
    table=SchemaReference(name='customers', version=Version.LATEST, alias='c'),
    joins=[
        JoinQuery(
            table=SchemaReference(name='orders', version=Version.LATEST, alias='o'),
            on=Conditions(
                Condition(
                    field=FieldReference(field=Field(name='customer_id'), table_name='o'),
                    lookup=FieldLookup.EQ,
                    value=FieldReference(field=Field(name='id'), table_name='c'),
                ),
            ),
        ),
    ],
)
```

That is equivalent to the following SQL query:

```sql
SELECT c.name, o.amount
FROM customers AS c
  JOIN orders AS o ON o.customer_id = c.id
```

Note, customers and orders are located in different databases. So, the AMSDAL Glue will split this query into two
queries and execute them separately. Then, it will join the results in memory.
