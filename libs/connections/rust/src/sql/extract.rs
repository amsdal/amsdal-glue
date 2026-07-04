use pyo3::prelude::*;
use pyo3::types::{PyBool, PyBytes, PyDict, PyFloat, PyInt, PyList, PyNone, PyString, PyTuple};

use qcraft::ast::common::*;
use qcraft::ast::conditions::*;
use qcraft::ast::ddl::*;
use qcraft::ast::dml::*;
use qcraft::ast::expr::*;
use qcraft::ast::query::*;
use qcraft::ast::tcl::{LockMode as QLockMode, LockTableDef, LockTableStmt, TransactionStmt};
use qcraft::ast::value::Value;
use crate::sql::error::SqlGenError;
use crate::sql::value_conv::{bytes_to_hex, PyValue, pyvalue_to_qcraft};

// ---------------------------------------------------------------------------
// Top-level: QueryStatement
// ---------------------------------------------------------------------------

pub fn extract_query_stmt(ob: &Bound<PyAny>) -> PyResult<QueryStmt> {
    let (from, columns, distinct, set_op) = extract_from_and_columns(ob)?;
    let expressions = extract_optional_list(ob, "expressions", extract_select_expr)?;
    let joins = extract_optional_list(ob, "joins", extract_join_query)?;
    let where_clause = extract_optional_conditions(ob, "where")?;
    let group_by = extract_optional_list(ob, "group_by", extract_group_by)?;
    let having = extract_optional_conditions(ob, "having")?;
    let order_by = extract_optional_list(ob, "order_by", extract_order_by)?;
    let limit = extract_optional(ob, "limit", extract_limit)?;
    let ctes = extract_optional_list(ob, "ctes", extract_cte)?;
    let lock = extract_optional(ob, "lock", extract_select_lock)?;

    // Merge `only` columns and `expressions` into qcraft columns
    let mut all_columns = columns;
    if let Some(exprs) = expressions {
        for sel_expr in exprs {
            all_columns.push(SelectColumn::Expr {
                expr: sel_expr.0,
                alias: Some(sel_expr.1),
            });
        }
    }

    Ok(QueryStmt {
        ctes,
        columns: all_columns,
        distinct,
        from: from.map(|f| vec![f]),
        joins,
        where_clause,
        group_by,
        having,
        window: None,
        order_by,
        limit,
        lock: lock.map(|l| vec![l]),
        set_op,
    })
}

/// Extract FROM source, SELECT columns, and DISTINCT from the Python query object.
fn extract_from_and_columns(ob: &Bound<PyAny>) -> PyResult<(Option<FromItem>, Vec<SelectColumn>, Option<DistinctDef>, Option<Box<SetOpDef>>)> {
    let table_attr = ob.getattr(pyo3::intern!(ob.py(), "table"))?;
    let type_name: String = table_attr.get_type().qualname()?.extract()?;

    let only = extract_optional_list(ob, "only", extract_field_selection)?;
    let columns = match only {
        None => vec![SelectColumn::Star(None)],
        Some(fields) if fields.is_empty() => vec![],
        Some(fields) => fields,
    };

    let distinct = extract_optional(ob, "distinct", extract_distinct_clause)?;

    if type_name == "SetOperation" {
        // If the outer query has no extra clauses (order_by, limit, where, joins,
        // group_by, having), use set_op directly on QueryStmt (needed for CTE bodies).
        // Otherwise keep as FromItem::SetOp so the wrapper SELECT can apply those clauses.
        let has_extra = !ob.getattr(pyo3::intern!(ob.py(), "order_by"))?.is_none()
            || !ob.getattr(pyo3::intern!(ob.py(), "limit"))?.is_none()
            || !ob.getattr(pyo3::intern!(ob.py(), "where"))?.is_none()
            || !ob.getattr(pyo3::intern!(ob.py(), "joins"))?.is_none()
            || !ob.getattr(pyo3::intern!(ob.py(), "group_by"))?.is_none()
            || !ob.getattr(pyo3::intern!(ob.py(), "having"))?.is_none();

        if has_extra {
            let from = extract_from_item(&table_attr)?;
            Ok((Some(from), columns, distinct, None))
        } else {
            let set_op = extract_set_op(&table_attr)?;
            Ok((None, columns, distinct, Some(Box::new(set_op))))
        }
    } else {
        let from = extract_from_item(&table_attr)?;
        Ok((Some(from), columns, distinct, None))
    }
}

// ---------------------------------------------------------------------------
// FromItem / TableSource
// ---------------------------------------------------------------------------

fn extract_from_item(ob: &Bound<PyAny>) -> PyResult<FromItem> {
    let source = extract_table_source(ob)?;
    Ok(FromItem {
        source,
        only: false,
        sample: None,
        index_hint: None,
    })
}

fn extract_table_source(ob: &Bound<PyAny>) -> PyResult<TableSource> {
    let type_name: String = ob.get_type().qualname()?.extract()?;
    match type_name.as_str() {
        "SchemaReference" => Ok(TableSource::Table(extract_schema_ref(ob)?)),
        "SubQueryStatement" => Ok(TableSource::SubQuery(extract_sub_query(ob)?)),
        "SetOperation" => Ok(TableSource::SetOp(Box::new(extract_set_op(ob)?))),
        "FromValues" => extract_from_values(ob),
        other => Err(pyo3::exceptions::PyValueError::new_err(format!(
            "Unsupported table source type: {other}"
        ))),
    }
}

fn extract_schema_ref(ob: &Bound<PyAny>) -> PyResult<SchemaRef> {
    let name: String = ob.getattr(pyo3::intern!(ob.py(), "name"))?.extract()?;
    let alias = extract_optional_string(ob, "alias")?;
    let namespace = extract_optional_string(ob, "namespace")?;
    Ok(SchemaRef { name, alias, namespace })
}

// ---------------------------------------------------------------------------
// SubQuery / SetOperation
// ---------------------------------------------------------------------------

fn extract_sub_query(ob: &Bound<PyAny>) -> PyResult<SubQueryDef> {
    let query = extract_query_stmt(&ob.getattr(pyo3::intern!(ob.py(), "query"))?)?;
    let alias: String = ob.getattr(pyo3::intern!(ob.py(), "alias"))?.extract()?;
    Ok(SubQueryDef {
        query: Box::new(query),
        alias,
    })
}

fn extract_from_values(ob: &Bound<PyAny>) -> PyResult<TableSource> {
    let py_rows = ob.getattr(pyo3::intern!(ob.py(), "rows"))?;
    let alias: String = ob.getattr(pyo3::intern!(ob.py(), "alias"))?.extract()?;
    let col_names: Vec<String> = ob.getattr(pyo3::intern!(ob.py(), "columns"))?.extract()?;

    let mut rows: Vec<Vec<Expr>> = Vec::new();
    for py_row in py_rows.try_iter()? {
        let py_row = py_row?;
        let mut row: Vec<Expr> = Vec::new();
        for py_expr in py_row.try_iter()? {
            row.push(extract_expr(&py_expr?)?);
        }
        rows.push(row);
    }

    Ok(TableSource::Values {
        rows,
        alias,
        columns: col_names,
    })
}

fn extract_set_op(ob: &Bound<PyAny>) -> PyResult<SetOpDef> {
    let left = extract_query_stmt(&ob.getattr(pyo3::intern!(ob.py(), "left"))?)?;
    let right = extract_query_stmt(&ob.getattr(pyo3::intern!(ob.py(), "right"))?)?;
    let operation = extract_set_operation_type(&ob.getattr(pyo3::intern!(ob.py(), "operation"))?)?;
    Ok(SetOpDef {
        left: Box::new(left),
        right: Box::new(right),
        operation,
    })
}

// ---------------------------------------------------------------------------
// Field / FieldReference
// ---------------------------------------------------------------------------

/// Walk a FieldDef chain and remove the last child, returning its name.
/// e.g. data -> address -> city  =>  data -> address  +  "city"
/// e.g. data -> email            =>  data             +  "email"
fn strip_last_child(field: &mut FieldDef) -> String {
    if field.child.is_none() {
        // Single field (no child) — the field itself is the last key
        return field.name.clone();
    }
    let mut current = field;
    loop {
        let has_grandchild = current
            .child
            .as_ref()
            .map(|c| c.child.is_some())
            .unwrap_or(false);
        if !has_grandchild {
            // current.child is the last node
            let last = current.child.take().unwrap();
            return last.name;
        }
        current = current.child.as_mut().unwrap();
    }
}

fn extract_field_def(ob: &Bound<PyAny>) -> PyResult<FieldDef> {
    let name: String = ob.getattr(pyo3::intern!(ob.py(), "name"))?.extract()?;
    let child_attr = ob.getattr(pyo3::intern!(ob.py(), "child"))?;
    let child = if child_attr.is_none() {
        None
    } else {
        Some(Box::new(extract_field_def(&child_attr)?))
    };
    Ok(FieldDef { name, child })
}

fn extract_field_ref(ob: &Bound<PyAny>) -> PyResult<FieldRef> {
    let field = extract_field_def(&ob.getattr(pyo3::intern!(ob.py(), "field"))?)?;
    let table_name: String = ob.getattr(pyo3::intern!(ob.py(), "table_name"))?.extract()?;
    let namespace = extract_optional_string(ob, "namespace")?;
    Ok(FieldRef { field, table_name, namespace })
}

fn extract_field_selection(ob: &Bound<PyAny>) -> PyResult<SelectColumn> {
    let type_name: String = ob.get_type().qualname()?.extract()?;
    match type_name.as_str() {
        "FieldReferenceAliased" => {
            let field_ref = extract_field_ref(ob)?;
            let alias: String = ob.getattr(pyo3::intern!(ob.py(), "alias"))?.extract()?;
            Ok(SelectColumn::Field { field: field_ref, alias: Some(alias) })
        }
        _ => {
            let field_ref = extract_field_ref(ob)?;
            Ok(SelectColumn::Field { field: field_ref, alias: None })
        }
    }
}

// ---------------------------------------------------------------------------
// Distinct
// ---------------------------------------------------------------------------

fn extract_distinct_clause(ob: &Bound<PyAny>) -> PyResult<DistinctDef> {
    let on_fields_attr = ob.getattr(pyo3::intern!(ob.py(), "on_fields"))?;
    if on_fields_attr.is_none() {
        Ok(DistinctDef::Distinct)
    } else {
        let list: Vec<Expr> = extract_py_list(&on_fields_attr, |item| {
            let type_name: String = item.get_type().qualname()?.extract()?;
            let fr = match type_name.as_str() {
                "FieldReferenceAliased" => extract_field_ref(item)?,
                _ => extract_field_ref(item)?,
            };
            Ok(Expr::Field(fr))
        })?;
        Ok(DistinctDef::DistinctOn(list))
    }
}

// ---------------------------------------------------------------------------
// Expressions
// ---------------------------------------------------------------------------

