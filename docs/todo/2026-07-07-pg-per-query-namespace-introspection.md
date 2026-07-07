# TODO: per-query namespace for PostgreSQL schema introspection

## Goal

`query_schema` / `introspect_schema` should resolve the target PostgreSQL schema
in this order:

1. If the request specifies a namespace (`SchemaReference.namespace`), introspect
   **that** schema.
2. Otherwise, default to the **connection's** schema (the one set via
   `connect(schema=...)` / `search_path`).
3. If the specified schema does not exist, let the database raise — that is the
   correct, honest failure.

Rationale: `query_schema` is a **connection-level** operation, so it queries the
connection's own database; but a caller that names a namespace should be served
that namespace without opening a new connection.

## Current state (after the connection-schema fix)

Introspection now uses the connection's configured schema instead of a hardcoded
`'public'` (columns/constraints/indexes queries + the `namespace` stamp), and the
registry views are built for that schema. What is still missing is honoring a
**per-request** namespace that differs from the connection default.

## The blocker

The registry views bake the schema into their `WHERE nspname = <schema>`. A single
session-scoped set of views reflects exactly one schema, so a per-request
namespace that differs from it is not served by the view-based table list.

## Approach to design

Preferred: make the registry views **schema-agnostic** — expose a `namespace`
(a.k.a. `schemaname`) column and do NOT filter the schema inside the view. Then:

- The table-list query filters by the requested namespace (defaulting to the
  connection schema) via a normal `WHERE namespace = ...`.
- The join-based metadata-query feature (`query_schema` over
  `__amsdal__property_registry` etc.) can filter by `namespace` as a first-class
  column — which also generalizes the whole feature across schemas.
- Per-table introspection (columns/constraints/indexes) takes the namespace of the
  matched table rather than a fixed connection schema.

Alternative (worse): recreate the views per requested namespace — churn, and
breaks the single-session assumption.

## Open architecture questions

- How does the namespace flow through `query_schema` when the request joins the
  registries (which registry row's `namespace` wins on a multi-registry join)?
- Interaction with multiple state connections on different schemas + one lakehouse
  — confirm each connection introspects its own database/schema and nothing
  reaches across.
- Whether `namespace` should also become a filter on the per-table introspection
  helpers (`_introspect_columns/_constraints/_indexes`) so they honor a
  non-default schema.

This needs a deliberate design pass; it was split out of the connection-schema fix
to avoid blocking the latter.
