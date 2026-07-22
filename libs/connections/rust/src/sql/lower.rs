//! Rewrite the canonical (Postgres) JSON AST into the SQLite forms that return the same rows.
//!
//! Postgres is the reference: `extract` builds exactly the AST Postgres must render, and qcraft
//! renders that AST faithfully. SQLite, however, has no JSON type -- `->` yields TEXT holding JSON and
//! `->>` yields the native SQL value -- so rendering the same AST literally there gives *different
//! answers*, silently. `payload->'age' > 1000000` is true for every row, because SQLite orders every
//! INTEGER below every TEXT.
//!
//! So the compat layer lives here, in glue, as an ordinary AST-to-AST pass -- not inside qcraft, whose
//! job is to render what it is given. If SQLite ever aligns its operators with Postgres, this module
//! is deleted and nothing else changes.
//!
//! The mapping (all verified against a live SQLite 3.50 and Postgres 16):
//!
//! | intent                    | Postgres                    | SQLite                                  |
//! |---------------------------|-----------------------------|-----------------------------------------|
//! | JSON extraction (default) | `col->'a'->'b'`             | `col->'a'->>'b'`      (native value)    |
//! | TEXT extraction           | `col->'a'->>'b'`            | `CASE json_type(...)` (see `text_form`) |
//! | typed extraction          | `(col->'a'->>'b')::bigint`  | `CAST(col->'a'->>'b' AS bigint)`        |
//! | JSON param, scalar        | `Jsonb(18)`                 | raw `18`                                |
//! | JSON param, container     | `Jsonb({...})`              | `jsonb(?)`                              |
//! | whole JSON column         | `col = $1`                  | `jsonb(col) = jsonb(?)`                 |
//! | `= JSON null`             | `col->'a' = 'null'::jsonb`  | `json_type(col->'a') = 'null'`          |
//! | `IS NULL` (key absent)    | `col->'a' IS NULL`          | `col->'a' IS NULL`   (`->`, not `->>`)  |

use qcraft::ast::common::*;
use qcraft::ast::conditions::*;
use qcraft::ast::ddl::*;
use qcraft::ast::dml::*;
use qcraft::ast::expr::*;
use qcraft::ast::query::*;
use qcraft::ast::value::Value;

pub fn lower_query(stmt: &mut QueryStmt) {
    if let Some(ctes) = stmt.ctes.as_mut() {
        for cte in ctes {
            lower_query(&mut cte.query);
        }
    }
    if let Some(from) = stmt.from.as_mut() {
        for item in from {
            lower_from_item(item);
        }
    }
    if let Some(joins) = stmt.joins.as_mut() {
        for join in joins {
            lower_from_item(&mut join.source);
            if let Some(JoinCondition::On(on)) = join.condition.as_mut() {
                lower_conditions(on);
            }
        }
    }
    if let Some(where_clause) = stmt.where_clause.as_mut() {
        lower_conditions(where_clause);
    }
    if let Some(having) = stmt.having.as_mut() {
        lower_conditions(having);
    }
    if let Some(set_op) = stmt.set_op.as_mut() {
        lower_query(&mut set_op.left);
        lower_query(&mut set_op.right);
    }
    // SELECT projection, GROUP BY and ORDER BY need the SAME JSON-extraction lowering as WHERE:
    // a nested field kept in its Postgres `col->'k'` shape returns JSON *text* on SQLite (quoted
    // strings, lexical ordering), whereas `jsonb_extract`/native `->>` returns the native value.
    for column in &mut stmt.columns {
        lower_select_column(column);
    }
    if let Some(group_by) = stmt.group_by.as_mut() {
        for item in group_by {
            lower_group_by_item(item);
        }
    }
    if let Some(order_by) = stmt.order_by.as_mut() {
        for order in order_by {
            lower_expr(&mut order.expr);
        }
    }
}

/// Lower a SELECT column. A bare `Expr` column is lowered in place; a `Field` projection carrying a
/// JSON path (`payload->'name'`) has no `Expr` to recurse into, so it is rebuilt as a lowered
/// expression column (preserving any alias) -- exactly the native extraction WHERE already produces.
fn lower_select_column(column: &mut SelectColumn) {
    match column {
        SelectColumn::Field { field, alias } if field.field.child.is_some() => {
            let mut expr = Expr::Field(field.clone());
            lower_expr(&mut expr);
            let alias = alias.clone();
            *column = SelectColumn::Expr { expr, alias };
        }
        SelectColumn::Expr { expr, .. } => lower_expr(expr),
        _ => {}
    }
}