pub fn extract_expr(ob: &Bound<PyAny>) -> PyResult<Expr> {
    let type_name: String = ob.get_type().qualname()?.extract()?;
    match type_name.as_str() {
        "Value" | "LazyValue" | "LazyTupleValue" => {
            let value_attr = ob.getattr(pyo3::intern!(ob.py(), "value"))?;
            if value_attr.is_instance_of::<PyTuple>() {
                extract_tuple_expr(&value_attr)
            } else {
                let val = extract_py_value(&value_attr)?;
                Ok(Expr::Value(pyvalue_to_qcraft(&val)))
            }
        }
        "FieldReferenceExpression" => {
            let field_ref = extract_field_ref(&ob.getattr(pyo3::intern!(ob.py(), "field_reference"))?)?;
            Ok(Expr::Field(field_ref))
        }
        "Combined" => {
            let left = extract_expr(&ob.getattr(pyo3::intern!(ob.py(), "left"))?)?;
            let operator: String = ob.getattr(pyo3::intern!(ob.py(), "operator"))?.extract()?;
            let right = extract_expr(&ob.getattr(pyo3::intern!(ob.py(), "right"))?)?;
            let op = match operator.as_str() {
                "+" => BinaryOp::Add,
                "-" => BinaryOp::Sub,
                "*" => BinaryOp::Mul,
                "/" => BinaryOp::Div,
                "%" => BinaryOp::Mod,
                "&" => BinaryOp::BitwiseAnd,
                "|" => BinaryOp::BitwiseOr,
                "<<" => BinaryOp::ShiftLeft,
                ">>" => BinaryOp::ShiftRight,
                "||" => BinaryOp::Concat,
                "**" => BinaryOp::Power,
                "^" => BinaryOp::BitwiseXor,
                _ => {
                    return Err(pyo3::exceptions::PyValueError::new_err(format!(
                        "Unknown combined expression operator: '{operator}'"
                    )))
                }
            };
            Ok(Expr::Binary {
                left: Box::new(left),
                op,
                right: Box::new(right),
            })
        }
        "JsonbArray" => {
            let args_attr = ob.getattr(pyo3::intern!(ob.py(), "args"))?;
            let items = extract_py_list(&args_attr, extract_expr)?;
            Ok(Expr::JsonArray(items))
        }
        "Now" => Ok(Expr::Now),
        "Func" | "Coalesce" | "Greatest" | "Least" | "Lower" | "Upper"
        | "SearchVector" | "SearchQuery" | "SearchRank" | "SearchHeadline" => {
            let name: String = ob.getattr(pyo3::intern!(ob.py(), "name"))?.extract()?;
            let args_attr = ob.getattr(pyo3::intern!(ob.py(), "args"))?;
            let args = extract_py_list(&args_attr, extract_expr)?;
            Ok(Expr::Func { name, args })
        }
        "Sum" | "Count" | "Avg" | "Min" | "Max" | "Aggregation" => {
            extract_aggregation_expr(ob)
        }
        "Cast" => {
            let expression = extract_expr(&ob.getattr(pyo3::intern!(ob.py(), "expression"))?)?;
            let to_type = extract_field_type_str(&ob.getattr(pyo3::intern!(ob.py(), "to_type"))?)?;
            Ok(Expr::Cast {
                expr: Box::new(expression),
                to_type,
            })
        }
        "JsonPathText" => {
            // JsonPathText wraps a FieldReferenceExpression with nested child fields.
            // We need to split: all children except the last use -> (Expr::Field),
            // and the last child becomes the path for ->> (Expr::JsonPathText).
            let inner = ob.getattr(pyo3::intern!(ob.py(), "expression"))?;
            let fr_attr = inner.getattr(pyo3::intern!(ob.py(), "field_reference"))?;
            let mut field_def = extract_field_def(&fr_attr.getattr(pyo3::intern!(ob.py(), "field"))?)?;
            let table_name: String = fr_attr.getattr(pyo3::intern!(ob.py(), "table_name"))?.extract()?;
            let namespace = extract_optional_string(&fr_attr, "namespace")?;

            // Walk to the last child, strip it off
            let last_key = strip_last_child(&mut field_def);

            let base = Expr::Field(FieldRef { field: field_def, table_name, namespace });
            Ok(Expr::JsonPathText {
                expr: Box::new(base),
                path: last_key,
            })
        }
        "Case" => {
            let cases_attr = ob.getattr(pyo3::intern!(ob.py(), "cases"))?;
            let cases = extract_py_list(&cases_attr, extract_when_clause)?;
            let default_attr = ob.getattr(pyo3::intern!(ob.py(), "default"))?;
            let default = if default_attr.is_none() {
                None
            } else {
                Some(Box::new(extract_expr(&default_attr)?))
            };
            Ok(Expr::Case(CaseDef { cases, default }))
        }
        "CurrentTimestamp" => Ok(Expr::CurrentTimestamp),
        "CurrentDate" => Ok(Expr::CurrentDate),
        "CurrentTime" => Ok(Expr::CurrentTime),
        "RawExpression" => {
            let value: String = ob.getattr(pyo3::intern!(ob.py(), "value"))?.extract()?;
            let params_attr = ob.getattr(pyo3::intern!(ob.py(), "params"))?;
            let params = if params_attr.is_none() {
                vec![]
            } else if params_attr.is_instance_of::<PyTuple>() {
                let tuple = params_attr.downcast::<PyTuple>()?;
                tuple
                    .iter()
                    .map(|item| {
                        let pv = extract_py_value(&item)?;
                        Ok(pyvalue_to_qcraft(&pv))
                    })
                    .collect::<PyResult<Vec<_>>>()?
            } else if params_attr.is_instance_of::<PyList>() {
                let list = params_attr.downcast::<PyList>()?;
                list.iter()
                    .map(|item| {
                        let pv = extract_py_value(&item)?;
                        Ok(pyvalue_to_qcraft(&pv))
                    })
                    .collect::<PyResult<Vec<_>>>()?
            } else {
                let type_name: String = params_attr.get_type().qualname()?.extract()?;
                return Err(pyo3::exceptions::PyTypeError::new_err(format!(
                    "RawExpression.params must be a tuple or list, got '{type_name}'"
                )));
            };
            Ok(Expr::Raw { sql: value, params })
        }
        "Window" => {
            let expression = extract_expr(&ob.getattr(pyo3::intern!(ob.py(), "expression"))?)?;
            let partition_by = extract_optional_list_expr(ob, "partition_by")?;
            let order_by = extract_optional_list(ob, "order_by", extract_order_by)?;
            let frame = extract_optional(ob, "frame", extract_window_frame)?;
            Ok(Expr::Window(WindowDef {
                expression: Box::new(expression),
                partition_by,
                order_by,
                frame,
            }))
        }
        "Exists" => {
            let subquery = extract_sub_query(&ob.getattr(pyo3::intern!(ob.py(), "subquery"))?)?;
            let negated: bool = ob.getattr(pyo3::intern!(ob.py(), "negated"))?.extract()?;
            // qcraft Expr::Exists wraps a QueryStmt; negation handled in conditions
            // For expression context, wrap in Unary::Not if negated
            let exists = Expr::Exists(subquery.query);
            if negated {
                Ok(Expr::Unary { op: UnaryOp::Not, expr: Box::new(exists) })
            } else {
                Ok(exists)
            }
        }
        "SubQueryStatement" => {
            let sub = extract_sub_query(ob)?;
            Ok(Expr::SubQuery(sub.query))
        }
        "ArraySubquery" => {
            let sub = extract_sub_query(&ob.getattr(pyo3::intern!(ob.py(), "subquery"))?)?;
            Ok(Expr::ArraySubQuery(sub.query))
        }
        "VectorExpression" | "L2Distance" | "InnerProduct"
        | "CosineDistance" | "L1Distance" => {
            let left = extract_expr(&ob.getattr(pyo3::intern!(ob.py(), "left"))?)?;
            let right = extract_expr(&ob.getattr(pyo3::intern!(ob.py(), "right"))?)?;
            let operator: String = ob.getattr(pyo3::intern!(ob.py(), "operator"))?.extract()?;
            let op = match operator.as_str() {
                "<->" => qcraft::qcraft_postgres::PgVectorOp::L2Distance.into(),
                "<#>" => qcraft::qcraft_postgres::PgVectorOp::InnerProduct.into(),
                "<=>" => qcraft::qcraft_postgres::PgVectorOp::CosineDistance.into(),
                "<+>" => qcraft::qcraft_postgres::PgVectorOp::L1Distance.into(),
                _ => {
                    return Err(pyo3::exceptions::PyValueError::new_err(format!(
                        "Unknown vector operator: {operator}"
                    )))
                }
            };
            Ok(Expr::Binary {
                left: Box::new(left),
                op,
                right: Box::new(right),
            })
        }
        "Collate" => {
            let expression = extract_expr(&ob.getattr(pyo3::intern!(ob.py(), "expression"))?)?;
            let collation: String = ob.getattr(pyo3::intern!(ob.py(), "collation"))?.extract()?;
            Ok(Expr::Collate {
                expr: Box::new(expression),
                collation,
            })
        }
        "TupleExpression" => {
            let items_attr = ob.getattr(pyo3::intern!(ob.py(), "items"))?;
            let items = extract_py_list(&items_attr, extract_expr)?;
            Ok(Expr::Tuple(items))
        }
        other => Err(pyo3::exceptions::PyValueError::new_err(format!(
            "Unsupported expression type: {other}"
        ))),
    }
}

fn extract_aggregation_expr(ob: &Bound<PyAny>) -> PyResult<Expr> {
    let name: String = ob.get_type().getattr(pyo3::intern!(ob.py(), "name"))?.extract()?;
    let expr_attr = ob.getattr(pyo3::intern!(ob.py(), "expression"))?;
    let expression = if expr_attr.is_none() {
        None
    } else {
        Some(Box::new(extract_expr(&expr_attr)?))
    };
    let distinct: bool = ob.getattr(pyo3::intern!(ob.py(), "distinct"))?.extract()?;
    let filter = extract_optional(ob, "filter", extract_conditions)?;
    let args = extract_optional_list(ob, "args", extract_expr)?;
    let order_by = extract_optional_list(ob, "order_by", extract_order_by)?;

    Ok(Expr::Aggregate(AggregationDef {
        name,
        expression,
        distinct,
        filter,
        args,
        order_by,
    }))
}

fn extract_when_clause(ob: &Bound<PyAny>) -> PyResult<WhenClause> {
    let condition = extract_conditions(&ob.getattr(pyo3::intern!(ob.py(), "condition"))?)?;
    let result = extract_expr(&ob.getattr(pyo3::intern!(ob.py(), "result"))?)?;
    Ok(WhenClause { condition, result })
}

fn extract_window_frame(ob: &Bound<PyAny>) -> PyResult<WindowFrameDef> {
    let frame_type = extract_window_frame_type(&ob.getattr(pyo3::intern!(ob.py(), "frame_type"))?)?;
    let start_attr = ob.getattr(pyo3::intern!(ob.py(), "start"))?;
    let start = if start_attr.is_none() {
        WindowFrameBound::Preceding(None) // UNBOUNDED PRECEDING
    } else {
        let n: i64 = start_attr.extract()?;
        i64_to_frame_bound(n, true)
    };
    let end_attr = ob.getattr(pyo3::intern!(ob.py(), "end"))?;
    let end = if end_attr.is_none() {
        Some(WindowFrameBound::CurrentRow)
    } else {
        let n: i64 = end_attr.extract()?;
        Some(i64_to_frame_bound(n, false))
    };
    Ok(WindowFrameDef {
        frame_type,
        start,
        end,
    })
}

fn i64_to_frame_bound(val: i64, _is_start: bool) -> WindowFrameBound {
    match val {
        0 => WindowFrameBound::CurrentRow,
        n if n > 0 => WindowFrameBound::Following(Some(n as u64)),
        n => WindowFrameBound::Preceding(Some((-n) as u64)),
    }
}

