use pyo3::prelude::*;

/// Formats the sum of two numbers as string.
#[pyfunction]
fn sum_as_string(a: usize, b: usize) -> PyResult<String> {
    Ok((a + b).to_string())
}

//
// 使用 pyo3 实现 fib(), PyResult, 会严重拖慢性能!!!
//  - 详细请参考 try-cython 中性能对比测试数据!!!
//
#[pyfunction]
fn fib(n: usize) -> PyResult<f64> {
    // 不要使用递归实现:
    let mut a = 0.0;
    let mut b = 1.0;
    for _ in 0..n {
        let tmp = b;
        b = a + b;
        a = tmp;
    }
    Ok(a)
}

/// A Python module implemented in Rust.
#[pymodule]
fn rspx(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(sum_as_string, m)?)?;
    m.add_function(wrap_pyfunction!(fib, m)?)?;
    Ok(())
}
