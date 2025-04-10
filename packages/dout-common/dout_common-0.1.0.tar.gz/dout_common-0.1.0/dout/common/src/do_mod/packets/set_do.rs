use binrw::binrw;

#[cfg(feature = "pyo3")]
use pyo3::prelude::*;

#[binrw]
#[derive(Debug, Clone)]
#[cfg_attr(feature = "pyo3", pyo3::pyclass(get_all, set_all))]
pub struct SetDoutsRequest {
    pub bin_layout: u16,
}

#[cfg(feature = "pyo3")]
#[pymethods]
impl SetDoutsRequest {
    #[new]
    pub fn new(bin_layout: u16) -> Self {
        Self { bin_layout }
    }
}

#[binrw]
#[brw(big)]
#[derive(Debug, Clone)]
#[cfg_attr(feature = "pyo3", pyo3::pyclass(get_all, set_all))]
pub struct SetDoutsResponse {
    pub success: u8,
}

#[cfg(feature = "pyo3")]
#[pymethods]
impl SetDoutsResponse {
    #[new]
    pub fn new(success: u8) -> Self {
        Self { success }
    }
}

#[cfg(feature = "pyo3")]
pub(crate) fn pymodule(py: Python) -> PyResult<pyo3::Bound<'_, pyo3::types::PyModule>> {
    PyModule::new(py, "set_do").map(|module| {
        module.add_class::<SetDoutsRequest>()?;
        module.add_class::<SetDoutsResponse>()?;
        Ok(module)
    })?
}