/// Extract FieldType as string representation for CAST
fn extract_field_type_str(ob: &Bound<PyAny>) -> PyResult<String> {
    let type_name: String = ob.get_type().qualname()?.extract()?;
    match type_name.as_str() {
        "ScalarType" => ob.getattr(pyo3::intern!(ob.py(), "value"))?.extract(),
        "CustomType" => ob.getattr(pyo3::intern!(ob.py(), "name"))?.extract(),
        other => Err(pyo3::exceptions::PyValueError::new_err(format!(
            "Unsupported FieldType for CAST: {other}"
        ))),
    }
}

fn extract_optional_list_expr(
    ob: &Bound<PyAny>,
    attr: &str,
) -> PyResult<Option<Vec<Expr>>> {
    let val = ob.getattr(attr)?;
    if val.is_none() {
        Ok(None)
    } else {
        Ok(Some(extract_py_list(&val, extract_expr)?))
    }
}

/// Convert a Python tuple recursively into `Expr::Tuple`.
/// Each element: tuple → nested Expr::Tuple, otherwise → Expr::Value.
fn extract_tuple_expr(ob: &Bound<PyAny>) -> PyResult<Expr> {
    let tuple = ob.downcast::<PyTuple>()?;
    let items: PyResult<Vec<Expr>> = tuple
        .iter()
        .map(|item| {
            if item.is_instance_of::<PyTuple>() {
                extract_tuple_expr(&item)
            } else {
                let py_val = extract_py_value(&item)?;
                Ok(Expr::Value(pyvalue_to_qcraft(&py_val)))
            }
        })
        .collect();
    Ok(Expr::Tuple(items?))
}

// ---------------------------------------------------------------------------
// Values
// ---------------------------------------------------------------------------

pub fn extract_py_value(ob: &Bound<PyAny>) -> PyResult<PyValue> {
    if ob.is_instance_of::<PyNone>() || ob.is_none() {
        return Ok(PyValue::Null);
    }
    if ob.is_instance_of::<PyBool>() {
        return Ok(PyValue::Bool(ob.extract()?));
    }
    if ob.is_instance_of::<PyInt>() {
        return match ob.extract::<i64>() {
            Ok(i) => Ok(PyValue::Int(i)),
            Err(_) => Ok(PyValue::Decimal(ob.str()?.extract()?)),
        };
    }
    if ob.is_instance_of::<PyFloat>() {
        return Ok(PyValue::Float(ob.extract()?));
    }
    if ob.is_instance_of::<PyString>() {
        return Ok(PyValue::Str(ob.extract()?));
    }
    if ob.is_instance_of::<PyBytes>() {
        return Ok(PyValue::Bytes(ob.extract()?));
    }
    if ob.is_instance_of::<PyList>() {
        let list = ob.downcast::<PyList>()?;
        let items: PyResult<Vec<PyValue>> = list.iter().map(|item| extract_py_value(&item)).collect();
        return Ok(PyValue::List(items?));
    }
    if ob.is_instance_of::<PyDict>() {
        let json_val = py_any_to_serde_json(ob)?;
        return Ok(PyValue::Json(json_val));
    }

    let type_name: String = ob.get_type().qualname()?.extract()?;
    match type_name.as_str() {
        "datetime" => Ok(PyValue::DateTime(ob.str()?.extract()?)),
        "date" => Ok(PyValue::Date(ob.str()?.extract()?)),
        "time" => Ok(PyValue::Time(ob.str()?.extract()?)),
        "Decimal" => Ok(PyValue::Decimal(ob.str()?.extract()?)),
        "UUID" => Ok(PyValue::UUID(ob.str()?.extract()?)),
        "timedelta" => {
            let days: i64 = ob.getattr(pyo3::intern!(ob.py(), "days"))?.extract()?;
            let seconds: i64 = ob.getattr(pyo3::intern!(ob.py(), "seconds"))?.extract()?;
            let microseconds: i64 = ob.getattr(pyo3::intern!(ob.py(), "microseconds"))?.extract()?;
            Ok(PyValue::TimeDelta {
                days,
                seconds,
                microseconds,
            })
        }
        "bytearray" => Ok(PyValue::Bytes(ob.extract()?)),
        "memoryview" => Ok(PyValue::Bytes(ob.call_method0("tobytes")?.extract()?)),
        "Vector" => {
            let values_attr = ob.getattr(pyo3::intern!(ob.py(), "values"))?;
            let values_list = values_attr.downcast::<PyList>()?;
            let mut floats: Vec<String> = Vec::with_capacity(values_list.len());
            for (i, item) in values_list.iter().enumerate() {
                if let Ok(f) = item.extract::<f64>() {
                    floats.push(f.to_string());
                } else if let Ok(i_val) = item.extract::<i64>() {
                    floats.push(i_val.to_string());
                } else {
                    let type_name: String = item.get_type().qualname()?.extract()?;
                    return Err(pyo3::exceptions::PyTypeError::new_err(format!(
                        "Vector values must be numeric, got '{}' at index {}",
                        type_name, i,
                    )));
                }
            }
            Ok(PyValue::Str(format!("[{}]", floats.join(","))))
        }
        _ => Err(pyo3::exceptions::PyValueError::new_err(format!(
            "Cannot convert Python value of type '{type_name}' to SQL parameter"
        ))),
    }
}

/// Convert any Python object to a serde_json::Value (recursive).
fn py_any_to_serde_json(ob: &Bound<PyAny>) -> PyResult<serde_json::Value> {
    if ob.is_none() || ob.is_instance_of::<PyNone>() {
        return Ok(serde_json::Value::Null);
    }
    if ob.is_instance_of::<PyBool>() {
        return Ok(serde_json::Value::Bool(ob.extract()?));
    }
    if ob.is_instance_of::<PyInt>() {
        let i: i64 = ob.extract()?;
        return Ok(serde_json::json!(i));
    }
    if ob.is_instance_of::<PyFloat>() {
        let f: f64 = ob.extract()?;
        return Ok(serde_json::json!(f));
    }
    if ob.is_instance_of::<PyString>() {
        let s: String = ob.extract()?;
        return Ok(serde_json::Value::String(s));
    }
    if ob.is_instance_of::<PyBytes>() {
        let b: Vec<u8> = ob.extract()?;
        let hex = bytes_to_hex(&b);
        return Ok(serde_json::Value::String(hex));
    }
    if ob.is_instance_of::<PyList>() {
        let list = ob.downcast::<PyList>()?;
        let items: PyResult<Vec<serde_json::Value>> =
            list.iter().map(|item| py_any_to_serde_json(&item)).collect();
        return Ok(serde_json::Value::Array(items?));
    }
    if ob.is_instance_of::<PyDict>() {
        let dict = ob.downcast::<PyDict>()?;
        let mut map = serde_json::Map::new();
        for (k, v) in dict.iter() {
            let key: String = k.str()?.extract()?;
            let val = py_any_to_serde_json(&v)?;
            map.insert(key, val);
        }
        return Ok(serde_json::Value::Object(map));
    }
    let s: String = ob.str()?.extract()?;
    Ok(serde_json::Value::String(s))
}

// ---------------------------------------------------------------------------
// Conditions
// ---------------------------------------------------------------------------

fn extract_condition(ob: &Bound<PyAny>) -> PyResult<Comparison> {
    let left = extract_expr(&ob.getattr(pyo3::intern!(ob.py(), "left"))?)?;
    let lookup = extract_compare_op(&ob.getattr(pyo3::intern!(ob.py(), "lookup"))?)?;
    let right = extract_expr(&ob.getattr(pyo3::intern!(ob.py(), "right"))?)?;
    let negate: bool = ob.getattr(pyo3::intern!(ob.py(), "negate"))?.extract()?;
    Ok(Comparison {
        left,
        op: lookup,
        right,
        negate,
    })
}

fn extract_condition_node(ob: &Bound<PyAny>) -> PyResult<ConditionNode> {
    let type_name: String = ob.get_type().qualname()?.extract()?;
    match type_name.as_str() {
        "Condition" => Ok(ConditionNode::Comparison(Box::new(extract_condition(ob)?))),
        "Conditions" => Ok(ConditionNode::Group(extract_conditions(ob)?)),
        "Exists" => {
            let subquery = extract_sub_query(&ob.getattr(pyo3::intern!(ob.py(), "subquery"))?)?;
            let negated: bool = ob.getattr(pyo3::intern!(ob.py(), "negated"))?.extract()?;
            if negated {
                // Wrap in negated group
                let exists_node = ConditionNode::Exists(subquery.query);
                Ok(ConditionNode::Group(Conditions {
                    children: vec![exists_node],
                    connector: Connector::And,
                    negated: true,
                }))
            } else {
                Ok(ConditionNode::Exists(subquery.query))
            }
        }
        other => Err(pyo3::exceptions::PyValueError::new_err(format!(
            "Unsupported condition node type: {other}"
        ))),
    }
}

pub fn extract_conditions(ob: &Bound<PyAny>) -> PyResult<Conditions> {
    let children_attr = ob.getattr(pyo3::intern!(ob.py(), "children"))?;
    let children = extract_py_list(&children_attr, extract_condition_node)?;
    let connector = extract_connector(&ob.getattr(pyo3::intern!(ob.py(), "connector"))?)?;
    let negated: bool = ob.getattr(pyo3::intern!(ob.py(), "negated"))?.extract()?;
    Ok(Conditions {
        children,
        connector,
        negated,
    })
}

/// Extract an optional `where`/`having` `Conditions`, filtering out an EMPTY condition group
/// (a `Conditions` with no children) so it renders no clause at all — never `WHERE NOT ()` or a
/// dangling `WHERE`. Guarding against building an empty group is otherwise the caller's job; this
/// only normalises the degenerate empty-group input to "no clause".
fn extract_optional_conditions(ob: &Bound<PyAny>, attr: &str) -> PyResult<Option<Conditions>> {
    match extract_optional(ob, attr, extract_conditions)? {
        Some(conditions) if conditions.children.is_empty() => Ok(None),
        other => Ok(other),
    }
}

// ---------------------------------------------------------------------------
// SelectExpression / GroupBy / CTE / SelectLock
// ---------------------------------------------------------------------------

fn extract_select_expr(ob: &Bound<PyAny>) -> PyResult<(Expr, String)> {
    let expression = extract_expr(&ob.getattr(pyo3::intern!(ob.py(), "expression"))?)?;
    let alias: String = ob.getattr(pyo3::intern!(ob.py(), "alias"))?.extract()?;
    Ok((expression, alias))
}

fn extract_group_by(ob: &Bound<PyAny>) -> PyResult<GroupByItem> {
    let expression = extract_expr(&ob.getattr(pyo3::intern!(ob.py(), "expression"))?)?;
    Ok(GroupByItem::Expr(expression))
}

fn extract_cte(ob: &Bound<PyAny>) -> PyResult<CteDef> {
    let name: String = ob.getattr(pyo3::intern!(ob.py(), "name"))?.extract()?;
    let query = extract_query_stmt(&ob.getattr(pyo3::intern!(ob.py(), "query"))?)?;
    let recursive: bool = ob.getattr(pyo3::intern!(ob.py(), "recursive"))?.extract()?;
    Ok(CteDef {
        name,
        query: Box::new(query),
        recursive,
        column_names: None,
        materialized: None,
    })
}