fn lower_group_by_item(item: &mut GroupByItem) {
    match item {
        GroupByItem::Expr(expr) => lower_expr(expr),
        GroupByItem::Rollup(exprs) | GroupByItem::Cube(exprs) => {
            for expr in exprs {
                lower_expr(expr);
            }
        }
        GroupByItem::GroupingSets(sets) => {
            for set in sets {
                for expr in set {
                    lower_expr(expr);
                }
            }
        }
    }
}

pub fn lower_mutation(stmt: &mut MutationStmt) {
    match stmt {
        // INSERT values are the STORAGE form -- a JSON column holds JSON text, so they are left alone.
        MutationStmt::Insert(_) | MutationStmt::Custom(_) => {}
        MutationStmt::Update(update) => {
            if let Some(where_clause) = update.where_clause.as_mut() {
                lower_conditions(where_clause);
            }
        }
        MutationStmt::Delete(delete) => {
            if let Some(where_clause) = delete.where_clause.as_mut() {
                lower_conditions(where_clause);
            }
        }
    }
}

/// Rewrite DDL column types for SQLite. The canonical AST carries Postgres type names (e.g. `bytea`),
/// which are rendered verbatim; SQLite needs its own spelling. Currently only `bytea` -> `BLOB`:
/// SQLite's native binary type (BLOB affinity), so a binary column is created correctly and a
/// `BLOB`->BYTEA introspection round-trip leaves migrations untouched.
pub fn lower_schema(stmt: &mut SchemaMutationStmt) {
    match stmt {
        SchemaMutationStmt::CreateTable { schema, .. } => {
            for column in &mut schema.columns {
                lower_field_type(&mut column.field_type);
            }
        }
        SchemaMutationStmt::AddColumn { column, .. } => lower_field_type(&mut column.field_type),
        SchemaMutationStmt::AlterColumnType { new_type, .. } => lower_field_type(new_type),
        _ => {}
    }
}

fn lower_field_type(field_type: &mut FieldType) {
    match field_type {
        FieldType::Scalar(name) if name.eq_ignore_ascii_case("bytea") => {
            *name = "BLOB".to_string();
        }
        FieldType::Array(inner) => lower_field_type(inner),
        _ => {}
    }
}

fn lower_from_item(item: &mut FromItem) {
    lower_table_source(&mut item.source);
}

fn lower_table_source(source: &mut TableSource) {
    if let TableSource::SubQuery(sub) = source {
        lower_query(&mut sub.query);
    }
}

fn lower_conditions(conditions: &mut Conditions) {
    for child in &mut conditions.children {
        match child {
            ConditionNode::Comparison(cmp) => {
                // Decided BEFORE lowering: afterwards a JSON parameter has become a native value and
                // is no longer distinguishable from a plain one.
                let json_null_row = json_null_also_satisfies(cmp);

                lower_comparison(cmp);

                if let Some(json_expr) = json_null_row {
                    *child = or_json_null(json_expr, (**cmp).clone());
                }
            }
            ConditionNode::Group(group) => lower_conditions(group),
            ConditionNode::Exists(query) => lower_query(query),
            _ => {}
        }
    }
}

/// A JSON `null` is a VALUE in Postgres, and the LOWEST one -- jsonb orders
/// `Object > Array > Boolean > Number > String > Null`. So `age < 18` matches a row whose `age` is
/// JSON `null`, and so does `age != 36`.
///
/// SQLite cannot see that: `->>` has already turned the JSON `null` into SQL NULL, and every
/// comparison against NULL is NULL. The row has to be brought back explicitly.
///
/// Only these three need it. `>` and `>=` are already right: nothing is below a JSON `null`, and
/// SQLite's NULL excludes the row just the same. `=` is handled by `lower_json_null_comparison`.
/// A MISSING key stays excluded in both engines -- `->` yields SQL NULL there, and `json_type(NULL)`
/// is NULL, so the guard below does not fire for it either.
fn json_null_also_satisfies(cmp: &Comparison) -> Option<Expr> {
    let (json_expr, other, op) = match (&cmp.left, &cmp.right) {
        (left, right) if is_json_extraction(left) => (left, right, cmp.op.clone()),
        (left, right) if is_json_extraction(right) => (right, left, mirror(&cmp.op)),
        _ => return None,
    };

    if !matches!(op, CompareOp::Neq | CompareOp::Lt | CompareOp::Lte) {
        return None;
    }
    // Only a JSON counterpart makes this a JSON comparison. Anything else would be a type error in
    // Postgres anyway, so there is no reference behaviour to reproduce.
    if !is_json_comparand(other) {
        return None;
    }

    Some(json_expr.clone())
}

