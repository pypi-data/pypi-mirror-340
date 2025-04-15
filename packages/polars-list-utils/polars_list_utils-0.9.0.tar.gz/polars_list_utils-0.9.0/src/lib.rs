mod agg;
mod dsp;
mod dsp_util;
mod feat;
mod numpy;
mod util;
use {pyo3::prelude::*, pyo3_polars::PolarsAllocator};

#[pymodule]
fn _internal(
    _py: Python,
    m: &Bound<PyModule>,
) -> PyResult<()> {
    m.add("__version__", env!("CARGO_PKG_VERSION"))?;
    Ok(())
}

#[global_allocator]
static ALLOC: PolarsAllocator = PolarsAllocator::new();
