use what_phmsa_data_reveals_about_pipeline_failures_core::issues_per_mile;
use numpy::{PyArray1, PyReadonlyArray1, IntoPyArray};
use pyo3::prelude::*;

#[pyfunction]
fn issues_per_mile_py<'py>(py: Python<'py>, issues: PyReadonlyArray1<f64>, miles: PyReadonlyArray1<f64>) -> PyResult<Bound<'py, PyArray1<f64>>> {
    Ok(issues_per_mile(issues.as_slice()?, miles.as_slice()?).into_pyarray(py))
}

#[pyfunction]
#[pyo3(signature = (issues, miles, iterations=100_000))]
fn bench_kernel_py(issues: PyReadonlyArray1<f64>, miles: PyReadonlyArray1<f64>, iterations: usize) -> PyResult<f64> {
    let i = issues.as_slice()?.to_vec(); let m = miles.as_slice()?.to_vec();
    let start = std::time::Instant::now();
    for _ in 0..iterations { let _ = issues_per_mile(&i, &m); }
    Ok(start.elapsed().as_secs_f64())
}

#[pymodule]
fn what_phmsa_data_reveals_about_pipeline_failures_rs(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(issues_per_mile_py, m)?)?;
    m.add_function(wrap_pyfunction!(bench_kernel_py, m)?)?;
    Ok(())
}