fn or_json_null(json_expr: Expr, cmp: Comparison) -> ConditionNode {
    let is_json_null = Comparison {
        left: Expr::Func {
            name: "json_type".to_string(),
            args: vec![json_expr],
        },
        op: CompareOp::Eq,
        right: sql_literal("'null'"),
        negate: false,
    };

    ConditionNode::Group(Conditions {
        children: vec![
            ConditionNode::Comparison(Box::new(is_json_null)),
            ConditionNode::Comparison(Box::new(cmp)),
        ],
        connector: Connector::Or,
        negated: false,
    })
}

/// The same comparison seen from the other operand: `18 > age` is `age < 18`.
fn mirror(op: &CompareOp) -> CompareOp {
    match op {
        CompareOp::Lt => CompareOp::Gt,
        CompareOp::Lte => CompareOp::Gte,
        CompareOp::Gt => CompareOp::Lt,
        CompareOp::Gte => CompareOp::Lte,
        other => other.clone(),
    }
}

// ---------------------------------------------------------------------------
// Comparisons
// ---------------------------------------------------------------------------

fn lower_comparison(cmp: &mut Comparison) {
    // `IS NULL` must keep the `->` chain. `->>` collapses a JSON `null` into SQL NULL, which would
    // make "the key is absent" and "the value is JSON null" indistinguishable -- Postgres keeps them
    // apart, so SQLite has to as well.
    if matches!(cmp.op, CompareOp::IsNull) {
        return;
    }

    // Case-sensitive text match -> case-sensitive `glob(...)`. SQLite's `LIKE` is case-INsensitive
    // for ASCII, so the default `col LIKE ?` would make `STARTSWITH='Test'` match `'test'`; `GLOB`
    // is case-sensitive. Intercept BEFORE the JSON-extraction lowering below, but build the call
    // over the *lowered* left so a JSON-extracted field is the string argument.
    if lower_text_match_glob(cmp) {
        return;
    }

    if lower_json_null_comparison(cmp) {
        return;
    }
    if lower_whole_column_comparison(cmp) {
        return;
    }

    // A JSON parameter compared against a native extraction must itself be native: `col ->> 'age'`
    // yields INTEGER 36, so binding the JSON text '18' would compare INTEGER to TEXT -- and SQLite
    // ranks every INTEGER below every TEXT, which is the always-true bug this pass exists to kill.
    if is_json_extraction(&cmp.left) {
        adapt_json_param(&mut cmp.right);
    }
    if is_json_extraction(&cmp.right) {
        adapt_json_param(&mut cmp.left);
    }

    // A JSON operand compared with a `jsonb_array(...)` expression (the historical metadata join
    // `object_id = jsonb_array(pk...)`). The array lowers to a JSONB blob (see the `JsonArray` branch
    // in `lower_expr`), so the OTHER side must become a blob too or the equality matches nothing:
    //   * a whole column (`object_id`) keeps `json.dumps` spacing / raw text -> wrap in `jsonb()`;
    //   * a `->`/`->>` extraction (the reverse-FK case `team->'ref'->>'object_id'`) yields the JSON
    //     TEXT of the array -> also wrap in `jsonb()`, so `jsonb(team->'ref'->>'object_id')` parses
    //     that text back to the same canonical blob the array produces.
    // Without wrapping the extraction side, a TEXT extraction would be compared to a BLOB array and
    // SQLite never treats TEXT as equal to BLOB -- which silently breaks composite-PK reverse joins.
    if matches!(cmp.op, CompareOp::Eq | CompareOp::Neq) {
        if is_json_column_operand(&cmp.left) && is_json_array(&cmp.right) {
            cmp.left = jsonb_normalised(&cmp.left);
        } else if is_json_column_operand(&cmp.right) && is_json_array(&cmp.left) {
            cmp.right = jsonb_normalised(&cmp.right);
        }
    }

    lower_expr(&mut cmp.left);
    lower_expr(&mut cmp.right);
}

