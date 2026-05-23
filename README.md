# What PHMSA Data Reveals About Pipeline Failures

Published: 2025-08-19
Medium: [https://medium.com/@kyle-t-jones/what-phmsa-data-reveals-about-pipeline-failures-8780d5498b80](https://medium.com/@kyle-t-jones/what-phmsa-data-reveals-about-pipeline-failures-8780d5498b80)

## Business context

Pipelines are critical infrastructure, carrying the energy that powers modern life. But like all infrastructure, they fail. The Pipeline and Hazardous Materials Safety Administration (PHMSA) tracks incidents, leaks, and failures across the U.S. pipeline network. By analyzing these records, we can see which causes dominate and where prevention efforts may have the biggest impact.

The stacked bar chart shows the breakdown of incidents, leaks, and failures by cause. One factor stands far above the rest: equipment-related issues. With more than 1,200 recorded cases, equipment problems account for the overwhelming majority of failures.

In contrast, other causes like construction errors, corrosion, and third-party damage fall in the low hundreds. Weather events, incorrect operations, internal corrosion, and stress cracking barely register by comparison.

## About

Place the code for this article in this repository.
The original article export is saved as `article.md`.

## Files

Add your `.ipynb`, `.py`, `.yaml`, `.js`, `.ts`, or other project files here.

## Rust performance port

Side-by-side **Python vs Rust** implementation of the numeric hot loop — issues-per-mile for aligned arrays. Reference PyO3 benchmark: **~7×** on a release build (local machine; run `benchmark_rust.py` to reproduce).

| Path | Role |
|------|------|
| `src/compute_kernel.py` | Python/numpy reference kernel |
| `rust/core/` | Pure Rust library |
| `rust/py/` | PyO3 bindings |
| `rust/bench/` | Standalone CLI benchmark |
| `benchmark_rust.py` | Python vs Rust timing + correctness check |

```bash
# Rust-only CLI benchmark
cd rust && cargo run --release -p what_phmsa_data_reveals_about_pipeline_failures_bench

# Python vs Rust (PyO3)
pip install maturin numpy
maturin develop --release -m rust/py/Cargo.toml
python benchmark_rust.py
```

Python ML training, solvers, and orchestration stay in Python; Rust targets the numeric hot loops. Stochastic generators validate output shapes; deterministic kernels match at tight floating-point tolerance.


## Disclaimer

Educational/demo code only. Not financial, safety, or engineering advice. Use at your own risk. Verify results independently before any production or operational use.

## License

MIT — see [LICENSE](LICENSE).