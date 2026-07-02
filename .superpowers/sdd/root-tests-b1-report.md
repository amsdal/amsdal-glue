# Root-tests B1 Report — re-point 5 root-level connection tests to Rust generator

## Status: COMPLETE — 29/29 passing, golden suite 170/170 unchanged

---

## Per-file summary

| File | Commit | Assertions | Re-baselined | Deleted? | SUSPICIOUS count |
|---|---|---|---|---|---|
| `test_exists.py` | `635235b` | 8 | 8 | no | 0 |
| `test_nested_subquery.py` | `3f13bfd` | 2 | 2 | no | 0 |
| `test_output_type_value.py` | `8591bda` | 8 | 8 | no | 5 |
| `test_default_projection.py` | `87b2e9a` | 7 | 5 | no | 3 |
| `test_jsonb_array_expression.py` | `fffd3c4` | 4 | 4 | no | 4 |

**Total: 29 assertions, 27 re-baselined, 0 deleted, 12 SUSPICIOUS.**

---

## Migration changes applied (§7 cheatsheet)

- `Exists(query=sub)` → `Exists(subquery=SubQueryStatement(query=sub, alias=''))`
- `annotations=[AnnotationQuery(ExpressionAnnotation(...))]` → `expressions=[SelectExpression(...)]`
- `build_sql_query(q, transform=get_sqlite_transform())` → `SqlGenerator('sqlite', param_style='qmark').compile_query(q)`
- `build_expression(expr, transform=...)` / `build_conditions(where, transform=...)` → wrapped in `QueryStatement` with `compile_query`
- `JsonbArrayExpression` → `JsonbArray` (class renamed in core)
- Quote style: SQLite single-quoted identifiers (`'t'.'c'`) → ANSI double-quoted (`"t"."c"`)
- Rust emits `EXISTS(` (no space before paren); old builder emitted `EXISTS (`

---

## SUSPICIOUS — full detail

### S1 — `test_output_type_value.py`: `output_type` CAST/json() behavior entirely gone

The Rust extractor does NOT read `output_type` on `Value`. All 5 affected tests:

| Test | Old SQL fragment | New SQL fragment |
|---|---|---|
| `test_value_string_output_type_str_emits_cast_text_sqlite` | `cast(? as TEXT)` | `?` |
| `test_value_string_output_type_none_vs_str_postgres` | `(%s)::TEXT` for `output_type=str` | `%s` |
| `test_value_int_output_type_int_emits_cast_integer_sqlite` | `cast(? as INTEGER)` | `?` |
| `test_value_datetime_output_type_none_emits_plain_placeholder_sqlite` | param was Python `datetime` object | param is ISO string `'2026-01-01 12:00:00+00:00'` |
| `test_value_dict_output_type_none_wraps_with_json_sqlite` | `json(?)` | `?` (no wrapping) |

**Impact**: Any caller relying on `output_type=str/int/float` to emit CAST in the final SQL, or relying on `json(?)` wrapping for dict columns in SQLite, will get different SQL. The `datetime` serialisation change also affects what the DB driver receives (string instead of Python object). Needs review if `output_type` is used anywhere in production paths.

### S2 — `test_default_projection.py`: `SELECT *` not qualified on JOINs

The old Python builder emitted `SELECT 'Table'.*` (table-qualified) when `only=None` and JOINs were present, to prevent column-name pollution. The Rust generator always emits bare `SELECT *`.

Affected tests (3):
- `test_only_none_with_join_qualifies_to_base_table_name`: old `SELECT 'Company'.*` → new `SELECT *`
- `test_only_none_with_join_qualifies_to_base_table_alias_when_set`: old `SELECT 'c'.*` → new `SELECT *`
- `test_subquery_from_with_join_qualifies_to_subquery_alias`: old `SELECT 'c'.*` → new `SELECT *`

**Impact**: On multi-table JOINs where `only=None`, the result set now includes columns from ALL joined tables instead of only the primary table. This can cause column-name conflicts and may return more data than callers expect. Any production query with `only=None` + JOINs is affected.

### S3 — `test_jsonb_array_expression.py`: SQLite JSON function + behavior change

Old Python builder (via `func_transform`): `jsonb_array(CASE WHEN json_valid(col) THEN jsonb(col) ELSE col END, ...)`
Rust generator: `json_array(col1, col2, ...)`

Two distinct differences:
1. **Function name**: `jsonb_array` (binary-JSON) → `json_array` (text-JSON). Semantically different in SQLite 3.45+.
2. **CASE WHEN handling**: The old builder's CASE WHEN preserved structure when a column already contained a JSON string. The Rust generator does no such pre-processing — if a column holds a JSON string it will be treated as a plain string value within the array.

Affected tests (all 4 SQLite tests in the file).

---

## New §7 gotcha discovered

None beyond what is already in the compat notes.

---

## Final counts

- Files migrated: 5
- Tests passing: 29
- Golden suite: 170 passing, 3 xfailed (unchanged)
- SUSPICIOUS items: 12 individual test re-baselines across 3 semantic issue categories
