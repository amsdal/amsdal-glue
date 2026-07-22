use pyo3::exceptions::PyException;
use pyo3::{create_exception, PyErr};
use thiserror::Error;

// Python exception hierarchy: SqlGenError -> specific subclasses
create_exception!(amsdal_glue_history_core, PySqlGenError, PyException);
create_exception!(amsdal_glue_history_core, PyUnsupportedDialectError, PySqlGenError);
create_exception!(amsdal_glue_history_core, PyUnsupportedFeatureError, PySqlGenError);
create_exception!(amsdal_glue_history_core, PyInvalidValueError, PySqlGenError);
create_exception!(amsdal_glue_history_core, PyExtractionError, PySqlGenError);

#[derive(Error, Debug)]
pub enum SqlGenError {
    #[error("Unsupported dialect: {0}")]
    UnsupportedDialect(String),

    #[error("Unsupported feature: {0}")]
    UnsupportedFeature(String),

    #[error("Invalid value: {0}")]
    InvalidValue(String),

    #[error("Extraction error: {0}")]
    Extraction(String),
}

impl From<SqlGenError> for PyErr {
    fn from(err: SqlGenError) -> PyErr {
        match &err {
            SqlGenError::UnsupportedDialect(_) => PyUnsupportedDialectError::new_err(err.to_string()),
            SqlGenError::UnsupportedFeature(_) => PyUnsupportedFeatureError::new_err(err.to_string()),
            SqlGenError::InvalidValue(_) => PyInvalidValueError::new_err(err.to_string()),
            SqlGenError::Extraction(_) => PyExtractionError::new_err(err.to_string()),
        }
    }
}

impl From<qcraft::error::RenderError> for SqlGenError {
    fn from(err: qcraft::error::RenderError) -> Self {
        match err {
            qcraft::error::RenderError::Unsupported { feature, message } => {
                SqlGenError::UnsupportedFeature(format!("{feature}: {message}"))
            }
            qcraft::error::RenderError::Other(msg) => SqlGenError::UnsupportedFeature(msg),
        }
    }
}
