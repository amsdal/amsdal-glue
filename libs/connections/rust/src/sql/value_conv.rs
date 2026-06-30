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

pub fn qcraft_value_to_py(py: Python, val: &Value) -> PyResult<PyObject> {
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
        Value::Json(s) | Value::Jsonb(s) => {
            let json_val: serde_json::Value =
                serde_json::from_str(s).unwrap_or(serde_json::Value::String(s.clone()));
            serde_json_to_py(py, &json_val)
        }
        Value::Array(items) => {
            let py_items: PyResult<Vec<PyObject>> =
                items.iter().map(|v| qcraft_value_to_py(py, v)).collect();
            Ok(py_items?.into_py_any(py)?)
        }
        Value::IpNetwork(s) => Ok(s.into_py_any(py)?),
        Value::Vector(v) => Ok(v.into_py_any(py)?),
    }
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
            } else if let Some(f) = n.as_f64() {
                Ok(f.into_py_any(py)?)
            } else {
                Ok(py.None())
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