/// Rewrite a case-sensitive text-match comparison into the case-sensitive `glob(pattern, col) = 1`.
///
/// qcraft renders CONTAINS/STARTSWITH/ENDSWITH as `col LIKE ?`, but SQLite's `LIKE` is
/// case-INsensitive for ASCII, so that silently matches the wrong rows. SQLite has no `GLOB`
/// operator in qcraft, but the `glob(pattern, str)` FUNCTION has identical (case-sensitive)
/// semantics, so the comparison is rebuilt as `glob(<pattern>, <left>) = 1` (verified on SQLite
/// 3.50: `glob('Test*','test2')` = 0, `glob('Test*','Test2')` = 1).
///
/// The right operand is always a `Value(str)` search term. Its GLOB metacharacters (`*`, `?`, `[`)
/// are escaped so it matches literally, then the wildcard(s) are wrapped around it per the op.
/// `negate` is preserved, so `exclude(name__startswith=…)` renders `NOT (glob(...) = 1)`.
/// The `I` variants (case-insensitive) are left to qcraft's `LOWER(col) LIKE LOWER(?)`.
fn lower_text_match_glob(cmp: &mut Comparison) -> bool {
    let (prefix_star, suffix_star) = match cmp.op {
        CompareOp::Contains => (true, true),
        CompareOp::StartsWith => (false, true),
        CompareOp::EndsWith => (true, false),
        _ => return false,
    };

    // The search term is always a string Value; anything else falls through to the default path.
    let raw = match &cmp.right {
        Expr::Value(Value::Str(s)) => s.clone(),
        _ => return false,
    };

    let mut pattern = String::new();
    if prefix_star {
        pattern.push('*');
    }
    pattern.push_str(&escape_glob(&raw));
    if suffix_star {
        pattern.push('*');
    }

    // Lower the left first so a lakehouse JSON-extracted field (`col->>'name'`) is the string arg.
    let mut left = cmp.left.clone();
    lower_expr(&mut left);

    cmp.left = Expr::Func {
        name: "glob".to_string(),
        args: vec![Expr::Value(Value::Str(pattern)), left],
    };
    cmp.op = CompareOp::Eq;
    cmp.right = sql_literal("1");
    // cmp.negate is intentionally preserved.

    true
}

/// Escape GLOB metacharacters so a search term matches literally: `*`->`[*]`, `?`->`[?]`, `[`->`[[]`.
/// `%` and `_` are already literal under GLOB (unlike LIKE), so they are left untouched.
fn escape_glob(value: &str) -> String {
    let mut out = String::with_capacity(value.len());
    for ch in value.chars() {
        match ch {
            '*' => out.push_str("[*]"),
            '?' => out.push_str("[?]"),
            '[' => out.push_str("[[]"),
            other => out.push(other),
        }
    }
    out
}

/// `col->'a' = 'null'::jsonb` -> `json_type(col->'a') = 'null'`.
///
/// SQLite cannot express this through the value: `->>` turns JSON `null` into SQL NULL, and `NULL = NULL`
/// is never true. The type has to be asked for directly.
fn lower_json_null_comparison(cmp: &mut Comparison) -> bool {
    if !matches!(cmp.op, CompareOp::Eq | CompareOp::Neq) {
        return false;
    }

    let json_expr = match (&cmp.left, &cmp.right) {
        (left, right) if is_json_extraction(left) && is_json_null(right) => left.clone(),
        (left, right) if is_json_null(left) && is_json_extraction(right) => right.clone(),
        _ => return false,
    };

    cmp.left = Expr::Func {
        name: "json_type".to_string(),
        args: vec![json_expr],
    };
    cmp.right = sql_literal("'null'");

    true
}

/// A whole JSON column compared with a JSON value: normalise BOTH sides.
///
/// The stored text carries `json.dumps` spacing (`{"k": 1}`) while SQLite re-renders JSON minified
/// (`{"k":1}`); wrapping BOTH sides in `jsonb()` (`jsonb(col) = jsonb(?)`) normalises whitespace, so
/// older spaced rows still compare equal.
fn lower_whole_column_comparison(cmp: &mut Comparison) -> bool {
    let left_is_column = is_plain_field(&cmp.left);
    let right_is_column = is_plain_field(&cmp.right);

    let matched = (left_is_column && is_json_value(&cmp.right)) || (right_is_column && is_json_value(&cmp.left));
    if !matched {
        return false;
    }

    cmp.left = jsonb_normalised(&cmp.left);
    cmp.right = jsonb_normalised(&cmp.right);

    true
}

