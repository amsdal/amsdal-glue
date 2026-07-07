# Querying schema metadata

AMSDAL Glue lets you query the structure of a database — its tables, columns,
constraints and indexes — through the **same** `QueryStatement` API you use for
data, and get back `Schema` objects. This is done through `query_schema`.

You never write a driver-specific catalog query (`information_schema`, `pg_*`,
`PRAGMA`). You describe *what* you are looking for against a small set of virtual
"registry" tables, and the connection returns the full `Schema` of every table
that matches — identically on SQLite and PostgreSQL.

## The model

- Your query always starts from the **table registry** (`TABLE_REGISTRY`). Its
  `name` column is the table name, and `query_schema` returns one `Schema` per
  matching table.
- To filter by columns, constraints or indexes, **JOIN** the corresponding
  registry and put your conditions in `WHERE`.
- The result is always `list[Schema]` — full schemas of the matched tables, with
  their properties, constraints and indexes.

```
query_schema(QueryStatement over TABLE_REGISTRY
             [JOIN a metadata registry ...]
             [WHERE ...])
        -> list[Schema]
```

## The registries

Import the names as constants — do not hard-code the string values.

```python
from amsdal_glue_connections.sql import (
    TABLE_REGISTRY,
    TABLE_PROPERTY_REGISTRY,
    TABLE_CONSTRAINT_REGISTRY,
    TABLE_INDEX_REGISTRY,
)
```

| Constant | Virtual table | Columns |
|---|---|---|
| `TABLE_REGISTRY` | `__amsdal__table_registry` | `name` |
| `TABLE_PROPERTY_REGISTRY` | `__amsdal__property_registry` | `table_name`, `name`, `type`, `udt_name`, `is_nullable`, `column_default`, `ordinal_position` |
| `TABLE_CONSTRAINT_REGISTRY` | `__amsdal__constraint_registry` | `table_name`, `name`, `type` |
| `TABLE_INDEX_REGISTRY` | `__amsdal__index_registry` | `table_name`, `name`, `index_type`, `is_unique` |

Constraint `type` uses single-char codes: `p` primary key, `u` unique,
`f` foreign key, `c` check, `x` exclusion. The join key is always
`TABLE_REGISTRY.name == <registry>.table_name`.

## A small helper

The examples use one helper to keep them short:

```python
from amsdal_glue_core.common.data_models.conditions import Condition, Conditions
from amsdal_glue_core.common.data_models.field_reference import Field, FieldReference
from amsdal_glue_core.common.data_models.join import JoinQuery
from amsdal_glue_core.common.data_models.query import QueryStatement
from amsdal_glue_core.common.data_models.schema import SchemaReference
from amsdal_glue_core.common.enums import FieldLookup, JoinType, Version
from amsdal_glue_core.common.expressions.field_reference import FieldReferenceExpression
from amsdal_glue_core.common.expressions.value import Value


def field(name: str, table: str) -> FieldReferenceExpression:
    return FieldReferenceExpression(
        field_reference=FieldReference(field=Field(name=name), table_name=table),
    )
```

## Example 1 — every table

```python
schemas = connection.query_schema(
    QueryStatement(table=SchemaReference(name=TABLE_REGISTRY, version=Version.LATEST)),
)
# -> [Schema(name='orders', ...), Schema(name='events', ...), Schema(name='users', ...)]
```

## Example 2 — tables that have a column named `email`

```python
schemas = connection.query_schema(
    QueryStatement(
        table=SchemaReference(name=TABLE_REGISTRY, version=Version.LATEST),
        joins=[
            JoinQuery(
                table=SchemaReference(name=TABLE_PROPERTY_REGISTRY, version=Version.LATEST),
                on=Conditions(
                    Condition(
                        left=field('name', TABLE_REGISTRY),
                        lookup=FieldLookup.EQ,
                        right=field('table_name', TABLE_PROPERTY_REGISTRY),
                    ),
                ),
                join_type=JoinType.INNER,
            ),
        ],
        where=Conditions(
            Condition(
                left=field('name', TABLE_PROPERTY_REGISTRY),
                lookup=FieldLookup.EQ,
                right=Value('email'),
            ),
        ),
    ),
)
```

## Example 3 — tables that have a `DATETIME` column

Same shape as example 2, filtering on the property `type`:

```python
where=Conditions(
    Condition(
        left=field('type', TABLE_PROPERTY_REGISTRY),
        lookup=FieldLookup.EQ,
        right=Value('DATETIME'),
    ),
)
# -> full Schemas of every table that has at least one DATETIME column
```

## Example 4 — tables that have a UNIQUE constraint

Join the constraint registry and filter `type == 'u'`:

```python
joins=[
    JoinQuery(
        table=SchemaReference(name=TABLE_CONSTRAINT_REGISTRY, version=Version.LATEST),
        on=Conditions(
            Condition(
                left=field('name', TABLE_REGISTRY),
                lookup=FieldLookup.EQ,
                right=field('table_name', TABLE_CONSTRAINT_REGISTRY),
            ),
        ),
        join_type=JoinType.INNER,
    ),
],
where=Conditions(
    Condition(
        left=field('type', TABLE_CONSTRAINT_REGISTRY),
        lookup=FieldLookup.EQ,
        right=Value('u'),
    ),
)
```

## Example 5 — combine filters

Add more joins to intersect conditions — e.g. tables that have **both** a
`DATETIME` column **and** a unique constraint: join `TABLE_PROPERTY_REGISTRY`
**and** `TABLE_CONSTRAINT_REGISTRY`, and put both conditions in `WHERE`. Every
join narrows the set of matched tables.

## How it runs

`query_schema` does two things:

1. **One** query to find the matching table names — your full `QueryStatement`
   (all joins, `WHERE`, subqueries) is executed against the registry views, and
   the table names are collected. No matter how complex the filter, this is a
   single query.
2. For each matched table, the connection introspects the real catalog to build
   the complete `Schema` (columns, constraints, indexes).

So the cost is `1 + (number of matched tables)` round trips, independent of how
elaborate the filter is.

## Database independence

The same `QueryStatement` runs unchanged on SQLite and PostgreSQL — the registry
views map to each engine's own catalog, and constraint `type` codes are the same
on both.

**SQLite constraint caveat:** SQLite does not expose constraints in a queryable
catalog the way PostgreSQL does, so `__amsdal__constraint_registry` on SQLite is
an approximation built from `PRAGMA` output. It covers **primary key (`p`),
unique (`u`) and foreign key (`f`)** constraints. `CHECK` (`c`) and `EXCLUSION`
(`x`) constraints are not reported on SQLite. On PostgreSQL all constraint types
are reported.
