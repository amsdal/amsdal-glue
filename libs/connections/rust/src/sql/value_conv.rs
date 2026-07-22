use pyo3::prelude::*;
use pyo3::IntoPyObjectExt;
use qcraft::ast::value::Value;

// ---------------------------------------------------------------------------
// PyValue definition (extracted from Python objects)
// ---------------------------------------------------------------------------

#[derive(Debug, Clone)]
pub enum PyValue {
    Null,
    Bool(bool),
    Int(i64),
    Float(f64),
    Str(String),
    Bytes(Vec<u8>),
    Date(String),
    DateTime(String),
    Time(String),
    List(Vec<PyValue>),
    Json(serde_json::Value),
    Decimal(String),
    UUID(String),
    TimeDelta {
        days: i64,
        seconds: i64,
        microseconds: i64,
    },
}

// ---------------------------------------------------------------------------
// PyValue → qcraft::Value
// ---------------------------------------------------------------------------

pub fn pyvalue_to_qcraft(val: &PyValue) -> Value {
    match val {
        PyValue::Null => Value::Null,
        PyValue::Bool(b) => Value::Bool(*b),
        PyValue::Int(i) => Value::Int(*i),
        PyValue::Float(f) => Value::Float(*f),
        PyValue::Str(s) => Value::Str(s.clone()),
        PyValue::Bytes(b) => Value::Bytes(b.clone()),
        PyValue::Date(s) => Value::Date(s.clone()),
        PyValue::DateTime(s) => Value::DateTime(s.clone()),
        PyValue::Time(s) => Value::Time(s.clone()),
        PyValue::Decimal(s) => Value::Decimal(s.clone()),
        PyValue::UUID(s) => Value::Uuid(s.clone()),
        PyValue::Json(j) => Value::Jsonb(serde_json::to_string(j).unwrap_or_default()),
        PyValue::List(items) => Value::Array(items.iter().map(pyvalue_to_qcraft).collect()),
        PyValue::TimeDelta {
            days,
            seconds,
            microseconds,
        } => Value::TimeDelta {
            years: 0,
            months: 0,
            days: *days,
            seconds: *seconds,
            microseconds: *microseconds,
        },
    }
}

// ---------------------------------------------------------------------------
// qcraft::Value → Python
// ---------------------------------------------------------------------------

/// Convert a top-level parameter. A JSON value here becomes a ``JsonValue`` marker for the connection
/// to bind (psycopg ``Jsonb`` / SQLite ``json.dumps``).
pub fn qcraft_value_to_py(py: Python, val: &Value) -> PyResult<PyObject> {
    value_to_py(py, val, true)
}

/// ``as_marker`` distinguishes a top-level parameter (where a JSON value must be marked so the binding
/// layer can wrap it) from a value NESTED inside an array. A nested value must be a plain Python object:
/// the whole array is bound as one JSON parameter (``json.dumps`` / a ``jsonb`` array dumper), so a
/// marker inside it would only break that serialisation.
fn value_to_py(py: Python, val: &Value, as_marker: bool) -> PyResult<PyObject> {
    match val {
        Value::Null => Ok(py.None()),
        Value::Bool(b) => Ok(b.into_py_any(py)?),
        Value::Int(i) => Ok(i.into_py_any(py)?),
        Value::BigInt(i) => Ok(i.into_py_any(py)?),
        Value::Float(f) => Ok(f.into_py_any(py)?),
        Value::Str(s) | Value::Date(s) | Value::DateTime(s) | Value::Time(s) => {
            Ok(s.into_py_any(py)?)
        }
        Value::Bytes(b) => Ok(b.into_py_any(py)?),
        Value::Decimal(s) => {
            let decimal_mod = py.import("decimal")?;
            let decimal_cls = decimal_mod.getattr("Decimal")?;
            let obj = decimal_cls.call1((s,))?;
            Ok(obj.into_py_any(py)?)
        }
        Value::Uuid(s) => {
            let uuid_mod = py.import("uuid")?;
            let uuid_cls = uuid_mod.getattr("UUID")?;
            let obj = uuid_cls.call1((s,))?;
            Ok(obj.into_py_any(py)?)
        }
        Value::TimeDelta {
            days,
            seconds,
            microseconds,
            ..
        } => {
            let dt_mod = py.import("datetime")?;
            let td_cls = dt_mod.getattr("timedelta")?;
            let kwargs = pyo3::types::PyDict::new(py);
            kwargs.set_item("days", days)?;
            kwargs.set_item("seconds", seconds)?;
            kwargs.set_item("microseconds", microseconds)?;
            let obj = td_cls.call((), Some(&kwargs))?;
            Ok(obj.into_py_any(py)?)
        }
        Value::Json(s) if as_marker => json_marker(py, s, "JSON"),
        Value::Jsonb(s) if as_marker => json_marker(py, s, "JSONB"),
        Value::Json(s) | Value::Jsonb(s) => json_text_to_py(py, s),
        Value::Array(items) => {
            // Array elements are always plain: the array is one JSON parameter, serialised whole.
            let py_items: PyResult<Vec<PyObject>> =
                items.iter().map(|v| value_to_py(py, v, false)).collect();
            Ok(py_items?.into_py_any(py)?)
        }
        Value::IpNetwork(s) => Ok(s.into_py_any(py)?),
        Value::Vector(v) => Ok(v.into_py_any(py)?),
    }
}