/// Adapt a JSON parameter to the native extraction it is compared against.
fn adapt_json_param(expr: &mut Expr) {
    let Expr::Value(value) = expr else {
        return;
    };

    // An `IN` list: each element is a candidate in its own right, so each is adapted on its own.
    if let Value::Array(items) = value {
        let lowered: Vec<Expr> = items
            .iter()
            .map(|item| native_or_normalised(item).unwrap_or_else(|| Expr::Value(item.clone())))
            .collect();

        // A list of plain values stays a value array, so it still renders as `IN (?, ?)`. Only a
        // container element (which needs a `json(?)` call around it) forces an expression list.
        *expr = match lowered
            .iter()
            .map(|item| match item {
                Expr::Value(v) => Some(v.clone()),
                _ => None,
            })
            .collect::<Option<Vec<Value>>>()
        {
            Some(values) => Expr::Value(Value::Array(values)),
            None => Expr::Tuple(lowered),
        };

        return;
    }

    if let Some(replacement) = native_or_normalised(value) {
        *expr = replacement;
    }
}

/// A JSON scalar becomes the native SQL value; a JSON container stays JSON but is normalised by
/// `json()`, so SQLite's minified rendering and Python's spaced `json.dumps` agree.
fn native_or_normalised(value: &Value) -> Option<Expr> {
    let text = match value {
        Value::Json(text) | Value::Jsonb(text) => text,
        _ => return None,
    };
    let parsed: serde_json::Value = serde_json::from_str(text).ok()?;

    let native = match parsed {
        serde_json::Value::Bool(b) => Value::Bool(b),
        serde_json::Value::String(s) => Value::Str(s),
        serde_json::Value::Number(n) => {
            if let Some(i) = n.as_i64() {
                Value::Int(i)
            } else if let Some(f) = n.as_f64() {
                Value::Float(f)
            } else {
                return None;
            }
        }
        // Objects, arrays and `null` are not scalars -- keep them JSON, normalised.
        _ => return Some(json_normalised(&Expr::Value(value.clone()))),
    };

    Some(Expr::Value(native))
}

// ---------------------------------------------------------------------------
// Expressions
// ---------------------------------------------------------------------------

fn lower_expr(expr: &mut Expr) {
    match expr {
        // A typed extraction: `->>` is ALREADY the native form in SQLite, so the cast applies straight
        // to it. Recursing would turn the inner `->>` into the TEXT compat form and cast that instead.
        Expr::Cast { expr: inner, .. } => {
            if !contains_json_path_text(inner) {
                lower_expr(inner);
            }
        }
        Expr::Field(field_ref) if field_ref.field.child.is_some() => {
            *expr = native_extraction(field_ref.clone());
        }
        Expr::JsonPathText { .. } => {
            *expr = text_form(expr.clone());
        }
        Expr::Tuple(items) => {
            for item in items {
                lower_expr(item);
            }
        }
        // `Expr::JsonArray` renders as SQLite's `json_array(...)`, which returns JSON *text*. The
        // metadata join needs the JSONB form `jsonb_array(...)` instead, whose canonicalisation lets
        // a freshly minified array compare equal to a stored, spaced `json.dumps` `object_id`. There
        // is no `Expr::JsonbArray` node, so this is rewritten into a plain `Func` -- `jsonb_array` is
        // a real SQLite function (3.45+) and renders correctly.
        Expr::JsonArray(items) => {
            let args = items
                .iter()
                .map(|item| {
                    let mut item = item.clone();
                    lower_expr(&mut item);
                    json_array_item(item)
                })
                .collect();
            *expr = Expr::Func {
                name: "jsonb_array".to_string(),
                args,
            };
        }
        Expr::Binary { left, right, .. } => {
            lower_expr(left);
            lower_expr(right);
        }
        Expr::Unary { expr: inner, .. } => lower_expr(inner),
        Expr::Func { args, .. } => {
            for arg in args {
                lower_expr(arg);
            }
        }
        Expr::Exists(query) | Expr::SubQuery(query) | Expr::ArraySubQuery(query) => lower_query(query),
        _ => {}
    }
}

