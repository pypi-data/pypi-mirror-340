use binrw::binrw;

#[cfg(feature = "pyo3")]
use pyo3::prelude::*;

#[binrw]
#[derive(Debug, Clone)]
#[cfg_attr(feature = "pyo3", pyo3::pyclass(get_all, set_all))]
pub struct GetDoutsRequest {}

#[cfg(feature = "pyo3")]
#[pymethods]
impl GetDoutsRequest {
    #[new]
    pub fn new() -> Self {
        Self {}
    }
}

#[binrw]
#[brw(big)]
#[derive(Debug, Clone)]
#[cfg_attr(feature = "pyo3", pyo3::pyclass(get_all, set_all))]
pub struct GetDoutsResponse {
    pub bin_layout: u16,
}

#[cfg(feature = "pyo3")]
#[pymethods]
impl GetDoutsResponse {
    #[new]
    pub fn new(bin_layout: u16) -> Self {
        Self { bin_layout }
    }
}

#[cfg(feature = "pyo3")]
pub(crate) fn pymodule(py: Python) -> PyResult<pyo3::Bound<'_, pyo3::types::PyModule>> {
    PyModule::new(py, "get_do").map(|module| {
        module.add_class::<GetDoutsRequest>()?;
        module.add_class::<GetDoutsResponse>()?;
        Ok(module)
    })?
}
