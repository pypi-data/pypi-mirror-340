#![cfg_attr(not(feature = "std"), no_std)]

#[cfg(feature = "pyo3")]
use pyo3::prelude::*;

pub mod do_mod;

#[cfg(feature = "pyo3")]
#[pymodule(name = "dout_common")]
fn pymodule(py: Python, m: &Bound<'_, PyModule>) -> PyResult<()> {
    let submodule = &do_mod::pymodule(py)?;
    py.import("sys")?
        .getattr("modules")?
        .set_item("dout_common.do_mod", submodule)?;
    m.add_submodule(submodule)?;
    Ok(())
}