/// `col->'a'->'b'`  ->  `col->'a'->>'b'` -- the native value, which is what SQLite must compare.
fn native_extraction(field_ref: FieldRef) -> Expr {
    let FieldRef {
        mut field,
        table_name,
        namespace,
    } = field_ref;
    let last_key = strip_last(&mut field);

    Expr::JsonPathText {
        expr: Box::new(Expr::Field(FieldRef {
            field,
            table_name,
            namespace,
        })),
        path: last_key,
    }
}

/// Reproduce Postgres' `->>` for every scalar kind.
///
/// SQLite's `->>` unwraps to the NATIVE value, so a JSON number gives INTEGER 36 where Postgres gives
/// the text '36', and a JSON boolean gives INTEGER 1 where Postgres gives 'true'. Only asking for the
/// JSON type first gets all of them right:
///
/// ```sql
/// CASE WHEN json_type(col->'a') = 'null' THEN NULL          -- JSON null  -> SQL NULL, as in PG
///      WHEN json_type(col->'a') = 'text' THEN col->>'a'     -- a string   -> unquoted
///      ELSE col->'a'                                        -- number/bool/object/array -> JSON text
/// END
/// ```
///
/// It is built on `->` because `->>` has already collapsed JSON `null` into SQL NULL by the time the
/// CASE could look at it.
fn text_form(path_text: Expr) -> Expr {
    let Expr::JsonPathText { expr: base, path } = &path_text else {
        return path_text;
    };

    // Rebuild the `->` form of the same path. Only a field reference can be rebuilt; anything else
    // keeps the plain `->>`, which is already correct for a text-valued expression.
    let Expr::Field(field_ref) = base.as_ref() else {
        return path_text;
    };
    let json_expr = Expr::Field(with_child(field_ref.clone(), path));

    let json_type = Expr::Func {
        name: "json_type".to_string(),
        args: vec![json_expr.clone()],
    };

    Expr::Case(CaseDef {
        cases: vec![
            WhenClause {
                condition: single(json_type.clone(), CompareOp::Eq, sql_literal("'null'")),
                result: sql_literal("NULL"),
            },
            WhenClause {
                condition: single(json_type, CompareOp::Eq, sql_literal("'text'")),
                result: path_text.clone(),
            },
        ],
        default: Some(Box::new(json_expr)),
    })
}

/// Wrap one `jsonb_array` item as `CASE WHEN json_valid(x) = 1 THEN jsonb(x) ELSE x END`.
///
/// SQLite's `jsonb_array(...)` treats each argument as an opaque scalar, so a column whose TEXT holds
/// a JSON object (a composite-PK / reference column such as `{"ref": {...}}`) is double-escaped into
/// a string instead of embedded as structure. That breaks the historical metadata join
/// (`object_id = jsonb_array(pk...)`) for through / composite-PK models, which then matches nothing.
/// Parsing valid-JSON items back with `jsonb()` embeds them as structure; a plain scalar (e.g. a
/// single-PK `partition_key` that is not valid JSON) is left untouched, so `jsonb_array("p-1")` still
/// yields `["p-1"]`. This reproduces the pre-migration (`main`) `CASE WHEN json_valid(col) THEN
/// jsonb(col) ELSE col END` semantics verbatim.
fn json_array_item(item: Expr) -> Expr {
    let json_valid = Expr::Func {
        name: "json_valid".to_string(),
        args: vec![item.clone()],
    };
    let json_parsed = Expr::Func {
        name: "jsonb".to_string(),
        args: vec![item.clone()],
    };

    Expr::Case(CaseDef {
        cases: vec![WhenClause {
            condition: single(json_valid, CompareOp::Eq, sql_literal("1")),
            result: json_parsed,
        }],
        default: Some(Box::new(item)),
    })
}

// ---------------------------------------------------------------------------
// Predicates and small builders
// ---------------------------------------------------------------------------

/// A `->` chain out of a JSON column: the default (JSONB) extraction, still in its Postgres shape.
fn is_json_extraction(expr: &Expr) -> bool {
    matches!(expr, Expr::Field(field_ref) if field_ref.field.child.is_some())
}