/// Parse JSON text into a Python object, falling back to the raw string when it is not valid JSON.
fn json_text_to_py(py: Python, text: &str) -> PyResult<PyObject> {
    let json_val: serde_json::Value =
        serde_json::from_str(text).unwrap_or_else(|_| serde_json::Value::String(text.to_string()));
    serde_json_to_py(py, &json_val)
}

/// A JSON-typed parameter crosses back as a ``JsonValue`` marker rather than as a bare dict/str/int.
///
/// The driver wrapper cannot be built here: `psycopg.types.json.Jsonb` is a psycopg object, and SQLite
/// has no JSON type at all. So the marker stays dialect-neutral and each connection binds it its own
/// way. A bare flattened value would leave the binding layer guessing from the Python type, which
/// only ever works for `dict`/`list`.
fn json_marker(py: Python, text: &str, scalar_type: &str) -> PyResult<PyObject> {
    let inner = json_text_to_py(py, text)?;

    let cls = py
        .import("amsdal_glue_core.common.data_models.json_value")?
        .getattr("JsonValue")?;
    let scalar = py
        .import("amsdal_glue_core.common.enums")?
        .getattr("ScalarType")?
        .getattr(scalar_type)?;

    Ok(cls.call1((inner, scalar))?.into_py_any(py)?)
}

// ---------------------------------------------------------------------------
// serde_json → Python
// ---------------------------------------------------------------------------

fn serde_json_to_py(py: Python, val: &serde_json::Value) -> PyResult<PyObject> {
    match val {
        serde_json::Value::Null => Ok(py.None()),
        serde_json::Value::Bool(b) => Ok(b.into_py_any(py)?),
        serde_json::Value::Number(n) => {
            if let Some(i) = n.as_i64() {
                Ok(i.into_py_any(py)?)
            } else if let Some(u) = n.as_u64() {
                Ok(u.into_py_any(py)?)
            } else {
                // An arbitrary-precision number that fits neither 64-bit integer type: a big int
                // (e.g. a snowflake id) or a float. Rebuild from the EXACT decimal text so a big
                // integer round-trips as a Python int, not a lossy float. Only a value with a
                // fractional / exponent part becomes a float.
                let text = n.to_string();
                if text.contains(['.', 'e', 'E']) {
                    let f: f64 = text.parse().unwrap_or(f64::NAN);
                    Ok(f.into_py_any(py)?)
                } else {
                    let int_obj = py.import("builtins")?.getattr("int")?.call1((text,))?;
                    Ok(int_obj.into_py_any(py)?)
                }
            }
        }
        serde_json::Value::String(s) => Ok(s.into_py_any(py)?),
        serde_json::Value::Array(items) => {
            let py_items: PyResult<Vec<PyObject>> =
                items.iter().map(|v| serde_json_to_py(py, v)).collect();
            Ok(py_items?.into_py_any(py)?)
        }
        serde_json::Value::Object(map) => {
            let dict = pyo3::types::PyDict::new(py);
            for (k, v) in map {
                dict.set_item(k, serde_json_to_py(py, v)?)?;
            }
            Ok(dict.into_py_any(py)?)
        }
    }
}

// ---------------------------------------------------------------------------
// Utility: fast hex encoding
// ---------------------------------------------------------------------------

const HEX_CHARS: &[u8; 16] = b"0123456789abcdef";

pub fn bytes_to_hex(bytes: &[u8]) -> String {
    let mut hex = String::with_capacity(bytes.len() * 2);
    for &b in bytes {
        hex.push(HEX_CHARS[(b >> 4) as usize] as char);
        hex.push(HEX_CHARS[(b & 0x0f) as usize] as char);
    }
    hex
}
