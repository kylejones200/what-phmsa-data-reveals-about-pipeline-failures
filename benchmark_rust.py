#!/usr/bin/env python3
import time, sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parent; sys.path.insert(0,str(ROOT/"src"))
from compute_kernel import issues_per_mile
def main():
    i=np.ascontiguousarray(np.arange(10000,dtype=float))
    m=np.ascontiguousarray(10.+i,dtype=float)
    t0=time.perf_counter()
    for _ in range(200):
        issues_per_mile(i,m)
    py_s=time.perf_counter()-t0
    try:
        import what_phmsa_data_reveals_about_pipeline_failures_rs as rs
    except ImportError:
        print("Build: cd rust && maturin develop --release -m py/Cargo.toml"); print(f"Python {py_s:.3f}s"); return
    rs_s=rs.bench_kernel_py(i,m,200)
    print(f"Python {py_s:.3f}s Rust {rs_s:.3f}s speedup {py_s/max(rs_s,1e-9):.1f}x")
    py_out=issues_per_mile(i,m)
    rs_out=np.asarray(rs.issues_per_mile_py(i,m))
    np.testing.assert_allclose(py_out, rs_out, rtol=1e-12)
    print("Correctness: OK")
if __name__=="__main__": main()