fn extract_select_lock(ob: &Bound<PyAny>) -> PyResult<SelectLockDef> {
    let strength = extract_lock_strength(&ob.getattr(pyo3::intern!(ob.py(), "strength"))?)?;
    let of_attr = ob.getattr(pyo3::intern!(ob.py(), "of"))?;
    let of = if of_attr.is_none() {
        None
    } else {
        Some(extract_py_list(&of_attr, extract_schema_ref)?)
    };
    let nowait: bool = ob.getattr(pyo3::intern!(ob.py(), "nowait"))?.extract()?;
    let skip_locked: bool = ob.getattr(pyo3::intern!(ob.py(), "skip_locked"))?.extract()?;
    Ok(SelectLockDef {
        strength,
        of,
        nowait,
        skip_locked,
        wait: None,
    })
}

// ---------------------------------------------------------------------------
// Enums
// ---------------------------------------------------------------------------

fn extract_enum_value(ob: &Bound<PyAny>) -> PyResult<String> {
    ob.getattr(pyo3::intern!(ob.py(), "value"))?.extract()
}

fn extract_connector(ob: &Bound<PyAny>) -> PyResult<Connector> {
    let val = extract_enum_value(ob)?;
    match val.as_str() {
        "AND" => Ok(Connector::And),
        "OR" => Ok(Connector::Or),
        _ => Err(pyo3::exceptions::PyValueError::new_err(format!(
            "Unknown FilterConnector: {val}"
        ))),
    }
}

fn extract_compare_op(ob: &Bound<PyAny>) -> PyResult<CompareOp> {
    let val = extract_enum_value(ob)?;
    match val.as_str() {
        "EXACT" | "EQ" => Ok(CompareOp::Eq),
        "NEQ" => Ok(CompareOp::Neq),
        "GT" => Ok(CompareOp::Gt),
        "GTE" => Ok(CompareOp::Gte),
        "LT" => Ok(CompareOp::Lt),
        "LTE" => Ok(CompareOp::Lte),
        "IN" => Ok(CompareOp::In),
        "CONTAINS" => Ok(CompareOp::Contains),
        "ICONTAINS" => Ok(CompareOp::IContains),
        "STARTSWITH" => Ok(CompareOp::StartsWith),
        "ISTARTSWITH" => Ok(CompareOp::IStartsWith),
        "ENDSWITH" => Ok(CompareOp::EndsWith),
        "IENDSWITH" => Ok(CompareOp::IEndsWith),
        "ISNULL" => Ok(CompareOp::IsNull),
        "REGEX" => Ok(CompareOp::Regex),
        "IREGEX" => Ok(CompareOp::IRegex),
        "BETWEEN" => Ok(CompareOp::Between),
        "JSONB_CONTAINS" => Ok(CompareOp::JsonbContains),
        "JSONB_CONTAINED_BY" => Ok(CompareOp::JsonbContainedBy),
        "JSONB_HAS_KEY" => Ok(CompareOp::JsonbHasKey),
        "JSONB_HAS_ANY_KEY" => Ok(CompareOp::JsonbHasAnyKey),
        "JSONB_HAS_ALL_KEYS" => Ok(CompareOp::JsonbHasAllKeys),
        "FTS_MATCH" => Ok(CompareOp::FtsMatch),
        "TRIGRAM_SIMILAR" => Ok(CompareOp::TrigramSimilar),
        "TRIGRAM_WORD_SIMILAR" => Ok(CompareOp::TrigramWordSimilar),
        "TRIGRAM_STRICT_WORD_SIMILAR" => Ok(CompareOp::TrigramStrictWordSimilar),
        "RANGE_CONTAINS" => Ok(CompareOp::RangeContains),
        "RANGE_CONTAINED_BY" => Ok(CompareOp::RangeContainedBy),
        "RANGE_OVERLAP" => Ok(CompareOp::RangeOverlap),
        "RANGE_STRICTLY_LEFT" => Ok(CompareOp::RangeStrictlyLeft),
        "RANGE_STRICTLY_RIGHT" => Ok(CompareOp::RangeStrictlyRight),
        "RANGE_NOT_LEFT" => Ok(CompareOp::RangeNotLeft),
        "RANGE_NOT_RIGHT" => Ok(CompareOp::RangeNotRight),
        "RANGE_ADJACENT" => Ok(CompareOp::RangeAdjacent),
        _ => Err(pyo3::exceptions::PyValueError::new_err(format!(
            "Unknown FieldLookup: {val}"
        ))),
    }
}

fn extract_join_type(ob: &Bound<PyAny>) -> PyResult<(JoinType, bool)> {
    let val = extract_enum_value(ob)?;
    match val.as_str() {
        "INNER" => Ok((JoinType::Inner, false)),
        "LEFT" => Ok((JoinType::Left, false)),
        "RIGHT" => Ok((JoinType::Right, false)),
        "FULL" => Ok((JoinType::Full, false)),
        "CROSS" => Ok((JoinType::Cross, false)),
        "INNER_LATERAL" => Ok((JoinType::Inner, true)),
        "LEFT_LATERAL" => Ok((JoinType::Left, true)),
        _ => Err(pyo3::exceptions::PyValueError::new_err(format!(
            "Unknown JoinType: {val}"
        ))),
    }
}

fn extract_order_direction(ob: &Bound<PyAny>) -> PyResult<OrderDir> {
    let val = extract_enum_value(ob)?;
    match val.as_str() {
        "ASC" => Ok(OrderDir::Asc),
        "DESC" => Ok(OrderDir::Desc),
        _ => Err(pyo3::exceptions::PyValueError::new_err(format!(
            "Unknown OrderDirection: {val}"
        ))),
    }
}

fn extract_window_frame_type(ob: &Bound<PyAny>) -> PyResult<WindowFrameType> {
    let val = extract_enum_value(ob)?;
    match val.as_str() {
        "rows" => Ok(WindowFrameType::Rows),
        "range" => Ok(WindowFrameType::Range),
        "groups" => Ok(WindowFrameType::Groups),
        _ => Err(pyo3::exceptions::PyValueError::new_err(format!(
            "Unknown WindowFrameType: {val}"
        ))),
    }
}

fn extract_set_operation_type(ob: &Bound<PyAny>) -> PyResult<SetOperationType> {
    let val = extract_enum_value(ob)?;
    match val.as_str() {
        "union" => Ok(SetOperationType::Union),
        "union_all" => Ok(SetOperationType::UnionAll),
        "intersect" => Ok(SetOperationType::Intersect),
        "except" => Ok(SetOperationType::Except),
        _ => Err(pyo3::exceptions::PyValueError::new_err(format!(
            "Unknown SetOperationType: {val}"
        ))),
    }
}

fn extract_lock_strength(ob: &Bound<PyAny>) -> PyResult<LockStrength> {
    let val = extract_enum_value(ob)?;
    match val.as_str() {
        "for_update" => Ok(LockStrength::Update),
        "for_no_key_update" => Ok(LockStrength::NoKeyUpdate),
        "for_share" => Ok(LockStrength::Share),
        "for_key_share" => Ok(LockStrength::KeyShare),
        _ => Err(pyo3::exceptions::PyValueError::new_err(format!(
            "Unknown LockStrength: {val}"
        ))),
    }
}

// ---------------------------------------------------------------------------
// Join
// ---------------------------------------------------------------------------

fn extract_join_query(ob: &Bound<PyAny>) -> PyResult<JoinDef> {
    let (join_type, lateral) = extract_join_type(&ob.getattr(pyo3::intern!(ob.py(), "join_type"))?)?;
    let on = extract_optional(ob, "on", extract_conditions)?;

    let table_attr = ob.getattr(pyo3::intern!(ob.py(), "table"))?;
    let mut from = extract_from_item(&table_attr)?;

    // Wrap in Lateral if needed
    if lateral {
        from = FromItem {
            source: TableSource::Lateral(Box::new(from)),
            only: false,
            sample: None,
            index_hint: None,
        };
    }

    Ok(JoinDef {
        source: from,
        condition: on.map(JoinCondition::On),
        join_type,
        natural: false,
    })
}

// ---------------------------------------------------------------------------
// Order By
// ---------------------------------------------------------------------------

fn extract_order_by(ob: &Bound<PyAny>) -> PyResult<OrderByDef> {
    let direction = extract_order_direction(&ob.getattr(pyo3::intern!(ob.py(), "direction"))?)?;
    let expr_attr = ob.getattr(pyo3::intern!(ob.py(), "expression"))?;
    let expr = if expr_attr.is_none() {
        let field = extract_field_ref(&ob.getattr(pyo3::intern!(ob.py(), "field"))?)?;
        Expr::Field(field)
    } else {
        extract_expr(&expr_attr)?
    };
    Ok(OrderByDef {
        expr,
        direction,
        nulls: None,
    })
}

// ---------------------------------------------------------------------------
// Limit
// ---------------------------------------------------------------------------

fn extract_limit(ob: &Bound<PyAny>) -> PyResult<LimitDef> {
    let limit: u64 = ob.getattr(pyo3::intern!(ob.py(), "limit"))?.extract()?;
    let offset: u64 = ob.getattr(pyo3::intern!(ob.py(), "offset"))?.extract()?;
    let with_ties: bool = ob.getattr(pyo3::intern!(ob.py(), "with_ties"))?.extract()?;

    let kind = if with_ties {
        LimitKind::FetchFirst { count: limit, with_ties: true, percent: false }
    } else {
        LimitKind::Limit(limit)
    };

    Ok(LimitDef {
        kind,
        offset: if offset > 0 { Some(offset) } else { None },
    })
}

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

fn extract_optional_string(ob: &Bound<PyAny>, attr: &str) -> PyResult<Option<String>> {
    let val = ob.getattr(attr)?;
    if val.is_none() {
        Ok(None)
    } else {
        Ok(Some(val.extract()?))
    }
}

fn extract_optional<T>(
    ob: &Bound<PyAny>,
    attr: &str,
    extractor: fn(&Bound<PyAny>) -> PyResult<T>,
) -> PyResult<Option<T>> {
    let val = ob.getattr(attr)?;
    if val.is_none() {
        Ok(None)
    } else {
        Ok(Some(extractor(&val)?))
    }
}

fn extract_optional_list<T>(
    ob: &Bound<PyAny>,
    attr: &str,
    extractor: fn(&Bound<PyAny>) -> PyResult<T>,
) -> PyResult<Option<Vec<T>>> {
    let val = ob.getattr(attr)?;
    if val.is_none() {
        Ok(None)
    } else {
        Ok(Some(extract_py_list(&val, extractor)?))
    }
}

fn extract_py_list<T>(
    ob: &Bound<PyAny>,
    extractor: fn(&Bound<PyAny>) -> PyResult<T>,
) -> PyResult<Vec<T>> {
    let list = ob.downcast::<PyList>()?;
    list.iter().map(|item| extractor(&item)).collect()
}

// ---------------------------------------------------------------------------
// Mutation extraction
// ---------------------------------------------------------------------------

pub fn extract_mutation(ob: &Bound<PyAny>) -> PyResult<MutationStmt> {
    let type_name: String = ob.get_type().qualname()?.extract()?;
    match type_name.as_str() {
        "InsertData" => Ok(MutationStmt::Insert(extract_insert(ob)?)),
        "InsertFromSelect" => Ok(MutationStmt::Insert(extract_insert_from_select(ob)?)),
        "UpdateData" => Ok(MutationStmt::Update(extract_update(ob)?)),
        "DeleteData" => Ok(MutationStmt::Delete(extract_delete(ob)?)),
        other => Err(pyo3::exceptions::PyValueError::new_err(format!(
            "Unsupported mutation type: {other}"
        ))),
    }
}


