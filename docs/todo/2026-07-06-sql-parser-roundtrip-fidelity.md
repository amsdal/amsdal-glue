# TODO: round-trip fidelity for `amsdal_glue_sql_parser`

**Goal.** Make what `amsdal_glue_sql_parser` extracts from SQL match what is later
regenerated from that representation. That is, `SQL → parse → operation →
generate → SQL'` should yield `SQL'` that is semantically (ideally also textually,
up to normalization) equivalent to the original `SQL`. This property is currently
broken for computed columns.

## Symptom

```sql
SELECT UPPER(a) FROM t
```

after parse → generate becomes

```sql
SELECT UPPER(a) AS upper FROM t
```

The `upper` alias was absent in the source — the **parser synthesized it**.
Round-trip diverged. Same for aggregates: `SELECT SUM(a)` → `SELECT SUM(a) AS sum_a`.

## Root cause

The model requires an alias, so the parser is forced to invent one.

- `libs/core/src/amsdal_glue_core/common/data_models/select_expression.py`

  ```python
  @dataclass(kw_only=True)
  class SelectExpression:
      expression: Expression
      alias: str          # <-- required, not Optional
  ```

- `libs/sql-parser/src/amsdal_glue_sql_parser/parsers/sqloxide_parser.py`,
  `_process_expressions` — alias synthesis where none existed in the source:
  - line ~758 (aggregates): `alias or f'{func}_{field}'`
  - line ~770 (POWER):      `alias or name.lower()`
  - line ~781 (Func):       `alias or name.lower()`

- Generator (Rust qcraft binding), `libs/connections/rust/src/sql/extract.rs`:
  for `SelectColumn::Field` the alias can already be `None` (line ~233), but for
  `SelectColumn::Expr` the binding always passes `Some(alias)` (lines ~37, ~1221),
  because the model's alias is mandatory. So every expression emits `AS ...`.

Previously `alias: str` left no choice, and every computed column acquired a
synthesized alias. Round-trip fidelity was never a tested requirement — adopting
it **as a goal** is a deliberate decision made now.

## Related review findings (symptoms of the same root)

- **M14** — auto-alias collision: `SELECT UPPER(a), UPPER(b)` produces two
  `SelectExpression`s with the same `alias='upper'`; the second clobbers the
  first. This is already a result bug, not just round-trip. The proper root fix
  (below) also removes M14.
- **M15** — `_process_expressions` / `_process_only` drops `SELECT x AS y` for a
  simple identifier (only `CompoundIdentifier` is handled; a bare `Identifier` is
  skipped). Also about projection fidelity; consider together.

## Proposed direction

Make the alias truly optional end-to-end, so bare functions carry `None` and the
generator emits no `AS`:

1. `SelectExpression.alias: str | None` (default `None`) in the core model.
2. `sqloxide_parser._process_expressions`: **do not synthesize** an alias — when
   the source has none, leave `None` (for aggregates, POWER, Func).
3. Binding `extract_select_expr` (`extract.rs` ~766): `alias: String` →
   `Option<String>` (via `extract_optional_string`), pass it through as-is
   (`SelectColumn::Expr { alias }` without forcing `Some`).
4. Rebuild the PyO3 extension `_sql_core`.
5. api-server body `SelectExpressionBody.alias: str` → optional
   (`query_commands.py`).
6. Golden / round-trip tests (see acceptance criteria).

### Cost estimate

Moderate, and a **qcraft fork is most likely NOT needed.** In the binding
`SelectColumn::Expr { alias: Some(...) }` — so qcraft's `alias` field is already
`Option<String>`, and the renderer should already skip `AS` on `None` (as it does
for `Field`). We only need to **confirm** that rendering `Expr` with `alias=None`
actually omits `AS` (rather than failing / emitting an empty one). If confirmed,
the change is localized to the Python model + binding extraction + parser.

## Open questions

- [ ] Confirm qcraft rendering: `SelectColumn::Expr` with `alias=None` → no `AS`.
- [ ] Are there consumers that rely on a computed column's alias being present
      (e.g. mapping results by column name)? Check core/queries final executor and
      the polars path before removing synthesis.
- [ ] Normalization for textual round-trip comparison (quoting, keyword case,
      whitespace) — compare semantically, or run both sides through one normalizer.
- [ ] Fold M15 into this approach or handle separately.

## Acceptance criteria

- Round-trip test: for a set of `SELECT`s (bare functions, aggregates, POWER, mix
  with explicit aliases) `parse → generate` yields SQL with no added `AS`,
  semantically equal to the original; explicit aliases are preserved.
- `SELECT UPPER(a), UPPER(b)` produces two distinct columns with no collision
  (closes M14).
- Existing golden tests pass (or are deliberately updated where expected output
  changes due to removed `AS`).