fn is_plain_field(expr: &Expr) -> bool {
    matches!(expr, Expr::Field(field_ref) if field_ref.field.child.is_none())
}

/// A JSON-valued column operand that must be `jsonb()`-normalised to compare against a `jsonb_array`:
/// either a whole JSON column (`object_id`) or a `->`/`->>` extraction out of one (`team->'ref'->…`).
/// Both yield JSON that has to be parsed back to a canonical blob to equal the array's blob.
fn is_json_column_operand(expr: &Expr) -> bool {
    is_plain_field(expr) || is_json_extraction(expr)
}

fn is_json_array(expr: &Expr) -> bool {
    matches!(expr, Expr::JsonArray(_))
}

fn is_json_value(expr: &Expr) -> bool {
    matches!(expr, Expr::Value(Value::Json(_) | Value::Jsonb(_)))
}

/// A JSON value on the other side of a comparison -- what makes it a JSON comparison at all. A JSON
/// `null` is excluded: `lower_json_null_comparison` owns that case.
fn is_json_comparand(expr: &Expr) -> bool {
    is_json_value(expr) && !is_json_null(expr)
}

fn is_json_null(expr: &Expr) -> bool {
    match expr {
        Expr::Value(Value::Json(text) | Value::Jsonb(text)) => text == "null",
        _ => false,
    }
}

fn contains_json_path_text(expr: &Expr) -> bool {
    match expr {
        Expr::JsonPathText { .. } => true,
        Expr::Tuple(items) => items.iter().any(contains_json_path_text),
        _ => false,
    }
}

/// `json(expr)` -- SQLite's JSON (TEXT) normaliser. Used only where the OTHER side of the comparison
/// is a `->`/`->>` extraction, which yields TEXT: a nested container parameter (`col->'meta' = {...}`)
/// is compared against `col->'meta'`, so both stay TEXT. Using `jsonb()` here would make one side a
/// binary blob and the other TEXT, and SQLite never treats a TEXT value as equal to a BLOB.
fn json_normalised(expr: &Expr) -> Expr {
    Expr::Func {
        name: "json".to_string(),
        args: vec![expr.clone()],
    }
}

/// `jsonb(expr)` -- SQLite's JSONB normaliser. Used where BOTH sides become the JSONB binary form:
/// whole-column equality (`jsonb(col) = jsonb(?)`) and the metadata array join
/// (`jsonb(object_id) = jsonb_array(...)`, whose RHS is itself a JSONB blob). `jsonb()` canonicalises
/// whitespace (key order is left untouched, exactly as `json()`), so a value stored the older spaced
/// `json.dumps` way still compares equal to a freshly minified one -- no data migration is required.
fn jsonb_normalised(expr: &Expr) -> Expr {
    Expr::Func {
        name: "jsonb".to_string(),
        args: vec![expr.clone()],
    }
}

/// Verbatim SQL, with no bind parameter. Used for the JSON type names and the NULL keyword inside the
/// CASE: routing those through `Expr::Value` would turn each into a placeholder, adding parameters and
/// making the expression unusable in an index.
fn sql_literal(sql: &str) -> Expr {
    Expr::Raw {
        sql: sql.to_string(),
        params: vec![],
    }
}

fn single(left: Expr, op: CompareOp, right: Expr) -> Conditions {
    Conditions {
        children: vec![ConditionNode::Comparison(Box::new(Comparison {
            left,
            op,
            right,
            negate: false,
        }))],
        connector: Connector::And,
        negated: false,
    }
}

fn with_child(field_ref: FieldRef, name: &str) -> FieldRef {
    let FieldRef {
        mut field,
        table_name,
        namespace,
    } = field_ref;
    append_child(&mut field, name);

    FieldRef {
        field,
        table_name,
        namespace,
    }
}

fn append_child(field: &mut FieldDef, name: &str) {
    match field.child.as_mut() {
        Some(child) => append_child(child, name),
        None => {
            field.child = Some(Box::new(FieldDef {
                name: name.to_string(),
                child: None,
            }))
        }
    }
}

fn strip_last(field: &mut FieldDef) -> String {
    let mut current = field;
    loop {
        let has_grandchild = current.child.as_ref().and_then(|c| c.child.as_ref()).is_some();
        if !has_grandchild {
            return current.child.take().map(|c| c.name).unwrap_or_default();
        }
        current = current.child.as_mut().unwrap();
    }
}