fn extract_insert(ob: &Bound<PyAny>) -> PyResult<InsertStmt> {
    let schema = extract_schema_ref(&ob.getattr(pyo3::intern!(ob.py(), "schema"))?)?;
    let data_list = ob.getattr(pyo3::intern!(ob.py(), "data"))?;
    let raw_rows = extract_py_list(&data_list, extract_data_row)?;

    if raw_rows.is_empty() {
        return Err(pyo3::exceptions::PyValueError::new_err(
            "INSERT requires at least one row",
        ));
    }

    // Extract column names from first row
    let col_names: Vec<String> = raw_rows[0].iter().map(|(k, _)| k.clone()).collect();

    // Build value rows
    let mut rows: Vec<Vec<Expr>> = Vec::with_capacity(raw_rows.len());
    for raw_row in &raw_rows {
        let mut values: Vec<Expr> = Vec::with_capacity(col_names.len());
        if raw_row.len() == col_names.len()
            && raw_row.iter().zip(col_names.iter()).all(|((k, _), c)| k == c)
        {
            // Fast path: same order
            for (_, v) in raw_row {
                values.push(Expr::Value(pyvalue_to_qcraft(v)));
            }
        } else {
            // Slow path: reorder by col_names
            let row_map: std::collections::HashMap<&str, &PyValue> =
                raw_row.iter().map(|(k, v)| (k.as_str(), v)).collect();
            for col in &col_names {
                let v = row_map.get(col.as_str()).copied().unwrap_or(&PyValue::Null);
                values.push(Expr::Value(pyvalue_to_qcraft(v)));
            }
        }
        rows.push(values);
    }

    let on_conflict_attr = ob.getattr(pyo3::intern!(ob.py(), "on_conflict"))?;
    let on_conflict = if on_conflict_attr.is_none() {
        None
    } else {
        Some(extract_on_conflict(&on_conflict_attr, &col_names)?)
    };
    let returning = extract_optional_returning(ob)?;

    let ctes = extract_optional_list(ob, "ctes", extract_cte)?;

    Ok(InsertStmt {
        table: schema,
        columns: Some(col_names),
        source: InsertSource::Values(rows),
        on_conflict: on_conflict.map(|oc| vec![oc]),
        returning,
        ctes,
        overriding: None,
        conflict_resolution: None,
        partition: None,
        ignore: false,
    })
}

fn extract_insert_from_select(ob: &Bound<PyAny>) -> PyResult<InsertStmt> {
    let schema = extract_schema_ref(&ob.getattr(pyo3::intern!(ob.py(), "schema"))?)?;
    let query = extract_query_stmt(&ob.getattr(pyo3::intern!(ob.py(), "query"))?)?;
    let columns = extract_optional_list(ob, "columns", extract_field_ref)?;
    let returning = extract_optional_returning(ob)?;

    let col_names = columns.map(|cols| cols.iter().map(|c| c.field.name.clone()).collect());

    Ok(InsertStmt {
        table: schema,
        columns: col_names,
        source: InsertSource::Select(Box::new(query)),
        on_conflict: None,
        returning,
        ctes: None,
        overriding: None,
        conflict_resolution: None,
        partition: None,
        ignore: false,
    })
}

fn extract_update(ob: &Bound<PyAny>) -> PyResult<UpdateStmt> {
    let schema = extract_schema_ref(&ob.getattr(pyo3::intern!(ob.py(), "schema"))?)?;
    let assignments = extract_update_assignments(ob)?;
    let where_clause = extract_optional(ob, "query", extract_conditions)?;
    let from_tables = extract_optional_list(ob, "from_tables", extract_table_source)?;
    let returning = extract_optional_returning(ob)?;
    let ctes = extract_optional_list(ob, "ctes", extract_cte)?;

    Ok(UpdateStmt {
        table: schema,
        assignments,
        from: from_tables,
        where_clause,
        returning,
        ctes,
        conflict_resolution: None,
        order_by: None,
        limit: None,
        offset: None,
        only: false,
        partition: None,
        ignore: false,
    })
}

fn extract_delete(ob: &Bound<PyAny>) -> PyResult<DeleteStmt> {
    let schema = extract_schema_ref(&ob.getattr(pyo3::intern!(ob.py(), "schema"))?)?;
    let where_clause = extract_optional(ob, "query", extract_conditions)?;
    let returning = extract_optional_returning(ob)?;
    let ctes = extract_optional_list(ob, "ctes", extract_cte)?;

    Ok(DeleteStmt {
        table: schema,
        using: None,
        where_clause,
        returning,
        ctes,
        order_by: None,
        limit: None,
        offset: None,
        only: false,
        partition: None,
        ignore: false,
    })
}

fn extract_returning_item(ob: &Bound<PyAny>) -> PyResult<SelectColumn> {
    let class_name: String = ob.get_type().qualname()?.extract()?;
    match class_name.as_str() {
        "FieldReference" => {
            let f = extract_field_ref(ob)?;
            if f.field.name == "*" {
                let table = if f.table_name.is_empty() {
                    None
                } else {
                    Some(f.table_name.clone())
                };
                Ok(SelectColumn::Star(table))
            } else {
                Ok(SelectColumn::Field {
                    field: f,
                    alias: None,
                })
            }
        }
        "SelectExpression" => {
            let (expr, alias) = extract_select_expr(ob)?;
            Ok(SelectColumn::Expr {
                expr,
                alias: Some(alias),
            })
        }
        _ => Err(pyo3::exceptions::PyTypeError::new_err(format!(
            "Unsupported returning item type: {class_name}"
        ))),
    }
}

fn extract_optional_returning(ob: &Bound<PyAny>) -> PyResult<Option<Vec<SelectColumn>>> {
    let val = ob.getattr("returning")?;
    if val.is_none() {
        return Ok(None);
    }
    let list = val.downcast::<pyo3::types::PyList>()?;
    if list.is_empty() {
        return Ok(None);
    }
    let items: Vec<SelectColumn> = list
        .iter()
        .map(|item| extract_returning_item(&item))
        .collect::<PyResult<_>>()?;
    Ok(Some(items))
}

fn extract_on_conflict(ob: &Bound<PyAny>, all_columns: &[String]) -> PyResult<OnConflictDef> {
    let fields_attr = ob.getattr(pyo3::intern!(ob.py(), "fields"))?;
    let fields = extract_py_list(&fields_attr, extract_field_ref)?;
    let action_str = extract_conflict_action(&ob.getattr(pyo3::intern!(ob.py(), "action"))?)?;
    let update_fields = extract_optional_list(ob, "update_fields", extract_field_ref)?;
    let where_clause = extract_optional(ob, "where", extract_conditions)?;

    let conflict_columns: Vec<String> = fields.iter().map(|f| f.field.name.clone()).collect();

    let target = Some(ConflictTarget::Columns {
        columns: conflict_columns.clone(),
        where_clause,
    });

    let action = match action_str.as_str() {
        "nothing" => ConflictAction::DoNothing,
        "update" => {
            let update_col_names: Vec<String> = match update_fields {
                Some(ref ufs) => ufs.iter().map(|f| f.field.name.clone()).collect(),
                None => {
                    // Auto-fill: all columns except conflict columns
                    all_columns
                        .iter()
                        .filter(|c| !conflict_columns.contains(c))
                        .cloned()
                        .collect()
                }
            };
            // Build assignments: col = EXCLUDED.col
            let assignments: Vec<(String, Expr)> = update_col_names
                .iter()
                .map(|col| {
                    (
                        col.clone(),
                        Expr::Field(FieldRef {
                            field: FieldDef { name: col.clone(), child: None },
                            table_name: "excluded".to_string(),
                            namespace: None,
                        }),
                    )
                })
                .collect();
            ConflictAction::DoUpdate {
                assignments,
                where_clause: None,
            }
        }
        other => {
            return Err(pyo3::exceptions::PyValueError::new_err(format!(
                "Unknown conflict action: '{other}'"
            )))
        }
    };

    Ok(OnConflictDef { target, action })
}

fn extract_data_row(ob: &Bound<PyAny>) -> PyResult<Vec<(String, PyValue)>> {
    let data_attr = ob.getattr(pyo3::intern!(ob.py(), "data"))?;
    let dict = data_attr.downcast::<PyDict>()?;
    let mut pairs = Vec::new();
    for (key, value) in dict.iter() {
        let col_name: String = key.extract()?;
        let py_val = extract_py_value(&value)?;
        pairs.push((col_name, py_val));
    }
    Ok(pairs)
}

fn extract_update_assignments(ob: &Bound<PyAny>) -> PyResult<Vec<(String, Expr)>> {
    let data_attr = ob.getattr(pyo3::intern!(ob.py(), "data"))?;
    let dict = data_attr.downcast::<PyDict>()?;
    let mut result = Vec::new();
    for (key, value) in dict.iter() {
        let col_name: String = key.extract()?;
        let expr = extract_expr(&value)?;
        result.push((col_name, expr));
    }
    Ok(result)
}

fn extract_conflict_action(ob: &Bound<PyAny>) -> PyResult<String> {
    extract_enum_value(ob)
}

// ---------------------------------------------------------------------------
// Schema mutation (DDL) extraction
// ---------------------------------------------------------------------------

