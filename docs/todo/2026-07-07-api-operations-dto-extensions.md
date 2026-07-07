# TODO: API operations DTO — deferred extensions

The api-server operations request DTOs (`libs/api-server/.../controllers/operations/`)
were redesigned to be pydantic-native (no monkey-patching of core modules, no
`arbitrary_types_allowed` leak). The redesign deliberately covers only the
**currently supported** request surface. This document records the extensions
that were intentionally deferred, so the API can grow without re-introducing
crutches.

The extension seam is the discriminated `ExpressionBody` union (a custom callable
discriminator that selects the DTO by input structure, keeping the wire shape
tag-free). New expression kinds are added as new arms + a converter branch.

## 1. Richer expression types

Today the API accepts only these operand/expression kinds:
- field reference
- literal value
- aggregations: `SUM`, `COUNT`, `AVG`, `MIN`, `MAX`
- subquery

The core expression tree is much larger and is **not** reachable from the API yet.
To accept these, add a tagged `ExpressionBody` arm + a `expression_body_to_core`
branch for each:

- `Func` — scalar functions, e.g. `UPPER(name)`, `LOWER(x)`, `COALESCE(...)`.
- `Combined` — infix operators, e.g. `a + b`, `a * b`, `a ^ b`.
- `Case` / `When` — conditional expressions.
- `Cast` — type casts.
- `Exists` — `EXISTS (subquery)`.
- Window functions.
- `Raw` — raw SQL fragment (guard carefully — injection surface).
- `JsonPathText`, `Vector` ops, and any other core expression added later.

Each new arm must round-trip JSON natively and convert to the matching
`amsdal_glue_core` expression. Only add the ones with a real consumer (avoid a
full mirror with no caller).

## 2. Full `FieldType` for `Value.output_type`

Today `Value.output_type` on the API is restricted to a plain `ScalarType`
string (e.g. `"integer"`, `"text"`, `"date"`) — which is all the API has ever
used.

The core `FieldType` is a recursive union: `ScalarType | CustomType | ArrayType |
NestedType | DictType | VectorType`. If a use case appears that needs a value
typed as an array/nested/vector/custom type, extend `output_type` to a recursive
`FieldType` DTO (a discriminated union mirroring the core type tree) rather than
re-exposing the raw core union.

## 3. Omitted `QueryStatement` features

`QueryStatementBody` currently drops several fields that exist on core
`QueryStatement`. Add DTO support when needed:

- `having`
- `ctes` (common table expressions)
- `lock` / `SelectLock`
- `SetOperation` as a table source (UNION / INTERSECT / EXCEPT)
- `FieldReferenceAliased` in `only` (aliased projections)

## Principle

Every extension here plugs into the native discriminated-union DTO design. None of
them justify reaching into core module internals or `arbitrary_types_allowed`.
If a change tempts you toward either, stop and model the DTO explicitly instead.
