use pyo3::prelude::*;
use pyo3::IntoPyObjectExt;

use qcraft::ast::value::Value;
use qcraft::render::ctx::ParamStyle;

use crate::sql::error::SqlGenError;
use crate::sql::extract;
use crate::sql::value_conv::qcraft_value_to_py;

// ---------------------------------------------------------------------------
// Renderer wrapper
// ---------------------------------------------------------------------------

enum RendererKind {
    Postgres(qcraft::qcraft_postgres::PostgresRenderer),
    Sqlite(qcraft::qcraft_sqlite::SqliteRenderer),
}

impl RendererKind {
    fn name(&self) -> &str {
        match self {
            RendererKind::Postgres(_) => "postgresql",
            RendererKind::Sqlite(_) => "sqlite",
        }
    }

    fn render_query(
        &self,
        stmt: &qcraft::ast::query::QueryStmt,
    ) -> Result<(String, Vec<Value>), SqlGenError> {
        match self {
            RendererKind::Postgres(r) => Ok(r.render_query_stmt(stmt)?),
            RendererKind::Sqlite(r) => Ok(r.render_query_stmt(stmt)?),
        }
    }

    fn render_mutation(
        &self,
        stmt: &qcraft::ast::dml::MutationStmt,
    ) -> Result<(String, Vec<Value>), SqlGenError> {
        match self {
            RendererKind::Postgres(r) => Ok(r.render_mutation_stmt(stmt)?),
            RendererKind::Sqlite(r) => Ok(r.render_mutation_stmt(stmt)?),
        }
    }

    fn render_schema(
        &self,
        stmt: &qcraft::ast::ddl::SchemaMutationStmt,
    ) -> Result<Vec<(String, Vec<Value>)>, SqlGenError> {
        match self {
            RendererKind::Postgres(r) => Ok(r.render_schema_stmt(stmt)?),
            RendererKind::Sqlite(r) => Ok(r.render_schema_stmt(stmt)?),
        }
    }

    fn render_transaction(
        &self,
        stmt: &qcraft::ast::tcl::TransactionStmt,
    ) -> Result<(String, Vec<Value>), SqlGenError> {
        match self {
            RendererKind::Postgres(r) => Ok(r.render_transaction_stmt(stmt)?),
            RendererKind::Sqlite(r) => Ok(r.render_transaction_stmt(stmt)?),
        }
    }

    fn render_lock(
        &self,
        stmt: &extract::LockStmt,
    ) -> Result<(String, Vec<Value>), SqlGenError> {
        // SQLite has no advisory locks and no LOCK TABLE — reject up front
        // instead of letting extraction succeed and rendering fail late.
        if matches!(self, RendererKind::Sqlite(_)) {
            return Err(SqlGenError::UnsupportedFeature(
                "LockCommand is not supported by the SQLite dialect".to_string(),
            ));
        }
        match stmt {
            extract::LockStmt::AdvisoryQuery(q) => self.render_query(q),
            extract::LockStmt::TableLock(t) => self.render_transaction(t),
        }
    }
}

// ---------------------------------------------------------------------------
// Helper: convert qcraft Value vec → Python list
// ---------------------------------------------------------------------------

fn values_to_py_list(py: Python, values: Vec<Value>) -> PyResult<PyObject> {
    let py_items: PyResult<Vec<PyObject>> =
        values.iter().map(|v| qcraft_value_to_py(py, v)).collect();
    py_items?.into_py_any(py)
}

// ---------------------------------------------------------------------------
// PyO3 class
// ---------------------------------------------------------------------------

#[pyclass]
pub struct SqlGenerator {
    renderer: RendererKind,
    param_style_name: &'static str,
}

#[pymethods]
impl SqlGenerator {
    #[new]
    #[pyo3(signature = (dialect, *, param_style=None, use_json_operators=false))]
    fn new(dialect: &str, param_style: Option<&str>, use_json_operators: bool) -> PyResult<Self> {
        let _ = use_json_operators; // kept for API compat, qcraft handles this per-renderer

        let (renderer, default_style_name) = match dialect {
            "postgresql" | "postgres" => {
                let qcraft_style = match param_style {
                    Some("dollar") => ParamStyle::Dollar,
                    Some("format") | Some("pyformat") => ParamStyle::Percent,
                    Some("qmark") => ParamStyle::QMark,
                    Some(s) => {
                        return Err(SqlGenError::UnsupportedFeature(format!(
                            "Unknown param_style: '{s}'. Use 'dollar', 'format', or 'qmark'"
                        ))
                        .into())
                    }
                    None => ParamStyle::Percent, // default for postgres: format (%s)
                };
                let style_name = match qcraft_style {
                    ParamStyle::Dollar => "dollar",
                    ParamStyle::Percent => "format",
                    ParamStyle::QMark => "qmark",
                };
                let r = qcraft::qcraft_postgres::PostgresRenderer::new().with_param_style(qcraft_style);
                (RendererKind::Postgres(r), style_name)
            }
            "sqlite" => {
                if let Some(s) = param_style {
                    if s != "qmark" {
                        return Err(SqlGenError::UnsupportedFeature(format!(
                            "SQLite only supports 'qmark' param_style, got '{s}'"
                        ))
                        .into());
                    }
                }
                (RendererKind::Sqlite(qcraft::qcraft_sqlite::SqliteRenderer::new()), "qmark")
            }
            _ => return Err(SqlGenError::UnsupportedDialect(dialect.to_string()).into()),
        };

        Ok(SqlGenerator {
            renderer,
            param_style_name: default_style_name,
        })
    }

    #[getter]
    fn dialect(&self) -> &str {
        self.renderer.name()
    }

    #[getter]
    fn param_style(&self) -> &str {
        self.param_style_name
    }

    fn compile_query(&self, py: Python, query: &Bound<PyAny>) -> PyResult<(String, PyObject)> {
        let stmt = extract::extract_query_stmt(query)?;
        let (sql, values) = self.renderer.render_query(&stmt)?;
        let params = values_to_py_list(py, values)?;
        Ok((sql, params))
    }

    fn compile_mutation(
        &self,
        py: Python,
        mutation: &Bound<PyAny>,
    ) -> PyResult<(String, PyObject)> {
        let stmt = extract::extract_mutation(mutation)?;
        let (sql, values) = self.renderer.render_mutation(&stmt)?;
        let params = values_to_py_list(py, values)?;
        Ok((sql, params))
    }

    fn compile_schema_mutation(
        &self,
        py: Python,
        mutation: &Bound<PyAny>,
    ) -> PyResult<PyObject> {
        let stmts = extract::extract_schema_mutation(mutation)?;
        let mut result: Vec<(String, PyObject)> = Vec::new();
        for stmt in &stmts {
            let pairs = self.renderer.render_schema(stmt)?;
            for (sql, values) in pairs {
                let params = values_to_py_list(py, values)?;
                result.push((sql, params));
            }
        }
        Ok(result.into_py_any(py)?)
    }

    fn compile_lock_command(
        &self,
        py: Python,
        lock: &Bound<PyAny>,
    ) -> PyResult<(String, PyObject)> {
        let stmt = extract::extract_lock_command(lock)?;
        let (sql, values) = self.renderer.render_lock(&stmt)?;
        let params = values_to_py_list(py, values)?;
        Ok((sql, params))
    }
}