pub fn extract_schema_mutation(ob: &Bound<PyAny>) -> PyResult<Vec<SchemaMutationStmt>> {
    let type_name: String = ob.get_type().qualname()?.extract()?;
    match type_name.as_str() {
        "RegisterSchema" => {
            let schema = extract_schema_def(&ob.getattr(pyo3::intern!(ob.py(), "schema"))?)?;
            let if_not_exists: bool = ob.getattr(pyo3::intern!(ob.py(), "if_not_exists"))?.extract()?;

            let mut stmts = vec![SchemaMutationStmt::CreateTable {
                schema: schema.clone(),
                if_not_exists,
                temporary: false,
                unlogged: false,
                tablespace: None,
                partition_by: None,
                inherits: None,
                using_method: None,
                with_options: None,
                on_commit: None,
                table_options: None,
                without_rowid: false,
                strict: false,
            }];

            // Emit indexes as separate CREATE INDEX statements
            if let Some(ref indexes) = schema.indexes {
                let schema_ref = SchemaRef {
                    name: schema.name.clone(),
                    alias: None,
                    namespace: schema.namespace.clone(),
                };
                for index in indexes {
                    stmts.push(SchemaMutationStmt::CreateIndex {
                        schema_ref: schema_ref.clone(),
                        index: index.clone(),
                        if_not_exists,
                        concurrently: false,
                    });
                }
            }

            Ok(stmts)
        }
        "DeleteSchema" => {
            let schema_ref = extract_schema_ref(&ob.getattr(pyo3::intern!(ob.py(), "schema_ref"))?)?;
            let if_exists: bool = ob.getattr(pyo3::intern!(ob.py(), "if_exists"))?.extract()?;
            let cascade: bool = ob.getattr(pyo3::intern!(ob.py(), "cascade"))?.extract()?;
            Ok(vec![SchemaMutationStmt::DropTable {
                schema_ref,
                if_exists,
                cascade,
            }])
        }
        "TruncateSchema" => {
            let schema_ref = extract_schema_ref(&ob.getattr(pyo3::intern!(ob.py(), "schema_ref"))?)?;
            let restart_identity: bool = ob.getattr(pyo3::intern!(ob.py(), "restart_identity"))?.extract()?;
            let cascade: bool = ob.getattr(pyo3::intern!(ob.py(), "cascade"))?.extract()?;
            Ok(vec![SchemaMutationStmt::TruncateTable {
                schema_ref,
                restart_identity,
                cascade,
            }])
        }
        "RenameSchema" => {
            let schema_ref = extract_schema_ref(&ob.getattr(pyo3::intern!(ob.py(), "schema_ref"))?)?;
            let new_name: String = ob.getattr(pyo3::intern!(ob.py(), "new_name"))?.extract()?;
            Ok(vec![SchemaMutationStmt::RenameTable {
                schema_ref,
                new_name,
            }])
        }
        "AddProperty" => {
            let schema_ref = extract_schema_ref(&ob.getattr(pyo3::intern!(ob.py(), "schema_ref"))?)?;
            let property = extract_property(&ob.getattr(pyo3::intern!(ob.py(), "property"))?)?;
            let col = property_to_column_def(&property)?;
            Ok(vec![SchemaMutationStmt::AddColumn {
                schema_ref,
                column: Box::new(col),
                if_not_exists: false,
                position: None,
            }])
        }
        "DeleteProperty" => {
            let schema_ref = extract_schema_ref(&ob.getattr(pyo3::intern!(ob.py(), "schema_ref"))?)?;
            let property_name: String = ob.getattr(pyo3::intern!(ob.py(), "property_name"))?.extract()?;
            Ok(vec![SchemaMutationStmt::DropColumn {
                schema_ref,
                name: property_name,
                if_exists: false,
                cascade: false,
            }])
        }
        "RenameProperty" => {
            let schema_ref = extract_schema_ref(&ob.getattr(pyo3::intern!(ob.py(), "schema_ref"))?)?;
            let old_name: String = ob.getattr(pyo3::intern!(ob.py(), "old_name"))?.extract()?;
            let new_name: String = ob.getattr(pyo3::intern!(ob.py(), "new_name"))?.extract()?;
            Ok(vec![SchemaMutationStmt::RenameColumn {
                schema_ref,
                old_name,
                new_name,
            }])
        }
        "UpdateProperty" => {
            let schema_ref = extract_schema_ref(&ob.getattr(pyo3::intern!(ob.py(), "schema_ref"))?)?;
            let property = extract_property(&ob.getattr(pyo3::intern!(ob.py(), "property"))?)?;
            let field_type = property_to_field_type(&property.field_type);

            let mut stmts = vec![SchemaMutationStmt::AlterColumnType {
                schema_ref: schema_ref.clone(),
                column_name: property.name.clone(),
                new_type: field_type,
                using_expr: None,
            }];

            stmts.push(SchemaMutationStmt::AlterColumnNullability {
                schema_ref: schema_ref.clone(),
                column_name: property.name.clone(),
                not_null: property.required,
            });

            stmts.push(SchemaMutationStmt::AlterColumnDefault {
                schema_ref,
                column_name: property.name,
                default: property.default,
            });

            Ok(stmts)
        }
        "AddConstraint" => {
            let schema_ref = extract_schema_ref(&ob.getattr(pyo3::intern!(ob.py(), "schema_ref"))?)?;
            let constraint = extract_constraint_def(&ob.getattr(pyo3::intern!(ob.py(), "constraint"))?)?;
            let not_valid: bool = ob.getattr(pyo3::intern!(ob.py(), "not_valid"))?.extract()?;
            Ok(vec![SchemaMutationStmt::AddConstraint {
                schema_ref,
                constraint,
                not_valid,
            }])
        }
        "DeleteConstraint" => {
            let schema_ref = extract_schema_ref(&ob.getattr(pyo3::intern!(ob.py(), "schema_ref"))?)?;
            let constraint_name: String = ob.getattr(pyo3::intern!(ob.py(), "constraint_name"))?.extract()?;
            Ok(vec![SchemaMutationStmt::DropConstraint {
                schema_ref,
                constraint_name,
                if_exists: false,
                cascade: false,
            }])
        }
        "ValidateConstraint" => {
            let schema_ref = extract_schema_ref(&ob.getattr(pyo3::intern!(ob.py(), "schema_ref"))?)?;
            let constraint_name: String = ob.getattr(pyo3::intern!(ob.py(), "constraint_name"))?.extract()?;
            Ok(vec![SchemaMutationStmt::ValidateConstraint {
                schema_ref,
                constraint_name,
            }])
        }
        "AddIndex" => {
            let schema_ref = extract_schema_ref(&ob.getattr(pyo3::intern!(ob.py(), "schema_ref"))?)?;
            let index = extract_index_def(&ob.getattr(pyo3::intern!(ob.py(), "index"))?)?;
            let if_not_exists: bool = ob.getattr(pyo3::intern!(ob.py(), "if_not_exists"))?.extract()?;
            let concurrent: bool = ob.getattr(pyo3::intern!(ob.py(), "concurrent"))?.extract()?;
            Ok(vec![SchemaMutationStmt::CreateIndex {
                schema_ref,
                index,
                if_not_exists,
                concurrently: concurrent,
            }])
        }
        "DeleteIndex" => {
            let schema_ref = extract_schema_ref(&ob.getattr(pyo3::intern!(ob.py(), "schema_ref"))?)?;
            let index_name: String = ob.getattr(pyo3::intern!(ob.py(), "index_name"))?.extract()?;
            let if_exists: bool = ob.getattr(pyo3::intern!(ob.py(), "if_exists"))?.extract()?;
            let concurrent: bool = ob.getattr(pyo3::intern!(ob.py(), "concurrent"))?.extract()?;
            Ok(vec![SchemaMutationStmt::DropIndex {
                schema_ref,
                index_name,
                if_exists,
                concurrently: concurrent,
                cascade: false,
            }])
        }
        "CreateExtension" => {
            let extension_name: String = ob.getattr(pyo3::intern!(ob.py(), "extension_name"))?.extract()?;
            let if_not_exists: bool = ob.getattr(pyo3::intern!(ob.py(), "if_not_exists"))?.extract()?;
            let schema_name: Option<String> = ob
                .getattr(pyo3::intern!(ob.py(), "schema_name"))
                .ok()
                .and_then(|v| if v.is_none() { None } else { v.extract().ok() });
            let version: Option<String> = ob
                .getattr(pyo3::intern!(ob.py(), "version"))
                .ok()
                .and_then(|v| if v.is_none() { None } else { v.extract().ok() });
            let cascade: bool = ob.getattr(pyo3::intern!(ob.py(), "cascade"))?.extract()?;
            Ok(vec![SchemaMutationStmt::CreateExtension {
                name: extension_name,
                if_not_exists,
                schema: schema_name,
                version,
                cascade,
            }])
        }
        "DropExtension" => {
            let extension_name: String = ob.getattr(pyo3::intern!(ob.py(), "extension_name"))?.extract()?;
            let if_exists: bool = ob.getattr(pyo3::intern!(ob.py(), "if_exists"))?.extract()?;
            let cascade: bool = ob.getattr(pyo3::intern!(ob.py(), "cascade"))?.extract()?;
            Ok(vec![SchemaMutationStmt::DropExtension {
                name: extension_name,
                if_exists,
                cascade,
            }])
        }
        "CreateCollation" => {
            let collation_name: String = ob.getattr(pyo3::intern!(ob.py(), "collation_name"))?.extract()?;
            let provider: String = ob.getattr(pyo3::intern!(ob.py(), "provider"))?.extract()?;
            if !matches!(provider.to_lowercase().as_str(), "icu" | "libc" | "builtin") {
                return Err(crate::sql::error::SqlGenError::InvalidValue(format!(
                    "Invalid collation provider: '{provider}'"
                ))
                .into());
            }
            let locale: String = ob.getattr(pyo3::intern!(ob.py(), "locale"))?.extract()?;
            let deterministic: bool = ob.getattr(pyo3::intern!(ob.py(), "deterministic"))?.extract()?;
            Ok(vec![SchemaMutationStmt::CreateCollation {
                name: collation_name,
                if_not_exists: true,
                locale: Some(locale),
                lc_collate: None,
                lc_ctype: None,
                provider: Some(provider),
                deterministic: Some(deterministic),
                from_collation: None,
            }])
        }
        "RemoveCollation" => {
            let collation_name: String = ob.getattr(pyo3::intern!(ob.py(), "collation_name"))?.extract()?;
            let if_exists: bool = ob.getattr(pyo3::intern!(ob.py(), "if_exists"))?.extract()?;
            Ok(vec![SchemaMutationStmt::DropCollation {
                name: collation_name,
                if_exists,
                cascade: false,
            }])
        }
        other => Err(pyo3::exceptions::PyValueError::new_err(format!(
            "Unsupported schema mutation type: {other}"
        ))),
    }
}


fn extract_schema_def(ob: &Bound<PyAny>) -> PyResult<SchemaDef> {
    let name: String = ob.getattr(pyo3::intern!(ob.py(), "name"))?.extract()?;
    let namespace = extract_optional_string(ob, "namespace")?;
    let properties_attr = ob.getattr(pyo3::intern!(ob.py(), "properties"))?;
    let properties = extract_py_list(&properties_attr, extract_property)?;
    let constraints_raw = extract_optional_list(ob, "constraints", |c| extract_constraint_def(c))?;
    let indexes_raw = extract_optional_list(ob, "indexes", |i| extract_index_def(i))?;

    // Convert properties to ColumnDefs
    let columns: Vec<ColumnDef> = properties
        .iter()
        .map(|p| property_to_column_def(p))
        .collect::<PyResult<Vec<_>>>()?;

    Ok(SchemaDef {
        name,
        namespace,
        columns,
        constraints: constraints_raw,
        indexes: indexes_raw,
        like_tables: None,
    })
}

// Internal property type (intermediate before converting to ColumnDef)
struct PropertyInfo {
    name: String,
    field_type: FieldTypeInfo,
    required: bool,
    default: Option<Expr>,
    generated: Option<Expr>,
    collation: Option<String>,
    identity: Option<IdentityInfo>,
}

#[derive(Clone)]
struct IdentityInfo {
    always: bool,
    start: Option<i64>,
    increment: Option<i64>,
    min_value: Option<i64>,
    max_value: Option<i64>,
    cycle: bool,
    cache: Option<i64>,
}

#[derive(Clone)]
enum FieldTypeInfo {
    Scalar(String),
    Custom { name: String, params: Option<Vec<(String, String)>> },
    Array(Box<FieldTypeInfo>),
    Vector(i64),
    Nested,
    Dict,
}

fn extract_optional_i64(obj: &Bound<PyAny>, attr: &str) -> Option<i64> {
    obj.getattr(attr)
        .ok()
        .and_then(|v| if v.is_none() { None } else { v.extract().ok() })
}

fn extract_identity_info(ob: &Bound<PyAny>) -> PyResult<Option<IdentityInfo>> {
    let identity_attr = ob.getattr(pyo3::intern!(ob.py(), "identity"));
    let identity_val = match identity_attr {
        Ok(v) if !v.is_none() => v,
        _ => return Ok(None),
    };

    // identity=True → default config
    if let Ok(flag) = identity_val.extract::<bool>() {
        return if flag {
            Ok(Some(IdentityInfo {
                always: false,
                start: None,
                increment: None,
                min_value: None,
                max_value: None,
                cycle: false,
                cache: None,
            }))
        } else {
            Ok(None)
        };
    }

    // identity=IdentityConfig(...)
    Ok(Some(IdentityInfo {
        always: identity_val
            .getattr(pyo3::intern!(ob.py(), "always"))
            .and_then(|v| v.extract())
            .unwrap_or(false),
        start: extract_optional_i64(&identity_val, "start"),
        increment: extract_optional_i64(&identity_val, "increment"),
        min_value: extract_optional_i64(&identity_val, "min_value"),
        max_value: extract_optional_i64(&identity_val, "max_value"),
        cycle: identity_val
            .getattr(pyo3::intern!(ob.py(), "cycle"))
            .and_then(|v| v.extract())
            .unwrap_or(false),
        cache: extract_optional_i64(&identity_val, "cache"),
    }))
}

