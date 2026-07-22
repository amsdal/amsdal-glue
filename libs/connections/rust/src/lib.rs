use pyo3::prelude::*;

mod sql;

#[pymodule]
fn _sql_core(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add("__version__", "0.1.0")?;
    m.add_class::<sql::generator::SqlGenerator>()?;
    m.add("SqlGenError", m.py().get_type::<sql::error::PySqlGenError>())?;
    m.add("UnsupportedDialectError", m.py().get_type::<sql::error::PyUnsupportedDialectError>())?;
    m.add("UnsupportedFeatureError", m.py().get_type::<sql::error::PyUnsupportedFeatureError>())?;
    m.add("InvalidValueError", m.py().get_type::<sql::error::PyInvalidValueError>())?;
    m.add("ExtractionError", m.py().get_type::<sql::error::PyExtractionError>())?;
    Ok(())
}