fn extract_property(ob: &Bound<PyAny>) -> PyResult<PropertyInfo> {
    let name: String = ob.getattr(pyo3::intern!(ob.py(), "name"))?.extract()?;
    let field_type = extract_field_type_info(&ob.getattr(pyo3::intern!(ob.py(), "type"))?)?;
    let required: bool = ob.getattr(pyo3::intern!(ob.py(), "required"))?.extract()?;
    let default = extract_optional(ob, "default", extract_expr)?;
    let generated = extract_optional(ob, "generated", extract_expr)?;
    let collation: Option<String> = ob
        .getattr(pyo3::intern!(ob.py(), "db_collation"))
        .ok()
        .and_then(|v| if v.is_none() { None } else { v.extract().ok() });
    let identity = extract_identity_info(ob)?;
    Ok(PropertyInfo {
        name,
        field_type,
        required,
        default,
        generated,
        collation,
        identity,
    })
}

fn extract_field_type_info(ob: &Bound<PyAny>) -> PyResult<FieldTypeInfo> {
    let type_name: String = ob.get_type().qualname()?.extract()?;
    match type_name.as_str() {
        "ScalarType" => {
            let val: String = ob.getattr(pyo3::intern!(ob.py(), "value"))?.extract()?;
            Ok(FieldTypeInfo::Scalar(val))
        }
        "CustomType" => {
            let name: String = ob.getattr(pyo3::intern!(ob.py(), "name"))?.extract()?;
            let params_attr = ob.getattr(pyo3::intern!(ob.py(), "params"))?;
            let params = if params_attr.is_none() {
                None
            } else {
                let dict = params_attr.downcast::<PyDict>()?;
                let mut pairs = Vec::new();
                for (k, v) in dict.iter() {
                    let key: String = k.extract()?;
                    let val: String = v.str()?.extract()?;
                    pairs.push((key, val));
                }
                Some(pairs)
            };
            Ok(FieldTypeInfo::Custom { name, params })
        }
        "ArrayType" => {
            let item_type = extract_field_type_info(&ob.getattr(pyo3::intern!(ob.py(), "item_type"))?)?;
            Ok(FieldTypeInfo::Array(Box::new(item_type)))
        }
        "VectorType" => {
            let dimensions: i64 = ob.getattr(pyo3::intern!(ob.py(), "dimensions"))?.extract()?;
            Ok(FieldTypeInfo::Vector(dimensions))
        }
        "NestedType" => Ok(FieldTypeInfo::Nested),
        "DictType" => Ok(FieldTypeInfo::Dict),
        other => Err(pyo3::exceptions::PyValueError::new_err(format!(
            "Unsupported FieldType: {other}"
        ))),
    }
}

fn property_to_field_type(ft: &FieldTypeInfo) -> FieldType {
    match ft {
        FieldTypeInfo::Scalar(s) => FieldType::Scalar(s.clone()),
        FieldTypeInfo::Custom { name, params } => {
            let p: Vec<String> = params.as_ref().map_or_else(Vec::new, |pairs| {
                pairs.iter().map(|(_, v)| v.clone()).collect()
            });
            if p.is_empty() {
                FieldType::Scalar(name.clone())
            } else {
                FieldType::Parameterized { name: name.clone(), params: p }
            }
        }
        FieldTypeInfo::Array(inner) => FieldType::Array(Box::new(property_to_field_type(inner))),
        FieldTypeInfo::Vector(dims) => FieldType::Vector(*dims),
        FieldTypeInfo::Nested | FieldTypeInfo::Dict => FieldType::Scalar("jsonb".to_string()),
    }
}

fn identity_info_to_column(info: &IdentityInfo) -> qcraft::ast::ddl::IdentityColumn {
    qcraft::ast::ddl::IdentityColumn {
        always: info.always,
        start: info.start,
        increment: info.increment,
        min_value: info.min_value,
        max_value: info.max_value,
        cycle: info.cycle,
        cache: info.cache,
    }
}

fn property_to_column_def(prop: &PropertyInfo) -> PyResult<ColumnDef> {
    // Explicit identity property → GENERATED AS IDENTITY (SQL standard)
    // SERIAL types pass through as-is (PostgreSQL-specific)
    let field_type = property_to_field_type(&prop.field_type);
    let identity = prop.identity.as_ref().map(identity_info_to_column);
    let generated = prop.generated.as_ref().map(|expr| {
        qcraft::ast::ddl::GeneratedColumn {
            expr: expr.clone(),
            stored: true,
        }
    });
    Ok(ColumnDef {
        name: prop.name.clone(),
        field_type,
        not_null: prop.required,
        default: prop.default.clone(),
        generated,
        identity,
        collation: prop.collation.clone(),
        comment: None,
        storage: None,
        compression: None,
    })
}

fn extract_constraint_def(ob: &Bound<PyAny>) -> PyResult<ConstraintDef> {
    let type_name: String = ob.get_type().qualname()?.extract()?;
    match type_name.as_str() {
        "PrimaryKeyConstraint" => {
            let name: String = ob.getattr(pyo3::intern!(ob.py(), "name"))?.extract()?;
            let fields: Vec<String> = ob.getattr(pyo3::intern!(ob.py(), "fields"))?.extract()?;
            Ok(ConstraintDef::PrimaryKey {
                name: Some(name),
                columns: fields,
                include: None,
            })
        }
        "ForeignKeyConstraint" => {
            let name: String = ob.getattr(pyo3::intern!(ob.py(), "name"))?.extract()?;
            let fields: Vec<String> = ob.getattr(pyo3::intern!(ob.py(), "fields"))?.extract()?;
            let ref_schema_obj = ob.getattr(pyo3::intern!(ob.py(), "reference_schema"))?;
            let ref_schema_name: String = ref_schema_obj.getattr(pyo3::intern!(ref_schema_obj.py(), "name"))?.extract()?;
            let ref_namespace = extract_optional_string(&ref_schema_obj, "namespace")?;
            let ref_fields: Vec<String> = ob.getattr(pyo3::intern!(ob.py(), "reference_fields"))?.extract()?;
            let on_delete = extract_referential_action(&ob.getattr(pyo3::intern!(ob.py(), "on_delete"))?)?;
            let on_update = extract_referential_action(&ob.getattr(pyo3::intern!(ob.py(), "on_update"))?)?;

            let ref_table = SchemaRef {
                name: ref_schema_name,
                alias: None,
                namespace: ref_namespace,
            };

            Ok(ConstraintDef::ForeignKey {
                name: Some(name),
                columns: fields,
                ref_table,
                ref_columns: ref_fields,
                on_delete: Some(on_delete),
                on_update: Some(on_update),
                deferrable: None,
                match_type: None,
            })
        }
        "UniqueConstraint" => {
            let name: String = ob.getattr(pyo3::intern!(ob.py(), "name"))?.extract()?;
            let fields: Vec<String> = ob.getattr(pyo3::intern!(ob.py(), "fields"))?.extract()?;
            let condition = extract_optional(ob, "condition", extract_conditions)?;
            Ok(ConstraintDef::Unique {
                name: Some(name),
                columns: fields,
                include: None,
                nulls_distinct: None,
                condition,
            })
        }
        "CheckConstraint" => {
            let name: String = ob.getattr(pyo3::intern!(ob.py(), "name"))?.extract()?;
            let condition = extract_conditions(&ob.getattr(pyo3::intern!(ob.py(), "condition"))?)?;
            Ok(ConstraintDef::Check {
                name: Some(name),
                condition,
                no_inherit: false,
                enforced: None,
            })
        }
        "ExclusionConstraint" => {
            let name: String = ob.getattr(pyo3::intern!(ob.py(), "name"))?.extract()?;
            let elements_attr = ob.getattr(pyo3::intern!(ob.py(), "elements"))?;
            let elements = extract_py_list(&elements_attr, extract_exclusion_element)?;
            let index_method: String = ob.getattr(pyo3::intern!(ob.py(), "index_method"))?.extract()?;
            validate_index_method(&index_method)?;
            let condition = extract_optional(ob, "condition", extract_conditions)?;
            Ok(ConstraintDef::Exclusion {
                name: Some(name),
                elements,
                index_method,
                condition,
            })
        }
        other => Err(pyo3::exceptions::PyValueError::new_err(format!(
            "Unsupported constraint type: {other}"
        ))),
    }
}

fn extract_referential_action(ob: &Bound<PyAny>) -> PyResult<ReferentialAction> {
    let val = extract_enum_value(ob)?;
    match val.as_str() {
        "no_action" => Ok(ReferentialAction::NoAction),
        "restrict" => Ok(ReferentialAction::Restrict),
        "cascade" => Ok(ReferentialAction::Cascade),
        "set_null" => Ok(ReferentialAction::SetNull(None)),
        "set_default" => Ok(ReferentialAction::SetDefault(None)),
        _ => Err(pyo3::exceptions::PyValueError::new_err(format!(
            "Unknown ReferentialAction: {val}"
        ))),
    }
}

fn extract_index_def(ob: &Bound<PyAny>) -> PyResult<IndexDef> {
    let name: String = ob.getattr(pyo3::intern!(ob.py(), "name"))?.extract()?;
    let fields_attr = ob.getattr(pyo3::intern!(ob.py(), "fields"))?;
    let columns = extract_py_list(&fields_attr, extract_index_column)?;
    let unique: bool = ob.getattr(pyo3::intern!(ob.py(), "unique"))?.extract()?;
    let index_type = extract_index_type_str(&ob.getattr(pyo3::intern!(ob.py(), "index_type"))?)?;
    let include_attr = ob.getattr(pyo3::intern!(ob.py(), "include"))?;
    let include: Option<Vec<String>> = if include_attr.is_none() {
        None
    } else {
        Some(include_attr.extract()?)
    };
    let condition = extract_optional(ob, "condition", extract_conditions)?;
    let parameters_attr = ob.getattr(pyo3::intern!(ob.py(), "parameters"))?;
    let parameters: Option<Vec<(String, String)>> = if parameters_attr.is_none() {
        None
    } else {
        let dict = parameters_attr.downcast::<PyDict>()?;
        let mut pairs = Vec::new();
        for (k, v) in dict.iter() {
            let key: String = k.extract()?;
            let val: String = v.extract()?;
            pairs.push((key, val));
        }
        Some(pairs)
    };
    Ok(IndexDef {
        name,
        columns,
        unique,
        index_type,
        include,
        condition,
        parameters,
        tablespace: None,
        nulls_distinct: None,
    })
}

fn extract_index_column(ob: &Bound<PyAny>) -> PyResult<IndexColumnDef> {
    let name: String = ob.getattr(pyo3::intern!(ob.py(), "name"))?.extract()?;
    let direction = extract_order_direction(&ob.getattr(pyo3::intern!(ob.py(), "direction"))?)?;
    let op_class = extract_optional_string(ob, "op_class")?;
    Ok(IndexColumnDef {
        expr: IndexExpr::Column(name),
        direction: Some(direction),
        nulls: None,
        opclass: op_class,
        collation: None,
    })
}

fn extract_index_type_str(ob: &Bound<PyAny>) -> PyResult<Option<String>> {
    let type_name: String = ob.get_type().qualname()?.extract()?;
    match type_name.as_str() {
        "BuiltinIndexType" => {
            let val: String = ob.getattr(pyo3::intern!(ob.py(), "value"))?.extract()?;
            Ok(Some(val))
        }
        "CustomIndexType" => {
            let name: String = ob.getattr(pyo3::intern!(ob.py(), "name"))?.extract()?;
            Ok(Some(name))
        }
        "NoneType" => Ok(None),
        other => Err(pyo3::exceptions::PyValueError::new_err(format!(
            "Unknown index type: '{other}'"
        ))),
    }
}

fn validate_exclusion_operator(op: &str) -> PyResult<()> {
    // Only allow known SQL operators to prevent SQL injection
    let valid = matches!(
        op,
        "=" | "<>" | "!=" | "<" | ">" | "<=" | ">=" | "&&" | "&<" | "&>" | "<<" | ">>"
            | "-|-" | "~=" | "@>" | "<@" | "WITH =" | "WITH <>" | "WITH &&" | "WITH @>"
            | "WITH <@" | "WITH -|-" | "WITH <<" | "WITH >>" | "WITH &<" | "WITH &>"
    );
    if !valid {
        return Err(crate::sql::error::SqlGenError::InvalidValue(format!(
            "Invalid exclusion operator: '{op}'"
        ))
        .into());
    }
    Ok(())
}

fn validate_index_method(method: &str) -> PyResult<()> {
    let valid = matches!(
        method.to_lowercase().as_str(),
        "btree" | "hash" | "gist" | "spgist" | "gin" | "brin"
    );
    if !valid {
        return Err(crate::sql::error::SqlGenError::InvalidValue(format!(
            "Invalid index method: '{method}'"
        ))
        .into());
    }
    Ok(())
}

fn extract_exclusion_element(ob: &Bound<PyAny>) -> PyResult<ExclusionElement> {
    let field: String = ob.getattr(pyo3::intern!(ob.py(), "field"))?.extract()?;
    let operator: String = ob.getattr(pyo3::intern!(ob.py(), "operator"))?.extract()?;
    validate_exclusion_operator(&operator)?;
    Ok(ExclusionElement {
        column: field,
        operator,
        opclass: None,
    })
}

// ---------------------------------------------------------------------------
// LockCommand extraction
// ---------------------------------------------------------------------------
//
// LockCommand — the glue-core dataclass for non-row locks (advisory + table).
// Row-level SELECT FOR UPDATE lives on QueryStatement.lock and is not handled
// here.
//
// Extraction outcome:
//   - All ``LockIdentifier`` targets → ``LockStmt::AdvisoryQuery``
//     (SELECT pg_(try_)advisory(_unlock)?[_shared](hashtextextended(?, 0))).
//   - All ``SchemaReference`` targets → ``LockStmt::TableLock``
//     (TransactionStmt::LockTable rendering to LOCK TABLE … IN <mode> MODE).
//   - Mixed-target command is rejected — two different SQL kinds can't share
//     one statement.
//
// ``timeout`` is rejected for advisory (PG `lock_timeout` does not apply to
// advisory locks); NOWAIT is the only non-blocking option there.  Table-lock
// timeout support is deferred.

/// Extracted lock statement — either a SELECT of advisory-lock functions or
/// a TransactionStmt::LockTable.  Generator dispatches to the appropriate
/// renderer path based on which variant.
pub enum LockStmt {
    AdvisoryQuery(QueryStmt),
    TableLock(TransactionStmt),
}

enum LockRefInner {
    Identifier(String),
    Schema(SchemaRef),
}

pub fn extract_lock_command(ob: &Bound<PyAny>) -> PyResult<LockStmt> {
    let action = extract_enum_value(&ob.getattr(pyo3::intern!(ob.py(), "action"))?)?;
    let mode = extract_enum_value(&ob.getattr(pyo3::intern!(ob.py(), "mode"))?)?;
    let parameter = extract_enum_value(&ob.getattr(pyo3::intern!(ob.py(), "parameter"))?)?;
    let scope = extract_enum_value(&ob.getattr(pyo3::intern!(ob.py(), "scope"))?)?;
    let timeout = extract_optional_f64(ob, "timeout")?;

    let locked_attr = ob.getattr(pyo3::intern!(ob.py(), "locked_objects"))?;
    let locked_list = locked_attr.downcast::<PyList>()?;
    if locked_list.is_empty() {
        return Err(SqlGenError::InvalidValue(
            "LockCommand.locked_objects cannot be empty".to_string(),
        )
        .into());
    }

    let refs: Vec<LockRefInner> = locked_list
        .iter()
        .map(|item| extract_lock_reference_inner(&item))
        .collect::<PyResult<Vec<_>>>()?;

    let all_identifiers = refs.iter().all(|r| matches!(r, LockRefInner::Identifier(_)));
    let all_schemas = refs.iter().all(|r| matches!(r, LockRefInner::Schema(_)));

    if !all_identifiers && !all_schemas {
        return Err(SqlGenError::UnsupportedFeature(
            "LockCommand with mixed LockIdentifier and SchemaReference targets is not supported"
                .to_string(),
        )
        .into());
    }

    if all_identifiers {
        build_advisory_query(&action, &mode, &parameter, &scope, timeout, &refs)
    } else {
        build_table_lock(&action, &mode, &parameter, timeout, &refs)
    }
}

fn extract_lock_reference_inner(ob: &Bound<PyAny>) -> PyResult<LockRefInner> {
    let inner = ob.getattr(pyo3::intern!(ob.py(), "reference"))?;
    let type_name: String = inner.get_type().qualname()?.extract()?;
    match type_name.as_str() {
        "LockIdentifier" => {
            let key: String = inner.getattr(pyo3::intern!(inner.py(), "key"))?.extract()?;
            Ok(LockRefInner::Identifier(key))
        }
        "SchemaReference" => Ok(LockRefInner::Schema(extract_schema_ref(&inner)?)),
        other => Err(SqlGenError::UnsupportedFeature(format!(
            "Unsupported LockReference.reference type: {other}"
        ))
        .into()),
    }
}

fn build_advisory_query(
    action: &str,
    mode: &str,
    parameter: &str,
    scope: &str,
    timeout: Option<f64>,
    refs: &[LockRefInner],
) -> PyResult<LockStmt> {
    if timeout.is_some() {
        return Err(SqlGenError::UnsupportedFeature(
            "PG advisory locks do not respect lock_timeout; use parameter=NOWAIT for non-blocking"
                .to_string(),
        )
        .into());
    }
    if parameter == "SKIP_LOCKED" {
        return Err(SqlGenError::UnsupportedFeature(
            "SKIP_LOCKED is not applicable to advisory locks".to_string(),
        )
        .into());
    }
    if action == "RELEASE" && scope == "TRANSACTION" {
        return Err(SqlGenError::UnsupportedFeature(
            "RELEASE on a TRANSACTION-scoped advisory lock is invalid: \
             pg_advisory_xact_lock auto-releases at commit/rollback and \
             has no unlock counterpart"
                .to_string(),
        )
        .into());
    }

    let fn_name = advisory_fn_name(action, mode, parameter, scope)?;

    let columns: Vec<SelectColumn> = refs
        .iter()
        .map(|r| match r {
            LockRefInner::Identifier(key) => SelectColumn::Expr {
                expr: Expr::Func {
                    name: fn_name.to_string(),
                    args: vec![Expr::Func {
                        name: "hashtextextended".to_string(),
                        args: vec![
                            Expr::Value(Value::Str(key.clone())),
                            Expr::Value(Value::Int(0)),
                        ],
                    }],
                },
                alias: None,
            },
            LockRefInner::Schema(_) => unreachable!("classified as advisory-only above"),
        })
        .collect();

    Ok(LockStmt::AdvisoryQuery(QueryStmt {
        columns,
        ..QueryStmt::default()
    }))
}

fn advisory_fn_name(
    action: &str,
    mode: &str,
    parameter: &str,
    scope: &str,
) -> PyResult<&'static str> {
    match (action, mode, parameter, scope) {
        // SESSION-scoped acquire — caller must explicitly RELEASE.
        ("ACQUIRE", "EXCLUSIVE", "NOWAIT", "SESSION") => Ok("pg_try_advisory_lock"),
        ("ACQUIRE", "EXCLUSIVE", "WAIT", "SESSION") => Ok("pg_advisory_lock"),
        ("ACQUIRE", "SHARED", "NOWAIT", "SESSION") => Ok("pg_try_advisory_lock_shared"),
        ("ACQUIRE", "SHARED", "WAIT", "SESSION") => Ok("pg_advisory_lock_shared"),
        // TRANSACTION-scoped acquire — auto-released at commit/rollback.
        ("ACQUIRE", "EXCLUSIVE", "NOWAIT", "TRANSACTION") => Ok("pg_try_advisory_xact_lock"),
        ("ACQUIRE", "EXCLUSIVE", "WAIT", "TRANSACTION") => Ok("pg_advisory_xact_lock"),
        ("ACQUIRE", "SHARED", "NOWAIT", "TRANSACTION") => Ok("pg_try_advisory_xact_lock_shared"),
        ("ACQUIRE", "SHARED", "WAIT", "TRANSACTION") => Ok("pg_advisory_xact_lock_shared"),
        // RELEASE — only valid for SESSION scope (TRANSACTION rejected upstream).
        ("RELEASE", "EXCLUSIVE", _, "SESSION") => Ok("pg_advisory_unlock"),
        ("RELEASE", "SHARED", _, "SESSION") => Ok("pg_advisory_unlock_shared"),
        _ => Err(SqlGenError::UnsupportedFeature(format!(
            "advisory lock: action={action}, mode={mode}, parameter={parameter}, \
             scope={scope} not supported"
        ))
        .into()),
    }
}

fn build_table_lock(
    action: &str,
    mode: &str,
    parameter: &str,
    _timeout: Option<f64>,
    refs: &[LockRefInner],
) -> PyResult<LockStmt> {
    if action != "ACQUIRE" {
        return Err(SqlGenError::UnsupportedFeature(
            "LOCK TABLE cannot be explicitly released; tables unlock on transaction end"
                .to_string(),
        )
        .into());
    }
    let qmode = match mode {
        "EXCLUSIVE" => QLockMode::Exclusive,
        "SHARED" => QLockMode::Share,
        other => {
            return Err(SqlGenError::UnsupportedFeature(format!(
                "LOCK TABLE mode={other} not supported"
            ))
            .into())
        }
    };
    let nowait = parameter == "NOWAIT";

    let tables: Vec<LockTableDef> = refs
        .iter()
        .map(|r| match r {
            LockRefInner::Schema(schema_ref) => LockTableDef {
                table: schema_ref.name.clone(),
                schema: schema_ref.namespace.clone(),
                mode: qmode,
                only: false,
                alias: schema_ref.alias.clone(),
                wait: None,
                partition: None,
            },
            LockRefInner::Identifier(_) => unreachable!("classified as schema-only above"),
        })
        .collect();

    Ok(LockStmt::TableLock(TransactionStmt::LockTable(
        LockTableStmt { tables, nowait },
    )))
}

fn extract_optional_f64(ob: &Bound<PyAny>, attr: &str) -> PyResult<Option<f64>> {
    let val = ob.getattr(attr)?;
    if val.is_none() {
        Ok(None)
    } else {
        Ok(Some(val.extract()?))
    }
}
